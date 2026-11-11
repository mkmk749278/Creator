import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {DepthLadder, Microspheres} from '../parts/drawings';
import {ez, Plate, tw, useSpring} from '../parts/kit';
import {P, SeaMap} from '../parts/SeaMap';
import {C, F} from '../theme';
import {DURATION, s0, s1, w0} from '../timing';
import {clip, cnt, CR, Deep, hero, insert, lab, photo, pre, shot, tag} from './common';

// Ch4 (inside, the aquanauts, S89–98), Ch5 (the foam and the delay, S99–113), Ch6 (the seabed, S114–132), the
// landing (S133–143) and the outro, word_map.md.
const S = s0;

/** the subscribe ask (owner, 2026-11-07), as in the last film: a pill on "Subscribe", pressed once, then breathing */
const SubscribePill: React.FC<{press: number}> = ({press}) => {
	const f = useCurrentFrame();
	const p = useSpring(0);
	const pr = useSpring(press, 260, 16);
	const tap = f >= press ? 1 - 0.06 * Math.sin(Math.min(1, (f - press) / 12) * Math.PI) : 1;
	const breathe = f > press + 12 ? 0.5 + 0.5 * Math.sin(((f - press - 12) / 60) * Math.PI * 2) : 0;
	return (
		<div style={{position: 'absolute', left: '50%', bottom: 320, transform: `translate(-50%, ${(1 - p) * 60}px)`, opacity: p,
			display: 'flex', alignItems: 'center', gap: 28, padding: '18px 22px 18px 18px', borderRadius: 999,
			background: 'rgba(13,17,23,0.92)', border: '2px solid rgba(238,243,248,0.16)', boxShadow: '0 24px 70px rgba(0,0,0,0.6)'}}>
			<Img src={staticFile('brand/logo_square.png')} style={{width: 96, height: 96, borderRadius: 999}} />
			<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 46, color: C.ink, letterSpacing: 1, whiteSpace: 'nowrap'}}>BE PRACTICAL WITH KISHORE</div>
			<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 46, letterSpacing: 2, padding: '16px 34px', borderRadius: 999, whiteSpace: 'nowrap',
				color: pr > 0.5 ? C.ink : '#0d1117', background: pr > 0.5 ? C.red : C.ink, transform: `scale(${tap})`,
				boxShadow: `0 0 ${20 + 30 * breathe}px rgba(255,59,59,${0.25 + 0.35 * breathe * pr})`}}>
				SUBSCRIBE
			</div>
		</div>
	);
};

/** the end card: the channel's mark over the deep (the only logo in the film, §5) */
const EndCard: React.FC<{dur: number}> = ({dur}) => {
	const f = useCurrentFrame();
	const logo = useSpring(10);
	const fade = tw(f, 0, 24, 0, 1, ez.arrive);
	return (
		<AbsoluteFill>
			<Deep dur={dur} />
			<AbsoluteFill style={{background: `rgba(3,7,13,${0.8 * fade})`, alignItems: 'center', justifyContent: 'center'}}>
				<Img src={staticFile('brand/logo_square.png')} style={{width: 420, height: 420, opacity: logo, transform: `scale(${0.9 + 0.1 * logo})`, borderRadius: 24}} />
			</AbsoluteFill>
		</AbsoluteFill>
	);
};

/** S93–94: oxygen in, carbon dioxide out, over the seats */
const Breath: React.FC<{co2: number}> = ({co2}) => {
	const f = useCurrentFrame();
	const a = tw(f, 0, 30, 0, 1, ez.sweep);
	const b = tw(f, co2, co2 + 30, 0, 1, ez.sweep);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
			<line x1={300} y1={220} x2={300 + 520 * a} y2={420} stroke={C.cyan} strokeWidth={14} strokeLinecap="round" />
			<line x1={1100} y1={460} x2={1100 + 520 * b} y2={260} stroke={C.dim} strokeWidth={14} strokeLinecap="round" strokeDasharray="4 22" />
		</svg>
	);
};

/** S120–122: India's official boundary, then down to the Central Indian Ocean Basin and India's licensed area */
const Basin: React.FC<{dur: number; area: number; since: number; robot: number; lead: number}> = ({dur, area, since, robot}) => (
	<SeaMap
		dur={dur}
		keys={[
			{f: 0, lon: 80, lat: 12, zoom: 0.95},
			{f: area, lon: 77, lat: -4, zoom: 0.95},
			{f: dur, lon: 76, lat: -10, zoom: 1.25},
		]}
		area={{at: area, ll: P.ciob, km2: 75000}}
		pins={[
			{at: area, ll: P.ciob, label: 'CENTRAL INDIAN OCEAN BASIN', sub: 'INDIA’S AREA · ABOUT 75,000 KM² (APPROX. PLACE)', side: 'right'},
			{at: robot, ll: [75.0, -11.8], label: 'ROBOT SUB · 2022', sub: 'MORE THAN 5 KM DOWN', side: 'left', color: C.cyan},
		]}
	/>
);

const ch4: Part = {
	shots: [
		hero(S(89), 'H1_cutaway', 0),
		hero(S(93), 'H1_dive', 9.2),
		photo(S(95), 'ifr_nautile_surface.jpg', CR.ifr),
		insert(S(96), 'F06_nautile', CR.osn, 1),
		photo(S(97), 'ifr_nautile_inside.jpg', CR.ifr),
		photo(S(98), 'ifr_nautile_recovery.jpg', CR.ifr),
	],
	overlays: [
		tag(w0(90, 'eight'), s1(90), '80 MM WALL', 140, 180, 56, C.ti),
		tag(w0(90, 'two'), s1(90) + 20, 'JUST OVER 2 M INSIDE', 140, 270, 56, C.amber, false, 'OUR CALCULATION: 2,260 − 2 × 80 MM'),
		tag(w0(92, 'two'), s1(92), '3 PEOPLE', 140, 180, 56),
		tag(w0(92, 'twelve'), s1(92) + 10, '12 HOURS A DIVE', 140, 270, 56, C.cyan),
		lab(S(93), s1(94), 'breath', <Breath co2={w0(94, 'carbon') - S(93)} />),
		tag(w0(93, 'oxygen'), s1(94), 'OXYGEN IN', 140, 180, 56, C.cyan),
		tag(w0(94, 'carbon'), s1(94), 'CO₂ CLEANED AWAY', 1100, 180, 56, C.dim),
		tag(w0(96, 'french'), s1(96), 'FRANCE · NAUTILE', 140, 180, 56),
		tag(w0(96, 'august'), s1(96), 'AUGUST 2025', 140, 270, 48, C.dim, true),
		tag(w0(97, 'raju'), s1(97) + 10, 'RAJU RAMESH', 140, 760, 56, C.ink, false, 'SCIENTIST · ABOUT 4,025 M'),
		tag(w0(98, 'commander'), s1(98) + 10, 'CDR JATINDER PAL SINGH (RETD)', 140, 760, 52, C.ink, false, 'ABOUT 5,002 M'),
	],
};

const ch5: Part = {
	shots: [
		hero(S(99), 'H1_dark', 2.0),
		hero(S(102), 'H3_assemble', 0),
		shot(pre(w0(106, 'tiny')), 'microspheres', () => <Microspheres />, {tag: 'ILLUSTRATION'}),
		photo(S(107), 'pib_dom_foam.png', CR.pib),
		photo(S(109), 'pib_wet_foam.jpg', CR.pib, 'contain'),
		photo(S(112), 'pib_wet_crane.jpg', CR.pib, 'contain'),
		insert(pre(w0(113, 'twenty')), 'F03_water', CR.ddt),
	],
	overlays: [
		tag(w0(100, 'not'), s1(101), 'NOT QUITE', 140, 760, 64),
		tag(w0(103, 'batteries'), s1(103), 'BATTERIES', 140, 180, 52),
		tag(w0(103, 'lights'), s1(103), 'LIGHTS', 140, 260, 52),
		tag(w0(103, 'motors'), s1(103), 'MOTORS', 140, 340, 52),
		tag(w0(103, 'arms'), s1(103), 'ARMS', 140, 420, 52),
		tag(w0(104, 'sinks'), s1(104), 'SINKS LIKE A STONE', 140, 760, 56, C.amber),
		tag(w0(105, 'foam'), s1(105) + 10, 'A SPECIAL FOAM', 140, 760, 56, C.amber),
		tag(w0(106, 'glass'), s1(106), 'HOLLOW GLASS BUBBLES', 140, 180, 56),
		tag(w0(107, 'titanium'), s1(107), 'TITANIUM · TAKES THE SQUEEZE', 140, 180, 52, C.ti),
		tag(w0(108, 'foam'), s1(108) + 10, 'FOAM · BRINGS THEM HOME', 140, 270, 52, C.amber),
		tag(w0(109, 'france'), s1(109), 'FROM FRANCE · ARRIVED LATE', 140, 180, 52),
		tag(w0(110, 'crack'), s1(110), 'A SMALL CRACK IN ITS COVER', 140, 270, 52, C.amber),
		tag(w0(111, 'five'), s1(111) + 10, '500 M TEST DIVE · HELD UP', 140, 360, 52),
		tag(w0(112, 'sixth'), s1(112), '06.11.2026', 140, 180, 56, C.ink, true, 'TRIALS NEAR CHENNAI · NO PEOPLE INSIDE'),
		tag(w0(113, 'twenty'), s1(113) + 20, '2027', 140, 180, 72, C.amber, true, 'OFFICIALS SAY: THE FULL 6 KM DIVE'),
	],
};

const ch6: Part = {
	shots: [
		hero(S(114), 'H1_dive', 0.4),
		hero(S(116), 'H3_seabed', 0),
		shot(S(120), 'basin', (d, l) => <Basin dur={d} area={w0(120, 'patch') - S(120) + l} since={w0(121, 'two') - S(120) + l} robot={w0(122, 'robot') - S(120) + l} lead={l} />),
		hero(S(123), 'H3_seabed', 11.6),
		hero(S(125), 'H3_descent', 0.0),
		hero(S(128), 'H1_dive', 5.0),
		shot(S(130), 'ladder', (d, l) => (
			<Plate dur={d} seed="ladder">
				<DepthLadder china={w0(131, 'deepest') - S(130) + l} six={w0(132, 'six') - S(130) + l} />
			</Plate>
		)),
	],
	overlays: [
		tag(w0(116, 'sunlight'), s1(116), 'NO SUNLIGHT', 140, 180, 56),
		tag(w0(117, 'lights'), s1(117), 'YOUR LIGHTS ONLY', 140, 180, 56, C.amber),
		tag(w0(118, 'freezing'), s1(118), 'NEAR FREEZING', 140, 760, 60, C.cyan, false, 'NOAA'),
		tag(w0(119, 'black'), s1(119) + 10, 'BLACK LUMPS OF METAL', 140, 760, 56),
		tag(w0(121, 'two'), s1(121) + 10, 'SINCE 2002', 140, 180, 60, C.amber, true),
		tag(w0(123, 'nickel'), s1(123) + 10, 'NICKEL · COPPER · COBALT', 140, 180, 56, C.amber),
		tag(w0(124, 'phone'), s1(124), 'IN YOUR PHONE’S BATTERY', 140, 270, 52),
		tag(w0(126, 'nobody'), s1(127), 'NO MINING YET', 140, 760, 64, C.amber),
		tag(w0(127, 'rules'), s1(127), 'THE RULES ARE STILL BEING WRITTEN', 140, 860, 44, C.dim),
		tag(w0(128, 'mining'), s1(128), 'NOT A MINING MACHINE', 140, 760, 56),
		tag(w0(129, 'eyes'), s1(129) + 20, 'A PAIR OF EYES', 140, 860, 64, C.cyan),
	],
};

const land: Part = {
	shots: [
		hero(S(133), 'H1_dark', 0),
		hero(S(138), 'H3_descent', 0),
		hero(S(141), 'H3_descent', 4.6),
		shot(s1(143) + 6, 'endcard', (d) => <EndCard dur={d} />, {hard: true}),
	],
	overlays: [
		tag(w0(135, 'not'), s1(135), 'NOT TO SEA WITH PEOPLE · YET', 140, 760, 52),
		tag(w0(136, 'public'), s1(136), 'NO PUBLIC REPORT OF A FULL-PRESSURE TEST', 140, 760, 48),
		tag(w0(138, 'one'), s1(138) + 6, 'ONE DIVE', 140, 180, 64, C.amber),
		tag(w0(139, 'six'), s1(139) + 6, '6 KM', 140, 270, 64, C.amber),
		tag(w0(140, 'every'), s1(140) + 10, 'EVERY NUMBER, CHECKED AT ONCE', 140, 360, 52),
		lab(pre(w0(143, 'subscribe')), Math.min(DURATION, s1(143) + 4), 'subscribe', <SubscribePill press={w0(143, 'subscribe') - pre(w0(143, 'subscribe'))} />),
	],
};

export const a3: Part = {
	shots: [...ch4.shots, ...ch5.shots, ...ch6.shots, ...land.shots],
	overlays: [...ch4.overlays, ...ch5.overlays, ...ch6.overlays, ...land.overlays],
};
export {clip};
