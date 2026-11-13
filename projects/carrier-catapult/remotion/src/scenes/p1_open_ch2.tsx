import React from 'react';
import {AbsoluteFill} from 'remotion';
import type {Part} from '../Film';
import {Cooker, DeckPlan, Doc, Elevation61, HullCut, Meter, Radar, RampSide, SteamSplit} from '../parts/drawings';
import {Clip, Hero, Plate} from '../parts/kit';
import {SeaMap} from '../parts/SeaMap';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {clip, cnt, CR, draw, hero, insert, lab, photo, pre, shot, stamp, tag} from './common';

// Cold open (S0–15), ch1 What the ramp costs (S16–41), ch2 The catapult India had (S42–91). word_map.md.
const S = s0;
/** a word's frame inside a shot that starts at `at` with lead `l` */
const at = (word: number, shotStart: number, l: number) => word - shotStart + l;

const open: Part = {
	shots: [
		// the thumbnail's subject: the Navy's own landing footage, slowed (the clip is 4.6 s)
		clip(S(0), 'LAND_touch', CR.navyIT),
		// S2–3: the deck plan; the slot draws and stops dead at the ramp on "A catapult."
		draw(S(2), 'deckplan-open', (d, l) => <DeckPlan slotAt={at(w0(2, 'missing'), S(2), l)} slotEnd={at(w0(3, 'catapult'), S(2), l)} />, 'ILLUSTRATION'),
		clip(S(4), 'FORD_launch', CR.usn, 4.0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(5), 'LAND_bow', CR.navyIT),
		insert(S(6), 'LAND_ramp', CR.navyNDTV),
		shot(S(7), 'goa', (d) => (
			<SeaMap dur={d} keys={[{f: 0, lon: 76, lat: 17, zoom: 1.6}, {f: d, lon: 74.2, lat: 15.6, zoom: 3.2}]} pins={[{at: 8, ll: [73.83, 15.49], label: 'GOA', sub: 'SHORE RAMP TRIALS', side: 'left'}]} />
		)),
		// the match cut: the Rafale's wheel, then a Sea Hawk's wheel on the 1961 deck
		clip(S(8), 'LAND_touch', CR.navyIT, 3.2),
		clip(S(9), 'SH_nose', CR.archive, 0, undefined, 'none'),
		clip(pre(w0(9, 'throwing')), 'SH_launch', CR.archive, 0, undefined, 'none'),
		draw(S(10), 'deckplan-model', (d, l) => <DeckPlan slotAt={l} slotEnd={l + 24} modelAt={at(w0(10, 'small'), S(10), l)} />, 'ILLUSTRATION'),
		// S11–15: a real launch, a home meter ghosted over it; the rupee figure
		shot(S(11), 'meter-launch', (d, l) => (
			<AbsoluteFill>
				<Clip name="EM12_launch" dur={d} grade="day" startAt={0.5} />
				<AbsoluteFill style={{opacity: 0.9}}>
					<svg width={1920} height={1080}>
						<Meter x={1560} y={520} scale={0.75} a={0} b={19} f0={at(w0(13, 'electricity'), S(11), l)} f1={at(w0(13, 'rupees'), S(11), l)} />
					</svg>
				</AbsoluteFill>
			</AbsoluteFill>
		), {credit: CR.usn}),
		clip(S(14), 'FORD_launch', CR.usn, 5.0),
		clip(S(15), 'FORD_cat', CR.usn),
	],
	overlays: [
		tag(w0(0, 'twenty'), s1(1), '29 OCT 2026', 140, 180, 52, C.ink, true),
		tag(w0(1, 'rafale'), s1(1), 'RAFALE M', 140, 760, 60),
		tag(w0(1, 'vikrant'), s1(1), 'INS VIKRANT', 140, 860, 52, C.dim),
		tag(w0(2, 'nineteen'), s1(3), 'FIRST VIKRANT · 1961', 140, 860, 50, C.slot),
		tag(w0(4, 'thrown'), s1(4), 'A CATAPULT LAUNCH', 140, 860, 52),
		tag(w0(5, 'ramp'), s1(5), 'A RAMP', 140, 860, 64, C.slot),
		tag(w0(9, 'sixty'), s1(9), '1961', 140, 180, 90, C.slot, true),
		tag(w0(10, 'catapult'), s1(10), 'WANTED AGAIN', 140, 860, 52),
		tag(w0(13, 'two'), s1(13), 'UNDER ₹200', 140, 760, 80, C.green, true),
		tag(w0(14, 'hardest'), s1(14), 'ONE OF THE HARDEST MACHINES', 140, 860, 50),
	],
};

const ch1: Part = {
	shots: [
		clip(S(16), 'TRAP_deck', CR.navyPrint),
		clip(S(17), 'PXL_flyover', CR.pex),
		clip(pre(w0(17, 'ends')), 'LAND_bow', CR.navyIT, 0.6),
		draw(S(18), 'ramp-noparts', (d, l) => <RampSide noPartsAt={at(w0(19, 'none'), S(18), l)} />, 'SIMPLIFIED'),
		insert(S(20), 'LAND_ramp', CR.navyNDTV, 16 / 9, 1.0),
		draw(S(21), 'ramp-nothing', () => <RampSide noPartsAt={0} />, 'SIMPLIFIED'),
		insert(S(23), 'MIG_deck', CR.navy, 9 / 16, 0, 900),
		// the balance: what the ramp costs (a roadside seller's real two-pan balance)
		clip(S(24), 'PXL_balance', CR.pex),
		clip(S(28), 'PXL_balance2', CR.pex),
		draw(S(31), 'heavy', (d, l) => <RampSide heavyAt={l} dropAt={at(w0(32, 'ramp'), S(31), l)} />, 'SIMPLIFIED'),
		shot(S(33), 'radar-plane', (d, l) => (
			<Plate dur={d} seed="radar">
				<Radar heliAt={99999} planeAt={l + 10} contactAt={at(w0(35, 'trouble'), S(33), l)} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		clip(S(36), 'TRAP_trap', CR.navyPrint, 0.5),
		shot(S(38), 'radar-both', (d, l) => (
			<Plate dur={d} seed="radar2">
				<Radar heliAt={l} planeAt={at(w0(38, 'plane'), S(38), l)} contactAt={at(w0(38, 'plane'), S(38), l) + 20} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		clip(S(39), 'LAND_bow', CR.navyIT, 1.0),
		insert(S(40), 'LAND_ramp', CR.navyNDTV, 16 / 9, 2.5),
		clip(S(41), 'SH_sea', CR.archive, 0, undefined, 'none'),
		clip(pre(w0(41, 'catapult')), 'SH_deck', CR.archive, 0, undefined, 'none'),
	],
	overlays: [
		tag(w0(16, 'stand'), s1(16), 'ON VIKRANT’S DECK', 140, 860, 52),
		tag(w0(17, 'flyover'), pre(w0(17, 'ends')), 'LIKE A FLYOVER', 140, 860, 56, C.slot),
		tag(w0(23, 'clever'), s1(23), 'CHEAP · NOTHING TO BREAK', 140, 860, 50),
		tag(w0(25, 'jet'), s1(27), 'JET', 1180, 240, 64),
		tag(w0(26, 'lighter'), s1(27), 'TAKES OFF LIGHTER', 140, 860, 56, C.slot),
		tag(w0(27, 'fuel'), s1(27), 'LESS FUEL', 1180, 360, 52, C.amber),
		tag(w0(27, 'weapons'), s1(27), 'FEWER WEAPONS', 1180, 460, 52, C.amber),
		tag(w0(28, 'how'), s1(30), 'HOW MUCH LIGHTER?', 140, 760, 60),
		stamp(w0(29, 'published'), s1(30), 'NOT PUBLISHED', C.slot, 1340, 420),
		tag(w0(32, 'heavy'), s1(32), 'HEAVY AND SLOW: NO', 140, 860, 56),
		tag(w0(34, 'flying'), s1(35), 'THE FLYING RADAR', 140, 180, 60, C.cyan),
		tag(w0(36, 'helicopter'), s1(37), 'INDIA’S CARRIERS: A HELICOPTER', 140, 860, 50),
		tag(w0(39, 'price'), s1(39), 'THE RAMP HAS A PRICE', 140, 860, 56, C.slot),
	],
};

const ch2: Part = {
	shots: [
		clip(S(42), 'AL_ship', CR.archive, 0, undefined, 'none'),
		clip(S(43), 'AL_folded', CR.archive, 0, undefined, 'none'),
		clip(pre(w0(43, 'aircraft')), 'AL_ship', CR.archive, 0.2, undefined, 'none'),
		clip(pre(w0(43, 'finished')), 'SH_tail', CR.archive, 0, undefined, 'none'),
		clip(S(44), 'SH_pilot', CR.archive, 0, undefined, 'none'),
		clip(S(45), 'SH_deck', CR.archive, 0, undefined, 'none'),
		clip(S(46), 'SH_launch', CR.archive, 0, undefined, 'none'),
		draw(S(47), 'cooker', (d, l) => <Cooker buildAt={at(w0(49, 'builds'), S(47), l)} burstAt={at(w0(49, 'goes', 1), S(47), l)} />, 'ILLUSTRATION'),
		// the 1961 catapult: the piston fires (2.5 s into the render) on "drives"
		hero(S(50), 'H_catapult', 2.5 - (w0(50, 'drives') - S(50)) / 60, 'ILLUSTRATION · SIMPLIFIED'),
		clip(S(51), 'SH_bow', CR.archive, 0, undefined, 'none'),
		hero(S(52), 'H_drum', 0),
		shot(S(54), 'drum-slow', (d, l) => <Hero name="H_drum" dur={d} startAt={2.0} rate={0.6} />, {tag: 'ILLUSTRATION'}),
		shot(S(56), 'doc-1970', (d, l) => (
			<Plate dur={d} seed="doc70">
				<Doc
					at={l}
					head="THE FIRST VIKRANT · BOMBAY, JUNE 1970"
					lines={['Serious cracks in a boiler drum', 'The other drums: beyond repair by welding', 'A lasting repair: not possible in India']}
					mark={2}
					markAt={at(w0(56, 'lasting'), S(56), l)}
					stamp="SOURCE: THE NAVY’S OFFICIAL HISTORY, VIA GLOBALSECURITY"
				/>
			</Plate>
		)),
		draw(S(57), 'steam-split', (d, l) => (
			<SteamSplit propAt={at(w0(58, 'propellers'), S(57), l)} slotAt={at(w0(58, 'catapult'), S(57), l)} redAt={at(w0(59, 'blow'), S(57), l)} />
		), 'SIMPLIFIED'),
		clip(S(60), 'W71_sea', CR.fd, 0, undefined, 'none'),
		clip(S(61), 'AL_ship', CR.archive, 0.4, undefined, 'none'),
		clip(S(62), 'W71_sea', CR.fd, 1.0, undefined, 'none'),
		clip(S(63), 'SH_sea', CR.archive, 0, undefined, 'none'),
		clip(S(64), 'W71_deck', CR.fd, 0, undefined, 'none'),
		shot(S(65), 'doc-nanda', (d, l) => (
			<Plate dur={d} seed="nanda">
				<Doc
					at={l}
					head="ADMIRAL NANDA, NAVY CHIEF · 1971"
					lines={['“…Vikrant would be called a white elephant', 'and naval aviation would be written off.”']}
					mark={0}
					markAt={at(w0(66, 'white'), S(65), l)}
					stamp="AS RECALLED IN THE NAVY’S OFFICIAL HISTORY"
				/>
			</Plate>
		)),
		hero(S(67), 'H_room', 5.0),
		photo(S(68), 'roy_face.jpg', CR.pib),
		// the bands go on: band 1 lands about 8.0 s into the render, on "steel"
		hero(S(70), 'H_drum', 8.0 - (w0(71, 'steel') - S(70)) / 60),
		hero(S(73), 'H_room', 7.5),
		clip(S(74), 'PX_steam', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		hero(S(75), 'H_room', 4.4),
		clip(S(76), 'W71_bow', CR.fd, 0, undefined, 'none'),
		shot(pre(w0(76, 'coxs')), 'map-cox', (d) => (
			<SeaMap dur={d} keys={[{f: 0, lon: 88, lat: 19, zoom: 2.2}, {f: d, lon: 90.5, lat: 20.6, zoom: 3.2}]} pins={[{at: 6, ll: [91.98, 21.43], label: 'COX’S BAZAR', sub: '4 DECEMBER 1971', side: 'left'}]} />
		)),
		photo(S(77), 'vrc_medal.jpg', CR.pib),
		hero(S(78), 'H_drum', 12.0),
		clip(pre(w0(79, 'war')), 'W71_bow', CR.fd, 1.0, undefined, 'none'),
		clip(S(80), 'SH_sea', CR.archive, 0, undefined, 'none'),
		draw(S(81), 'elev-harrier', () => <Elevation61 sealAt={99999} liftAt={99999} />, 'ILLUSTRATION'),
		clip(S(82), 'AL_start', CR.archive, 0, undefined, 'none'),
		clip(pre(w0(82, 'retired')), 'AL_ship', CR.archive, 0, undefined, 'none'),
		draw(S(83), 'elev-ramp', (d, l) => <Elevation61 sealAt={at(w0(83, 'catapult'), S(83), l)} liftAt={at(w0(83, 'ramp'), S(83), l)} />, 'ILLUSTRATION · SIMPLIFIED'),
		clip(S(84), 'LAND_bow', CR.navyIT, 0.2),
		insert(S(86), 'MIG_deck', CR.navy, 9 / 16, 0, 900),
		clip(pre(w0(86, 'ramp')), 'LAND_bow', CR.navyIT, 1.2),
		draw(S(87), 'hullcut', (d, l) => <HullCut turbAt={at(w0(87, 'gas'), S(87), l)} fillAt={at(w0(89, 'room'), S(87), l)} />, 'ILLUSTRATION · SIMPLIFIED'),
		clip(S(90), 'TRAP_deck', CR.navyPrint, 0.3),
		clip(S(91), 'TRAP_trap', CR.navyPrint, 0),
		clip(pre(w0(91, 'electricity')), 'EM12_trough', CR.usn),
	],
	overlays: [
		tag(w0(42, 'belfast'), s1(42), 'BELFAST', 140, 760, 64),
		tag(w0(42, 'fourth'), s1(42), '4 MARCH 1961', 140, 860, 52, C.slot, true),
		tag(w0(43, 'bought'), s1(43), 'BOUGHT FROM BRITAIN', 140, 860, 52),
		tag(w0(44, 'vikrant'), s1(44), 'VIKRANT', 140, 860, 64, C.slot),
		tag(w0(45, 'steam'), s1(46), 'A STEAM CATAPULT', 140, 860, 56, C.amber),
		tag(w0(48, 'pressure'), s1(48), 'YOUR PRESSURE COOKER', 140, 860, 56, C.amber),
		tag(w0(51, 'nine'), s1(51), '1961 → 1970', 140, 180, 70, C.slot, true),
		tag(w0(52, 'june'), s1(52), 'JUNE 1970 · BOMBAY', 140, 180, 56, C.ink, true),
		tag(w0(52, 'cracks'), s1(53), 'CRACKS IN A BOILER', 140, 860, 56, C.amber),
		tag(w0(54, 'many'), s1(54), 'MANY', 140, 860, 64, C.amber),
		tag(w0(55, 'weld'), s1(55), 'CANNOT BE WELDED', 140, 860, 56),
		tag(w0(59, 'admiral'), s1(59), 'ADMIRAL ARUN PRAKASH', 140, 180, 46, C.ink),
		tag(w0(61, 'fourteen'), s1(61), '14 KNOTS', 140, 760, 80, C.slot, true),
		tag(w0(62, 'twenty'), s1(62), '≈ 26 KM/H', 140, 870, 60, C.ink, true),
		tag(w0(63, 'slow'), s1(63), 'TOO SLOW FOR A CARRIER', 140, 860, 52),
		tag(w0(64, 'leave'), s1(64), '“LEAVE HER OUT”', 140, 860, 56),
		tag(w0(67, 'engine'), s1(67), 'THE ENGINE ROOM', 140, 860, 52),
		tag(w0(68, 'commander'), s1(69), 'CDR BENOY ROY CHOWDHURY', 140, 820, 50, C.ink, false, 'SHIP’S ENGINEER · PHOTO: LATER YEARS'),
		tag(w0(69, 'beeloo'), s1(69), '“BILU”', 1500, 820, 60, C.slot),
		tag(w0(71, 'steel'), s1(71), 'STEEL BANDS', 140, 860, 60, C.slot),
		tag(w0(72, 'safety'), s1(72), 'SAFETY VALVES RESET', 140, 860, 52),
		tag(w0(73, 'empty'), s1(73), 'THE ROOM KEPT ALMOST EMPTY', 140, 860, 50),
		tag(w0(76, 'fourth'), s1(76), '4 DEC 1971', 140, 180, 70, C.slot, true),
		tag(w0(77, 'vir'), s1(77), 'VIR CHAKRA', 140, 760, 64, C.slot, false, 'A MEDAL FOR BRAVERY'),
		tag(w0(79, 'steel'), s1(79), 'KEPT ALIVE WITH STEEL BANDS', 140, 860, 50, C.slot),
		tag(w0(81, 'harrier'), s1(81), 'SEA HARRIER · NEEDS NO CATAPULT', 140, 860, 50),
		tag(w0(82, 'nineteen'), s1(82), 'LAST ALIZÉS RETIRED · 1989', 140, 860, 50, C.ink),
		tag(w0(86, 'ramp'), s1(86), 'DESIGNED FOR A RAMP JET', 140, 860, 52),
		tag(w0(89, 'naval'), s1(89), 'NAVAL ANALYSTS', 140, 180, 46, C.dim, false, 'THEIR VIEW, NOT THE NAVY’S'),
		tag(w0(91, 'electricity'), s1(91), 'ELECTRICITY', 140, 860, 64, C.copper),
	],
};

export const p1: Part[] = [open, ch1, ch2];
