// Year roller (PLAYBOOK §8.4): an engraved brass odometer that rolls from one year to another with a whoosh and lands
// with a thud. Every digit column carries like a real counter; speed blurs the digits vertically.
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {fontStacks} from '../fonts';
import {ease, pop, tween} from '../motion';
import {SfxCue} from '../sfx';

export const yearRollerCues = (start: number, land: number): SfxCue[] => [
	{frame: start, sfx: 'whoosh_long', gainDb: -8},
	{frame: start + Math.round((land - start) * 0.4), sfx: 'mechanical_tick_run', gainDb: -16},
	{frame: land, sfx: 'thud_metal', gainDb: -6},
];

const DIGIT_H = 1.15; // line height in em

/**
 * The value shown by column `i` (0 = units) when the counter reads `v`, like a real odometer: a column turns only
 * while every column below it shows 9 and is rolling over.
 */
const columnValue = (v: number, i: number): number => {
	if (i === 0) {
		return v;
	}
	const lower = columnValue(v, i - 1);
	const ld = ((Math.floor(lower) % 10) + 10) % 10;
	return Math.floor(v / Math.pow(10, i)) + (ld === 9 ? lower - Math.floor(lower) : 0);
};

export const YearRoller: React.FC<{from: number; to: number; start: number; land: number; size?: number; label?: string}> = ({
	from,
	to,
	start,
	land,
	size = 220,
	label,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const v = tween(frame, start, land, from, to, ease.sweep);
	const vPrev = tween(frame - 1, start, land, from, to, ease.sweep);
	const speed = Math.abs(v - vPrev) * fps; // years per second
	const digits = String(Math.max(from, to)).length;
	const landed = pop(frame, fps, land, 220, 12);
	const flash = frame >= land ? tween(frame, land, land + 36, 1, 0, ease.leave) : 0;
	const enter = pop(frame, fps, start - 24, 120, 18);
	return (
		// centred in the frame (it was a bare block, so it sat in the top-left corner wherever a caller forgot to centre it)
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', pointerEvents: 'none'}}>
		<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: enter, transform: `scale(${0.92 + 0.08 * enter})`}}>
			<svg width={0} height={0} style={{position: 'absolute'}}>
				<filter id="yr-vblur">
					<feGaussianBlur stdDeviation={`0 ${Math.min(14, speed * 0.9).toFixed(2)}`} />
				</filter>
			</svg>
			<div
				style={{
					display: 'flex',
					gap: size * 0.06,
					padding: `${size * 0.12}px ${size * 0.16}px`,
					background: 'linear-gradient(180deg, #2A2018 0%, #17120E 100%)',
					border: `3px solid ${colors.bronze}`,
					borderRadius: 8,
					boxShadow: `0 20px 60px rgba(0,0,0,0.7), inset 0 2px 0 rgba(255,220,160,0.15), 0 0 ${60 * flash}px rgba(212,175,55,${0.5 * flash})`,
					transform: `translateY(${(1 - landed) * -6}px)`,
				}}
			>
				{new Array(digits).fill(0).map((_, k) => {
					const i = digits - 1 - k;
					const cv = columnValue(v, i);
					const moving = Math.abs(cv - columnValue(vPrev, i)) * fps > 0.3;
					const frac = cv - Math.floor(cv);
					const d = Math.floor(cv) % 10;
					return (
						<div
							key={k}
							style={{
								position: 'relative',
								width: size * 0.62,
								height: size * DIGIT_H,
								overflow: 'hidden',
								background: 'linear-gradient(180deg, #0B0A09 0%, #1C1712 50%, #0B0A09 100%)',
								borderRadius: 4,
								boxShadow: 'inset 0 10px 18px rgba(0,0,0,0.9), inset 0 -10px 18px rgba(0,0,0,0.9)',
							}}
						>
							<div style={{position: 'absolute', left: 0, right: 0, top: -frac * size * DIGIT_H, filter: moving ? 'url(#yr-vblur)' : undefined}}>
								{[d, (d + 1) % 10].map((n, j) => (
									<div
										key={j}
										style={{
											height: size * DIGIT_H,
											lineHeight: `${size * DIGIT_H}px`,
											textAlign: 'center',
											fontFamily: fontStacks.display,
											fontWeight: 700,
											fontSize: size,
											background: `linear-gradient(180deg, #F3D9A4 0%, ${colors.gold} 40%, ${colors.bronze} 75%, #8A5426 100%)`,
											WebkitBackgroundClip: 'text',
											backgroundClip: 'text',
											color: 'transparent',
										}}
									>
										{n}
									</div>
								))}
							</div>
						</div>
					);
				})}
			</div>
			{label ? (
				<div style={{marginTop: size * 0.14, fontFamily: fontStacks.text, fontWeight: 600, fontSize: size * 0.13, letterSpacing: '0.4em', color: colors.muted}}>{label}</div>
			) : null}
		</div>
		</AbsoluteFill>
	);
};
