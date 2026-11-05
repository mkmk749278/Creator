import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from './brand';
import {ease, pop, tween} from './motion';

/**
 * A document on the isometric desk (owner's directive G.1 §3; PLAYBOOK §8.3): perspective(1000px) rotateX(10deg)
 * rotateY(-5deg), paper texture, soft shadow, a slow drift, dropped in with a spring at `at`.
 * Children are laid out on the page (a real scan via `file`, or typeset period text for a quote card that is clearly
 * typography, never a fake of a real document).
 */
export const Paper: React.FC<{
	at?: number;
	width?: number;
	height?: number;
	file?: string;
	x?: number;
	y?: number;
	tone?: 'cream' | 'newsprint' | 'card';
	seed?: string;
	children?: React.ReactNode;
}> = ({at = 0, width = 1100, height, file, x = 0, y = 0, tone = 'cream', seed = 'paper', children}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = pop(frame, fps, at, 100, 17);
	const sway = noise2D(seed, frame / 260, 0);
	const bg =
		tone === 'newsprint'
			? 'linear-gradient(170deg, #E4DCC8 0%, #D8CDB2 100%)'
			: tone === 'card'
				? 'linear-gradient(170deg, #E9DDC2 0%, #D9C7A2 100%)'
				: 'linear-gradient(165deg, #F1E8D3 0%, #E3D4B3 70%, #D3BF97 100%)';
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', perspective: 1000}}>
			<div
				style={{
					position: 'relative',
					width,
					height,
					background: bg,
					boxShadow: `0 40px 80px rgba(0,0,0,${0.6 * p}), 0 6px 14px rgba(0,0,0,0.4)`,
					transform: `translate(${x}px, ${y + (1 - p) * 140}px) rotateX(${10 + sway * 1.5}deg) rotateY(${-5 + sway * 2}deg) rotate(${sway * 0.6}deg)`,
					opacity: Math.min(1, p * 1.5),
					overflow: 'hidden',
				}}
			>
				{file ? <Img src={staticFile(file)} style={{width: '100%', display: 'block', mixBlendMode: 'multiply'}} /> : null}
				{children}
				{/* paper fibre and edge burn */}
				<svg style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'multiply', opacity: 0.35, pointerEvents: 'none'}}>
					<filter id={`${seed}fib`}>
						<feTurbulence type="fractalNoise" baseFrequency="0.9 0.25" numOctaves={3} seed={7} />
						<feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0.55 0" />
					</filter>
					<rect width="100%" height="100%" filter={`url(#${seed}fib)`} />
				</svg>
				<div style={{position: 'absolute', inset: 0, boxShadow: 'inset 0 0 90px rgba(90,60,25,0.45)', pointerEvents: 'none'}} />
			</div>
		</AbsoluteFill>
	);
};

/**
 * Highlighter sweeping across a span exactly as the voice reads it (G.1 §3). Position in the parent's pixels.
 * `from`/`to` = local frames of the first and last highlighted word.
 */
export const Highlight: React.FC<{x: number; y: number; w: number; h: number; from: number; to: number; color?: string}> = ({
	x,
	y,
	w,
	h,
	from,
	to,
	color = colors.gold,
}) => {
	const frame = useCurrentFrame();
	const p = tween(frame, from, to, 0, 1, ease.sweep);
	return (
		<svg style={{position: 'absolute', left: x, top: y, width: w, height: h, overflow: 'visible', pointerEvents: 'none', mixBlendMode: 'multiply'}}>
			<rect x={0} y={h * 0.08} width={w * p} height={h * 0.84} rx={h * 0.18} fill={color} opacity={0.55} />
		</svg>
	);
};

/** Period type set on a paper: for a quote card that is plainly typography (never imitates a real document). */
export const PaperText: React.FC<{children: React.ReactNode; size?: number; pad?: number; serif?: boolean; color?: string}> = ({
	children,
	size = 40,
	pad = 70,
	serif = true,
	color = '#2E2418',
}) => (
	<div
		style={{
			padding: pad,
			fontFamily: serif ? "'Cinzel', serif" : "'Inter', sans-serif",
			fontSize: size,
			lineHeight: 1.45,
			color,
			letterSpacing: serif ? '0.04em' : '0.01em',
		}}
	>
		{children}
	</div>
);
