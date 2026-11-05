import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {inkPalette} from './InkFigure';
import {smoothClosed, smoothOpen} from './draw';
import {V2, boil, hash, seedOf} from './rig';

/** The INK world: an SVG stage over charcoal blueprint paper. Children are SVG (figures, props, ink lines). */
export const InkStage: React.FC<{children: React.ReactNode; paper?: boolean; grid?: number; style?: React.CSSProperties}> = ({
	children,
	paper = true,
	grid = 0.07,
	style,
}) => (
	<AbsoluteFill style={{background: colors.bg, ...style}}>
		{paper ? <InkPaper grid={grid} /> : null}
		<AbsoluteFill>
			<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{overflow: 'visible'}}>
				{children}
			</svg>
		</AbsoluteFill>
	</AbsoluteFill>
);

/** Charcoal blueprint paper: a faint grid that boils at 12 fps with the lines, and paper fibre. */
export const InkPaper: React.FC<{grid?: number}> = ({grid = 0.07}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const fr = Math.floor((frame / fps) * 12) % 3;
	const step = 64;
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} viewBox="0 0 1920 1080">
				<defs>
					<filter id={`paper${fr}`}>
						<feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves={3} seed={fr + 3} />
						<feColorMatrix type="matrix" values="0 0 0 0 0.75  0 0 0 0 0.55  0 0 0 0 0.38  0 0 0 0.05 0" />
					</filter>
					<radialGradient id="paperWarm" cx="50%" cy="45%" r="75%">
						<stop offset="0%" stopColor="#1A1714" />
						<stop offset="100%" stopColor={colors.bg} />
					</radialGradient>
				</defs>
				<rect width={1920} height={1080} fill="url(#paperWarm)" />
				<rect width={1920} height={1080} filter={`url(#paper${fr})`} />
				<g stroke={colors.muted} strokeWidth={1} opacity={grid}>
					{new Array(Math.ceil(1920 / step) + 1).fill(0).map((_, i) => (
						<line key={`v${i}`} x1={i * step + (hash(i + fr * 31) - 0.5) * 0.8} y1={0} x2={i * step + (hash(i + 7 + fr * 31) - 0.5) * 0.8} y2={1080} />
					))}
					{new Array(Math.ceil(1080 / step) + 1).fill(0).map((_, i) => (
						<line key={`h${i}`} x1={0} y1={i * step + (hash(i + 99 + fr * 17) - 0.5) * 0.8} x2={1920} y2={i * step + (hash(i + 55 + fr * 17) - 0.5) * 0.8} />
					))}
				</g>
			</svg>
		</AbsoluteFill>
	);
};

/** A hand-inked line (props, buildings, horizon): a polyline that boils at 12 fps like the figures. */
export const InkLine: React.FC<{
	pts: V2[];
	seed: string;
	w?: number;
	color?: string;
	opacity?: number;
	amp?: number;
	closed?: boolean;
	fill?: string;
	dash?: string;
	/** Draw a smooth curve through the points instead of straight segments. */
	smooth?: boolean;
}> = ({pts, seed, w = 2.4, color = inkPalette.ink, opacity = 1, amp = 0.9, closed = false, fill = 'none', dash, smooth = false}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const s = seedOf(seed);
	const jittered: V2[] = pts.map((p, i) => {
		const b = boil(t, s + i * 3.3, amp);
		return [p[0] + b[0], p[1] + b[1]];
	});
	const d = smooth
		? closed
			? smoothClosed(jittered)
			: smoothOpen(jittered)
		: `M${jittered.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join('L')}${closed ? 'Z' : ''}`;
	return <path d={d} fill={fill} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" opacity={opacity} strokeDasharray={dash} />;
};
