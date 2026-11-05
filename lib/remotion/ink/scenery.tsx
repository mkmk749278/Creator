// INK scenery: the world the figures stand in, drawn with the same boiling bronze line on charcoal.
import {noise2D} from '@remotion/noise';
import React from 'react';
import {random, useCurrentFrame, useVideoConfig} from 'remotion';
import {InkLine} from './InkStage';
import {inkPalette} from './InkFigure';
import {V2} from './rig';

const DARK = '#121317';

/** A dusk sky over the works: charcoal at the top, furnace glow at the horizon. */
export const DuskSky: React.FC<{horizon: number; glow?: string; glowX?: number; id?: string; strength?: number}> = ({
	horizon,
	glow = '#B4521F',
	glowX = 0.35,
	id = 'dusk',
	strength = 1,
}) => {
	const frame = useCurrentFrame();
	const pulse = 0.9 + 0.1 * noise2D(id, frame / 120, 0);
	return (
		<g>
			<defs>
				<linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#0B0D12" stopOpacity={0.0} />
					<stop offset={(horizon / 1080) * 0.6} stopColor="#1A1714" stopOpacity={0.55} />
					<stop offset={horizon / 1080} stopColor="#4A2614" stopOpacity={0.75 * strength} />
					<stop offset={Math.min(1, horizon / 1080 + 0.02)} stopColor="#1B1410" stopOpacity={0.6} />
					<stop offset="1" stopColor="#0D0E11" stopOpacity={0.2} />
				</linearGradient>
				<radialGradient id={`${id}-glow`} cx={glowX} cy={horizon / 1080} r="0.55" gradientTransform={`translate(${glowX} ${horizon / 1080}) scale(1 0.45) translate(${-glowX} ${-horizon / 1080})`}>
					<stop offset="0" stopColor={glow} stopOpacity={0.62 * strength * pulse} />
					<stop offset="0.45" stopColor={glow} stopOpacity={0.18 * strength * pulse} />
					<stop offset="1" stopColor={glow} stopOpacity={0} />
				</radialGradient>
			</defs>
			<rect width={1920} height={1080} fill={`url(#${id}-sky)`} />
			<rect width={1920} height={1080} fill={`url(#${id}-glow)`} style={{mixBlendMode: 'screen'}} />
		</g>
	);
};

/** Soft smoke drifting from a point (stack tops), seeded and slow. */
export const Smoke: React.FC<{from: V2; seed: string; scale?: number; color?: string; opacity?: number; wind?: number}> = ({
	from,
	seed,
	scale = 1,
	color = '#3A3330',
	opacity = 0.5,
	wind = 0.6,
}) => {
	const frame = useCurrentFrame();
	const puffs = 9;
	return (
		<g style={{filter: `blur(${10 * scale}px)`}} opacity={opacity}>
			{new Array(puffs).fill(0).map((_, i) => {
				const life = 420;
				const t = ((frame + (i * life) / puffs + random(`${seed}${i}`) * 40) % life) / life;
				const x = from[0] + t * 260 * wind * scale + noise2D(seed + i, t * 2, 0) * 30 * scale;
				const y = from[1] - t * 220 * scale;
				const r = (16 + t * 70) * scale;
				return <circle key={i} cx={x} cy={y} r={r} fill={color} opacity={Math.sin(Math.PI * t) * 0.9} />;
			})}
		</g>
	);
};

/** A 1910s–1920s steelworks on the horizon: blast furnace towers, hot-blast stoves, chimneys, a few lit windows. */
export const Steelworks: React.FC<{x: number; ground: number; scale?: number; seed?: string; lit?: boolean}> = ({x, ground, scale = 1, seed = 'works', lit = true}) => {
	const frame = useCurrentFrame();
	const S = (px: number, py: number): V2 => [x + px * scale, ground - py * scale];
	const flick = (i: number) => 0.55 + 0.45 * noise2D(`${seed}w${i}`, frame / 50, 0);
	// blast furnace: a tapering tower with a bustle pipe and a charging incline; stoves: domed cylinders
	const furnace = (cx: number, hgt: number, i: number) => [
		<InkLine
			key={`f${i}`}
			seed={`${seed}f${i}`}
			closed
			fill={DARK}
			w={1.8}
			pts={[S(cx - 34, 0), S(cx - 30, hgt * 0.55), S(cx - 22, hgt * 0.85), S(cx - 14, hgt), S(cx + 14, hgt), S(cx + 22, hgt * 0.85), S(cx + 30, hgt * 0.55), S(cx + 34, 0)]}
		/>,
		<InkLine key={`fb${i}`} seed={`${seed}fb${i}`} w={1.4} pts={[S(cx - 40, hgt * 0.32), S(cx + 40, hgt * 0.32)]} />,
		<InkLine key={`fd${i}`} seed={`${seed}fd${i}`} w={1.4} pts={[S(cx, hgt), S(cx + 6, hgt + 40), S(cx - 70, hgt + 52)]} />,
		<InkLine key={`fi${i}`} seed={`${seed}fi${i}`} w={1.4} pts={[S(cx + 14, hgt), S(cx + 170, 0)]} />,
		<InkLine key={`fj${i}`} seed={`${seed}fj${i}`} w={1.1} pts={[S(cx + 30, hgt * 0.85), S(cx + 150, 0)]} opacity={0.6} />,
	];
	const stove = (cx: number, hgt: number, i: number) => (
		<InkLine
			key={`s${i}`}
			seed={`${seed}s${i}`}
			closed
			fill={DARK}
			w={1.6}
			pts={[S(cx - 18, 0), S(cx - 18, hgt), S(cx - 12, hgt + 12), S(cx, hgt + 16), S(cx + 12, hgt + 12), S(cx + 18, hgt), S(cx + 18, 0)]}
		/>
	);
	const chimney = (cx: number, hgt: number, i: number) => (
		<InkLine key={`c${i}`} seed={`${seed}c${i}`} closed fill={DARK} w={1.6} pts={[S(cx - 9, 0), S(cx - 6, hgt), S(cx + 6, hgt), S(cx + 9, 0)]} />
	);
	return (
		<g>
			{[0, 1, 2].map((i) => (
				<Smoke key={`sm${i}`} seed={`${seed}sm${i}`} from={S([-120, 260, 410][i], [300, 330, 280][i])} scale={scale} opacity={0.4} />
			))}
			{/* the shed: a long low roof line */}
			<InkLine seed={`${seed}shed`} closed fill={DARK} w={1.6} pts={[S(-420, 0), S(-420, 70), S(-260, 110), S(-100, 70), S(-100, 0)]} />
			<InkLine seed={`${seed}shed2`} closed fill={DARK} w={1.6} pts={[S(470, 0), S(470, 60), S(620, 96), S(780, 60), S(780, 0)]} />
			{chimney(-120, 300, 0)}
			{chimney(260, 330, 1)}
			{chimney(410, 280, 2)}
			{stove(-20, 150, 0)}
			{stove(20, 150, 1)}
			{stove(60, 150, 2)}
			{furnace(140, 210, 0)}
			{stove(330, 135, 3)}
			{stove(365, 135, 4)}
			{furnace(520, 190, 1)}
			{lit
				? [S(-380, 30), S(-330, 30), S(-280, 34), S(-220, 30), S(520, 26), S(570, 26), S(640, 30), S(700, 26)].map((p, i) => (
						<rect key={`w${i}`} x={p[0]} y={p[1] - 8 * scale} width={14 * scale} height={10 * scale} fill="#FFB25E" opacity={0.65 * flick(i)} style={{filter: `blur(${1.2 * scale}px)`}} />
					))
				: null}
			{/* the furnace mouth glowing at the base */}
			<ellipse cx={S(140, 0)[0]} cy={S(140, 6)[1]} rx={60 * scale} ry={14 * scale} fill="#FF7A2A" opacity={0.5 * flick(20)} style={{filter: `blur(${10 * scale}px)`}} />
			<ellipse cx={S(520, 0)[0]} cy={S(520, 6)[1]} rx={50 * scale} ry={12 * scale} fill="#FF7A2A" opacity={0.4 * flick(21)} style={{filter: `blur(${10 * scale}px)`}} />
		</g>
	);
};

/** A line of sal trees: the jungle the town was cut from. */
export const TreeLine: React.FC<{x0: number; x1: number; ground: number; seed: string; height?: number}> = ({x0, x1, ground, seed, height = 110}) => {
	const n = Math.round((x1 - x0) / 46);
	const pts: V2[] = [[x0, ground]];
	for (let i = 0; i <= n; i++) {
		const x = x0 + (i / n) * (x1 - x0);
		const hgt = height * (0.6 + random(`${seed}${i}`) * 0.5);
		pts.push([x - 14, ground - hgt * 0.75], [x, ground - hgt], [x + 16, ground - hgt * 0.8]);
	}
	pts.push([x1, ground]);
	return <InkLine seed={seed} pts={pts} closed fill="#0F1013" w={1.4} opacity={0.9} amp={0.6} />;
};

export {inkPalette};
