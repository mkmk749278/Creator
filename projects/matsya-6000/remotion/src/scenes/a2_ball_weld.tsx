import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {Alvin, BeadInAir, SteelBall2021, TubeVsBall, WeldBars} from '../parts/drawings';
import {ez, Insert, Plate, tw} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {clip, cnt, CR, hero, lab, photo, pre, shot, stamp, tag} from './common';

// Ch2 (why a ball, S42–52) and Ch3 (ISRO's hardest weld, S53–88), word_map.md.
const S = s0;

/** S71: a beam line across the chamber shot, white-blue, on "beam of electrons" */
const Beam: React.FC = () => {
	const f = useCurrentFrame();
	const k = tw(f, 0, 24, 0, 1, ez.sweep);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			<line x1={-40} y1={300} x2={-40 + 1100 * k} y2={540} stroke="#bfe6ff" strokeWidth={10} opacity={0.85} />
			<line x1={-40} y1={300} x2={-40 + 1100 * k} y2={540} stroke="#ffffff" strokeWidth={3} />
		</svg>
	);
};

/** S86: a cyan scan line sweeping down a frame (X-ray) */
const Scan: React.FC<{color?: string}> = ({color = C.cyan}) => {
	const f = useCurrentFrame();
	const y = ((f * 9) % 1300) - 120;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			<rect x={0} y={y} width={1920} height={6} fill={color} opacity={0.9} />
			<rect x={0} y={y - 120} width={1920} height={120} fill={color} opacity={0.08} />
		</svg>
	);
};

/** S87: rings of sound spreading from a point */
const Rings: React.FC<{x: number; y: number}> = ({x, y}) => {
	const f = useCurrentFrame();
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			{[0, 1, 2, 3].map((i) => {
				const k = ((f + i * 18) % 72) / 72;
				return <circle key={i} cx={x} cy={y} r={30 + 420 * k} fill="none" stroke={C.cyan} strokeWidth={6} opacity={1 - k} />;
			})}
		</svg>
	);
};

const ch2: Part = {
	shots: [
		shot(S(42), 'tube', (d, l) => (
			<Plate dur={d} seed="tube">
				<TubeVsBall tubeEnds={l + 50} ring={l + 600} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		clip(pre(w0(43, 'long')), 'VAG_surf', CR.navy),
		hero(S(44), 'H4_squeeze', 7.0, 'SIMPLIFIED'),
		photo(pre(w0(47, 'alvin')), 'alvin_panorama.jpg', CR.alvin),
		shot(S(48), 'alvin', (d, l) => (
			<Plate dur={d} seed="alvin">
				<Alvin steel={w0(48, 'steel') - S(48) + l} ti={w0(49, 'titanium') - S(48) + l} bars={w0(49, 'twice') - S(48) + l} />
			</Plate>
		), {tag: 'ILLUSTRATION'}),
		clip(S(50), 'PX_ship', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		shot(pre(w0(51, 'lowered')), 'steel2021', (d, l) => <SteelBall2021 dur={d} date={1} depth={w0(51, 'six') - pre(w0(51, 'lowered')) + l} />, {tag: 'ILLUSTRATION'}),
		clip(S(52), 'ISRO_ti', CR.isro, 6.0),
	],
	overlays: [
		tag(w0(45, 'spread'), s1(45), 'THE PUSH SPREADS', 140, 760, 56, C.amber),
		tag(w0(46, 'corner'), s1(46) + 10, 'NO CORNER · NO FLAT SIDE', 140, 860, 52),
		tag(w0(51, 'twenty'), pre(w0(51, 'lowered')), 'OCTOBER 2021', 140, 300, 52),
		tag(w0(51, 'bay'), s1(51), 'BAY OF BENGAL', 140, 480, 48, C.dim),
		tag(w0(52, 'titanium'), s1(52) + 10, 'THEN TITANIUM', 140, 760, 64, C.ti),
	],
};

// S57–64: H2_pieces with ISRO's own drawing cut in on "drawing" for 1.6 s
const drawingAt = pre(w0(57, 'drawing'));
const backAt = drawingAt + 96;

const ch3: Part = {
	shots: [
		clip(S(53), 'ISRO_ring', CR.isro),
		clip(S(54), 'ISRO_machining', CR.isro),
		clip(S(55), 'ISRO_hall', CR.isro),
		clip(S(56), 'ISRO_forge', CR.isro),
		hero(S(57), 'H2_pieces', 0),
		shot(drawingAt, 'ISRO_drawing', (d) => <Insert name="ISRO_drawing" dur={d} startAt={0.6} height={860} />, {credit: CR.isro}),
		hero(backAt, 'H2_pieces', (backAt - S(57)) / 60),
		clip(S(65), 'ISRO_shell', CR.isro),
		clip(S(66), 'ISRO_ti', CR.isro, 3.0),
		clip(S(67), 'PX_weld', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		shot(pre(w0(67, 'grabs')), 'bead', (d, l) => (
			<Plate dur={d} seed="bead">
				<BeadInAir atoms={w0(67, 'oxygen') - pre(w0(67, 'grabs')) + l} holes={w0(68, 'holes') - pre(w0(67, 'grabs')) + l} crack={w0(68, 'crack') - pre(w0(67, 'grabs')) + l} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		clip(S(69), 'PX_flame', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(70), 'ISRO_chamber', CR.isro),
		clip(pre(w0(71, 'electrons')), 'ISRO_console', CR.isro),
		clip(S(72), 'ISRO_ebglow', CR.isro),
		clip(S(73), 'ISRO_operator', CR.isro),
		clip(pre(w0(74, 'welding')), 'ISRO_chamber', CR.isro),
		shot(pre(w0(74, 'two')), 'bars', (d, l) => (
			<Plate dur={d} seed="bars2">
				<WeldBars show20={w0(74, 'two') - pre(w0(74, 'two')) + l} show80={w0(75, 'eight') - pre(w0(74, 'two')) + l} />
			</Plate>
		)),
		clip(pre(w0(76, 'machine')), 'ISRO_screens', CR.isro),
		clip(S(77), 'ISRO_monitor', CR.isro),
		clip(pre(w0(78, 'seven')), 'ISRO_console2', CR.isro),
		hero(S(79), 'H2_seam', 0),
		clip(pre(w0(79, 'real')), 'ISRO_bead', CR.isro),
		hero(pre(w0(79, 'real')) + 72, 'H2_seam', (pre(w0(79, 'real')) + 72 - S(79)) / 60),
		clip(S(84), 'ISRO_bead', CR.isro, 0.6),
		clip(S(85), 'ISRO_operator', CR.isro),
		clip(S(86), 'ISRO_shell', CR.isro),
		clip(pre(w0(86, 'x-ray')) + 60, 'ISRO_xray', CR.isro),
		clip(S(87), 'ISRO_ut', CR.isro),
		clip(S(88), 'F01_hall', CR.dd),
	],
	overlays: [
		tag(w0(55, 'big'), s1(55), '2.26 M ACROSS', 140, 760, 56),
		tag(w0(58, 'hatch'), s1(58) + 6, 'TOP HATCH', 140, 200, 56),
		tag(w0(59, 'rings'), s1(59) + 6, 'THREE RINGS', 140, 200, 56),
		tag(w0(60, 'dome'), s1(60) + 6, 'BOTTOM DOME', 140, 200, 56),
		tag(w0(61, 'weigh'), s1(61) + 20, '5,691 KG', 140, 200, 64, C.amber, true, 'ISRO’S PIECE WEIGHTS, ADDED: OUR CALCULATION'),
		tag(w0(62, 'seven'), s1(62) + 6, 'SEVEN WELDS', 140, 200, 60, C.weld),
		tag(w0(63, 'four'), s1(63) + 6, '4 BELTS', 140, 290, 56, C.weld),
		tag(w0(64, 'three'), s1(64) + 10, '3 ROUND THE WINDOWS', 140, 380, 52, C.weld),
		tag(w0(66, 'fussy'), s1(66), 'TITANIUM IS FUSSY', 140, 760, 56),
		tag(w0(71, 'beam'), s1(71), 'A BEAM OF ELECTRONS', 140, 180, 56, C.cyan),
		lab(w0(71, 'beam'), s1(71), 'beam', <Beam />),
		tag(w0(71, 'vacuum'), s1(72), 'IN A VACUUM', 140, 270, 52),
		tag(w0(72, 'air'), s1(72), 'NO AIR GETS IN', 140, 760, 52, C.green),
		tag(w0(74, 'bengaluru'), s1(74), 'ISRO · LPSC BENGALURU', 140, 180, 48, C.dim),
		cnt(w0(76, 'powerful'), w0(76, 'powerful') + 60, s1(76) + 60, 40, 'KW', 140, 200, 110, C.amber, 15),
		cnt(w0(78, 'seven'), w0(78, 'trial'), s1(78) + 20, 700, 'TRIAL WELDS'),
		tag(w0(81, 'eight'), s1(81), '80 MM DEEP', 140, 180, 56, C.weld),
		tag(w0(81, 'seven'), s1(81) + 30, '7.1 M LONG', 1100, 180, 64, C.amber, true, 'OUR CALCULATION: π × 2.26 M'),
		cnt(w0(82, 'thirty-two'), w0(82, 'minutes'), s1(82) + 20, 32, 'MIN · ONE GO', 140, 760, 110, C.weld),
		tag(w0(83, 'first'), s1(83), 'FIRST IN INDIA', 140, 760, 60, C.amber, false, 'ISRO'),
		tag(w0(86, 'x-ray'), s1(86), 'X-RAY · 7.5 MEV', 140, 180, 56, C.cyan),
		lab(w0(86, 'x-ray'), s1(86), 'scan', <Scan />),
		tag(w0(87, 'sound'), s1(87), 'SOUND WAVES', 140, 180, 56, C.cyan),
		lab(w0(87, 'sound'), s1(87), 'rings', <Rings x={1250} y={560} />),
		stamp(w0(88, 'certify'), s1(88) + 20, 'CERTIFIED', C.green),
	],
};

export const a2: Part = {shots: [...ch2.shots, ...ch3.shots], overlays: [...ch2.overlays, ...ch3.overlays]};
