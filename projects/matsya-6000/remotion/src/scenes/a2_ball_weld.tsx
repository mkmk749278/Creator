import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {Alvin, BeadInAir, SteelBall2021, TubeVsBall, WeldBars} from '../parts/drawings';
import {ez, Insert, Plate, tw} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {ask, clip, cnt, CR, hero, lab, photo, pre, shot, stamp, tag} from './common';

// Narration v3: why a ball (S48–59) and ISRO's hardest weld (S60–102).
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
		// a real cricket ball, then a real hand squeezing a ball: together they say the sentence
		clip(S(48), 'PX_cricket', CR.px, 5.2),
		clip(S(49), 'PX_ball', CR.pex, 2.2),
		hero(S(50), 'H4_squeeze', 7.0, 'SIMPLIFIED'),
		shot(S(52), 'tube', (d, l) => (
			<Plate dur={d} seed="tube">
				<TubeVsBall tubeEnds={w0(52, 'tube') - S(52) + l} ring={l + 20} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		clip(pre(w0(52, 'normal')), 'VAG_surf', CR.navy),
		photo(S(53), 'alvin_panorama.jpg', CR.alvin),
		shot(S(54), 'alvin', (d, l) => (
			<Plate dur={d} seed="alvin">
				<Alvin steel={w0(54, 'steel') - S(54) + l} ti={w0(55, 'titanium') - S(54) + l} bars={w0(55, 'twice') - S(54) + l} />
			</Plate>
		), {tag: 'ILLUSTRATION'}),
		clip(S(56), 'PX_ship', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		shot(pre(w0(57, 'lowered')), 'steel2021', (d, l) => <SteelBall2021 dur={d} date={1} depth={w0(57, 'six') - pre(w0(57, 'lowered')) + l} />, {tag: 'ILLUSTRATION'}),
		clip(S(58), 'ISRO_ti', CR.isro, 6.0),
	],
	overlays: [
		tag(w0(48, 'cricket'), s1(49), 'A CRICKET BALL', 140, 760, 56),
		tag(w0(50, 'spreads'), s1(50), 'THE PUSH SPREADS', 140, 760, 56, C.amber),
		tag(w0(51, 'corner'), s1(51) + 10, 'NO CORNER · NO FLAT SIDE', 140, 860, 52),
		tag(w0(53, 'alvin'), s1(53), 'ALVIN · USA', 140, 760, 56),
		tag(w0(56, 'india'), s1(56), 'INDIA · THE SAME ROAD', 140, 760, 52),
		tag(w0(57, 'twenty'), pre(w0(57, 'lowered')), 'OCTOBER 2021', 140, 300, 52),
		tag(w0(57, 'bay'), s1(57), 'BAY OF BENGAL', 140, 480, 48, C.dim),
		tag(w0(58, 'titanium'), s1(59), 'THEN TITANIUM', 140, 760, 64, C.ti),
	],
};

// S61–67: H2_pieces (its hatch lifts about 6.9 s in) with ISRO's own drawing cut in on "drawing" for 1.6 s
const piecesAt = S(61);
const piecesFrom = 2.9;
const drawingAt = pre(w0(62, 'drawing'));
const backAt = drawingAt + 96;
// S90–97: H2_seam, with ISRO's real weld bead on "How long did it take? Thirty-two minutes. One pass."
const seamAt = S(90);

const ch3: Part = {
	shots: [
		clip(S(60), 'ISRO_ring', CR.isro),
		clip(pre(w0(60, 'this')), 'ISRO_machining', CR.isro),
		hero(piecesAt, 'H2_pieces', piecesFrom),
		shot(drawingAt, 'ISRO_drawing', (d) => <Insert name="ISRO_drawing" dur={d} startAt={0.6} height={860} />, {credit: CR.isro}),
		hero(backAt, 'H2_pieces', piecesFrom + (backAt - piecesAt) / 60),
		clip(S(67), 'ISRO_shell', CR.isro),
		hero(S(68), 'H2_seam', 0),
		clip(S(71), 'ISRO_ti', CR.isro, 3.0),
		clip(S(72), 'PX_weld', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		shot(pre(w0(72, 'oxygen')), 'bead', (d, l) => (
			<Plate dur={d} seed="bead">
				<BeadInAir atoms={l + 9} holes={w0(73, 'holes') - pre(w0(72, 'oxygen')) + l} crack={w0(74, 'crack') - pre(w0(72, 'oxygen')) + l} />
			</Plate>
		), {tag: 'SIMPLIFIED'}),
		clip(S(75), 'PX_flame', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(77), 'ISRO_chamber', CR.isro),
		clip(pre(w0(77, 'electrons')), 'ISRO_console', CR.isro),
		clip(pre(w0(77, 'inside')), 'ISRO_ebglow', CR.isro),
		clip(S(79), 'ISRO_operator', CR.isro),
		clip(S(80), 'ISRO_chamber', CR.isro),
		shot(pre(w0(80, 'two')), 'bars', (d, l) => (
			<Plate dur={d} seed="bars2">
				<WeldBars show20={l + 9} show80={w0(81, 'eight') - pre(w0(80, 'two')) + l} />
			</Plate>
		)),
		clip(S(82), 'ISRO_screens', CR.isro),
		clip(pre(w0(82, 'buy')), 'ISRO_monitor', CR.isro),
		clip(S(83), 'ISRO_console', CR.isro),
		clip(S(85), 'ISRO_operator', CR.isro),
		clip(S(86), 'ISRO_machining', CR.isro),
		clip(S(87), 'ISRO_console2', CR.isro),
		clip(pre(w0(89, 'until')), 'ISRO_screens', CR.isro),
		hero(seamAt, 'H2_seam', 0),
		clip(S(93), 'ISRO_bead', CR.isro),
		clip(S(96), 'ISRO_hall', CR.isro),
		hero(S(97), 'H2_seam', 11.5),
		clip(S(98), 'ISRO_shell', CR.isro),
		clip(S(99), 'F01_ball', CR.dd),
		clip(S(100), 'ISRO_xray', CR.isro),
		clip(pre(w0(100, 'see')), 'ISRO_monitor', CR.isro),
		clip(S(101), 'ISRO_ut', CR.isro),
		clip(S(102), 'F01_hall', CR.dd),
	],
	overlays: [
		tag(w0(60, 'big'), s1(60), '2.26 M ACROSS', 140, 760, 56),
		tag(w0(62, 'five'), s1(62), 'FIVE PIECES', 140, 760, 60),
		tag(w0(63, 'hatch'), s1(63) + 6, 'TOP HATCH', 140, 200, 56),
		tag(w0(64, 'rings'), s1(64) + 6, 'THREE RINGS', 140, 200, 56),
		tag(w0(65, 'dome'), s1(65) + 6, 'BOTTOM DOME', 140, 200, 56),
		tag(w0(66, 'five'), s1(66) + 10, '5,691 KG', 140, 200, 64, C.amber, true, 'ISRO’S PIECE WEIGHTS, ADDED: OUR CALCULATION'),
		tag(w0(68, 'seven'), s1(68) + 6, 'SEVEN WELDS', 140, 200, 60, C.weld),
		tag(w0(69, 'four'), s1(69) + 6, '4 BELTS', 140, 290, 56, C.weld),
		tag(w0(70, 'three'), s1(70) + 6, '3 ROUND THE WINDOWS', 140, 380, 52, C.weld),
		tag(w0(71, 'weakness'), s1(71), 'TITANIUM’S ONE WEAKNESS', 140, 760, 56),
		tag(w0(72, 'hot'), pre(w0(72, 'oxygen')), 'WHEN IT’S HOT', 140, 760, 56, C.weld),
		tag(w0(75, 'flame'), s1(76), 'A NORMAL FLAME · NO USE', 140, 760, 52),
		tag(w0(77, 'beam'), s1(77), 'A BEAM OF ELECTRONS', 140, 180, 56, C.cyan),
		lab(w0(77, 'beam'), pre(w0(77, 'inside')), 'beam', <Beam />),
		tag(w0(77, 'vacuum'), s1(78), 'IN A VACUUM', 140, 270, 52),
		tag(w0(78, 'air'), s1(78), 'NO AIR GETS IN', 140, 760, 52, C.green),
		tag(w0(80, 'bengaluru'), pre(w0(80, 'two')), 'ISRO · LPSC BENGALURU', 140, 760, 52),
		ask(w0(82, 'buy'), s1(82) + 6, 'Then buy a bigger machine?'),
		tag(w0(83, 'own'), s1(83), 'THEY MADE THEIR OWN STRONGER', 140, 760, 50, C.green),
		cnt(w0(84, 'fifteen'), w0(84, 'forty'), s1(84) + 10, 40, 'KW', 140, 200, 110, C.amber, 15),
		tag(w0(87, 'ten'), w0(88, 'hundred'), 'NOT 10', 140, 200, 64, C.dim),
		tag(w0(88, 'hundred'), w0(89, 'seven'), 'NOT 100', 140, 200, 64, C.dim),
		cnt(w0(89, 'seven'), w0(89, 'trial'), s1(89) + 10, 700, 'TRIAL WELDS'),
		tag(w0(90, 'real'), s1(90), 'THE REAL ONE', 140, 760, 60, C.weld),
		tag(w0(92, 'eight'), s1(92), '80 MM DEEP', 140, 180, 56, C.weld),
		tag(w0(92, 'seven'), s1(92), '7.1 M LONG', 1100, 180, 64, C.amber, true, 'OUR CALCULATION: π × 2.26 M'),
		cnt(w0(94, 'thirty-two'), w0(94, 'minutes'), s1(95) + 10, 32, 'MINUTES', 140, 720, 120, C.weld),
		tag(w0(95, 'one'), s1(95) + 10, 'ONE PASS', 140, 180, 60, C.amber),
		tag(w0(96, 'first'), s1(96), 'FIRST IN INDIA', 140, 760, 60, C.amber, false, 'ISRO'),
		tag(w0(97, 'seven'), s1(97) + 10, '700 TRIES', 140, 180, 64, C.amber),
		tag(w0(97, 'thirty-two'), s1(97) + 10, 'FOR 32 MINUTES', 140, 280, 64, C.weld),
		tag(w0(100, 'x-ray'), s1(100), 'X-RAY · 7.5 MEV', 140, 180, 56, C.cyan),
		lab(w0(100, 'x-ray'), s1(100), 'scan', <Scan />),
		tag(w0(101, 'sound'), s1(101), 'SOUND WAVES', 140, 180, 56, C.cyan),
		lab(w0(101, 'sound'), s1(101), 'rings', <Rings x={1250} y={560} />),
		stamp(w0(102, 'certify'), s1(102) + 10, 'CERTIFIED', C.green),
	],
};

export const a2: Part = {shots: [...ch2.shots, ...ch3.shots], overlays: [...ch2.overlays, ...ch3.overlays]};
