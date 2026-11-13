import React from 'react';
import {AbsoluteFill} from 'remotion';
import type {Part} from '../Film';
import {Doc, DoteBars, EngineBars, FanUnroll, LandTrack, Radar, TwoMeters, Working} from '../parts/drawings';
import {Clip, Plate} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {big, clip, cnt, CR, draw, hero, insert, shot, stamp, tag} from './common';

// ch3 Three seconds (S92–126), ch4 The newcomer and the inventor (S127–152). word_map.md.
const S = s0;
const at = (word: number, shotStart: number, l: number) => word - shotStart + l;

const ch3: Part = {
	shots: [
		clip(S(92), 'PX_fan', CR.px),
		clip(S(94), 'PX_coil', CR.px, 3.0, 'ILLUSTRATIVE FOOTAGE'),
		// S1: the fan's motor unrolled into the line under the deck (one designed long take)
		draw(S(95), 'fan-unroll', (d, l) => (
			<FanUnroll
				glowAt={at(w0(95, 'chases'), S(95), l)}
				openAt={at(w0(96, 'cut'), S(95), l)}
				unrollEnd={at(w0(96, 'flat'), S(95), l) + 30}
				dropAt={at(w0(97, 'laid'), S(95), l)}
				runAt={at(w0(99, 'straight'), S(95), l)}
				patchAt={at(w0(99, 'takes'), S(95), l)}
				jetAt={at(w0(99, 'jet'), S(95), l)}
			/>
		), 'ILLUSTRATION · SIMPLIFIED', [1.0, 0, 0], [1.05, 0, 0]),
		// the real trough at Lakehurst: only the coils beside the carriage are switched on
		clip(S(100), 'EM12_trough', CR.usn, 1.0),
		clip(S(101), 'EM12_slot', CR.usn),
		// S2: count with me: a real launch in real time; the stroke starts on "One"
		clip(S(102), 'FORD_launch', CR.usn, Math.max(0, 5.0 - (w0(103, 'one') - S(102)) / 60)),
		clip(S(106), 'EM12_launch', CR.usn, 0.3),
		draw(S(107), 'working-a', (d, l) => <Working at={[l + 30, at(w0(109, 'nineteen'), S(107), l) - 40, at(w0(109, 'nineteen'), S(107), l)]} />, 'OUR CALCULATION'),
		clip(S(110), 'PX_fan', CR.px, 4.0),
		draw(S(111), 'working-b', (d, l) => <Working at={[0, 0, 0, l, at(w0(111, 'two'), S(111), l)]} />, 'OUR CALCULATION'),
		clip(S(112), 'FORD_cat', CR.usn, 1.0),
		draw(S(114), 'two-meters', (d, l) => <TwoMeters homeAt={at(w0(114, 'sips'), S(114), l)} catAt={at(w0(115, 'pour'), S(114), l)} />, 'OUR CALCULATION'),
		draw(S(116), 'engine-bars', (d, l) => <EngineBars barsAt={l} spikeAt={at(w0(116, 'fifty'), S(116), l)} />, 'OUR CALCULATION'),
		clip(S(118), 'LAND_touch', CR.navyIT, 1.0),
		hero(S(120), 'H_store', 0, 'ILLUSTRATION · SIMPLIFIED'),
		insert(pre2(w0(121, 'spinning')), 'PXL_lattu', CR.pex, 9 / 16, 1.0, 900),
		// the energy goes out along the bus at 10 s in the render: on "pull"
		hero(S(122), 'H_store', 10.0 - (w0(122, 'pull') - S(122)) / 60, 'ILLUSTRATION · SIMPLIFIED'),
		clip(S(123), 'FORD_launch', CR.usn, 5.5),
		hero(S(124), 'H_store', 12.5, 'ILLUSTRATION · SIMPLIFIED'),
	],
	overlays: [
		tag(w0(92, 'ceiling'), s1(93), 'YOUR CEILING FAN', 140, 860, 56),
		tag(w0(94, 'induction'), s1(94), 'AN INDUCTION MOTOR', 140, 860, 56, C.copper),
		tag(w0(100, 'only'), s1(101), 'ONLY THE COILS BESIDE THE JET', 140, 860, 50, C.copper),
		big(w0(103, 'one'), w0(104, 'two') - 4, 'ONE'),
		big(w0(104, 'two'), w0(105, 'three') - 4, 'TWO'),
		big(w0(105, 'three'), s1(105) + 18, 'THREE', C.slot),
		tag(w0(106, 'thirty'), s1(106), '30-TONNE FIGHTER', 140, 760, 56),
		cnt(w0(106, 'standing'), w0(106, 'hour'), s1(106) + 20, 240, 'KM/H', 140, 180, 120, C.slot),
		tag(w0(110, 'six'), s1(110), 'ABOUT 6 DAYS OF YOUR HOME', 140, 860, 54, C.slot),
		tag(w0(113, 'three'), s1(113), 'IN THE THREE SECONDS', 140, 860, 60, C.slot),
		tag(w0(117, 'half'), s1(117), 'MORE THAN HALF', 140, 180, 60, C.red),
		tag(w0(119, 'no'), s1(119), 'NO', 140, 760, 90, C.ink),
		tag(w0(120, 'save'), s1(120), 'SO YOU SAVE UP', 140, 860, 56),
		tag(w0(121, 'thirty'), s1(121), 'EACH OVER 36 TONNES', 140, 860, 54, C.copper),
		tag(w0(122, 'push'), s1(122), 'THE ENERGY BECOMES THE PUSH', 140, 860, 50, C.copper),
		tag(w0(123, 'forty'), s1(123), 'EVERY 45 SECONDS', 140, 760, 64, C.slot, true),
		tag(w0(126, 'power'), s1(126), 'A POWER STATION', 140, 760, 70, C.slot, false, '3 SECONDS AT A TIME'),
	],
};

function pre2(f: number): number {
	return f - 9;
}

const ch4: Part = {
	shots: [
		clip(S(127), 'FORD_cat', CR.usn, 2.0),
		insert(S(130), 'KJ_launch', CR.pla, 16 / 9, 0),
		draw(S(131), 'land-track', (d, l) => <LandTrack drawAt={at(w0(132, 'twenty'), S(131), l)} />, 'ILLUSTRATION'),
		insert(S(133), 'KJ_launch', CR.pla, 16 / 9, 0.5),
		shot(S(134), 'radar-fujian', (d, l) => (
			<Plate dur={d} seed="radar3">
				<Radar heliAt={99999} planeAt={l} contactAt={l + 30} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		hero(S(135), 'H_store', 4.0, 'ILLUSTRATION · SIMPLIFIED'),
		clip(S(138), 'FORD_cat', CR.usn, 0),
		draw(S(140), 'dote', (d, l) => <DoteBars lineAt={at(w0(140, 'four'), S(140), l)} b1At={at(w0(141, 'one'), S(140), l)} b2At={at(w0(142, 'six'), S(140), l)} />, 'SOURCE: US DOT&E'),
		clip(S(144), 'FORD_launch', CR.usn, 0.5),
		clip(S(146), 'SH_launch', CR.archive, 0, undefined, 'none'),
		clip(S(147), 'EM12_launch', CR.usn, 2.0),
		shot(S(148), 'doc-memo', (d, l) => (
			<Plate dur={d} seed="memo">
				<Doc
					at={l}
					head="THE WHITE HOUSE · 13 AUGUST 2026"
					lines={['A plan “to replace the Electromagnetic Aircraft', 'Launch System … with steam”', 'on a future carrier (CVN-81)']}
					mark={1}
					markAt={at(w0(148, 'steam'), S(148), l)}
					stamp="PRESIDENTIAL MEMORANDUM"
				/>
			</Plate>
		)),
		shot(S(149), 'doc-ga', (d, l) => (
			<Plate dur={d} seed="ga">
				<Doc at={l} head="GENERAL ATOMICS (THE MAKER) · 17 AUGUST 2026" lines={['The decision', '“warrants careful reconsideration.”']} mark={1} markAt={at(w0(149, 'think'), S(149), l)} />
			</Plate>
		)),
		clip(S(151), 'KJ_launch', CR.pla, 2.0),
		insert(S(152), 'MIG_deck', CR.navy, 9 / 16, 0.6, 900),
	],
	overlays: [
		tag(w0(128, 'two'), s1(129), 'TWO NAVIES HAVE', 140, 860, 56),
		tag(w0(130, 'china'), s1(130), 'CHINA', 140, 180, 70),
		tag(w0(131, 'never'), s1(131), 'NO STEAM CATAPULT AT SEA', 140, 860, 50),
		tag(w0(132, 'twenty'), s1(132), 'FROM 2016', 140, 180, 64, C.slot, true),
		tag(w0(133, 'november'), s1(133), 'FUJIAN · NOV 2025', 140, 180, 60, C.ink, true),
		tag(w0(134, 'radar'), s1(134), 'A FLYING RADAR PLANE', 140, 860, 54, C.cyan),
		tag(w0(135, 'nuclear'), s1(135), 'NOT NUCLEAR', 140, 860, 64, C.slot),
		tag(w0(137, 'stored'), s1(137), 'STORED POWER', 140, 860, 64, C.copper),
		tag(w0(139, 'u-s-s'), s1(139), 'USS FORD', 140, 760, 64),
		tag(w0(143, 'far'), s1(143), 'FAR SHORT', 140, 180, 64, C.cyan),
		cnt(w0(145, 'thirty'), w0(145, 'launches'), s1(145) + 30, 36863, 'LAUNCHES', 140, 180, 110, C.cyan),
		tag(w0(145, 'programme'), s1(145), 'SOURCE: THE PROGRAMME’S OWN COUNT', 140, 860, 40, C.dim),
		tag(w0(147, 'young'), s1(147), 'STILL YOUNG', 140, 860, 60),
		stamp(w0(150, 'nothing'), s1(150) + 10, 'NO DECISION YET', C.slot, 1340, 860),
		tag(w0(151, 'inventor'), s1(151), 'THE INVENTOR: IN TWO MINDS', 140, 760, 50),
		tag(w0(151, 'newcomer'), s1(151), 'THE NEWCOMER: FLYING', 140, 860, 50, C.slot),
	],
};

export const p2: Part[] = [ch3, ch4];
