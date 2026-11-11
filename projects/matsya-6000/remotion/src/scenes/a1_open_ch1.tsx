import React from 'react';
import {AbsoluteFill} from 'remotion';
import type {Part} from '../Film';
import {BuffaloTrueScale, CarbonHull, Fall, NailPress, WeldBars} from '../parts/drawings';
import {Clip, Hero, Plate} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {ask, clip, cnt, CR, Deep, hero, insert, lab, pre, PressureCompare, Quote, ReportPose, shot, stamp, tag} from './common';

// Narration v3 (2026-11-11). Cold open (S0–16), the pressure (S17–26), Titan and what India does differently (S27–47).
// Frames from the locked audio (vo/timing.json).
const S = s0;

const open: Part = {
	shots: [
		// the thumbnail's subject first (the ball), sinking through real-looking water with the depth counter
		// (owner on r6: the deep looked like space; SeaOver now makes it sea), then the real ball on "this titanium ball"
		hero(S(0), 'H1_dive', 0),
		clip(pre(w0(0, 'this')), 'F01_ballhall', CR.dd),
		// the hall clip pans to another vehicle after 3 s: the squeeze takes over on 'almost one lakh tonnes'
		hero(pre(w0(0, 'almost')), 'H4_squeeze', 3.0, 'SIMPLIFIED'),
		hero(S(1), 'H1_cutaway', 12.2),
		clip(S(2), 'ISRO_hall', CR.isro),
		clip(pre(w0(2, 'india')), 'F08_ball', CR.tn),
		hero(S(3), 'H2_seam', 0),
		clip(S(5), 'ISRO_ballred', CR.isro),
		clip(S(6), 'ISRO_ebglow', CR.isro),
		// ISRO's own lift-off film (PSLV-C51), a framed insert: the source is 480p
		insert(S(7), 'ISRO_liftoff', CR.isro, 16 / 9, 2.0),
		clip(S(8), 'ISRO_bead', CR.isro),
		clip(S(9), 'F01_ball', CR.dd),
		shot(S(10), 'weldbars', (d, l) => (
			<Plate dur={d} seed="bars">
				<WeldBars show20={l + 4} show80={w0(11, 'eight') - S(10) + l} grow={w0(11, 'eight') - S(10) + l + 24} />
			</Plate>
		)),
		clip(S(12), 'ISRO_console2', CR.isro),
		clip(S(13), 'ISRO_monitor', CR.isro),
		shot(S(14), 'deep-titan0', (d, l) => <Deep dur={d} word={{at: w0(14, 'titan') - S(14) + l, text: 'TITAN'}} />),
		clip(S(15), 'F01_ball', CR.dd, 0.4),
		clip(S(16), 'PX_phone2', CR.px),
	],
	overlays: [
		cnt(w0(0, 'lakh'), w0(0, 'tonnes'), S(1), 100000, 'TONNES', 140, 760, 120),
		cnt(w0(0, 'six'), w0(0, 'sea'), pre(w0(0, 'this')), 6000, 'M DOWN', 140, 180, 110, C.amber),
		tag(w0(1, 'three'), s1(1), 'THREE INDIANS INSIDE', 140, 760, 56),
		tag(w0(2, 'matsya'), s1(2) + 10, 'MATSYA 6000', 140, 760, 72, C.amber),
		tag(w0(3, 'seven'), s1(4), '7 WELDS', 140, 760, 64, C.weld),
		tag(w0(4, 'weak'), s1(4), 'ONE WEAK WELD IS ENOUGH', 140, 860, 48, C.red),
		tag(w0(6, 'isro'), s1(6), 'MADE BY ISRO', 140, 760, 60, C.weld),
		tag(w0(7, 'rocket'), s1(7), 'THE ROCKET PEOPLE', 140, 860, 52),
		tag(w0(8, 'hardest'), s1(9), 'ISRO’S HARDEST WELD', 140, 760, 56, C.weld),
		cnt(w0(12, 'seven'), w0(12, 'tries'), s1(12) + 10, 700, 'TRIES'),
		tag(w0(16, 'phone'), s1(16), 'THE PHONE IN YOUR HAND', 140, 760, 56, C.cyan),
	],
};

const ch1: Part = {
	shots: [
		clip(S(17), 'PX_finger', CR.pex, 1.6),
		// real sea under the depth counter
		clip(S(18), 'PX_rays', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(19), 'PX_reef', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(21), 'PX_rays', CR.px, 6, 'ILLUSTRATIVE FOOTAGE'),
		shot(S(22), 'nail-press', (d, l) => (
			<AbsoluteFill>
				<Clip name="PX_nail" dur={d} grade="day" from={[1.0, 0, 0]} to={[1.0, 0, 0]} />
				<NailPress arrow={w0(22, 'presses') - S(22) + l} kg={w0(22, 'six', 1) - S(22) + l} />
			</AbsoluteFill>
		), {tag: 'OUR CALCULATION', credit: CR.pex}),
		clip(S(23), 'PX_buffalo', CR.px),
		shot(pre(w0(23, 'standing')), 'nail-buffalo', (d) => (
			<Plate dur={d} seed="nail2" from={[1.0, 0, 0]} to={[1.03, 0, 0]}>
				<BuffaloTrueScale dur={d} />
			</Plate>
		), {tag: 'OUR CALCULATION'}),
		hero(S(24), 'H4_squeeze', 0, 'SIMPLIFIED'),
		clip(pre(w0(24, 'buffalo')), 'PX_herd', CR.px),
		hero(S(26), 'H4_squeeze', 3.0, 'SIMPLIFIED'),
	],
	overlays: [
		lab(S(18), S(22), 'fall', <Fall bare dur={S(22) - S(18)} target={w0(21, 'six') - S(18)} beats={[w0(19, 'ten') - S(18), w0(20, 'twenty') - S(18)]} race={w0(21, 'keep') - S(18)} />),
		tag(w0(21, 'six'), S(22), '600 TIMES', 140, 760, 64, C.amber),
		tag(w0(23, 'full'), pre(w0(23, 'standing')), 'ABOUT 600 KG', 140, 760, 64, C.amber),
		tag(w0(24, 'buffalo'), S(26), 'A BUFFALO ON EVERY NAIL', 140, 760, 56, C.amber),
		cnt(w0(26, 'lakh'), w0(26, 'tonnes'), s1(26) + 20, 100000, 'TONNES'),
		tag(w0(26, 'every'), s1(26) + 20, 'FROM EVERY SIDE', 140, 860, 52),
	],
};

const titan: Part = {
	shots: [
		clip(S(27), 'F01_hall', CR.dd),
		clip(S(29), 'F01_ball', CR.dd),
		clip(S(30), 'PX_surface', CR.px, 3.0, 'ILLUSTRATIVE FOOTAGE'),
		shot(S(31), 'deep-titan', (d, l) => <Deep dur={d} word={{at: w0(31, 'titan') - S(31) + l, text: 'TITAN'}} />),
		shot(S(32), 'report', (d, l) => <ReportPose dur={d} dim={l + 30} />, {credit: CR.uscg}),
		shot(S(33), 'carbon', (d, l) => (
			<Plate dur={d} seed="carbon">
				<CarbonHull dur={d} part={w0(34, 'layers') - S(33) + l} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		shot(S(35), 'quote', (d) => (
			<Quote
				dur={d}
				text="“OceanGate’s failure to follow established engineering protocols for safety, testing, and maintenance of their submersible, was the primary causal factor.”"
				source="US COAST GUARD MARINE BOARD OF INVESTIGATION · 2025"
			/>
		)),
		shot(S(36), 'deep-number', (d) => <Deep dur={d} />),
		shot(pre(w0(37, 'titan')), 'pressure', (d, l) => (
			<Plate dur={d} seed="pressure">
				<PressureCompare titan={l + 9} matsya={w0(37, 'matsya') - pre(w0(37, 'titan')) + l} />
			</Plate>
		), {tag: 'OUR CALCULATION'}),
		clip(S(38), 'ISRO_hall', CR.isro),
		clip(S(40), 'ISRO_ti', CR.isro, 1.5),
		clip(S(41), 'F01_ball', CR.dd),
		clip(S(42), 'ISRO_ut', CR.isro),
		clip(S(43), 'ISRO_xray', CR.isro),
		clip(S(44), 'F01_hall', CR.dd),
		hero(S(45), 'H3_weights', 0),
	],
	overlays: [
		ask(w0(29, 'is'), S(30), 'Is this another Titan?'),
		tag(w0(30, 'june'), s1(32), '18.06.2023', 140, 180, 56, C.ink, true),
		tag(w0(34, 'kept'), s1(34), 'AND IT KEPT DIVING', 1180, 190, 48, C.red),
		tag(w0(38, 'india'), s1(39), 'WHAT INDIA DOES DIFFERENTLY', 140, 760, 52),
		tag(w0(40, 'titanium'), s1(40), 'TITANIUM', 140, 760, 64, C.ti),
		tag(w0(40, 'fifty'), s1(40), 'TRUSTED FOR 50+ YEARS', 140, 860, 48, C.dim),
		tag(w0(41, 'ball'), s1(41), 'A BALL', 140, 760, 64),
		tag(w0(42, 'builders'), s1(42), 'NOBODY PASSES THEIR OWN WORK', 140, 760, 50),
		stamp(w0(43, 'approve'), s1(43) + 10, 'CERTIFIED', C.green),
		tag(w0(44, 'norway'), s1(44) + 10, 'CHECKED IN NORWAY', 140, 760, 56, C.green),
		tag(w0(46, 'drop'), s1(46), 'DROP WEIGHTS', 140, 180, 56, C.amber),
		tag(w0(46, 'rises'), s1(46), 'IT RISES', 140, 270, 52),
		cnt(w0(47, 'ninety-six'), w0(47, 'hours'), s1(47) + 10, 96, 'HOURS OF AIR', 140, 720, 120, C.cyan),
	],
};

export const a1: Part = {shots: [...open.shots, ...ch1.shots, ...titan.shots], overlays: [...open.overlays, ...ch1.overlays, ...titan.overlays]};
export {Hero};
