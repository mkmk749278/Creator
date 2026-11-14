import React from 'react';
import {AbsoluteFill, Img, Loop, staticFile, useCurrentFrame} from 'remotion';
import type {Overlay, Shot} from '../Film';
import {DeckPlan} from '../parts/drawings';
import {Clip, Count, Credit, ez, Hero, Honesty, Insert, Label, Photo, Plate, tw, useSpring} from '../parts/kit';
import {C, F} from '../theme';
import {s0, w0} from '../timing';

/** cutaways land 9 frames (0.15 s) before their word (§9.5) */
export const pre = (f: number): number => f - 9;

export const CR = {
	navy: 'VIDEO: INDIAN NAVY',
	navyIT: 'VIDEO: INDIAN NAVY · VIA INDIA TODAY',
	navyNDTV: 'VIDEO: INDIAN NAVY · VIA NDTV',
	navyPrint: 'VIDEO: INDIAN NAVY · VIA THEPRINT',
	archive: 'ARCHIVE FILM · FIRST INS VIKRANT',
	fd: 'ARCHIVE: FILMS DIVISION',
	usn: 'VIDEO: U.S. NAVY',
	pla: 'VIDEO: CCTV / PLA NAVY',
	px: 'VIDEO: PIXABAY',
	pex: 'VIDEO: PEXELS',
	pib: 'PHOTO: PIB',
} as const;

/** a shot with an optional honesty tag and credit */
export const shot = (at: number, name: string, el: (dur: number, lead: number) => React.ReactNode, opts: {tag?: string; credit?: string; hard?: boolean} = {}): Shot => ({
	at,
	name,
	hard: opts.hard,
	el,
	// drawn by Film outside the reframing, so they never drift off the frame
	fixed: (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			{opts.tag ? <Honesty text={opts.tag} /> : null}
			{opts.credit ? <Credit text={opts.credit} /> : null}
		</AbsoluteFill>
	),
});

export const lab = (from: number, to: number, name: string, el: React.ReactNode): Overlay => ({from, to, name, el});

export const clip = (at: number, name: string, credit: string, startAt = 0, tag?: string, grade: 'day' | 'none' = 'day') =>
	shot(at, name, (d) => <Clip name={name} dur={d} startAt={startAt} grade={grade} />, {credit, tag});

/** our Blender hero shot whose second `startAt` falls on frame `at` (lead-corrected) */
export const hero = (at: number, name: string, startAt = 0, tag = 'ILLUSTRATION') =>
	shot(at, name, (d, l) => <Hero name={name} dur={d} startAt={Math.max(0, startAt - l / 60)} />, {tag});

export const photo = (at: number, src: string, credit: string, fit: 'cover' | 'contain' = 'contain') =>
	shot(at, src, (d) => <Photo src={src} dur={d} fit={fit} />, {credit});

export const insert = (at: number, name: string, credit: string, aspect = 16 / 9, startAt = 0, height = 760) =>
	shot(at, name, (d) => <Insert name={name} dur={d} aspect={aspect} startAt={startAt} height={height} />, {credit});

/** a drawing on the plate; `el` gets the shot's length and lead so it can turn word frames into its own */
export const draw = (at: number, name: string, el: (dur: number, lead: number) => React.ReactNode, tag?: string, from?: [number, number, number], to?: [number, number, number]) =>
	shot(at, name, (d, l) => (
		<Plate dur={d} seed={name} from={from} to={to}>
			{el(d, l)}
		</Plate>
	), {tag});

/** a stamp (NOT APPROVED…): lands with a spring on its word */
export const Stamp: React.FC<{at: number; text: string; color: string; x?: number; y?: number}> = ({at, text, color, x = 1340, y = 760}) => {
	const f = useCurrentFrame();
	const p = useSpring(at, 220, 14);
	if (f < at) {
		return null;
	}
	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				transform: `translate(-50%, -50%) rotate(-6deg) scale(${1.6 - 0.6 * p})`,
				opacity: p,
				border: `8px solid ${color}`,
				color,
				padding: '14px 34px',
				fontFamily: F.label,
				fontWeight: 800,
				fontSize: 64,
				letterSpacing: 6,
				background: 'rgba(3,7,13,0.55)',
				whiteSpace: 'nowrap',
			}}
		>
			{text}
		</div>
	);
};

/** Lower-thirds sit clear of YouTube's subtitles (a third of the audience reads them; viewer review r3 fix 2): the
 *  old rows y 760 / 820 / 860 move up to 570 / 640 / 690, ~25% larger, so even a two-row stack ends above 75% of the
 *  frame height. Tags placed higher (dates, names at the top) keep their place and size. */
export const lowY = (y: number, sub?: string): number => (y < 740 ? y : (y >= 850 ? 690 : y >= 800 ? 640 : 570) - (sub && y >= 800 ? 50 : 0));
export const tag = (from: number, to: number, text: string, x = 140, y = 760, size = 56, color: string = C.ink, mono = false, sub?: string): Overlay =>
	lab(from, to, 'tag ' + text, <Label at={0} text={text} x={x} y={lowY(y, sub)} size={y >= 740 ? Math.min(84, Math.round(size * 1.25)) : size} color={color} mono={mono} sub={sub} />);

export const cnt = (from: number, land: number, to: number, value: number, unit: string, x = 140, y = 200, size = 110, color: string = C.slot, startValue = 0, show?: number): Overlay =>
	lab(show ?? from, to, 'count ' + unit, <Count show={0} a={from - (show ?? from)} b={Math.max(12, land - from) + from - (show ?? from)} from={startValue} to={value} x={x} y={y} size={size} unit={unit} color={color} />);

export const stamp = (from: number, to: number, text: string, color: string, x?: number, y?: number): Overlay =>
	lab(from, to, 'stamp ' + text, <Stamp at={0} text={text} color={color} x={x} y={y !== undefined && y > 700 ? 640 : y} />);

/** the viewer's own objection, as they would say it to Kishore */
export const Ask: React.FC<{text: string}> = ({text}) => {
	const p = useSpring(0, 200, 16);
	return (
		<div style={{position: 'absolute', left: 140, top: 520, transform: `scale(${0.85 + 0.15 * p})`, transformOrigin: '0% 100%', opacity: p}}>
			<div style={{fontFamily: F.label, fontWeight: 700, fontSize: 36, letterSpacing: 3, color: C.slot, marginBottom: 10, textShadow: '0 2px 10px rgba(0,0,0,0.9)'}}>YOU ASK KISHORE</div>
			<div style={{display: 'inline-block', fontFamily: F.label, fontWeight: 800, fontSize: 60, color: '#0d1117', background: C.ink, padding: '18px 34px', borderRadius: '28px 28px 28px 4px', boxShadow: '0 20px 60px rgba(0,0,0,0.6)', whiteSpace: 'nowrap'}}>
				{text}
			</div>
		</div>
	);
};
export const ask = (from: number, to: number, text: string): Overlay => lab(from, to, 'ask ' + text, <Ask text={text} />);

/** the big count in the middle of the frame ("One." "Two." "Three."): one word, huge, then gone */
export const Big: React.FC<{text: string; color?: string}> = ({text, color = C.ink}) => {
	const p = useSpring(0, 260, 18);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', pointerEvents: 'none'}}>
			<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 260, color, transform: `scale(${1.25 - 0.25 * p})`, opacity: p, textShadow: '0 10px 60px rgba(0,0,0,0.85)'}}>{text}</div>
		</AbsoluteFill>
	);
};
export const big = (from: number, to: number, text: string, color?: string): Overlay => lab(from, to, 'big ' + text, <Big text={text} color={color} />);

/** the subscribe ask: a pill on "subscribe", pressed once, then breathing */
export const SubscribePill: React.FC<{press: number}> = ({press}) => {
	const f = useCurrentFrame();
	const p = useSpring(0);
	const pr = useSpring(press, 260, 16);
	const tap = f >= press ? 1 - 0.06 * Math.sin(Math.min(1, (f - press) / 12) * Math.PI) : 1;
	const breathe = f > press + 12 ? 0.5 + 0.5 * Math.sin(((f - press - 12) / 60) * Math.PI * 2) : 0;
	return (
		<div
			style={{
				position: 'absolute',
				left: '50%',
				bottom: 320,
				transform: `translate(-50%, ${(1 - p) * 60}px)`,
				opacity: p,
				display: 'flex',
				alignItems: 'center',
				gap: 28,
				padding: '18px 22px 18px 18px',
				borderRadius: 999,
				background: 'rgba(13,17,23,0.92)',
				border: '2px solid rgba(238,243,248,0.16)',
				boxShadow: '0 24px 70px rgba(0,0,0,0.6)',
			}}
		>
			<Img src={staticFile('brand/logo_square.png')} style={{width: 96, height: 96, borderRadius: 999}} />
			<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 46, color: C.ink, letterSpacing: 1, whiteSpace: 'nowrap'}}>BE PRACTICAL WITH KISHORE</div>
			<div
				style={{
					fontFamily: F.label,
					fontWeight: 800,
					fontSize: 46,
					letterSpacing: 2,
					padding: '16px 34px',
					borderRadius: 999,
					whiteSpace: 'nowrap',
					color: pr > 0.5 ? C.ink : '#0d1117',
					background: pr > 0.5 ? '#ff3b3b' : C.ink,
					transform: `scale(${tap})`,
					boxShadow: `0 0 ${20 + 30 * breathe}px rgba(255,59,59,${0.25 + 0.35 * breathe * pr})`,
				}}
			>
				SUBSCRIBE
			</div>
		</div>
	);
};

/** the end card (20 s, r3 fix 10: room for YouTube's end screen): the channel's mark (the only logo in the film) at
 *  the top over the deck plan on the plate, its slot glowing and breathing; the lower half stays clear for the
 *  end-screen video and subscribe elements. */
export const EndCard: React.FC<{dur: number}> = ({dur}) => {
	const f = useCurrentFrame();
	const logo = useSpring(10);
	const fade = tw(f, 0, 24, 0, 1, ez.arrive);
	return (
		<AbsoluteFill>
			{/* r4 check: the end card must never hold still: a steady push across the plate, and the slot redraws every 4 s */}
			<Plate dur={dur} seed="end" from={[1.0, 40, 0]} to={[1.22, -90, 30]}>
				<AbsoluteFill style={{opacity: 0.6}}>
					<Loop durationInFrames={240}>
						<DeckPlan slotAt={10} slotEnd={150} />
					</Loop>
				</AbsoluteFill>
			</Plate>
			<AbsoluteFill style={{background: `rgba(3,7,13,${0.55 * fade})`}} />
			<AbsoluteFill style={{alignItems: 'center', paddingTop: 70}}>
				<Img src={staticFile('brand/logo_square.png')} style={{width: 220, height: 220, opacity: logo, transform: `scale(${(0.9 + 0.1 * logo) * (1 + 0.05 * tw(f, 0, dur, 0, 1, (t) => t))})`, borderRadius: 20}} />
				<div style={{marginTop: 24, fontFamily: F.label, fontWeight: 800, fontSize: 52, color: C.ink, letterSpacing: 2, opacity: logo}}>BE PRACTICAL WITH KISHORE</div>
				<div style={{marginTop: 10, fontFamily: F.label, fontWeight: 700, fontSize: 38, color: C.slot, letterSpacing: 2, opacity: tw(f, 40, 70, 0, 1)}}>STAY PRACTICAL</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};

export {Count, Label, s0, w0};
