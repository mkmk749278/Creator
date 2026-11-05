import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from './brand';
import {fontStacks} from './fonts';
import {ease, pop, tween} from './motion';

const bronzeText: React.CSSProperties = {
	background: `linear-gradient(180deg, #F3D9A4 0%, ${colors.gold} 38%, ${colors.bronze} 72%, #8A5426 100%)`,
	WebkitBackgroundClip: 'text',
	backgroundClip: 'text',
	color: 'transparent',
	textShadow: 'none',
	filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.7))',
};

/**
 * Place/date stamp (PLAYBOOK §8.8): engraved capitals, tracking closing in as it sharpens, a hairline rule.
 * Sits bottom-left by default; `at`/`until` are local frames.
 */
export const Stamp: React.FC<{text: string; sub?: string; at: number; until: number; align?: 'left' | 'center'; size?: number; y?: number}> = ({
	text,
	sub,
	at,
	until,
	align = 'left',
	size = 50,
	y = 0,
}) => {
	const frame = useCurrentFrame();
	const inP = tween(frame, at, at + 26, 0, 1, ease.arrive);
	const out = tween(frame, until - 18, until, 1, 0, ease.leave);
	const o = Math.min(inP, out);
	const track = 0.62 - 0.26 * inP;
	const blur = (1 - inP) * 8;
	const rule = tween(frame, at + 8, at + 40, 0, 1, ease.arrive);
	return (
		<AbsoluteFill
			style={{
				justifyContent: 'flex-end',
				alignItems: align === 'left' ? 'flex-start' : 'center',
				// v9: lifted to about 81 % of the height, clear of YouTube's progress bar and caption band on a phone
				padding: align === 'left' ? '0 0 200px 120px' : '0 0 200px 0',
				transform: `translateY(${y}px)`,
				pointerEvents: 'none',
			}}
		>
			<div style={{opacity: o, filter: `blur(${blur}px)`, textAlign: align, position: 'relative'}}>
				{/* a soft dark scrim behind the engraving, so it reads on bright archive photos too */}
				<div
					style={{
						position: 'absolute',
						left: -110,
						right: -140,
						top: -60,
						bottom: -50,
						background: 'radial-gradient(ellipse 64% 66% at 45% 50%, rgba(8,8,10,0.9) 0%, rgba(8,8,10,0.7) 48%, rgba(8,8,10,0) 80%)',
						zIndex: -1,
					}}
				/>
				<div style={{...bronzeText, fontFamily: fontStacks.display, fontWeight: 700, fontSize: size, letterSpacing: `${track}em`, lineHeight: 1.1}}>
					{text}
				</div>
				<div
					style={{
						height: 2,
						marginTop: 14,
						width: `${rule * 100}%`,
						background: `linear-gradient(90deg, ${colors.bronze}, rgba(197,125,60,0))`,
						marginLeft: align === 'center' ? 'auto' : 0,
						marginRight: align === 'center' ? 'auto' : 0,
					}}
				/>
				{sub ? (
					<div style={{fontFamily: fontStacks.text, fontWeight: 600, fontSize: Math.max(30, size * 0.62), letterSpacing: '0.12em', color: '#EFE6D3', marginTop: 12, textTransform: 'uppercase', textShadow: '0 2px 8px rgba(0,0,0,0.85)'}}>
						{sub}
					</div>
				) : null}
			</div>
		</AbsoluteFill>
	);
};

/**
 * Name lower-third: "NAME · role · years" (PLAYBOOK §8.8). v8: the same engraving as the Stamp (one caption system
 * for the film): the name in Cinzel bronze, a hairline, the role in Garamond, on the Stamp's soft scrim. No box.
 */
export const LowerThird: React.FC<{name: string; role?: string; at: number; until: number}> = ({name, role, at, until}) => (
	<Stamp text={name} sub={role} at={at} until={until} size={50} />
);

/** Indian grouping: 23175000 → 2,31,75,000. */
export const inr = (n: number): string => {
	const s = Math.round(n).toString();
	if (s.length <= 3) {
		return s;
	}
	const last3 = s.slice(-3);
	const rest = s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',');
	return `${rest},${last3}`;
};

/**
 * A number that springs up and lands exactly on `land` (the spoken word's frame), PLAYBOOK §8.4.
 * `format` defaults to Indian grouping. Big, bold, tabular figures.
 */
export const Counter: React.FC<{
	to: number;
	from?: number;
	start: number;
	land: number;
	prefix?: string;
	suffix?: string;
	format?: (n: number) => string;
	size?: number;
	color?: string;
	label?: string;
	style?: React.CSSProperties;
}> = ({to, from = 0, start, land, prefix = '', suffix = '', format = inr, size = 120, color = colors.ink, label, style}) => {
	const frame = useCurrentFrame();
	const v = tween(frame, start, land, from, to, ease.arrive);
	const landed = frame >= land;
	const flash = tween(frame, land, land + 30, 1, 0, ease.leave);
	return (
		<div style={{textAlign: 'center', ...style}}>
			<div
				style={{
					fontFamily: fontStacks.numbers,
					fontWeight: 700,
					fontSize: size,
					fontVariantNumeric: 'lining-nums tabular-nums',
					letterSpacing: '0.02em',
					color: landed ? colors.gold : color,
					textShadow: `0 0 ${40 * flash}px rgba(212,175,55,${0.8 * flash}), 0 4px 18px rgba(0,0,0,0.8)`,
				}}
			>
				{prefix}
				{format(v)}
				{suffix}
			</div>
			{label ? (
				<div style={{fontFamily: fontStacks.text, fontWeight: 600, fontSize: size * 0.2, letterSpacing: '0.3em', color: colors.muted, textTransform: 'uppercase', marginTop: 8}}>
					{label}
				</div>
			) : null}
		</div>
	);
};

/** A short kinetic word or phrase (2–4 words), PLAYBOOK §6.3.3. Rises in with tracking, fades out. */
export const Kinetic: React.FC<{
	text: string;
	at: number;
	until: number;
	size?: number;
	color?: string;
	x?: number;
	y?: number;
	display?: boolean;
	scrim?: number;
}> = ({
	text,
	at,
	until,
	size = 72,
	color = colors.ink,
	x = 0,
	y = 0,
	display = false,
	scrim = 1,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = pop(frame, fps, at, 150, 22);
	const o = Math.min(p, tween(frame, until - 14, until, 1, 0, ease.leave));
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', pointerEvents: 'none'}}>
			{/* A soft dark pool behind the words: bronze on a sepia photograph is otherwise unreadable. */}
			<div
				style={{
					position: 'absolute',
					width: size * Math.max(4, text.length * 0.9),
					height: size * 2.6,
					transform: `translate(${x}px, ${y}px)`,
					opacity: o * scrim,
					background: 'radial-gradient(ellipse at center, rgba(8,8,10,0.78) 0%, rgba(8,8,10,0.5) 42%, rgba(8,8,10,0) 72%)',
				}}
			/>
			<div
				style={{
					transform: `translate(${x}px, ${y + (1 - p) * 26}px)`,
					opacity: o,
					fontFamily: display ? fontStacks.display : fontStacks.text,
					fontWeight: 700,
					fontSize: size,
					letterSpacing: display ? `${0.3 - 0.1 * p}em` : '0.02em',
					color,
					textShadow: '0 4px 24px rgba(0,0,0,0.85)',
					textAlign: 'center',
					whiteSpace: 'pre',
					...(display ? bronzeText : {}),
				}}
			>
				{text}
			</div>
		</AbsoluteFill>
	);
};

export {bronzeText};
