// Gem comparison to scale (cold open: "Two hundred and forty five carats. More than twice the size of the Kohinoor,
// as it is today."). The Jubilee (a cushion cut, 245.35 ct, claims T01) beside the Koh-i-Noor as recut in 1852 (an
// oval brilliant, 105.6 ct, claims T02).
//
// The maths of "to scale": both are diamond, so weight ∝ volume. Similar solids scale volume with the cube of their
// size, so linear size ∝ weight^(1/3) and the area you see from above ∝ weight^(2/3).
//   weight ratio  245.35 / 105.6       = 2.323
//   linear ratio  2.323^(1/3)          = 1.325
//   area ratio    2.323^(2/3)          = 1.755
// The two outlines differ in shape, so each is scaled until its own polygon area matches its target area exactly.
// (Real stones are not perfectly similar solids; this is the honest first-order picture, labelled with real weights.)
import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {fontStacks} from '../fonts';
import {ease, pop, tween} from '../motion';
import {SfxCue} from '../sfx';

type P = [number, number];

export const GEMS = {jubilee: 245.35, kohinoor: 105.6} as const;
export const AREA_RATIO = Math.pow(GEMS.jubilee / GEMS.kohinoor, 2 / 3);

export const gemCues = (kohinoorAt: number, jubileeAt: number): SfxCue[] => [
	{frame: kohinoorAt, sfx: 'glass_ting_soft', gainDb: -14},
	{frame: jubileeAt, sfx: 'riser_short', gainDb: -12},
	{frame: jubileeAt + 30, sfx: 'diamond_glint_shimmer', gainDb: -10},
];

/** Outline r(θ): a cushion (superellipse, n≈4) or an oval (ellipse). Unit-ish size before area scaling. */
const outline = (kind: 'cushion' | 'oval', n = 96): P[] =>
	new Array(n).fill(0).map((_, i) => {
		const a = (i / n) * Math.PI * 2;
		if (kind === 'oval') {
			return [Math.cos(a) * 1.0, Math.sin(a) * 0.78];
		}
		const e = 2 / 3.6;
		const c = Math.cos(a);
		const s = Math.sin(a);
		return [Math.sign(c) * Math.abs(c) ** e * 1.0, Math.sign(s) * Math.abs(s) ** e * 0.92];
	});

const areaOf = (pts: P[]): number => Math.abs(pts.reduce((s, p, i) => {
	const q = pts[(i + 1) % pts.length];
	return s + p[0] * q[1] - q[0] * p[1];
}, 0)) / 2;

const pathOf = (pts: P[]): string => `M${pts.map((p) => `${p[0].toFixed(2)} ${p[1].toFixed(2)}`).join('L')}Z`;

/** A faceted top view: table, star and kite facets mapped onto the outline. */
const Facets: React.FC<{pts: P[]; stroke: string; w: number}> = ({pts, stroke, w}) => {
	const n = pts.length;
	const k = 8;
	const at = (j: number, s: number): P => {
		const p = pts[Math.round((j / k) * n) % n];
		return [p[0] * s, p[1] * s];
	};
	const lines: string[] = [];
	for (let j = 0; j < k; j++) {
		const t0 = at(j, 0.5);
		const t1 = at(j + 1, 0.5);
		const g = at(j + 0.5, 1);
		const g0 = at(j, 1);
		lines.push(`M${t0[0]} ${t0[1]}L${t1[0]} ${t1[1]}`); // table edge
		lines.push(`M${t0[0]} ${t0[1]}L${at(j + 0.5, 0.72)[0]} ${at(j + 0.5, 0.72)[1]}L${t1[0]} ${t1[1]}`); // star
		lines.push(`M${at(j + 0.5, 0.72)[0]} ${at(j + 0.5, 0.72)[1]}L${g[0]} ${g[1]}`); // to girdle
		lines.push(`M${t0[0]} ${t0[1]}L${g0[0]} ${g0[1]}`); // kite main
	}
	return <path d={lines.join('')} stroke={stroke} strokeWidth={w} fill="none" strokeLinejoin="round" />;
};

const Gem: React.FC<{kind: 'cushion' | 'oval'; area: number; x: number; y: number; grow: number; hot: boolean; id: string}> = ({kind, area, x, y, grow, hot, id}) => {
	const frame = useCurrentFrame();
	const base = useMemo(() => outline(kind), [kind]);
	const s = Math.sqrt(area / areaOf(base));
	const pts = base.map(([px, py]) => [px * s, py * s] as P);
	const glint = 0.55 + 0.45 * Math.sin(frame / 14 + (hot ? 0 : 2));
	return (
		<g transform={`translate(${x} ${y}) scale(${grow})`}>
			<defs>
				<radialGradient id={`${id}-g`} cx="0.38" cy="0.32" r="0.8">
					<stop offset="0" stopColor={hot ? '#FFFFFF' : '#D9E2E8'} />
					<stop offset="0.5" stopColor={hot ? '#DCEBF5' : '#8E9AA3'} />
					<stop offset="1" stopColor={hot ? '#7F98AA' : '#3E464C'} />
				</radialGradient>
				<filter id={`${id}-b`}>
					<feGaussianBlur stdDeviation={18} />
				</filter>
			</defs>
			{hot ? <path d={pathOf(pts)} fill="#FFFFFF" opacity={0.22 * glint} filter={`url(#${id}-b)`} /> : null}
			<path d={pathOf(pts)} fill={`url(#${id}-g)`} stroke={hot ? '#FFFFFF' : '#B8C3CA'} strokeWidth={2.4} />
			<Facets pts={pts} stroke={hot ? 'rgba(90,120,140,0.55)' : 'rgba(40,50,58,0.6)'} w={1.4} />
			{hot ? (
				<g transform={`translate(${-s * 0.35} ${-s * 0.3}) rotate(${frame * 0.6})`} opacity={glint}>
					<path d="M0 -46 L4 -4 L46 0 L4 4 L0 46 L-4 4 L-46 0 L-4 -4 Z" fill="#FFFFFF" />
				</g>
			) : null}
		</g>
	);
};

export const GemCompare: React.FC<{kohinoorAt?: number; jubileeAt?: number; kohinoorArea?: number}> = ({kohinoorAt = 20, jubileeAt = 80, kohinoorArea = 52000}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const k = pop(frame, fps, kohinoorAt, 140, 18);
	const j = pop(frame, fps, jubileeAt, 110, 14);
	const lk = tween(frame, kohinoorAt + 16, kohinoorAt + 40, 0, 1, ease.arrive);
	const lj = tween(frame, jubileeAt + 20, jubileeAt + 44, 0, 1, ease.arrive);
	const jArea = kohinoorArea * AREA_RATIO;
	const label = (x: number, y: number, name: string, ct: string, o: number, gold: boolean) => (
		<g opacity={o} transform={`translate(${x} ${y + (1 - o) * 14})`}>
			<text textAnchor="middle" fontFamily={fontStacks.display} fontWeight={700} fontSize={40} letterSpacing="0.18em" fill={gold ? colors.gold : colors.ink}>
				{name}
			</text>
			<text textAnchor="middle" y={44} fontFamily={fontStacks.numbers} fontWeight={700} fontSize={30} letterSpacing="0.08em" fill={gold ? colors.gold : colors.muted}>
				{ct}
			</text>
		</g>
	);
	return (
		<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>
			{/* a shared baseline: both stones sit on the same line, centred in their halves */}
			<line x1={300} x2={1620} y1={790} y2={790} stroke={colors.bronze} strokeOpacity={0.35} strokeWidth={1.5} strokeDasharray="6 8" />
			<Gem kind="oval" area={kohinoorArea} x={640} y={540} grow={k} hot={false} id="koh" />
			<Gem kind="cushion" area={jArea} x={1240} y={540} grow={j} hot id="jub" />
			{label(640, 850, 'KOH-I-NOOR TODAY', '105.6 CARATS', lk, false)}
			{label(1240, 850, 'JUBILEE', '245.35 CARATS', lj, true)}
		</svg>
	);
};
