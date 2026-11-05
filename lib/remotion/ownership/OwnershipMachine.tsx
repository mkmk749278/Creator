// The ownership machine (the answer): Tata Sons as a riveted steel mould. The charitable trusts' share pours in as
// molten metal and cools to bronze; the Sir Dorabji Tata Trust's part at the base turns gold, with the diamond's glint
// under it; then the Shapoorji Pallonji group and Tata's own companies slide in as steel blocks. Heights are to scale
// (claims T76, T77, T111: trusts about 66%, the Dorabji trust 27.98%, Shapoorji Pallonji 18.37%, Tata companies about
// 13%; the small rest is drawn but not named). The only numbers on screen are the VO's: two thirds, 28%.
import {noise2D} from '@remotion/noise';
import React from 'react';
import {random, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {fontStacks} from '../fonts';
import {ease, pop, tween} from '../motion';
import {SfxCue} from '../sfx';

export const SHARES = {trusts: 0.66, dorabji: 0.2798, shapoorji: 0.1837, companies: 0.13} as const;

export type OwnershipTimeline = {pourFrom: number; pourTo: number; dorabji: number; shapoorji: number; companies: number};
export const ownershipDefaults: OwnershipTimeline = {pourFrom: 30, pourTo: 220, dorabji: 280, shapoorji: 380, companies: 450};

export const ownershipCues = (tl: OwnershipTimeline = ownershipDefaults): SfxCue[] => [
	{frame: tl.pourFrom - 20, sfx: 'ladle_tilt_creak', gainDb: -16},
	{frame: tl.pourFrom, sfx: 'molten_pour_long', gainDb: -8},
	{frame: tl.pourTo, sfx: 'metal_settle_hiss', gainDb: -14},
	{frame: tl.dorabji, sfx: 'diamond_glint_shimmer', gainDb: -12},
	{frame: tl.shapoorji + 22, sfx: 'steel_block_thud', gainDb: -8},
	{frame: tl.companies + 22, sfx: 'steel_block_thud', gainDb: -10},
];

// mould geometry (stage px): front face, plus a receding right side and top for 2.5D
const X0 = 760;
const W = 400;
const BOT = 968;
const H = 590;
const DX = 70;
const DY = -38;
const yAt = (share: number): number => BOT - share * H;

const face = (y0: number, y1: number): string => `M${X0} ${y0}L${X0 + W} ${y0}L${X0 + W} ${y1}L${X0} ${y1}Z`;
const side = (y0: number, y1: number): string => `M${X0 + W} ${y0}L${X0 + W + DX} ${y0 + DY}L${X0 + W + DX} ${y1 + DY}L${X0 + W} ${y1}Z`;
const top = (y: number): string => `M${X0} ${y}L${X0 + W} ${y}L${X0 + W + DX} ${y + DY}L${X0 + DX} ${y + DY}Z`;

/** A block of share: front, side and top faces in one tone. */
const Block: React.FC<{y0: number; y1: number; front: string; sideTone: string; topTone: string; edge: string; opacity?: number; dy?: number}> = ({
	y0,
	y1,
	front,
	sideTone,
	topTone,
	edge,
	opacity = 1,
	dy = 0,
}) => (
	<g transform={`translate(0 ${dy})`} opacity={opacity}>
		<path d={side(y0, y1)} fill={sideTone} stroke={edge} strokeWidth={1.2} />
		<path d={face(y0, y1)} fill={front} stroke={edge} strokeWidth={1.4} />
		{/* rolled-steel grain and a row of bolts along the seam */}
		{new Array(Math.max(2, Math.floor((y0 - y1) / 7))).fill(0).map((_, i) => (
			<path key={i} d={`M${X0 + 6} ${y1 + 4 + i * 7}H${X0 + W - 6}`} stroke="#FFFFFF" strokeOpacity={0.035} strokeWidth={1} />
		))}
		{new Array(9).fill(0).map((_, i) => (
			<circle key={`b${i}`} cx={X0 + 24 + i * ((W - 48) / 8)} cy={y0 - 9} r={3} fill="#6A6E76" stroke="#1A1B1E" strokeWidth={1} />
		))}
		<path d={top(y1)} fill={topTone} stroke={edge} strokeWidth={1.2} />
	</g>
);

const Label: React.FC<{y0: number; y1: number; name: string; value?: string; at: number; gold?: boolean; leftSide?: boolean}> = ({y0, y1, name, value, at, gold, leftSide}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = pop(frame, fps, at, 150, 20);
	const draw = tween(frame, at, at + 24, 0, 1, ease.sweep);
	if (frame < at) {
		return null;
	}
	const bx = leftSide ? X0 - 158 : X0 + W + DX + 108;
	const s = leftSide ? -1 : 1;
	const mid = (y0 + y1) / 2;
	const col = gold ? colors.gold : colors.ink;
	return (
		<g opacity={Math.min(1, p * 1.2)}>
			{/* a bracket spanning the share, drawn on */}
			<path
				d={`M${bx} ${y0 - 4}l${s * 16} 0L${bx + s * 16} ${y1 + 4}l${-s * 16} 0`}
				fill="none"
				stroke={gold ? colors.gold : colors.muted}
				strokeWidth={2}
				strokeDasharray={2000}
				strokeDashoffset={2000 * (1 - draw)}
			/>
			<g transform={`translate(${bx + s * (34 + (1 - p) * 30)} ${mid})`}>
				{value ? (
					<text
						textAnchor={leftSide ? 'end' : 'start'}
						y={-6}
						fontFamily={fontStacks.numbers}
						fontWeight={700}
						fontSize={58}
						fill={col}
						style={{filter: gold ? 'drop-shadow(0 0 14px rgba(212,175,55,0.6))' : undefined}}
					>
						{value}
					</text>
				) : null}
				<text
					textAnchor={leftSide ? 'end' : 'start'}
					y={value ? 30 : 10}
					fontFamily={fontStacks.text}
					fontWeight={700}
					fontSize={22}
					letterSpacing="0.2em"
					fill={gold ? colors.gold : colors.muted}
				>
					{name}
				</text>
			</g>
		</g>
	);
};

export const OwnershipMachine: React.FC<{timeline?: OwnershipTimeline}> = ({timeline = ownershipDefaults}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const tl = timeline;

	// the pour: level rises to two thirds; the metal cools from white-hot to bronze after it settles
	const level = tween(frame, tl.pourFrom, tl.pourTo, 0, SHARES.trusts, ease.camera);
	const pouring = frame >= tl.pourFrom - 10 && frame <= tl.pourTo + 10;
	const cool = tween(frame, tl.pourTo, tl.pourTo + 90, 0, 1, ease.leave);
	const hot = (c0: string, c1: string) => (cool < 1 ? c0 : c1);
	const wobble = pouring ? noise2D('pour', t * 3, 0) * 5 : 0;
	const yLevel = yAt(level);
	const gold = tween(frame, tl.dorabji, tl.dorabji + 40, 0, 1, ease.arrive);
	const ladleTilt = tween(frame, tl.pourFrom - 30, tl.pourFrom, 0, 1, ease.camera) - tween(frame, tl.pourTo, tl.pourTo + 30, 0, 1, ease.camera);

	// steel blocks drop in from above and land on the stack
	const drop = (at: number) => {
		const p = pop(frame, fps, at, 140, 16);
		return {dy: (1 - p) * -520, o: tween(frame, at, at + 10, 0, 1, ease.arrive)};
	};
	const sp = drop(tl.shapoorji);
	const tc = drop(tl.companies);
	const rest = drop(tl.companies + 20);
	const shake = (at: number) => (frame >= at + 20 && frame < at + 34 ? Math.sin((frame - at) * 2.4) * (34 - (frame - at)) * 0.25 : 0);
	const jolt = shake(tl.shapoorji) + shake(tl.companies);

	const yT = yAt(SHARES.trusts);
	const yD = yAt(SHARES.dorabji);
	const yS = yAt(SHARES.trusts + SHARES.shapoorji);
	const yC = yAt(SHARES.trusts + SHARES.shapoorji + SHARES.companies);
	const yTop = yAt(1);

	const molten = '#FFC25A';
	const glint = 0.6 + 0.4 * Math.sin(t * 3.2);
	return (
		<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>
			<defs>
				<linearGradient id="om-molten" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#FFF4D2" />
					<stop offset="0.25" stopColor={molten} />
					<stop offset="1" stopColor="#D2601E" />
				</linearGradient>
				<linearGradient id="om-bronze" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#6E4523" />
					<stop offset="0.45" stopColor={colors.bronze} />
					<stop offset="1" stopColor="#7A4C26" />
				</linearGradient>
				<linearGradient id="om-gold" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#8F6F1E" />
					<stop offset="0.45" stopColor="#F3D58A" />
					<stop offset="1" stopColor="#9A7722" />
				</linearGradient>
				<linearGradient id="om-steel" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#2A2C31" />
					<stop offset="0.5" stopColor="#4A4E56" />
					<stop offset="1" stopColor="#2A2C31" />
				</linearGradient>
				<filter id="om-blur">
					<feGaussianBlur stdDeviation={14} />
				</filter>
			</defs>
			<g transform={`translate(${jolt} 0)`}>
				{/* the steel structure: girder columns, a top beam carrying the name plate, cross-bracing */}
				{[X0 - 120, X0 + W + DX + 70].map((x, i) => (
					<g key={`gc${i}`}>
						<rect x={x - 14} y={yTop - 150} width={28} height={BOT - yTop + 172} fill="#17181B" stroke={colors.bronze} strokeWidth={1.4} />
						<path d={`M${x - 6} ${yTop - 150}V${BOT + 22}M${x + 6} ${yTop - 150}V${BOT + 22}`} stroke={colors.bronze} strokeOpacity={0.35} strokeWidth={1} />
						{new Array(12).fill(0).map((_, k) => (
							<circle key={k} cx={x} cy={yTop - 130 + k * ((BOT - yTop + 140) / 11)} r={2.4} fill={colors.bronze} opacity={0.7} />
						))}
					</g>
				))}
				<rect x={X0 - 150} y={yTop - 164} width={W + DX + 290} height={26} fill="#17181B" stroke={colors.bronze} strokeWidth={1.4} />
				{[0, 1, 2].map((k) => {
					const ya = yTop - 138 + k * ((BOT - yTop + 138) / 3);
					const yb = ya + (BOT - yTop + 138) / 3;
					return (
						<g key={`br${k}`} stroke={colors.bronze} strokeOpacity={0.28} strokeWidth={3}>
							<path d={`M${X0 - 120} ${ya}L${X0 - 14} ${yb}M${X0 - 120} ${yb}L${X0 - 14} ${ya}`} />
							<path d={`M${X0 + W + 14} ${ya}L${X0 + W + DX + 70} ${yb}M${X0 + W + 14} ${yb}L${X0 + W + DX + 70} ${ya}`} />
						</g>
					);
				})}
				{/* the mould's back walls and floor */}
				<path d={`M${X0 + DX} ${yTop + DY}L${X0 + W + DX} ${yTop + DY}L${X0 + W + DX} ${BOT + DY}L${X0 + DX} ${BOT + DY}Z`} fill="#141518" stroke={colors.muted} strokeOpacity={0.4} strokeWidth={1.2} />
				<path d={`M${X0} ${BOT}L${X0 + DX} ${BOT + DY}L${X0 + DX} ${yTop + DY}L${X0} ${yTop}Z`} fill="#111215" stroke={colors.muted} strokeOpacity={0.4} strokeWidth={1.2} />
				{/* scale ticks on the back wall: tenths, the blueprint under the story */}
				{new Array(11).fill(0).map((_, i) => (
					<path key={i} d={`M${X0 + DX} ${yAt(i / 10) + DY}l${W} 0`} stroke={colors.muted} strokeOpacity={0.12} strokeWidth={1} strokeDasharray="4 6" />
				))}

				{/* the trusts' metal: molten while it pours, then bronze; the Dorabji part turns gold */}
				{level > 0 ? (
					<>
						<path d={side(BOT, yLevel + wobble * 0.3)} fill={cool < 1 ? '#C2521C' : '#5E3B1F'} />
						<path d={face(BOT, yLevel + wobble)} fill={cool < 0.5 ? 'url(#om-molten)' : 'url(#om-bronze)'} />
						<path d={face(BOT, yLevel + wobble)} fill="url(#om-molten)" opacity={1 - cool} />
						<path d={top(yLevel + wobble)} fill={hot('#FFF0C0', '#B0743C')} opacity={1} />
						<path d={face(BOT, yLevel)} fill="#FFB050" opacity={0.35 * (1 - cool)} filter="url(#om-blur)" />
						{/* cast texture as it cools: pour lines and pits */}
						<g opacity={cool * 0.5}>
							{new Array(14).fill(0).map((_, i) => {
								const y = BOT - 12 - i * ((BOT - yLevel - 20) / 14);
								return <path key={i} d={`M${X0 + 8} ${y}Q${X0 + W / 2} ${y - 4 + (i % 3) * 3} ${X0 + W - 8} ${y}`} stroke="#3A2414" strokeWidth={1} fill="none" />;
							})}
						</g>
						{/* the pour lights the frame */}
						<ellipse cx={X0 + W / 2} cy={yLevel} rx={420} ry={160} fill="#FF9A45" opacity={0.18 * (1 - cool)} filter="url(#om-blur)" style={{mixBlendMode: 'screen'}} />
					</>
				) : null}
				{gold > 0 ? (
					<g opacity={gold}>
						<path d={side(BOT, yD)} fill="#7A5E1A" />
						<path d={face(BOT, yD)} fill="url(#om-gold)" />
						<path d={face(BOT, yD)} fill="#F3D58A" opacity={0.25 * glint} filter="url(#om-blur)" />
						<path d={`M${X0} ${yD}L${X0 + W} ${yD}L${X0 + W + DX} ${yD + DY}`} stroke="#FFF1C4" strokeWidth={2} fill="none" />
					</g>
				) : null}
				{/* the diamond's glint at the base: the one white-hot point */}
				{gold > 0 ? (
					<g transform={`translate(${X0 + W / 2} ${BOT - 40}) scale(${1.0 + 0.7 * gold})`} opacity={gold}>
						<circle r={46} fill="#FFFFFF" opacity={0.18 * glint} filter="url(#om-blur)" />
						<path d="M0 -15 L13 -4 L0 15 L-13 -4 Z" fill="#F4FBFF" stroke="#BFD7E6" strokeWidth={1.2} />
						<path d="M-13 -4 L13 -4 M0 -15 L-5 -4 L0 15 L5 -4 Z" fill="none" stroke="#9FB9C9" strokeWidth={0.8} />
						<g transform={`rotate(${t * 20})`} opacity={glint}>
							<path d="M0 -40 L3 -3 L40 0 L3 3 L0 40 L-3 3 L-40 0 L-3 -3 Z" fill="#FFFFFF" />
						</g>
					</g>
				) : null}

				{/* the rest of Tata Sons: steel blocks from above */}
				{frame >= tl.shapoorji ? <Block y0={yT} y1={yS} front="url(#om-steel)" sideTone="#24262B" topTone="#5A5F68" edge={colors.muted} opacity={sp.o} dy={sp.dy} /> : null}
				{frame >= tl.companies ? <Block y0={yS} y1={yC} front="#2C2B2E" sideTone="#1E1E21" topTone="#46454A" edge={colors.muted} opacity={tc.o} dy={tc.dy} /> : null}
				{frame >= tl.companies + 20 ? <Block y0={yC} y1={yTop} front="#1E1F22" sideTone="#18191B" topTone="#2E2F33" edge={colors.muted} opacity={rest.o * 0.9} dy={rest.dy} /> : null}

				{/* the mould's front frame: riveted steel flanges and the engraved name plate */}
				{[X0 - 14, X0 + W].map((x, i) => (
					<g key={i}>
						<rect x={x} y={yTop - 30} width={14} height={BOT - yTop + 50} fill="#1C1D21" stroke={colors.bronze} strokeWidth={1.6} />
						{new Array(18).fill(0).map((_, k) => (
							<circle key={k} cx={x + 7} cy={yTop - 14 + k * ((BOT - yTop + 30) / 17)} r={2.6} fill={colors.bronze} opacity={0.8} />
						))}
					</g>
				))}
				<rect x={X0 - 40} y={BOT + 20} width={W + DX + 80} height={22} fill="#1C1D21" stroke={colors.bronze} strokeWidth={1.6} />

				{/* the ladle above, tilting to pour; the stream falls to the surface */}
				<g transform={`translate(${X0 + W - 40} ${yTop - 210}) rotate(${ladleTilt * 38})`}>
					<path d="M-70 -40 L70 -40 L56 40 L-56 40 Z" fill="#1E1D20" stroke={colors.gold} strokeWidth={2} />
					<path d="M-74 -40 L74 -40" stroke={colors.gold} strokeWidth={4} />
					<ellipse cx={0} cy={-40} rx={66} ry={10} fill={molten} opacity={0.8 * (1 - cool)} />
				</g>
				{pouring ? (
					<g>
						<path
							d={`M${X0 + W - 102} ${yTop - 236} Q ${X0 + W - 120} ${yTop - 150} ${X0 + W - 110 + wobble} ${yLevel}`}
							stroke="#FFF4D2"
							strokeWidth={16 * Math.min(ladleTilt * 1.5, 1)}
							fill="none"
							strokeLinecap="round"
						/>
						<path
							d={`M${X0 + W - 102} ${yTop - 236} Q ${X0 + W - 120} ${yTop - 150} ${X0 + W - 110 + wobble} ${yLevel}`}
							stroke="#FFB050"
							strokeWidth={44}
							fill="none"
							opacity={0.35}
							filter="url(#om-blur)"
						/>
						{new Array(24).fill(0).map((_, i) => {
							const life = 0.4 + random(`os${i}`) * 0.5;
							const a = ((t + random(`oa${i}`) * life) % life) / life;
							const ang = -Math.PI * (0.1 + random(`og${i}`) * 0.8);
							const v = 120 + random(`ov${i}`) * 200;
							return (
								<circle
									key={i}
									cx={X0 + W - 110 + Math.cos(ang) * v * a * life}
									cy={yLevel + Math.sin(ang) * v * a * life + 400 * (a * life) ** 2}
									r={2}
									fill="#FFE2A8"
									opacity={1 - a}
								/>
							);
						})}
					</g>
				) : null}
				{/* the name plate, in front of the pour */}
				<g transform={`translate(${X0 + W / 2} ${yTop - 70})`}>
					<rect x={-190} y={-38} width={380} height={64} fill="#16171A" stroke={colors.bronze} strokeWidth={2} />
					{[-176, 176].map((x) => [-24, 12].map((y) => <circle key={`${x}${y}`} cx={x} cy={y} r={3.5} fill={colors.bronze} />))}
					<text
						textAnchor="middle"
						y={8}
						fontFamily={fontStacks.display}
						fontWeight={700}
						fontSize={40}
						letterSpacing="0.3em"
						style={{fill: 'url(#om-gold)'}}
					>
						TATA SONS
					</text>
				</g>
			</g>

			{/* labels: the VO's own words and numbers only */}
			<Label y0={yT} y1={BOT} name="CHARITABLE TRUSTS" value="TWO THIRDS" at={tl.pourTo - 20} leftSide />
			<Label y0={yD} y1={BOT} name="SIR DORABJI TATA TRUST" value="28%" at={tl.dorabji + 10} gold />
			<Label y0={yS} y1={yT} name="SHAPOORJI PALLONJI GROUP" at={tl.shapoorji + 24} />
			<Label y0={yC} y1={yS} name="TATA COMPANIES" at={tl.companies + 24} />
		</svg>
	);
};
