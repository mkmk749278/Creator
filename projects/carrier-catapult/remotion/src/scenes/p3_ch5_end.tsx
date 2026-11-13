import React from 'react';
import {AbsoluteFill} from 'remotion';
import type {Part} from '../Film';
import {ChinaIndia, DeckPlan, Doc, MeterSolo, RampOrCatapult, ScaleCompare, SubBlind, ThreeItems, ThreeSlots, TwoShips, Watch} from '../parts/drawings';
import {Clip, Plate} from '../parts/kit';
import {SeaMap} from '../parts/SeaMap';
import {C, F} from '../theme';
import {s0, s1, w0} from '../timing';
import {ask, big, clip, cnt, CR, draw, EndCard, hero, insert, lab, pre, shot, stamp, SubscribePill, tag} from './common';

// ch5 A small test model (S153–185), the landing (S186–206), the outro (S207–210). word_map.md.
const S = s0;
const at = (word: number, shotStart: number, l: number) => word - shotStart + l;

const ch5: Part = {
	shots: [
		shot(S(153), 'map-pune', (d) => (
			<SeaMap dur={d} keys={[{f: 0, lon: 78, lat: 20, zoom: 1.2}, {f: d, lon: 74.5, lat: 18.8, zoom: 3.4}]} pins={[{at: 10, ll: [73.86, 18.52], label: 'PUNE, MAHARASHTRA', sub: 'DRDO · R&DE(E)', side: 'left'}]} />
		)),
		clip(pre(w0(153, 'building')), 'PXL_tech', CR.pex, 0, 'ILLUSTRATIVE FOOTAGE'),
		// the test model at the scale of its reported numbers (no photo of it exists)
		draw(S(154), 'model-zoom', (d) => <ScaleCompare dur={d * 6} longAt={99999} jetAt={99999} />, 'ILLUSTRATION · AS REPORTED'),
		clip(S(157), 'PXL_tech', CR.pex, 5.0, 'ILLUSTRATIVE FOOTAGE'),
		// S3: seventeen metres beside a hundred: one continuous pull-back
		draw(S(158), 'scale-compare', (d, l) => <ScaleCompare dur={d} longAt={at(w0(158, 'beside'), S(158), l)} jetAt={at(w0(160, 'thirty'), S(158), l)} />, 'ILLUSTRATION · OUR CALCULATION', [1.0, 0, 0], [1.0, 0, 0]),
		shot(S(164), 'doc-decade', (d, l) => (
			<Plate dur={d} seed="decade">
				<Doc at={l} head="DEFENCE PRESS · 15 APRIL 2025 · OFFICIALS QUOTED" lines={['A full-size catapult for fighters:', '“a decade or more”']} mark={1} markAt={at(w0(164, 'decade'), S(164), l)} stamp="AS REPORTED" />
			</Plate>
		)),
		clip(S(165), 'PX_coil', CR.px, 2.0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(166), 'PXL_tech', CR.pex, 2.0, 'ILLUSTRATIVE FOOTAGE'),
		draw(S(168), 'china-india', (d, l) => <ChinaIndia trackAt={at(w0(168, 'china'), S(168), l)} shipAt={at(w0(170, 'ship'), S(168), l)} />, 'ILLUSTRATION'),
		draw(S(171), 'two-ships', (d, l) => <TwoShips slotsAt={at(w0(171, 'plan'), S(171), l)} rampAt={at(w0(172, 'repeat'), S(171), l)} />, 'ILLUSTRATION'),
		clip(S(174), 'FORD_cat', CR.usn, 3.0),
		shot(S(175), 'doc-2017', (d, l) => (
			<Plate dur={d} seed="usni">
				<Doc at={l} head="USNI NEWS · 20 OCTOBER 2017" lines={['“Reports: U.S. Offers EMALS', 'for Indian Carrier Development Program”']} />
			</Plate>
		)),
		shot(S(177), 'doc-france', (d, l) => (
			<Plate dur={d} seed="dsca">
				<Doc
					at={l}
					head="US NOTICE (DSCA) · 21 DECEMBER 2021"
					lines={['Possible sale to France:', 'EMALS and arresting gear, one ship', 'Estimated cost: $1.321 billion']}
					mark={2}
					markAt={at(w0(178, 'one'), S(177), l)}
				/>
			</Plate>
		)),
		draw(S(180), 'three-items', (d, l) => <ThreeItems tickAt={at(w0(181, 'ordered'), S(180), l)} smallAt={at(w0(183, 'small'), S(180), l)} dotAt={at(w0(184, 'not'), S(180), l)} />, 'ILLUSTRATION'),
		clip(pre(w0(182, 'twenty')), 'LAND_touch', CR.navyIT, 1.5),
		draw(S(183), 'three-items-2', (d, l) => <ThreeItems tickAt={0} smallAt={at(w0(183, 'small'), S(183), l)} dotAt={at(w0(184, 'not'), S(183), l)} />, 'ILLUSTRATION'),
		insert(S(185), 'LAND_ramp', CR.navyNDTV, 16 / 9, 1.0),
	],
	overlays: [
		tag(w0(156, 'four'), s1(156), '400 KG · ABOUT 17 M', 140, 180, 64, C.slot, true, 'AS REPORTED'),
		tag(w0(157, 'published'), s1(157), 'DRDO HAS PUBLISHED LITTLE', 140, 860, 50),
		tag(w0(163, 'seventy'), s1(163), '×75 THE WEIGHT', 140, 180, 80, C.slot, true),
		ask(w0(165, 'who'), s1(165), 'WHO IS STOPPING INDIA?'),
		big(w0(166, 'nobody'), s1(167), 'NOBODY', C.slot),
		tag(w0(171, 'fifteen'), s1(171), 'NAVY’S 15-YEAR PLAN', 140, 180, 52),
		tag(w0(172, 'forty'), s1(172), '≈ ₹40,000 CRORE (ESTIMATED)', 140, 860, 50, C.slot, true),
		stamp(w0(176, 'nothing'), s1(176) + 6, 'NOTHING SIGNED', C.slot, 1340, 860),
		tag(w0(179, 'eleven'), s1(179), '≈ ₹11,000 CRORE', 140, 860, 64, C.slot, true, 'OUR CALCULATION · RATE ON THE UPLOAD DAY'),
		tag(w0(182, 'twenty'), s1(182), '26 RAFALE M · ≈ ₹63,000 CRORE', 140, 860, 50, C.ink, true),
		tag(w0(185, 'ramps'), s1(185), 'FROM RAMPS', 140, 860, 64, C.slot),
	],
};

const landing: Part = {
	shots: [
		clip(S(186), 'LAND_bow', CR.navyIT, 0),
		hero(S(187), 'H_drum', 12.5),
		clip(S(188), 'TRAP_trap', CR.navyPrint, 1.0),
		draw(S(189), 'three-slots', (d, l) => (
			<ThreeSlots at={[at(w0(189, 'decision'), S(189), l), at(w0(189, 'test'), S(189), l), at(w0(189, 'ten'), S(189), l)]} words={['A DECISION', 'A TEST TRACK', '10 YEARS']} />
		)),
		shot(S(190), 'map-india', (d) => <SeaMap dur={d} keys={[{f: 0, lon: 80, lat: 21, zoom: 1.0}, {f: d, lon: 79, lat: 20, zoom: 1.25}]} />),
		clip(S(192), 'TRAP_deck', CR.navyPrint, 0.2),
		clip(S(193), 'LAND_bow', CR.navyIT, 1.0),
		clip(S(194), 'PX_fan', CR.px, 6.0),
		shot(S(195), 'meter-six', (d, l) => (
			<Plate dur={d} seed="meter6">
				<MeterSolo a={0} b={19} f0={l} f1={d} label="6 DAYS OF YOUR HOME" />
			</Plate>
		)),
		clip(S(196), 'FORD_launch', CR.usn, 5.0),
		clip(S(197), 'LAND_touch', CR.navyIT, 2.4),
		draw(S(198), 'deckplan-throw', (d, l) => <DeckPlan slotAt={l} slotEnd={l + 40} />, 'ILLUSTRATION'),
		draw(S(199), 'watch', (d, l) => (
			<Watch
				at={[at(w0(200, 'decision'), S(199), l), at(w0(201, 'first'), S(199), l), at(w0(202, 'test'), S(199), l)]}
				items={[
					['THE NEXT CARRIER', 'the decision'],
					['THE FIRST INDIAN RAFALE M', 'due around 2029'],
					['DRDO’S TEST MODEL, PUNE', 'something heavier'],
				]}
			/>
		)),
		clip(S(203), 'LAND_bow', CR.navyIT, 0.8),
		draw(S(204), 'deckplan-on', (d, l) => <DeckPlan slotAt={l} slotEnd={l + 60} />, 'ILLUSTRATION'),
		draw(S(205), 'ramp-or-catapult', (d, l) => <RampOrCatapult at={l + 10} />),
		draw(S(207), 'next', () => <SubBlind />, 'ILLUSTRATION'),
		shot(S(209), 'endcard', (d) => <EndCard dur={d} />, {hard: true}),
	],
	overlays: [
		tag(w0(187, 'cracked'), s1(187), 'TO WAR ON A CRACKED BOILER', 140, 860, 52, C.slot),
		tag(w0(188, 'designed'), s1(188), 'DESIGNED AND BUILT IN INDIA', 140, 860, 52, C.green),
		tag(w0(191, 'submarines'), s1(191), 'SUBMARINES AND THE ARMY FIRST?', 140, 860, 50),
		tag(w0(192, 'waits'), s1(192), 'THE SHIP STILL WAITS', 140, 860, 56),
		tag(w0(194, 'motor'), s1(194), 'THE MOTOR: YOUR FAN', 140, 860, 56, C.copper),
		big(w0(196, 'three'), s1(196) + 10, 'THREE SECONDS', C.slot),
		tag(w0(197, 'buy'), s1(197), 'YOU CAN BUY THE JET', 140, 760, 66),
		tag(w0(198, 'build'), s1(198) + 40, 'YOU HAVE TO BUILD THE THROW', 140, 860, 66, C.slot),
		lab(pre(w0(203, 'subscribe')), s1(204), 'subscribe', <SubscribePill press={w0(203, 'subscribe') - pre(w0(203, 'subscribe'))} />),
		tag(w0(208, 'submarine'), s1(208), 'A SUBMARINE THAT CANNOT HEAR', 140, 760, 56, C.cyan, false, 'WHAT IS RIGHT BEHIND IT'),
	],
};

export const p3: Part[] = [ch5, landing];
