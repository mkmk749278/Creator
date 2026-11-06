import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, interpolate, OffthreadVideo, random, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
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
	children: React.ReactNode;
}> = ({dur, from = [1, 0, 0], to = [1.08, 0, 0], drift = 4, seed = 'c', children}) => {
	const f = useCurrentFrame();
	const k = tw(f, 0, dur, 0, 1);
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
}> = ({name, dur, from = [1.04, 0, 0], to = [1.12, 0, 0], startAt = 0, grade = 'night', style}) => {
	const filter =
		grade === 'night'
			? 'contrast(1.08) saturate(0.85) brightness(0.92)'
			: grade === 'red'
				? 'contrast(1.1) saturate(1.05)'
				: grade === 'day'
					? 'contrast(1.05) saturate(0.95)'
					: undefined;
	return (
		<Cam dur={dur} from={from} to={to} seed={name}>
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
				<div style={{marginTop: 8, fontFamily: F.label, fontWeight: 700, fontSize: 32, color: C.dim, textTransform: 'uppercase', letterSpacing: 1, whiteSpace: 'nowrap'}}>
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

/** Source credit for third-party footage, bottom-left above the player bar zone. */
export const Credit: React.FC<{text: string}> = ({text}) => (
	<div style={{position: 'absolute', left: 72, bottom: 230, fontFamily: F.label, fontWeight: 700, fontSize: 30, color: C.dim, background: 'rgba(3,7,13,0.66)', padding: '4px 12px', letterSpacing: 1}}>
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
