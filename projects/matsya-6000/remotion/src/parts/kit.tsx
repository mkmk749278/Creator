import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, Img, interpolate, OffthreadVideo, random, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {C, F} from '../theme';
import LENS from '../../../media/clip_durations.json';

const clipLen = (name: string): number => (LENS as Record<string, number>)[name] ?? 999;
/** Playback rate so a shot never outruns its footage (a slower, never frozen, clip; at least 0.5×). */
export const fitRate = (name: string, durFrames: number, startAt: number): number => {
	const need = durFrames / 60;
	const have = clipLen(name) - startAt - 0.05;
	return need <= have ? 1 : Math.max(0.5, have / need);
};

// The film's small kit: every value is a function of the frame (PLAYBOOK §10.2).

export const ez = {
	cam: Easing.bezier(0.45, 0, 0.2, 1),
	arrive: Easing.bezier(0.16, 1, 0.3, 1),
	leave: Easing.bezier(0.7, 0, 0.84, 0),
	sweep: Easing.bezier(0.65, 0, 0.35, 1),
};

export const tw = (f: number, a: number, b: number, from: number, to: number, e: (t: number) => number = ez.cam): number =>
	interpolate(f, [a, b], [from, to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: e});

/** Spring from frame `at` (0 before), lands without wobble. */
export const useSpring = (at: number, stiffness = 140, damping = 18): number => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: f - at, fps, config: {stiffness, damping}});
};

/** Camera move over a shot: eased scale/translate keys plus a seeded drift (visible motion, §9.4). */
export const Cam: React.FC<{
	dur: number;
	from?: [number, number, number]; // scale, x, y
	to?: [number, number, number];
	drift?: number;
	seed?: string;
	ease?: (t: number) => number; // the move's easing; linear keeps a long shot moving to its last frame
	children: React.ReactNode;
}> = ({dur, from = [1, 0, 0], to = [1.08, 0, 0], drift = 4, seed = 'c', ease = ez.cam, children}) => {
	const f = useCurrentFrame();
	const k = tw(f, 0, dur, 0, 1, ease);
	const s = from[0] + (to[0] - from[0]) * k;
	const x = from[1] + (to[1] - from[1]) * k + drift * noise2D(seed + 'x', f / 150, 0);
	const y = from[2] + (to[2] - from[2]) * k + drift * noise2D(seed + 'y', 0, f / 170);
	return (
		<AbsoluteFill style={{overflow: 'hidden'}}>
			<AbsoluteFill style={{transform: `translate(${x}px, ${y}px) scale(${s})`, transformOrigin: '50% 50%'}}>{children}</AbsoluteFill>
		</AbsoluteFill>
	);
};

/** A footage excerpt prepared by tools (assets/media/clips/<name>.mp4, 1920×1080, 60 fps, used seconds only). */
export const Clip: React.FC<{
	name: string;
	dur: number;
	from?: [number, number, number];
	to?: [number, number, number];
	startAt?: number; // seconds into the prepared clip
	grade?: 'night' | 'day' | 'red' | 'none';
	style?: React.CSSProperties;
	ease?: (t: number) => number;
}> = ({name, dur, from = [1.04, 0, 0], to = [1.12, 0, 0], startAt = 0, grade = 'night', style, ease}) => {
	const filter =
		grade === 'night'
			? 'contrast(1.08) saturate(0.85) brightness(0.92)'
			: grade === 'red'
				? 'contrast(1.1) saturate(1.05)'
				: grade === 'day'
					? 'contrast(1.05) saturate(0.95)'
					: undefined;
	return (
		<Cam dur={dur} from={from} to={to} seed={name} ease={ease}>
			<OffthreadVideo
				src={staticFile(`assets/media/clips/${name}.mp4`)}
				startFrom={Math.round(startAt * 60)}
				playbackRate={fitRate(name, dur, startAt)}
				muted
				style={{width: '100%', height: '100%', objectFit: 'cover', filter, ...style}}
			/>
		</Cam>
	);
};

/** Fine film grain that steps once per frame, plus a 30% vignette (atmosphere layer, §9.2). */
export const Atmos: React.FC<{vignette?: number; grain?: number}> = ({vignette = 0.32, grain = 0.06}) => {
	const f = useCurrentFrame();
	const seed = Math.floor(random(`g${f}`) * 1000);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width="100%" height="100%" style={{position: 'absolute', opacity: grain, mixBlendMode: 'overlay'}}>
				<filter id={`gr${f}`}>
					<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={seed} />
					<feColorMatrix type="saturate" values="0" />
				</filter>
				<rect width="100%" height="100%" filter={`url(#gr${f})`} />
			</svg>
			<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 48%, transparent 52%, rgba(0,0,0,${vignette}) 78%, rgba(0,0,0,${vignette + 0.25}) 100%)`}} />
		</AbsoluteFill>
	);
};

/** Label: a 2–4 word caption on a dark scrim; arrives on its word with a spring (§9.6: ≥ 44 px when pointed to). */
export const Label: React.FC<{
	at: number;
	text: string;
	x: number;
	y: number;
	size?: number;
	color?: string;
	sub?: string;
	align?: 'left' | 'center' | 'right';
	until?: number;
	mono?: boolean;
}> = ({at, text, x, y, size = 48, color = C.ink, sub, align = 'left', until, mono}) => {
	const f = useCurrentFrame();
	const p = useSpring(at);
	const out = until === undefined ? 1 : tw(f, until - 10, until, 1, 0, ez.leave);
	if (f < at) {
		return null;
	}
	const tx = align === 'center' ? '-50%' : align === 'right' ? '-100%' : '0';
	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				transform: `translate(${tx}, ${(1 - p) * 18}px)`,
				opacity: p * out,
				textAlign: align,
			}}
		>
			<div
				style={{
					display: 'inline-block',
					padding: `${size * 0.16}px ${size * 0.34}px`,
					background: 'rgba(3,7,13,0.78)',
					borderLeft: align === 'left' ? `${Math.max(4, size / 9)}px solid ${color}` : undefined,
					borderRight: align === 'right' ? `${Math.max(4, size / 9)}px solid ${color}` : undefined,
					fontFamily: mono ? F.mono : F.label,
					fontWeight: mono ? 700 : 800,
					fontSize: size,
					letterSpacing: mono ? 0 : size * 0.02,
					textTransform: 'uppercase',
					color,
					lineHeight: 1.05,
					whiteSpace: 'nowrap',
				}}
			>
				{text}
			</div>
			{sub ? (
				<div style={{marginTop: 8, fontFamily: F.label, fontWeight: 700, fontSize: 40, color: C.dim, textTransform: 'uppercase', letterSpacing: 1, whiteSpace: 'nowrap'}}>
					<span style={{background: 'rgba(3,7,13,0.78)', padding: '4px 12px'}}>{sub}</span>
				</div>
			) : null}
		</div>
	);
};

/** Honesty tag, top-left, small and constant: ILLUSTRATION / RECONSTRUCTION / OUR CALCULATION. */
export const Honesty: React.FC<{text: string}> = ({text}) => (
	<div style={{position: 'absolute', left: 72, top: 60, fontFamily: F.label, fontWeight: 700, fontSize: 30, letterSpacing: 2, color: C.dim, background: 'rgba(3,7,13,0.7)', padding: '6px 14px'}}>
		{text}
	</div>
);

/** Source credit for third-party footage, top-right (labels live on the left and lower third). */
export const Credit: React.FC<{text: string}> = ({text}) => (
	<div style={{position: 'absolute', right: 72, top: 60, fontFamily: F.label, fontWeight: 700, fontSize: 30, color: C.dim, background: 'rgba(3,7,13,0.66)', padding: '4px 12px', letterSpacing: 1}}>
		{text}
	</div>
);

/** A number that counts on screen and lands on frame `b` (§9.9). */
export const Count: React.FC<{a: number; b: number; from: number; to: number; x: number; y: number; size?: number; unit?: string; color?: string; decimals?: number; align?: 'left' | 'center'}> = ({
	a,
	b,
	from,
	to,
	x,
	y,
	size = 96,
	unit = '',
	color = C.ink,
	decimals = 0,
	align = 'left',
}) => {
	const f = useCurrentFrame();
	if (f < a - 6) {
		return null;
	}
	const v = tw(f, a, b, from, to, ez.sweep);
	const p = tw(f, a - 6, a + 6, 0, 1, ez.arrive);
	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				transform: align === 'center' ? 'translateX(-50%)' : undefined,
				opacity: p,
				fontFamily: F.mono,
				fontWeight: 700,
				fontSize: size,
				color,
				textShadow: '0 4px 24px rgba(0,0,0,0.8)',
				whiteSpace: 'nowrap',
			}}
		>
			{v.toLocaleString('en-IN', {minimumFractionDigits: decimals, maximumFractionDigits: decimals})}
			<span style={{fontSize: size * 0.5, marginLeft: size * 0.12}}>{unit}</span>
		</div>
	);
};

/**
 * The steel inspection plate with its drafting grid: the one physical base every drawing sits on (§9.3).
 * Brushed steel from seeded turbulence, a warm overhead light pool, a slight fixed tilt for the whole film.
 */
export const Plate: React.FC<{children?: React.ReactNode; dur: number; seed?: string; from?: [number, number, number]; to?: [number, number, number]; light?: string}> = ({
	children,
	dur,
	seed = 'plate',
	from = [1.02, 0, 0],
	to = [1.09, -20, 0],
	light = 'rgba(190,210,230,0.16)',
}) => (
	<AbsoluteFill style={{background: '#0d1116'}}>
		<Cam dur={dur} from={from} to={to} seed={seed}>
			<AbsoluteFill style={{transform: 'perspective(2400px) rotateX(8deg) scale(1.0)', transformOrigin: '50% 55%'}}>
				<svg width="1920" height="1080" style={{position: 'absolute'}}>
					<defs>
						<filter id="brush">
							<feTurbulence type="fractalNoise" baseFrequency="0.003 0.22" numOctaves={2} seed={7} />
							<feColorMatrix type="matrix" values="0 0 0 0 0.16  0 0 0 0 0.18  0 0 0 0 0.21  0 0 0 0.28 0" />
						</filter>
						<pattern id="g1" width="40" height="40" patternUnits="userSpaceOnUse">
							<path d="M40 0H0V40" fill="none" stroke="#5b6b7c" strokeOpacity="0.16" strokeWidth="1" />
						</pattern>
						<pattern id="g2" width="200" height="200" patternUnits="userSpaceOnUse">
							<path d="M200 0H0V200" fill="none" stroke="#7d91a6" strokeOpacity="0.28" strokeWidth="1.6" />
						</pattern>
					</defs>
					<rect width="1920" height="1080" fill="#1a1f25" />
					<rect width="1920" height="1080" filter="url(#brush)" />
					<rect width="1920" height="1080" fill="url(#g1)" />
					<rect width="1920" height="1080" fill="url(#g2)" />
					{/* bolt heads at the plate's corners */}
					{[
						[60, 60],
						[1860, 60],
						[60, 1020],
						[1860, 1020],
					].map(([x, y], i) => (
						<g key={i}>
							<circle cx={x} cy={y} r={16} fill="#2c333b" stroke="#0a0d10" strokeWidth={3} />
							<path d={`M${x - 8} ${y}H${x + 8}`} stroke="#0a0d10" strokeWidth={3} />
						</g>
					))}
				</svg>
				{children}
			</AbsoluteFill>
		</Cam>
		<AbsoluteFill style={{background: `radial-gradient(ellipse 60% 55% at 50% 42%, ${light}, transparent 70%)`, mixBlendMode: 'screen'}} />
	</AbsoluteFill>
);

/** The night sea under the waves: a gradient lit from above, slow light shafts, drifting motes. */
export const Underwater: React.FC<{depth?: number}> = ({depth = 0}) => {
	const f = useCurrentFrame();
	const top = interpolate(depth, [0, 1], [0.32, 0.06]);
	return (
		<AbsoluteFill style={{background: `linear-gradient(180deg, rgba(40,120,160,${top}) 0%, #072135 38%, #020a12 100%)`}}>
			{[0, 1, 2, 3, 4].map((i) => {
				const x = 200 + i * 380 + 60 * noise2D('ray' + i, f / 300, 0);
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: x,
							top: -200,
							width: 140 + 60 * random('w' + i),
							height: 1300,
							transform: `rotate(${14 + 4 * noise2D('r' + i, 0, f / 400)}deg)`,
							background: `linear-gradient(180deg, rgba(150,210,255,${0.16 * (1 - depth)}), transparent 70%)`,
							filter: 'blur(28px)',
						}}
					/>
				);
			})}
		</AbsoluteFill>
	);
};

/** Real water over a 3D deep-sea shot (owner on r6: "looking like dark universe with stars"). Our Blender shots are
 *  lit objects on black with white specks; this lays the sea back on top: a blue body of water (screen, so black
 *  becomes deep blue and the lit object keeps its colour), light from above near the surface only, and real air
 *  bubbles rising (Pixabay 31611). `depth` 0 = near the surface, 1 = six kilometres down (no sunlight: a darker,
 *  even blue). `until` fades it out (frames), for a shot that goes inside the ball. */
export const SeaOver: React.FC<{dur: number; depth?: number; until?: number; bubbles?: number}> = ({dur, depth = 1, until, bubbles = 0.5}) => {
	const f = useCurrentFrame();
	const out = until === undefined ? 1 : interpolate(f, [until - 20, until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	if (out <= 0) {
		return null;
	}
	const a = interpolate(depth, [0, 1], [0.62, 0.34]);
	const b = interpolate(depth, [0, 1], [0.34, 0.26]);
	return (
		<AbsoluteFill style={{opacity: out, pointerEvents: 'none'}}>
			<AbsoluteFill style={{mixBlendMode: 'screen', background: `linear-gradient(180deg, rgba(22,104,150,${a}) 0%, rgba(9,58,96,${b}) 50%, rgba(4,30,54,${b * 0.8}) 100%)`}} />
			{depth < 0.6
				? [0, 1, 2, 3].map((i) => (
						<div
							key={i}
							style={{
								position: 'absolute',
								left: 160 + i * 470 + 70 * noise2D('sray' + i, f / 260, 0),
								top: -220,
								width: 170 + 70 * random('srw' + i),
								height: 1350,
								transform: `rotate(${13 + 4 * noise2D('srr' + i, 0, f / 380)}deg)`,
								background: `linear-gradient(180deg, rgba(160,220,255,${0.2 * (1 - depth)}), transparent 72%)`,
								filter: 'blur(30px)',
								mixBlendMode: 'screen',
							}}
						/>
					))
				: null}
			<OffthreadVideo
				src={staticFile('assets/media/clips/PX_bubbles.mp4')}
				startFrom={Math.round(60 * 2 * random('bub' + Math.round(dur)))}
				playbackRate={fitRate('PX_bubbles', dur, 2)}
				muted
				style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', mixBlendMode: 'screen', opacity: bubbles, filter: 'blur(0.6px) brightness(1.25)'}}
			/>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(1,10,20,0.55) 100%)'}} />
		</AbsoluteFill>
	);
};

/** Marine snow: specks drifting past the lens; `speed` px a frame upward reads as the camera sinking. */
export const MarineSnow: React.FC<{speed?: number; n?: number}> = ({speed = 1, n = 140}) => {
	const f = useCurrentFrame();
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
			{Array.from({length: n}).map((_, i) => {
				const x = random('sx' + i) * 1920 + 20 * noise2D('sn' + i, f / 200, 0);
				const z = 0.4 + random('sz' + i) * 0.9;
				const y = (((random('sy' + i) * 1200 - f * speed * z) % 1200) + 1200) % 1200 - 60;
				return <circle key={i} cx={x} cy={y} r={1.2 + 2.2 * z} fill="#cfe8ff" opacity={0.18 + 0.3 * z} />;
			})}
		</svg>
	);
};

/** A Blender hero clip (Drive renders/, prepared to 60 fps): frame 0 is its sentence's start, so it plays at 1x from
 *  `startAt` seconds; labels come from Remotion on top. */
export const Hero: React.FC<{name: string; dur: number; startAt?: number; from?: [number, number, number]; to?: [number, number, number]; style?: React.CSSProperties}> = ({
	name,
	dur,
	startAt = 0,
	from = [1.0, 0, 0],
	to = [1.04, 0, 0],
	style,
}) => <Clip name={name} dur={dur} startAt={startAt} from={from} to={to} grade="none" ease={(t) => t} style={style} />;

/** A still with a slow, eased push (never static over 1.5 s); `contain` frames a small or odd-shaped photo over a
 *  blurred copy of itself so it never floats in a void (§9.3). */
export const Photo: React.FC<{
	src: string;
	dur: number;
	from?: [number, number, number];
	to?: [number, number, number];
	fit?: 'cover' | 'contain';
	filter?: string;
}> = ({src, dur, from = [1.02, 0, 0], to = [1.12, -20, 0], fit = 'cover', filter = 'contrast(1.05) saturate(0.95)'}) => {
	const url = staticFile(`assets/media/photos/${src}`);
	if (fit === 'cover') {
		return (
			<Cam dur={dur} from={from} to={to} seed={src} ease={(t) => t}>
				<Img src={url} style={{width: '100%', height: '100%', objectFit: 'cover', filter}} />
			</Cam>
		);
	}
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Img src={url} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(40px) brightness(0.45) saturate(0.8)', transform: 'scale(1.15)'}} />
			<Cam dur={dur} from={from} to={to} seed={src} ease={(t) => t}>
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
					<Img src={url} style={{height: '82%', maxWidth: '86%', objectFit: 'contain', filter, boxShadow: '0 30px 80px rgba(0,0,0,0.7)', border: '2px solid rgba(238,243,248,0.12)'}} />
				</AbsoluteFill>
			</Cam>
		</AbsoluteFill>
	);
};

/** A low-resolution or square clip as a framed insert over its own blurred copy (F03 480p, F06 square). */
export const Insert: React.FC<{name: string; dur: number; startAt?: number; aspect?: number; height?: number}> = ({name, dur, startAt = 0, aspect = 16 / 9, height = 760}) => {
	const src = staticFile(`assets/media/clips/${name}.mp4`);
	const rate = fitRate(name, dur, startAt);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<OffthreadVideo src={src} startFrom={Math.round(startAt * 60)} playbackRate={rate} muted
				style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(40px) brightness(0.4)', transform: 'scale(1.2)'}} />
			<Cam dur={dur} from={[1.0, 0, 0]} to={[1.06, 0, -10]} seed={name} ease={(t) => t}>
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
					<div style={{width: height * aspect, height, overflow: 'hidden', boxShadow: '0 30px 80px rgba(0,0,0,0.7)', border: '2px solid rgba(238,243,248,0.12)'}}>
						<OffthreadVideo src={src} startFrom={Math.round(startAt * 60)} playbackRate={rate} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
					</div>
				</AbsoluteFill>
			</Cam>
		</AbsoluteFill>
	);
};
