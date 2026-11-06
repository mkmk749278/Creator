import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {ez, tw, useSpring} from './kit';

// Drawings on the steel plate: the Kalvari side profile (same shape as Sub3D), the AIP plug, the patrol strip,
// silhouettes. ILLUSTRATION wherever shown (the real internal layout is not public).

export const SUB_LEN_M = 67.5;

/** Side-profile outline of the Kalvari-type hull: origin at the stern tip, x to the bow, `px` pixels per metre. */
export const hullPath = (px: number, len = SUB_LEN_M): string => {
	const R = 3.1;
	const r = (x: number) => {
		const bow = 9;
		const stern = 20 * (len / SUB_LEN_M);
		if (x > len - bow) {
			const u = (len - x) / bow;
			return R * Math.sqrt(Math.max(0, 1 - (1 - u) * (1 - u)));
		}
		if (x < stern) {
			const u = x / stern;
			return 0.35 + (R - 0.35) * Math.pow(Math.sin((u * Math.PI) / 2), 1.35);
		}
		return R;
	};
	const N = 90;
	const top: string[] = [];
	const bot: string[] = [];
	for (let i = 0; i <= N; i++) {
		const x = (i / N) * len;
		top.push(`${(x * px).toFixed(1)} ${(-r(x) * px).toFixed(1)}`);
		bot.push(`${(x * px).toFixed(1)} ${(r(x) * px).toFixed(1)}`);
	}
	return `M${top.join(' L')} L${bot.reverse().join(' L')} Z`;
};

/** The fin (sail) and masts, in the same units; `finAt` is the fin's aft edge in metres from the stern tip. */
export const finPath = (px: number, finAt = 41.5): string => {
	const x0 = finAt * px;
	const L = 9.5 * px;
	const h = 4.6 * px;
	const base = -2.6 * px;
	return `M${x0} ${base} L${x0 + L} ${base} L${x0 + L - 0.6 * px} ${base - h + 0.6 * px} Q${x0 + L - 1.2 * px} ${base - h} ${x0 + L - 2.2 * px} ${base - h} L${x0 + 1.2 * px} ${base - h} Q${x0 + 0.2 * px} ${base - h} ${x0 + 0.1 * px} ${base - h + 1.4 * px} Z`;
};

const sternPlanes = (px: number) => `M${1.2 * px} ${-0.5 * px} L${4.2 * px} ${-0.5 * px} L${4.4 * px} ${-3.9 * px} L${1.8 * px} ${-3.9 * px} Z M${1.2 * px} ${0.5 * px} L${4.2 * px} ${0.5 * px} L${4.4 * px} ${3.9 * px} L${1.8 * px} ${3.9 * px} Z`;

/** A drawn submarine in side view (blueprint lines), drawn on over `draw` frames from `a`. */
export const SubSide: React.FC<{
	x: number;
	y: number;
	px: number;
	a?: number;
	draw?: number;
	stroke?: string;
	fill?: string;
	len?: number;
	plug?: {at: number; len: number; glow: number; color?: string};
	opacity?: number;
	mast?: number;
}> = ({x, y, px, a = 0, draw = 40, stroke = C.ink, fill = 'rgba(10,16,24,0.85)', len = SUB_LEN_M, plug, opacity = 1, mast = 0}) => {
	const f = useCurrentFrame();
	const k = tw(f, a, a + draw, 0, 1, ez.sweep);
	const fillO = tw(f, a + draw * 0.6, a + draw, 0, 1);
	const finAt = len - 26;
	return (
		<g transform={`translate(${x} ${y})`} opacity={opacity}>
			<path d={hullPath(px, len)} fill={fill} fillOpacity={fillO} stroke={stroke} strokeWidth={3} pathLength={1} strokeDasharray={`${k} 1`} />
			<path d={finPath(px, finAt)} fill={fill} fillOpacity={fillO} stroke={stroke} strokeWidth={3} pathLength={1} strokeDasharray={`${k} 1`} />
			<path d={sternPlanes(px)} fill={fill} fillOpacity={fillO} stroke={stroke} strokeWidth={2.5} pathLength={1} strokeDasharray={`${k} 1`} />
			{mast > 0 ? <rect x={(finAt + 5) * px} y={(-7.2 - 4 * mast) * px} width={0.45 * px} height={4 * mast * px + 0.1} fill={stroke} /> : null}
			{plug ? (
				<g>
					<rect x={plug.at * px} y={-3.1 * px} width={plug.len * px} height={6.2 * px} fill={plug.color ?? C.amber} opacity={0.5 * plug.glow} />
					<rect x={plug.at * px} y={-3.1 * px} width={plug.len * px} height={6.2 * px} fill="none" stroke={plug.color ?? C.amber} strokeWidth={3} opacity={plug.glow} strokeDasharray="12 8" />
				</g>
			) : null}
		</g>
	);
};

/**
 * The patrol strip (the film's motif): a strip of time with red marks where the boat must snorkel.
 * `marks` = positions 0..1 along the strip; each mark enters at `markAt` (staggered), its width scales with `width`.
 */
export const PatrolStrip: React.FC<{
	x: number;
	y: number;
	w: number;
	draw: number;
	marks: number[];
	markAt: number;
	markW?: number; // px
	shrinkAt?: number; // marks get narrower
	fewerAt?: number; // every other mark drops out
	spreadTo?: number[]; // marks move here (the AIP spacing) from spreadAt
	spreadAt?: number;
	goneAt?: number; // the last mark goes out
	label?: string;
	days?: number; // tick labels: day numbers across the strip
}> = ({x, y, w, draw, marks, markAt, markW = 34, shrinkAt, fewerAt, spreadTo, spreadAt, goneAt, label = 'PATROL', days = 0}) => {
	const f = useCurrentFrame();
	const k = tw(f, draw, draw + 40, 0, 1, ez.sweep);
	const shrink = shrinkAt === undefined ? 1 : tw(f, shrinkAt, shrinkAt + 24, 1, 0.38, ez.arrive);
	const Hh = 90;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			<rect x={x} y={y} width={w * k} height={Hh} fill="rgba(3,7,13,0.82)" stroke={C.dim} strokeWidth={2} />
			{Array.from({length: days + 1}).map((_, i) => {
				const tx = x + (w * i) / Math.max(1, days);
				return tx <= x + w * k ? <line key={i} x1={tx} x2={tx} y1={y + Hh} y2={y + Hh + 14} stroke={C.dim} strokeWidth={2} /> : null;
			})}
			{marks.map((m, i) => {
				const at = markAt + i * 8;
				const p = tw(f, at, at + 12, 0, 1, ez.arrive);
				const drop = fewerAt !== undefined && i % 2 === 1 ? tw(f, fewerAt, fewerAt + 16, 1, 0, ez.leave) : 1;
				const gone = goneAt !== undefined ? tw(f, goneAt, goneAt + 30, 1, 0, ez.leave) : 1;
				const pos = spreadTo && spreadAt !== undefined ? interpolate(tw(f, spreadAt, spreadAt + 40, 0, 1, ez.sweep), [0, 1], [m, spreadTo[i] ?? m]) : m;
				const mw = markW * shrink * p;
				const vis = Math.min(drop, gone) * (spreadTo && spreadTo[i] === undefined && spreadAt !== undefined ? tw(f, spreadAt, spreadAt + 20, 1, 0) : 1);
				return (
					<rect key={i} x={x + pos * w - mw / 2} y={y + 6} width={mw} height={Hh - 12} fill={C.red} opacity={vis} style={{filter: 'drop-shadow(0 0 10px rgba(255,59,59,0.7))'}} />
				);
			})}
			<text x={x} y={y - 18} fill={C.dim} fontFamily={F.label} fontWeight={800} fontSize={34} letterSpacing={3} opacity={k}>
				{label}
			</text>
		</svg>
	);
};

/** The AIP plug drawn as a blueprint: a hull section with its four parts. `parts` lights each on its frame. */
export const PlugDrawing: React.FC<{x: number; y: number; s: number; a: number; parts?: [number, number, number, number]; onLand?: number}> = ({x, y, s, a, parts, onLand}) => {
	const f = useCurrentFrame();
	const k = tw(f, a, a + 50, 0, 1, ez.sweep);
	const W = 520 * s;
	const Hh = 300 * s;
	const names = ['POWDER', 'OXYGEN', 'FUEL CELLS', 'WASTE'];
	const cols = [C.ink, C.frost, C.cyan, C.dim];
	const land = onLand === undefined ? 0 : tw(f, onLand, onLand + 30, 0, 1, ez.arrive);
	return (
		<g transform={`translate(${x} ${y})`}>
			<rect x={-W / 2} y={-Hh / 2} width={W} height={Hh} rx={Hh / 2} fill="rgba(10,16,24,0.85)" stroke={C.amber} strokeWidth={4} pathLength={1} strokeDasharray={`${k} 1`} />
			{[0, 1, 2, 3].map((i) => {
				const cx = -W / 2 + (W / 4) * (i + 0.5);
				const lit = parts ? tw(f, parts[i], parts[i] + 12, 0, 1, ez.arrive) : tw(f, a + 30 + i * 8, a + 44 + i * 8, 0, 1);
				return (
					<g key={i} opacity={k}>
						<rect x={cx - W / 9} y={-Hh / 3} width={(W / 9) * 2} height={(Hh / 3) * 2} rx={8} fill={cols[i]} fillOpacity={0.12 + 0.4 * lit} stroke={cols[i]} strokeWidth={3} />
					</g>
				);
			})}
			{parts
				? names.map((n, i) => {
						const cx = -W / 2 + (W / 4) * (i + 0.5);
						const lit = tw(f, parts[i], parts[i] + 12, 0, 1, ez.arrive);
						return (
							<text key={n} x={cx} y={Hh / 2 + 56} textAnchor="middle" fill={cols[i]} fontFamily={F.label} fontWeight={800} fontSize={38} opacity={lit}>
								{n}
							</text>
						);
					})
				: null}
			{land > 0 ? (
				<g opacity={land}>
					<rect x={-W / 2 - 60} y={Hh / 2 + 6} width={W + 120} height={26} fill="#3b3326" stroke={C.dim} strokeWidth={2} />
					{[-1, 1].map((d) => (
						<rect key={d} x={d * (W / 2 - 40) - 22} y={Hh / 2 - 6} width={44} height={14} fill={C.dim} />
					))}
				</g>
			) : null}
		</g>
	);
};

/** A small boat silhouette (side), for counts: six boats, a German design, a nuclear boat. */
export const Silhouette: React.FC<{x: number; y: number; px: number; len?: number; color?: string; at?: number; opacity?: number}> = ({x, y, px, len = SUB_LEN_M, color = C.ink, at = 0, opacity = 1}) => {
	const p = useSpring(at);
	return (
		<g transform={`translate(${x} ${y + (1 - p) * 20})`} opacity={p * opacity}>
			<path d={hullPath(px, len)} fill={color} />
			<path d={finPath(px, len - 26)} fill={color} />
		</g>
	);
};
