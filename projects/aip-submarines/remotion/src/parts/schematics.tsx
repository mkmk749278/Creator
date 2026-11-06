import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {Cam, ez, tw, useSpring} from './kit';
import {hullPath, finPath, SUB_LEN_M} from './drawings';
import {noise2D} from '@remotion/noise';

// Schematic drawings on the steel plate and instrument faces (ILLUSTRATION / SIMPLIFIED where shown).

/** A vertical source (the P-8I clip) in a frame on its own blurred fill: never stretched, never letterboxed black. */
export const VerticalClip: React.FC<{name: string; dur: number; startAt?: number}> = ({name, dur, startAt = 0}) => (
	<AbsoluteFill style={{background: '#000'}}>
		<AbsoluteFill style={{filter: 'blur(40px) brightness(0.45)', transform: 'scale(1.3)'}}>
			<OffthreadVideo src={staticFile(`assets/media/clips/${name}.mp4`)} startFrom={Math.round(startAt * 60)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
		</AbsoluteFill>
		<Cam dur={dur} from={[1.0, 0, 0]} to={[1.07, 0, -10]} seed={name}>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
				<div style={{height: 1000, width: 563, boxShadow: '0 30px 90px rgba(0,0,0,0.7)', border: '2px solid rgba(255,255,255,0.15)', overflow: 'hidden'}}>
					<OffthreadVideo src={staticFile(`assets/media/clips/${name}.mp4`)} startFrom={Math.round(startAt * 60)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				</div>
			</AbsoluteFill>
		</Cam>
	</AbsoluteFill>
);

/** The sea from above, the boat's outline under it; on `fade` the outline goes and only the surface stays. */
export const SeaFromAbove: React.FC<{dur: number; fade: number; cross?: number}> = ({dur, fade, cross}) => {
	const f = useCurrentFrame();
	const o = 1 - tw(f, fade, fade + 30, 0, 1);
	const x = cross === undefined ? 0 : tw(f, cross, cross + 14, 0, 1, ez.arrive);
	return (
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 40%, #0d2c44, #03101b 75%)'}}>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<defs>
					<filter id="waves">
						<feTurbulence type="fractalNoise" baseFrequency={`0.006 0.02`} numOctaves={3} seed={Math.floor(f / 3)} />
						<feColorMatrix type="matrix" values="0 0 0 0 0.6  0 0 0 0 0.75  0 0 0 0 0.9  0 0 0 0.16 0" />
					</filter>
				</defs>
				<rect width={1920} height={1080} filter="url(#waves)" />
				<g transform="translate(470 560)" opacity={0.85 * o}>
					<path d={hullPath(14.5)} fill="rgba(0,0,0,0.35)" stroke={C.dim} strokeWidth={3} strokeDasharray="16 12" transform="scale(1 0.55)" />
				</g>
				{x > 0 ? (
					<g stroke={C.red} strokeWidth={10} opacity={x * o} strokeLinecap="round">
						<line x1={860} y1={420} x2={1080} y2={700} />
						<line x1={1080} y1={420} x2={860} y2={700} />
					</g>
				) : null}
			</svg>
			<Honest />
		</AbsoluteFill>
	);
};

const Honest = () => (
	<div style={{position: 'absolute', left: 72, top: 60, fontFamily: F.label, fontWeight: 700, fontSize: 30, letterSpacing: 2, color: C.dim, background: 'rgba(3,7,13,0.7)', padding: '6px 14px'}}>
		ILLUSTRATION
	</div>
);

/** A radar scope (PPI): sweep, range rings, sea clutter; a dot appears at `dot`. */
export const RadarScope: React.FC<{dot: number}> = ({dot}) => {
	const f = useCurrentFrame();
	const ang = (f * 3) % 360;
	const dp = tw(f, dot, dot + 6, 0, 1, ez.arrive);
	const age = Math.max(0, f - dot) % 50;
	return (
		<AbsoluteFill style={{background: '#020806'}}>
			<Cam dur={300} from={[1, 0, 0]} to={[1.12, 0, 0]} seed="scope">
				<svg width={1920} height={1080}>
					<defs>
						<radialGradient id="scopeG">
							<stop offset="0" stopColor="#0b2a1c" />
							<stop offset="1" stopColor="#010604" />
						</radialGradient>
					</defs>
					<circle cx={960} cy={540} r={470} fill="url(#scopeG)" stroke="#2d6b4c" strokeWidth={4} />
					{[0.25, 0.5, 0.75].map((k) => (
						<circle key={k} cx={960} cy={540} r={470 * k} fill="none" stroke="#2d6b4c" strokeOpacity={0.5} strokeWidth={2} />
					))}
					{Array.from({length: 120}).map((_, i) => {
						const a = (i * 137.5 * Math.PI) / 180;
						const r = 60 + ((i * 53) % 400);
						return <circle key={i} cx={960 + Math.cos(a) * r} cy={540 + Math.sin(a) * r} r={2} fill="#3fd27a" opacity={0.15 + 0.15 * noise2D('cl' + i, f / 30, 0)} />;
					})}
					<g transform={`rotate(${ang} 960 540)`}>
						<path d="M960 540 L1430 540 A470 470 0 0 0 1366 305 Z" fill="#3fd27a" opacity={0.16} />
						<line x1={960} y1={540} x2={1430} y2={540} stroke="#5dff9c" strokeWidth={4} />
					</g>
					{dp > 0 ? (
						<g>
							<circle cx={1180} cy={390} r={14 * dp} fill={C.red} />
							<circle cx={1180} cy={390} r={16 + age * 1.6} fill="none" stroke={C.red} strokeWidth={4} opacity={1 - age / 50} />
						</g>
					) : null}
				</svg>
			</Cam>
		</AbsoluteFill>
	);
};

/** An acoustic line (what a sonobuoy hears): calm sea noise; on `spike` a diesel's tones stand up out of it. */
export const AcousticLine: React.FC<{spike: number}> = ({spike}) => {
	const f = useCurrentFrame();
	const k = tw(f, spike, spike + 18, 0, 1, ez.arrive);
	const N = 160;
	const pts = Array.from({length: N}, (_, i) => {
		const x = 160 + (i / (N - 1)) * 1600;
		const base = 40 * noise2D('n' + i, f / 9, 0) + 18 * noise2D('m' + i, 0, f / 4);
		const peak = [38, 62, 101].reduce((acc, c) => acc + 260 * Math.exp(-Math.pow((i - c) / 2.2, 2)), 0);
		return `${x.toFixed(0)} ${(620 - base - k * peak).toFixed(1)}`;
	});
	return (
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 55%, #071a26, #01060a 75%)'}}>
			<svg width={1920} height={1080}>
				<line x1={160} x2={1760} y1={640} y2={640} stroke={C.dim} strokeOpacity={0.4} strokeWidth={2} />
				<path d={`M${pts.join(' L')}`} fill="none" stroke={C.cyan} strokeWidth={4} style={{filter: 'drop-shadow(0 0 8px rgba(76,201,240,0.6))'}} />
			</svg>
		</AbsoluteFill>
	);
};

/**
 * The boat cut open on the plate (SIMPLIFIED: the real layout is not public). Systems light on their words:
 * battery deck, motor, lights, air plant, computers, diesels; air arrows down the mast; `sink` lowers the sea line.
 */
export const Cutaway: React.FC<{
	dur: number;
	lit: Partial<Record<'battery' | 'motor' | 'lights' | 'air' | 'computers' | 'diesels', number>>;
	airAt?: number;
	cutAirAt?: number;
}> = ({dur, lit, airAt, cutAirAt}) => {
	const f = useCurrentFrame();
	const px = 21;
	const L = (k: keyof typeof lit) => (lit[k] === undefined ? 0 : tw(f, lit[k]!, lit[k]! + 12, 0, 1, ez.arrive));
	const comp: {k: keyof typeof lit; x: number; w: number; y: number; h: number; c: string; t: string}[] = [
		{k: 'motor', x: 4, w: 7, y: -1.8, h: 3.6, c: C.cyan, t: 'MOTOR'},
		{k: 'diesels', x: 12, w: 9, y: -1.8, h: 3.6, c: C.amber, t: 'DIESELS'},
		{k: 'air', x: 22, w: 6, y: -2.4, h: 2.2, c: C.frost, t: 'AIR PLANT'},
		{k: 'computers', x: 37, w: 8, y: -2.4, h: 2.2, c: C.cyan, t: 'COMPUTERS'},
		{k: 'lights', x: 29, w: 7, y: -2.4, h: 2.2, c: C.ink, t: 'LIGHTS'},
		{k: 'battery', x: 22, w: 30, y: 0.4, h: 2.2, c: C.green, t: 'BATTERY'},
	];
	const ox = 960 - (SUB_LEN_M * px) / 2;
	const oy = 600;
	const air = airAt === undefined ? 0 : tw(f, airAt, airAt + 20, 0, 1);
	const cut = cutAirAt === undefined ? 0 : tw(f, cutAirAt, cutAirAt + 16, 0, 1, ez.arrive);
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<g transform={`translate(${ox} ${oy})`}>
					<path d={hullPath(px)} fill="rgba(10,16,24,0.92)" stroke={C.ink} strokeWidth={3} />
					<path d={finPath(px, SUB_LEN_M - 26)} fill="rgba(10,16,24,0.92)" stroke={C.ink} strokeWidth={3} />
					{comp.map((c) => {
						const l = L(c.k);
						return (
							<g key={c.k}>
								<rect x={c.x * px} y={c.y * px} width={c.w * px} height={c.h * px} rx={6} fill={c.c} fillOpacity={0.08 + 0.5 * l} stroke={c.c} strokeOpacity={0.35 + 0.65 * l} strokeWidth={3} style={l > 0.5 ? {filter: `drop-shadow(0 0 14px ${c.c})`} : undefined} />
							</g>
						);
					})}
					{/* the snorkel mast and the air going down it */}
					<rect x={(SUB_LEN_M - 21) * px} y={-11.6 * px} width={0.5 * px} height={4.6 * px} fill={C.ink} />
					{air > 0
						? [0, 1, 2].map((i) => {
								const t = ((f / 40 + i / 3) % 1) * air;
								return (
									<path key={i} d={`M${(SUB_LEN_M - 20.75) * px} ${(-11 + 9 * t) * px} l-12 -16 m12 16 l12 -16`} stroke={C.frost} strokeWidth={5} fill="none" opacity={(1 - cut) * 0.9} />
								);
							})
						: null}
					{cut > 0 ? (
						<g stroke={C.red} strokeWidth={9} opacity={cut} strokeLinecap="round">
							<line x1={(SUB_LEN_M - 22.5) * px} y1={-12 * px} x2={(SUB_LEN_M - 19) * px} y2={-8.5 * px} />
							<line x1={(SUB_LEN_M - 19) * px} y1={-12 * px} x2={(SUB_LEN_M - 22.5) * px} y2={-8.5 * px} />
						</g>
					) : null}
				</g>
			</svg>
			{comp.map((c) => {
				const l = L(c.k);
				if (l <= 0) {
					return null;
				}
				const cx = ox + (c.x + c.w / 2) * px;
				const cy = oy + (c.k === 'battery' ? 4.2 : -6.4) * px + (['air', 'computers'].includes(c.k) ? -150 : c.k === 'lights' ? -80 : 0) - 30;
				return (
					<div key={c.k} style={{position: 'absolute', left: cx, top: cy, transform: `translate(-50%, ${(1 - l) * 12}px)`, opacity: l, fontFamily: F.label, fontWeight: 800, fontSize: 44, color: c.c, background: 'rgba(3,7,13,0.8)', padding: '4px 14px', whiteSpace: 'nowrap'}}>
						{c.t}
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** A speed dial: CRAWL to SPRINT; the needle follows `keys` [[frame, 0..1], ...]. */
export const SpeedDial: React.FC<{x: number; y: number; keys: [number, number][]; at?: number}> = ({x, y, keys, at = 0}) => {
	const f = useCurrentFrame();
	const p = useSpring(at);
	let v = keys[0][1];
	for (let i = 1; i < keys.length; i++) {
		if (f >= keys[i][0]) {
			v = tw(f, keys[i][0], keys[i][0] + 18, keys[i - 1][1], keys[i][1], ez.arrive);
		}
	}
	const a = (-120 + 240 * v) * (Math.PI / 180);
	const R = 190;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: p}}>
			<g transform={`translate(${x} ${y})`}>
				<circle r={R + 30} fill="rgba(3,7,13,0.85)" stroke={C.dim} strokeWidth={3} />
				<path d={`M${R * Math.cos((-210 * Math.PI) / 180)} ${R * Math.sin((-210 * Math.PI) / 180)} A${R} ${R} 0 1 1 ${R * Math.cos((30 * Math.PI) / 180)} ${R * Math.sin((30 * Math.PI) / 180)}`} fill="none" stroke={C.dim} strokeWidth={6} />
				<line x1={0} y1={0} x2={Math.sin(a) * (R - 20)} y2={-Math.cos(a) * (R - 20)} stroke={v > 0.6 ? C.red : C.green} strokeWidth={9} strokeLinecap="round" />
				<circle r={16} fill={C.ink} />
				<text x={-R + 10} y={R + 80} fill={C.green} fontFamily={F.label} fontWeight={800} fontSize={40}>
					CRAWL
				</text>
				<text x={R - 10} y={R + 80} textAnchor="end" fill={C.red} fontFamily={F.label} fontWeight={800} fontSize={40}>
					SPRINT
				</text>
			</g>
		</svg>
	);
};

/** Three ways to make power without air, drawn as simple machines; each draws on its word; `keep` fades the others. */
export const ThreeMachines: React.FC<{at: [number, number, number]; keep?: number}> = ({at, keep}) => {
	const f = useCurrentFrame();
	const fade = keep === undefined ? 0 : tw(f, keep, keep + 20, 0, 1);
	const items = [
		{t: 'STIRLING ENGINE', c: C.dim},
		{t: 'STEAM TURBINE', c: C.dim},
		{t: 'FUEL CELL', c: C.cyan},
	];
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{items.map((it, i) => {
				const k = tw(f, at[i] - 4, at[i] + 30, 0, 1, ez.sweep);
				const o = i < 2 ? 1 - 0.8 * fade : 1;
				const cx = 420 + i * 540;
				const cy = 500;
				const sel = i === 2 ? fade : 0;
				return (
					<g key={i} opacity={o * Math.min(1, k * 2)} transform={`translate(${cx} ${cy}) scale(${1 + 0.15 * sel})`}>
						{i === 0 ? (
							<g fill="none" stroke={C.ink} strokeWidth={5} pathLength={1}>
								<rect x={-70} y={-150} width={140} height={200} rx={10} pathLength={1} strokeDasharray={`${k} 1`} />
								<rect x={-55} y={-60 + 40 * Math.sin(f / 8)} width={110} height={40} fill={C.amber} fillOpacity={0.6} />
								<line x1={0} y1={-20 + 40 * Math.sin(f / 8)} x2={0} y2={110} />
								<circle cx={0} cy={140} r={50} pathLength={1} strokeDasharray={`${k} 1`} />
							</g>
						) : i === 1 ? (
							<g fill="none" stroke={C.ink} strokeWidth={5}>
								<circle r={110} pathLength={1} strokeDasharray={`${k} 1`} />
								<g transform={`rotate(${f * 6})`}>
									{Array.from({length: 12}).map((_, b) => (
										<line key={b} x1={0} y1={0} x2={0} y2={-100} transform={`rotate(${b * 30}) skewX(20)`} opacity={k} />
									))}
								</g>
							</g>
						) : (
							<g fill="none" stroke={C.cyan} strokeWidth={5}>
								{Array.from({length: 7}).map((_, p) => (
									<rect key={p} x={-120 + p * 36} y={-130} width={22} height={260} rx={4} fill={C.cyan} fillOpacity={0.15 + 0.35 * sel} opacity={tw(f, at[i] + p * 3, at[i] + p * 3 + 10, 0, 1)} />
								))}
							</g>
						)}
						<text y={230} textAnchor="middle" fill={i === 2 ? C.cyan : C.ink} fontFamily={F.label} fontWeight={800} fontSize={46} opacity={k}>
							{it.t}
						</text>
					</g>
				);
			})}
		</svg>
	);
};
