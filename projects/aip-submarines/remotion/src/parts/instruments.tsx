import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {ez, tw, useSpring} from './kit';

// Instruments drawn for the film: the battery gauge, the radar scope and sweep, the acoustic line, the exhaust plume,
// the cut line over real footage. Everything a function of the frame; times are local to the enclosing Sequence.

/** Battery gauge: a cell outline whose charge falls from `from` to `to` (0..1) between frames a and b. Red below 20%. */
export const Battery: React.FC<{x: number; y: number; a: number; b: number; from: number; to: number; scale?: number; label?: string; appear?: number}> = ({
	x,
	y,
	a,
	b,
	from,
	to,
	scale = 1,
	label = 'BATTERY',
	appear = 0,
}) => {
	const f = useCurrentFrame();
	const p = useSpring(appear);
	const v = tw(f, a, b, from, to, ez.sweep);
	const col = v < 0.2 ? C.red : v < 0.45 ? C.amber : C.green;
	const blink = v < 0.2 ? 0.55 + 0.45 * Math.round((Math.sin(f / 7) + 1) / 2) : 1;
	const W = 300;
	const Hh = 120;
	return (
		<div style={{position: 'absolute', left: x, top: y, transform: `scale(${scale * (0.9 + 0.1 * p)})`, transformOrigin: '0 0', opacity: p}}>
			<div style={{background: 'rgba(3,7,13,0.78)', padding: '18px 22px', display: 'flex', alignItems: 'center', gap: 22}}>
				<svg width={W + 24} height={Hh}>
					<rect x={3} y={3} width={W - 6} height={Hh - 6} rx={14} fill="none" stroke={C.ink} strokeWidth={6} />
					<rect x={W} y={Hh / 2 - 22} width={18} height={44} rx={4} fill={C.ink} />
					<rect x={14} y={14} width={Math.max(0, (W - 28) * v)} height={Hh - 28} rx={6} fill={col} opacity={blink} />
				</svg>
				<div>
					<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 34, color: C.dim, letterSpacing: 2}}>{label}</div>
					<div style={{fontFamily: F.mono, fontWeight: 700, fontSize: 72, color: col, lineHeight: 1}}>{Math.round(v * 100)}%</div>
				</div>
			</div>
		</div>
	);
};

/** A sweeping radar line over the picture with a blip that lands at frame `blip` at (bx, by). */
export const RadarSweep: React.FC<{cx: number; cy: number; r: number; blip?: number; bx?: number; by?: number; lock?: number; color?: string}> = ({
	cx,
	cy,
	r,
	blip,
	bx = cx,
	by = cy,
	lock,
	color = C.red,
}) => {
	const f = useCurrentFrame();
	const ang = (f * 2.4) % 360;
	const bp = blip === undefined ? 0 : tw(f, blip, blip + 8, 0, 1, ez.arrive);
	const lk = lock === undefined ? 0 : tw(f, lock, lock + 14, 0, 1, ez.arrive);
	const pulse = (f - (blip ?? 0)) % 40;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			<defs>
				<radialGradient id="sweepG" cx="0" cy="0" r="1">
					<stop offset="0" stopColor={C.cyan} stopOpacity="0.0" />
					<stop offset="1" stopColor={C.cyan} stopOpacity="0.32" />
				</radialGradient>
			</defs>
			{[0.33, 0.66, 1].map((k) => (
				<circle key={k} cx={cx} cy={cy} r={r * k} fill="none" stroke={C.cyan} strokeOpacity={0.22} strokeWidth={2} />
			))}
			<g transform={`rotate(${ang} ${cx} ${cy})`}>
				<path d={`M${cx} ${cy} L${cx + r} ${cy} A${r} ${r} 0 0 0 ${cx + r * Math.cos(-0.5)} ${cy + r * Math.sin(-0.5)} Z`} fill={C.cyan} opacity={0.18} />
				<line x1={cx} y1={cy} x2={cx + r} y2={cy} stroke={C.cyan} strokeWidth={3} opacity={0.8} />
			</g>
			{bp > 0 ? (
				<g>
					<circle cx={bx} cy={by} r={12 * bp} fill={color} />
					<circle cx={bx} cy={by} r={12 + pulse * 1.4} fill="none" stroke={color} strokeWidth={3} opacity={Math.max(0, 1 - pulse / 40)} />
				</g>
			) : null}
			{lk > 0 ? (
				<g opacity={lk} stroke={color} strokeWidth={5} fill="none">
					{[0, 1, 2, 3].map((i) => {
						const s = 70 - 20 * lk;
						const dx = i % 2 ? 1 : -1;
						const dy = i > 1 ? 1 : -1;
						return <path key={i} d={`M${bx + dx * s} ${by + dy * (s - 26)} L${bx + dx * s} ${by + dy * s} L${bx + dx * (s - 26)} ${by + dy * s}`} />;
					})}
				</g>
			) : null}
		</svg>
	);
};

/** Diesel exhaust from the mast head: a soft plume of seeded puffs drifting downwind. */
export const Exhaust: React.FC<{x: number; y: number; start: number; scale?: number}> = ({x, y, start, scale = 1}) => {
	const f = useCurrentFrame();
	if (f < start) {
		return null;
	}
	const puffs = Array.from({length: 40}, (_, i) => i);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			{puffs.map((i) => {
				const born = start + i * 4;
				const age = f - born;
				if (age < 0 || age > 150) {
					return null;
				}
				const t = age / 150;
				const px = x + (180 * t + 30 * noise2D('ex' + i, t * 2, 0)) * scale;
				const py = y - (120 * Math.sqrt(t) + 20 * noise2D('ey' + i, 0, t * 2)) * scale;
				const sz = (30 + 160 * t) * scale;
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: px - sz / 2,
							top: py - sz / 2,
							width: sz,
							height: sz,
							borderRadius: '50%',
							background: 'radial-gradient(circle, rgba(140,150,165,0.45), rgba(140,150,165,0) 70%)',
							opacity: (1 - t) * Math.min(1, age / 10) * 0.8,
							filter: 'blur(6px)',
						}}
					/>
				);
			})}
		</AbsoluteFill>
	);
};

/** A glowing cut line drawn around a hull in real footage, with sparks where the line is being drawn. */
export const CutLine: React.FC<{d: string; a: number; b: number; len: number; color?: string; tip?: (k: number) => [number, number]}> = ({d, a, b, len, color = C.orange, tip}) => {
	const f = useCurrentFrame();
	const k = tw(f, a, b, 0, 1, ez.sweep);
	if (f < a) {
		return null;
	}
	const [tx, ty] = tip ? tip(k) : [0, 0];
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			<defs>
				<filter id="glowCut" x="-50%" y="-50%" width="200%" height="200%">
					<feGaussianBlur stdDeviation="7" result="b" />
					<feMerge>
						<feMergeNode in="b" />
						<feMergeNode in="SourceGraphic" />
					</feMerge>
				</filter>
			</defs>
			<path d={d} fill="none" stroke={color} strokeWidth={7} strokeDasharray={`${len * k} ${len}`} filter="url(#glowCut)" strokeLinecap="round" />
			{tip && k < 1
				? Array.from({length: 16}, (_, i) => {
						const age = ((f * 1.0 + i * 3.7) % 18) / 18;
						const ang = random('sp' + i + Math.floor((f + i * 3.7) / 18)) * Math.PI - Math.PI;
						const dist = 20 + 90 * age;
						return <circle key={i} cx={tx + Math.cos(ang) * dist} cy={ty + Math.sin(ang) * dist + 60 * age * age} r={3.5 * (1 - age)} fill="#ffd27a" opacity={1 - age} />;
					})
				: null}
		</svg>
	);
};

/** A ring of sound: concentric arcs leaving a point (active sonar), and the echo coming back. */
export const Ping: React.FC<{x: number; y: number; start: number; period?: number; color?: string; max?: number}> = ({x, y, start, period = 50, color = C.cyan, max = 700}) => {
	const f = useCurrentFrame();
	if (f < start) {
		return null;
	}
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			{[0, 1, 2].map((i) => {
				const age = (f - start - i * period) / (period * 3);
				if (age < 0 || age > 1) {
					return null;
				}
				return <circle key={i} cx={x} cy={y} r={max * age} fill="none" stroke={color} strokeWidth={4} opacity={(1 - age) * 0.9} />;
			})}
		</svg>
	);
};

/** Blinking word for the "exposed" ring: a red ring that locks around a point. */
export const RedRing: React.FC<{x: number; y: number; at: number; r?: number}> = ({x, y, at, r = 120}) => {
	const f = useCurrentFrame();
	const p = tw(f, at, at + 14, 0, 1, ez.arrive);
	if (p <= 0) {
		return null;
	}
	const rr = interpolate(p, [0, 1], [r * 2.2, r]);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			<circle cx={x} cy={y} r={rr} fill="none" stroke={C.red} strokeWidth={6} opacity={p} />
			<circle cx={x} cy={y} r={rr + 16} fill="none" stroke={C.red} strokeWidth={2} opacity={p * 0.6} strokeDasharray="10 14" />
		</svg>
	);
};
