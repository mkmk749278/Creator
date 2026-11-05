// Ownership flow (plan_v7; replaces the molten "ownership machine" the outside review read as a school science tank).
// Tata Sons as an institution. v8 (both outside reviews: "a dark dashboard"): drawn in ink on drafting vellum under the
// lamp, cards like pinned paper slips, warm ochre pulses where the money moves, labels big enough for a phone.
// Owners come in on the VO's words; the share bar inside Tata Sons is to scale (claims T76, T77, T111: trusts about
// 66%, the Sir Dorabji Tata Trust 27.98%, the Shapoorji Pallonji group 18.37%, Tata companies about 13%); the only
// numbers on screen are the VO's: TWO THIRDS and 28%. Then the money moves: dividends rise from the companies to Tata
// Sons and on to the trusts, and out of the trusts into hospitals, research and scholarships.
import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {fontStacks} from '../fonts';
import {ease, pop, tween} from '../motion';
import {SfxCue} from '../sfx';
import {SHARES} from './OwnershipMachine';

export type FlowTimeline = {
	sons: number;
	trusts: number;
	dorabji: number;
	shapoorji: number;
	companies: number;
	/** dividends rise (companies → Tata Sons → trusts) */
	up: number;
	/** money goes out of the trusts (hospitals, research, scholarships) */
	out: number;
};
/** Everything already in place, money moving gently: for the shots that come back to the structure. */
export const FLOW_HELD: FlowTimeline = {sons: -900, trusts: -800, dorabji: -700, shapoorji: -600, companies: -500, up: -400, out: -300};

export const flowCues = (t: FlowTimeline): SfxCue[] => [
	{frame: t.sons, sfx: 'glass_panel_slide', gainDb: -14},
	{frame: t.trusts, sfx: 'glass_panel_slide', gainDb: -12},
	{frame: t.dorabji, sfx: 'diamond_glint_shimmer', gainDb: -12},
	{frame: t.shapoorji, sfx: 'tick_soft', gainDb: -14},
	{frame: t.companies, sfx: 'tick_soft', gainDb: -14},
	{frame: t.up, sfx: 'data_pulse_rise', gainDb: -14},
	{frame: t.out, sfx: 'data_pulse_rise', gainDb: -14},
];

const INK = '#2B2318';
const OCHRE = '#B5542A';
const GOLD_INK = '#9C6B1E';
const GLASS = 'rgba(255,250,236,0.62)';
const EDGE = 'rgba(43,35,24,0.62)';
const COMPANIES = ['T.C.S.', 'TATA STEEL', 'TATA MOTORS', 'TATA CONSUMER', 'TITAN', 'AIR INDIA'];

const Card: React.FC<{x: number; y: number; w: number; h: number; at: number; children?: React.ReactNode; glow?: string; dim?: number}> = ({x, y, w, h, at, children, glow, dim = 1}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = pop(frame, fps, at, 140, 20);
	if (frame < at) return null;
	return (
		<div
			style={{
				position: 'absolute',
				left: x - w / 2,
				top: y - h / 2,
				width: w,
				height: h,
				background: GLASS,
				border: `1.5px solid ${EDGE}`,
				borderRadius: 10,
				boxShadow: `0 6px 18px rgba(60,40,20,0.28)${glow ? `, 0 0 40px ${glow}` : ''}`,
				opacity: Math.min(1, p * 1.4) * dim,
				transform: `translateY(${(1 - p) * 24}px) scale(${0.97 + 0.03 * p})`,
			}}
		>
			{children}
		</div>
	);
};

const Label: React.FC<{children: React.ReactNode; size?: number; color?: string; spacing?: string; weight?: number}> = ({children, size = 26, color = INK, spacing = '0.2em', weight = 700}) => (
	<div style={{fontFamily: fontStacks.text, fontWeight: weight, fontSize: size, letterSpacing: spacing, color, whiteSpace: 'nowrap'}}>{children}</div>
);

/** A bus line drawn on at `at` over `dur`, with light pulses running along it from `pulseFrom` (direction a → b). */
const Bus: React.FC<{d: string; len: number; at: number; dur?: number; pulseFrom?: number; color?: string; seed: string}> = ({d, len, at, dur = 40, pulseFrom = 1e9, color = GOLD_INK, seed}) => {
	const frame = useCurrentFrame();
	const p = tween(frame, at, at + dur, 0, 1, ease.sweep);
	if (p <= 0) return null;
	const pulses = frame >= pulseFrom ? [0, 1, 2] : [];
	return (
		<g>
			<path d={d} fill="none" stroke={EDGE} strokeWidth={2.6} strokeLinecap="round" strokeDasharray={`${len * p} ${len}`} />
			{pulses.map((k) => {
				const t = ((frame - pulseFrom) / 80 + k / 3 + noise2D(seed, k, 0) * 0.02) % 1;
				const L = Math.min(90, len * 0.35);
				return (
					<g key={k} opacity={Math.sin(Math.PI * t)}>
						<path d={d} fill="none" stroke={color} strokeWidth={7} strokeLinecap="round" strokeDasharray={`${L} ${len + L}`} strokeDashoffset={L - t * (len + L)} opacity={0.4} style={{filter: 'blur(3px)'}} />
						<path d={d} fill="none" stroke={color} strokeWidth={3.2} strokeLinecap="round" strokeDasharray={`${L * 0.6} ${len + L}`} strokeDashoffset={L * 0.6 - t * (len + L)} />
					</g>
				);
			})}
		</g>
	);
};

export const OwnershipFlow: React.FC<{t: FlowTimeline; background?: string}> = ({t, background}) => {
	const frame = useCurrentFrame();
	const {durationInFrames} = useVideoConfig();
	// the camera: close on Tata Sons, easing back as the owners arrive, then a slow drift
	const open = tween(frame, t.trusts - 50, t.trusts + 30, 0, 1, ease.camera);
	// never a still frame: a slow push and a lateral drift for the whole shot (the v7b cut froze here for 10 s)
	const drift = tween(frame, 0, durationInFrames, 0, 1, ease.camera);
	const zoom = 1.3 - 0.28 * open + 0.07 * drift;
	const camX = 40 - 80 * drift;
	const camY = 170 * (1 - open);
	// the share bar inside Tata Sons, to scale
	const BW = 640;
	const seg = (from: number, share: number) => tween(frame, from, from + 50, 0, share, ease.arrive) * BW;
	const trustsW = seg(t.trusts, SHARES.trusts);
	const dorW = seg(t.dorabji, SHARES.dorabji);
	const spW = seg(t.shapoorji, SHARES.shapoorji);
	const coW = seg(t.companies, SHARES.companies);
	const glint = tween(frame, t.dorabji + 20, t.dorabji + 40, 0, 1) * (1 - tween(frame, t.dorabji + 60, t.dorabji + 120, 0, 1));
	return (
		<AbsoluteFill style={{background: '#D9CCAE', overflow: 'hidden'}}>
			{/* drafting vellum under a warm lamp: paper tone, fibre grain, faint ruled lines, the edges falling off */}
			<AbsoluteFill style={{background: 'radial-gradient(ellipse 75% 70% at 48% 42%, #EFE5CF 0%, #DDCFB0 55%, #A8946E 100%)'}} />
			<svg width="100%" height="100%" style={{position: 'absolute', inset: 0, opacity: 0.22, mixBlendMode: 'multiply'}}>
				<filter id="vellum-grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={7} /><feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.27  0 0 0 0 0.18  0 0 0 0.9 0" /></filter>
				<rect width="100%" height="100%" filter="url(#vellum-grain)" />
			</svg>
			<AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(70,90,110,0.09) 1px, transparent 1px), linear-gradient(90deg, rgba(70,90,110,0.09) 1px, transparent 1px)', backgroundSize: '48px 48px'}} />
			<AbsoluteFill style={{boxShadow: 'inset 0 0 260px rgba(40,26,12,0.55)'}} />
			<AbsoluteFill style={{transform: `translate(${camX}px, ${camY}px) scale(${zoom})`, transformOrigin: '50% 28%'}}>
				<svg width={1920} height={1080} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
					{/* owners → Tata Sons */}
					<Bus d="M330 455 V300 H570" len={395} at={t.trusts + 10} pulseFrom={t.up + 40} seed="tr" />
					<Bus d="M1560 425 V300 H1350" len={335} at={t.shapoorji + 10} seed="sp" />
					<Bus d="M1790 575 V300 H1350" len={715} at={t.companies + 10} seed="co" />
					{/* Tata Sons → the companies it holds (the bus and its drops); dividends rise along it */}
					<Bus d="M960 375 V872" len={497} at={t.sons + 30} pulseFrom={t.up} color={OCHRE} seed="up" />
					{COMPANIES.map((_, i) => {
						const x = 260 + i * 280;
						return <Bus key={i} d={`M${x} 923 V872 H960`} len={Math.abs(960 - x) + 51} at={t.sons + 40 + i * 6} pulseFrom={t.up} color={OCHRE} seed={`c${i}`} />;
					})}
					{/* out of the trusts: hospitals, research, scholarships */}
					<Bus d="M330 735 V772" len={37} at={t.out - 20} pulseFrom={t.out} seed="o1" />
				</svg>
				<Card x={960} y={300} w={780} h={150} at={t.sons} glow={glint > 0 ? `rgba(255,236,190,${0.35 * glint})` : undefined}>
					<div style={{position: 'absolute', left: 70, top: 26}}>
						<Label size={46} spacing="0.3em" weight={700}>TATA SONS</Label>
					</div>
					<div style={{position: 'absolute', left: 70, top: 92, width: BW, height: 20, background: 'rgba(43,35,24,0.12)', borderRadius: 3, overflow: 'hidden'}}>
						<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: trustsW, background: colors.bronze, opacity: 0.9}} />
						<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: dorW, background: `linear-gradient(90deg, ${GOLD_INK}, #C99A3E)`, boxShadow: `0 0 ${24 * glint}px #E8C46A`}} />
						<div style={{position: 'absolute', left: BW * SHARES.trusts, top: 0, bottom: 0, width: spW, background: '#8A7F6E'}} />
						<div style={{position: 'absolute', left: BW * (SHARES.trusts + SHARES.shapoorji), top: 0, bottom: 0, width: Math.min(coW, BW * (1 - SHARES.trusts - SHARES.shapoorji)), background: '#5E5546'}} />
					</div>
				</Card>
				<Card x={330} y={525} w={430} h={140} at={t.trusts}>
					<div style={{position: 'absolute', left: 34, top: 24}}>
						<Label size={31} spacing="0.1em">CHARITABLE TRUSTS</Label>
						<div style={{fontFamily: fontStacks.numbers, fontSize: 56, fontWeight: 700, color: '#8C4F1E', marginTop: 6, opacity: tween(frame, t.trusts + 20, t.trusts + 40, 0, 1)}}>TWO THIRDS</div>
					</div>
				</Card>
				<Card x={330} y={675} w={430} h={120} at={t.dorabji} glow={`rgba(212,175,55,${0.25 + 0.3 * glint})`}>
					<div style={{position: 'absolute', left: 34, top: 18}}>
						<Label size={25} spacing="0.04em" color={GOLD_INK}>SIR DORABJI TATA TRUST</Label>
						<div style={{fontFamily: fontStacks.numbers, fontSize: 54, fontWeight: 700, color: GOLD_INK, marginTop: 4}}>28%</div>
					</div>
					{/* the diamond's light: the one white point */}
					<svg style={{position: 'absolute', right: 26, top: 30, width: 60, height: 60, overflow: 'visible', opacity: 0.55 + 0.45 * glint, filter: `drop-shadow(0 0 ${6 + 16 * glint}px #E8C46A)`}} viewBox="-30 -30 60 60">
						<path d={`M0 ${-26 - 10 * glint} L4 -4 L${26 + 10 * glint} 0 L4 4 L0 ${26 + 10 * glint} L-4 4 L${-26 - 10 * glint} 0 L-4 -4 Z`} fill={GOLD_INK} transform={`rotate(${frame * 0.15})`} />
					</svg>
				</Card>
				<Card x={1560} y={470} w={460} h={90} at={t.shapoorji}>
					<div style={{position: 'absolute', left: 30, top: 30}}>
						<Label size={26} spacing="0.03em">SHAPOORJI PALLONJI GROUP</Label>
					</div>
				</Card>
				<Card x={1560} y={620} w={460} h={90} at={t.companies}>
					<div style={{position: 'absolute', left: 30, top: 30}}>
						<Label size={29} spacing="0.08em">TATA'S OWN COMPANIES</Label>
					</div>
				</Card>
				{COMPANIES.map((c, i) => (
					<Card key={c} x={260 + i * 280} y={965} w={264} h={88} at={t.sons + 50 + i * 8} dim={0.85}>
						<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
							{/* v9: readable on a phone (22 px read as about 6 px in the 720p cut) */}
							<Label size={27} spacing="0.02em">{c}</Label>
						</div>
					</Card>
				))}
				{['HOSPITALS', 'RESEARCH', 'SCHOLARSHIPS'].map((c, i) => (
					<Card key={c} x={130 + i * 210} y={805} w={200} h={60} at={t.out + i * 12} glow="rgba(181,84,42,0.25)">
						<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
							<Label size={24} spacing="0.04em" color={OCHRE}>{c}</Label>
						</div>
					</Card>
				))}
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
