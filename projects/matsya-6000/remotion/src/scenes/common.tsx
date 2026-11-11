import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import type {Overlay, Shot} from '../Film';
import {Clip, Count, Credit, ez, Hero, Honesty, Insert, Label, MarineSnow, Photo, Plate, tw, Underwater, useSpring} from '../parts/kit';
import {C, F} from '../theme';
import {s0, w0} from '../timing';

/** cutaways land 9 frames (0.15 s) before their word (§9.5) */
export const pre = (f: number): number => f - 9;

export const CR = {
	isro: 'VIDEO: ISRO',
	dd: 'VIDEO: DD INDIA',
	ddt: 'VIDEO: DD NEWS TELANGANA',
	osn: 'VIDEO: OUR STATE, OUR NATION',
	tn: 'VIDEO: TIMES NOW',
	ifr: 'PHOTO: S. LESBATS / IFREMER · CC BY 4.0',
	pib: 'PHOTO: PIB',
	uscg: 'US COAST GUARD REPORT, 2025',
	map: 'MAP: NATURAL EARTH · INDIA’S OFFICIAL BOUNDARY',
} as const;

/** a shot with an optional honesty tag and credit */
export const shot = (at: number, name: string, el: (dur: number, lead: number) => React.ReactNode, opts: {tag?: string; credit?: string; hard?: boolean} = {}): Shot => ({
	at,
	name,
	hard: opts.hard,
	el: (dur, lead) => (
		<AbsoluteFill>
			{el(dur, lead)}
			{opts.tag ? <Honesty text={opts.tag} /> : null}
			{opts.credit ? <Credit text={opts.credit} /> : null}
		</AbsoluteFill>
	),
});

/** a label overlay from its word until `to` */
export const lab = (from: number, to: number, name: string, el: React.ReactNode): Overlay => ({from, to, name, el});

export const clip = (at: number, name: string, credit: string, startAt = 0, tag?: string) =>
	shot(at, name, (d) => <Clip name={name} dur={d} startAt={startAt} grade="day" />, {credit, tag});

/** a hero clip whose frame `startAt` (s) falls on frame `at`: from its first frame it cuts in hard on the sentence;
 *  later it dissolves in, starting `lead` frames earlier in the clip so its word timing stays exact */
export const hero = (at: number, name: string, startAt = 0, tag = 'ILLUSTRATION') =>
	shot(at, name, (d, l) => <Hero name={name} dur={d} startAt={Math.max(0, startAt - l / 60)} />, {tag, hard: startAt < 0.2});

export const photo = (at: number, src: string, credit: string, fit: 'cover' | 'contain' = 'cover') =>
	shot(at, src, (d) => <Photo src={src} dur={d} fit={fit} />, {credit});

export const insert = (at: number, name: string, credit: string, aspect = 16 / 9, startAt = 0) =>
	shot(at, name, (d) => <Insert name={name} dur={d} aspect={aspect} startAt={startAt} />, {credit});

/** the deep, empty: black water and drifting specks (a slow descent so the frame is never static) */
export const Deep: React.FC<{dur: number; word?: {at: number; text: string; color?: string}}> = ({word}) => {
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{background: C.night}}>
			<Underwater depth={1} />
			<MarineSnow speed={1.2} n={120} />
			{word && f >= word.at ? (
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
					<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 140, letterSpacing: 8, color: word.color ?? C.ink, opacity: tw(f, word.at, word.at + 18, 0, 1, ez.arrive)}}>{word.text}</div>
				</AbsoluteFill>
			) : null}
		</AbsoluteFill>
	);
};

/** the one document pose (§9.3): the report's cover lying on the plate, a slow push */
export const ReportPose: React.FC<{dur: number; dim?: number}> = ({dur, dim}) => {
	const f = useCurrentFrame();
	const d = dim === undefined ? 0 : tw(f, dim, dim + 40, 0, 0.45);
	return (
		<AbsoluteFill>
			<Plate dur={dur} from={[1.0, 0, 0]} to={[1.14, 0, -20]} seed="report">
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
					<Img
						src={staticFile('assets/media/photos/uscg_cover-001.png')}
						style={{height: 900, transform: 'rotate(-3deg)', boxShadow: '0 40px 90px rgba(0,0,0,0.75)', filter: 'sepia(0.08) brightness(0.96)'}}
					/>
				</AbsoluteFill>
			</Plate>
			<AbsoluteFill style={{background: `rgba(0,0,0,${d})`}} />
		</AbsoluteFill>
	);
};

/** a short line of the report's own words on the plate (verbatim, claim M27) */
export const Quote: React.FC<{dur: number; text: string; source: string}> = ({dur, text, source}) => {
	const f = useCurrentFrame();
	const p = tw(f, 6, 40, 0, 1, ez.arrive);
	return (
		<Plate dur={dur} seed="quote" from={[1.0, 0, 0]} to={[1.06, -10, 0]}>
			<AbsoluteFill style={{padding: '0 220px', justifyContent: 'center'}}>
				<div style={{opacity: p, fontFamily: F.label, fontWeight: 700, fontSize: 58, lineHeight: 1.3, color: C.ink, background: 'rgba(3,7,13,0.72)', padding: '40px 50px', borderLeft: `10px solid ${C.red}`}}>
					{text}
					<div style={{marginTop: 26, fontSize: 34, color: C.dim, letterSpacing: 2}}>{source}</div>
				</div>
			</AbsoluteFill>
		</Plate>
	);
};

/** a stamp (CERTIFIED, NO MINING YET): lands with a spring on its word */
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

export {Count, Label, s0, w0};

// Overlays run inside a Sequence that starts at `from`, so their frames are relative: these helpers take absolute
// word frames and convert.
export const tag = (from: number, to: number, text: string, x = 140, y = 760, size = 56, color: string = C.ink, mono = false, sub?: string): Overlay =>
	lab(from, to, 'tag ' + text, <Label at={0} text={text} x={x} y={y} size={size} color={color} mono={mono} sub={sub} />);

export const cnt = (from: number, land: number, to: number, value: number, unit: string, x = 140, y = 200, size = 110, color: string = C.amber, startValue = 0): Overlay =>
	lab(from, to, 'count ' + unit, <Count a={0} b={Math.max(12, land - from)} from={startValue} to={value} x={x} y={y} size={size} unit={unit} color={color} />);

export const stamp = (from: number, to: number, text: string, color: string, x?: number, y?: number): Overlay =>
	lab(from, to, 'stamp ' + text, <Stamp at={0} text={text} color={color} x={x} y={y} />);
