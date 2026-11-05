import {noise2D} from '@remotion/noise';
import React, {useMemo} from 'react';
import {AbsoluteFill, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from './brand';

/** Film grain: SVG turbulence re-seeded every 2 frames (deterministic), soft-light over the picture. */
export const Grain: React.FC<{opacity?: number; id?: string}> = ({opacity = 0.16, id = 'g'}) => {
	const frame = useCurrentFrame();
	const seed = Math.floor(frame / 2) % 24;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity}}>
			<svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="none">
				<filter id={`${id}${seed}`}>
					<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={seed} stitchTiles="stitch" />
					<feColorMatrix type="saturate" values="0" />
				</filter>
				<rect width="1920" height="1080" filter={`url(#${id}${seed})`} />
			</svg>
		</AbsoluteFill>
	);
};

/** ~30% vignette (PLAYBOOK §6.1). */
export const Vignette: React.FC<{strength?: number}> = ({strength = 0.55}) => (
	<AbsoluteFill
		style={{
			pointerEvents: 'none',
			background: `radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 45%, rgba(0,0,0,${strength}) 100%)`,
		}}
	/>
);

/** Warm light leak drifting slowly across one side; colour = era (ember for steel, aviation blue for J.R.D.). */
export const LightLeak: React.FC<{color?: string; side?: 'left' | 'right'; strength?: number; seed?: string}> = ({
	color = colors.ember,
	side = 'left',
	strength = 0.22,
	seed = 'leak',
}) => {
	const frame = useCurrentFrame();
	const drift = noise2D(seed, frame / 300, 0);
	const pulse = 0.75 + 0.25 * noise2D(seed + 'p', frame / 90, 3);
	const cx = (side === 'left' ? 8 : 92) + drift * 6;
	const cy = 30 + noise2D(seed + 'y', 0, frame / 260) * 10;
	return (
		<AbsoluteFill
			style={{
				pointerEvents: 'none',
				mixBlendMode: 'screen',
				opacity: strength * pulse,
				background: `radial-gradient(ellipse 45% 60% at ${cx}% ${cy}%, ${color} 0%, rgba(0,0,0,0) 70%)`,
			}}
		/>
	);
};

type Mote = {x: number; y: number; r: number; speed: number; phase: number; a: number};

/** Dust in a light beam: slow, seeded motes with soft focus. */
export const Dust: React.FC<{count?: number; seed?: string; color?: string; opacity?: number}> = ({
	count = 70,
	seed = 'dust',
	color = '#F3DDBB',
	opacity = 0.55,
}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const motes = useMemo<Mote[]>(
		() =>
			new Array(count).fill(0).map((_, i) => ({
				x: random(`${seed}x${i}`) * width,
				y: random(`${seed}y${i}`) * height,
				r: 1 + random(`${seed}r${i}`) * 3.2,
				speed: 0.08 + random(`${seed}s${i}`) * 0.25,
				phase: random(`${seed}p${i}`) * 1000,
				a: 0.25 + random(`${seed}a${i}`) * 0.75,
			})),
		[count, seed, width, height],
	);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity}}>
			<svg width={width} height={height}>
				{motes.map((m, i) => {
					const t = frame + m.phase;
					const x = (m.x + noise2D(seed + i, t / 400, 0) * 80 + t * m.speed * 0.3) % width;
					const y = (m.y + noise2D(seed + i, 0, t / 380) * 60 - t * m.speed * 0.15 + height * 4) % height;
					const tw = 0.6 + 0.4 * noise2D(seed + 'tw' + i, t / 40, 0);
					return <circle key={i} cx={x} cy={y} r={m.r} fill={color} opacity={m.a * tw} style={{filter: `blur(${m.r * 0.6}px)`}} />;
				})}
			</svg>
		</AbsoluteFill>
	);
};

/** Rising embers/sparks (steel scenes): seeded, flickering, curving up with heat shimmer. */
export const Embers: React.FC<{count?: number; seed?: string; intensity?: number; originY?: number}> = ({
	count = 60,
	seed = 'emb',
	intensity = 1,
	originY = 1.05,
}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	return (
		<AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'screen'}}>
			<svg width={width} height={height}>
				{new Array(count).fill(0).map((_, i) => {
					const life = 140 + random(`${seed}l${i}`) * 220;
					const birth = random(`${seed}b${i}`) * life;
					const t = ((frame + birth) % life) / life;
					const x0 = random(`${seed}x${i}`) * width;
					const x = x0 + noise2D(seed + i, t * 3, 0) * 120 + t * 60;
					const y = height * originY - t * height * (0.7 + random(`${seed}h${i}`) * 0.6);
					const r = (1 + random(`${seed}r${i}`) * 2.6) * (1 - t * 0.6);
					const flick = 0.55 + 0.45 * noise2D(seed + 'f' + i, frame / 6, 0);
					const a = Math.sin(Math.PI * t) * flick * intensity;
					return (
						<circle key={i} cx={x} cy={y} r={r} fill={i % 3 === 0 ? '#FFD08A' : colors.ember} opacity={a} style={{filter: `blur(${r * 0.5}px)`}} />
					);
				})}
			</svg>
		</AbsoluteFill>
	);
};

/** 2.35:1 bars for dramatic scenes, sliding in. */
export const Letterbox: React.FC<{amount?: number}> = ({amount = 1}) => {
	const bar = (1080 - 1920 / 2.35) / 2;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', top: 0, left: 0, right: 0, height: bar * amount, background: '#000'}} />
			<div style={{position: 'absolute', bottom: 0, left: 0, right: 0, height: bar * amount, background: '#000'}} />
		</AbsoluteFill>
	);
};

/** The standard atmosphere stack for every shot: grain + vignette (+ optional leak, dust). */
export const Atmosphere: React.FC<{leak?: string | false; dust?: boolean; grain?: number; vignette?: number; seed?: string}> = ({
	leak = false,
	dust = false,
	grain = 0.16,
	vignette = 0.55,
	seed = 'atm',
}) => (
	<>
		{leak ? <LightLeak color={leak} seed={seed + 'leak'} /> : null}
		{dust ? <Dust seed={seed + 'dust'} /> : null}
		<Vignette strength={vignette} />
		<Grain opacity={grain} id={seed + 'g'} />
	</>
);
