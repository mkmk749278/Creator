import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {BuffaloTrueScale, CarbonHull, Fall, NailPress, WeldBars} from '../parts/drawings';
import {Clip, ez, Hero, Plate, tw} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {clip, cnt, CR, Deep, hero, insert, lab, pre, Quote, ReportPose, shot, stamp, tag} from './common';

// Cold open and Ch1 (S0–S41), word_map.md. Frames from the locked audio r2 (vo/timing.json).

/** the dive window pass (H1_dive 7.3–7.8 s clips through the glass): a dip to near black and back */
const Dip: React.FC<{peak: number}> = ({peak}) => {
	const f = useCurrentFrame();
	const o = f < peak ? tw(f, peak - 18, peak, 0, 0.92, ez.leave) : tw(f, peak, peak + 20, 0.92, 0, ez.arrive);
	return <AbsoluteFill style={{background: `rgba(2,6,11,${o})`}} />;
};

const S = s0;
const open: Part = {
	shots: [
		hero(S(0), 'H1_dive', 0),
		clip(S(2), 'ISRO_hall', CR.isro),
		clip(pre(w0(2, 'deep-sea')) + 60, 'ISRO_ballred', CR.isro),
		hero(S(4), 'H2_pieces', 0),
		// ISRO's own lift-off film (PSLV-C51), a framed insert: the source is 480p
		insert(S(5), 'ISRO_liftoff', CR.isro, 16 / 9, 2.0),
		clip(S(7), 'ISRO_ebglow', CR.isro),
		clip(S(8), 'ISRO_ballred', CR.isro),
		shot(S(9), 'weldbars', (d, l) => (
			<Plate dur={d} seed="bars">
				<WeldBars show20={w0(9, 'thicker') - S(9) + l} show80={w0(9, 'thicker') - S(9) + l + 20} grow={w0(9, 'four') - S(9) + l} />
			</Plate>
		)),
		hero(S(11), 'H1_dive', 0.6),
	],
	overlays: [
		cnt(w0(0, 'lakh'), w0(0, 'tonnes'), S(1), 100000, 'TONNES', 140, 760, 120),
		lab(S(0) + 420, S(0) + 500, 'dip', <Dip peak={Math.round(7.55 * 60) - 420} />),
		tag(w0(2, 'people'), s1(2), 'FOR PEOPLE'),
		tag(w0(3, 'matsya'), s1(3) + 20, 'MATSYA 6000', 140, 760, 72, C.amber),
		tag(w0(4, 'five'), s1(4), '5 PIECES', 140, 720, 60),
		tag(w0(4, 'seven'), s1(4), '7 WELDS', 140, 820, 60, C.weld),
		tag(w0(6, 'rockets'), s1(6), 'ISRO · ROCKETS'),
		tag(w0(7, 'hardest'), s1(7), 'ITS HARDEST WELD', 140, 760, 56, C.weld),
		cnt(w0(10, 'seven'), w0(10, 'tries'), s1(10) + 20, 700, 'TRIES'),
		tag(w0(12, 'titan'), s1(12), 'TITAN', 140, 760, 64),
	],
};

const ch1: Part = {
	shots: [
		// real sea under the depth counter (owner, r3: a real clip for every idea)
		clip(S(14), 'PX_rays', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(15), 'PX_reef', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(16), 'PX_rays', CR.px, 6, 'ILLUSTRATIVE FOOTAGE'),
		// a real finger, a real nail, a real buffalo; then the buffalo on the nail drawn at true size (owner, r3)
		clip(S(19), 'PX_finger', CR.pex),
		shot(S(20), 'nail-press', (d, l) => (
			<AbsoluteFill>
				<Clip name="PX_nail" dur={d} grade="day" from={[1.0, 0, 0]} to={[1.0, 0, 0]} />
				<NailPress arrow={w0(20, 'press') - S(20) + l} kg={w0(20, 'six') - S(20) + l} />
			</AbsoluteFill>
		), {tag: 'OUR CALCULATION', credit: CR.pex}),
		clip(S(21), 'PX_buffalo', CR.px),
		shot(pre(w0(21, 'on')), 'nail-buffalo', (d) => (
			<Plate dur={d} seed="nail2" from={[1.0, 0, 0]} to={[1.03, 0, 0]}>
				<BuffaloTrueScale dur={d} />
			</Plate>
		), {tag: 'OUR CALCULATION'}),
		hero(S(22), 'H4_squeeze', 0, 'SIMPLIFIED'),
		clip(S(25), 'F01_ballhall', CR.dd),
		shot(S(26), 'deep-titan', (d, l) => <Deep dur={d} word={{at: w0(26, 'titan') - S(26) + l, text: 'TITAN'}} />),
		shot(S(27), 'report', (d, l) => <ReportPose dur={d} dim={w0(29, 'five') - S(27) + l} />, {credit: CR.uscg}),
		shot(S(30), 'carbon', (d, l) => (
			<Plate dur={d} seed="carbon">
				<CarbonHull dur={d} part={w0(31, 'layers') - S(30) + l} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		shot(S(32), 'quote', (d, l) => (
			<Quote
				dur={d}
				text="“OceanGate’s failure to follow established engineering protocols for safety, testing, and maintenance of their submersible, was the primary causal factor.”"
				source="US COAST GUARD MARINE BOARD OF INVESTIGATION · 2025"
			/>
		)),
		clip(S(33), 'ISRO_hall', CR.isro),
		clip(S(35), 'ISRO_ti', CR.isro, 1.5),
		hero(S(36), 'H2_seam', 0),
		clip(S(37), 'ISRO_ut', CR.isro),
		clip(S(38), 'F01_ball', CR.dd),
		hero(S(39), 'H3_weights', 0),
	],
	overlays: [
		tag(w0(28, 'june'), s1(29), '18.06.2023', 140, 180, 56, C.ink, true),
		cnt(w0(24, 'lakh'), w0(24, 'tonnes'), s1(24) + 20, 100000, 'TONNES'),
		lab(S(14), S(19), 'fall', <Fall bare dur={S(19) - S(14)} target={w0(14, 'six') - S(14)} beats={[w0(15, 'ten') - S(14), w0(16, 'once') - S(14), w0(17, 'again') - S(14), w0(18, 'again') - S(14)]} race={w0(18, 'again') - S(14) + 24} />),
		tag(w0(21, 'full'), pre(w0(21, 'on')), 'ABOUT 600 KG', 140, 760, 64, C.amber),
		tag(w0(31, 'kept'), s1(31), 'KEPT DIVING', 140, 860, 52, C.red),
		tag(w0(35, 'titanium'), s1(35), 'TITANIUM', 140, 760, 64, C.ti),
		tag(w0(36, 'ball'), s1(36), 'A BALL', 140, 760, 64),
		stamp(w0(37, 'approves'), s1(37) + 10, 'CERTIFIED', C.green),
		tag(w0(38, 'norway'), s1(38) + 10, 'CHECKED IN NORWAY', 140, 760, 56, C.green),
		tag(w0(40, 'drop'), s1(40), 'DROP WEIGHTS', 140, 180, 56, C.amber),
		tag(w0(40, 'rises'), s1(40), 'IT RISES', 140, 270, 52),
		cnt(w0(41, 'ninety-six'), w0(41, 'hours'), s1(41) + 20, 96, 'HOURS OF AIR', 140, 720, 120, C.cyan),
	],
};

export const a1: Part = {shots: [...open.shots, ...ch1.shots], overlays: [...open.overlays, ...ch1.overlays]};
export {Hero};
