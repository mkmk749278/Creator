import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {DepthLadder, FoamCrack, Microspheres} from '../parts/drawings';
import {ez, MarineSnow, Photo, Plate, tw, useSpring} from '../parts/kit';
import {P, SeaMap} from '../parts/SeaMap';
import {C, F} from '../theme';
import {DURATION, s0, s1, w0} from '../timing';
import {clip, cnt, CR, Deep, hero, insert, lab, Label, photo, pre, shot, tag} from './common';

// Narration v3: inside and the aquanauts (S103–116), the foam and the delay (S117–133), the seabed (S134–162),
// the landing (S163–175) and the outro (S176–182).
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
				<Img src={staticFile('brand/logo_square.png')} style={{width: 420, height: 420, opacity: logo, transform: `scale(${(0.9 + 0.1 * logo) * (1 + 0.08 * tw(f, 0, dur, 0, 1, (t) => t))})`, borderRadius: 24}} />
			</AbsoluteFill>
		</AbsoluteFill>
	);
};

/** S116: the last daylight fading out above the seabed's dark, with snow drifting past (r1: 3.5 s of plain black) */
const Abyss: React.FC = () => {
	const f = useCurrentFrame();
	const sun = tw(f, 0, 150, 0.32, 0, (t) => t);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<AbsoluteFill style={{background: `linear-gradient(180deg, rgba(60,130,175,${sun}) 0%, rgba(7,33,53,${sun * 0.6}) 45%, rgba(0,0,0,0) 100%)`}} />
			<MarineSnow speed={2.2} n={200} />
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
		hero(S(103), 'H1_cutaway', 0),
		photo(S(109), 'ifr_nautile_surface.jpg', CR.ifr),
		insert(S(110), 'F06_nautile', CR.osn, 1),
		photo(S(111), 'ifr_nautile_inside.jpg', CR.ifr),
		photo(S(112), 'ifr_nautile_recovery.jpg', CR.ifr),
		insert(S(113), 'F06_nautile', CR.osn, 1, 8.0),
		shot(S(114), 'nautile-theirs', (d) => <Photo src="ifr_nautile_surface.jpg" dur={d} from={[1.18, 30, 0]} to={[1.04, -20, 0]} />, {credit: CR.ifr}),
	],
	overlays: [
		tag(w0(104, 'eight'), s1(104), '80 MM WALL', 140, 180, 56, C.ti),
		tag(w0(104, 'two'), s1(105), 'JUST OVER 2 M INSIDE', 140, 270, 56, C.amber, false, 'OUR CALCULATION: 2,260 − 2 × 80 MM'),
		tag(w0(106, 'two'), s1(106), '3 PEOPLE', 140, 180, 56),
		tag(w0(106, 'twelve'), s1(106) + 10, '12 HOURS A DIVE', 140, 270, 56, C.cyan),
		lab(S(107), s1(108), 'breath', <Breath co2={w0(108, 'carbon') - S(107)} />),
		tag(w0(107, 'oxygen'), s1(108), 'OXYGEN IN', 140, 180, 56, C.cyan),
		tag(w0(108, 'carbon'), s1(108), 'CO₂ CLEANED AWAY', 1100, 180, 56, C.dim),
		tag(w0(109, 'two'), s1(109), 'TWO INDIANS · ALREADY DOWN', 140, 760, 52),
		tag(w0(110, 'august'), s1(110), 'AUGUST 2025', 140, 180, 48, C.dim, true),
		tag(w0(110, 'french'), s1(110), 'FRANCE · NAUTILE', 140, 270, 56),
		tag(w0(111, 'raju'), s1(111) + 10, 'RAJU RAMESH', 140, 760, 56, C.ink, false, 'SCIENTIST · ABOUT 4,025 M'),
		tag(w0(112, 'commander'), s1(112) + 10, 'CDR JATINDER PAL SINGH (RETD)', 140, 760, 52, C.ink, false, 'ABOUT 5,002 M'),
		cnt(w0(113, 'seven'), w0(113, 'hours'), s1(113) + 6, 7, 'HOURS EACH', 140, 180, 110, C.cyan),
		tag(w0(116, 'someone'), s1(116) + 10, 'SOMEONE ELSE’S SUB', 140, 760, 60, C.amber, false, 'FRANCE’S NAUTILE'),
	],
};

const ch5: Part = {
	shots: [
		clip(S(117), 'F08_ball', CR.tn),
		hero(S(120), 'H3_assemble', 0),
		shot(pre(w0(123, 'tiny')), 'microspheres', () => <Microspheres />, {tag: 'ILLUSTRATION'}),
		photo(S(124), 'pib_dom_foam.png', CR.pib),
		clip(S(126), 'ISRO_bead', CR.isro, 0.6),
		shot(S(127), 'foamblock', (d) => (
			<Plate dur={d} seed="foamblock">
				<FoamCrack dur={d} crack={1e6} slide />
			</Plate>
		), {tag: 'ILLUSTRATION'}),
		shot(S(128), 'foamcrack', (d, l) => (
			<Plate dur={d} seed="foamcrack" from={[1.3, 0, 40]} to={[1.42, -30, 40]}>
				<FoamCrack dur={d} crack={w0(128, 'crack') - S(128) + l} />
			</Plate>
		), {tag: 'ILLUSTRATION'}),
		clip(S(129), 'PX_storm', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		photo(S(131), 'pib_wet_foam.jpg', CR.pib, 'contain'),
		photo(S(132), 'pib_wet_crane.jpg', CR.pib, 'contain'),
		shot(pre(w0(132, 'chennai')), 'chennai', (d, l) => (
			<SeaMap
				dur={d}
				keys={[
					{f: 0, lon: 81.5, lat: 13.5, zoom: 2.2},
					{f: d, lon: 80.8, lat: 13.2, zoom: 2.8},
				]}
				pins={[{at: l + 9, ll: P.chennai, label: 'CHENNAI', side: 'right'}]}
			/>
		)),
		insert(pre(w0(133, 'six')), 'F03_water', CR.ddt),
	],
	overlays: [
		tag(w0(118, 'not'), s1(119), 'NOT YET', 140, 760, 64),
		tag(w0(121, 'batteries'), s1(121), 'BATTERIES', 140, 180, 52),
		tag(w0(121, 'lights'), s1(121), 'LIGHTS', 140, 260, 52),
		tag(w0(121, 'motors'), s1(121), 'MOTORS', 140, 340, 52),
		tag(w0(121, 'arms'), s1(121), 'ARMS', 140, 420, 52),
		tag(w0(122, 'sinks'), s1(122), 'SINKS LIKE A STONE', 140, 760, 56, C.amber),
		tag(w0(123, 'foam'), pre(w0(123, 'tiny')), 'A SPECIAL FOAM', 140, 760, 56, C.amber),
		tag(w0(123, 'glass'), s1(123), 'HOLLOW GLASS BUBBLES', 140, 180, 56),
		tag(w0(124, 'titanium'), s1(125) + 10, 'TITANIUM · TAKES THE SQUEEZE', 140, 180, 52, C.ti),
		tag(w0(125, 'foam'), s1(125) + 10, 'FOAM · BRINGS YOU HOME', 140, 270, 52, C.amber),
		tag(w0(126, 'welded'), s1(126), 'THE BALL · WELDED IN INDIA', 140, 760, 52, C.green),
		tag(w0(127, 'france'), s1(127), 'THE FOAM · FROM FRANCE · LATE', 140, 180, 52),
		tag(w0(128, 'crack'), s1(128), 'A SMALL CRACK IN ITS COVER', 140, 270, 52, C.amber),
		tag(w0(130, 'monsoon'), s1(130) + 10, 'NO TEST IN THE MONSOON', 140, 760, 56, C.cyan, false, 'A MINISTRY OFFICIAL, 2026'),
		tag(w0(131, 'five'), s1(131) + 10, '500 M TEST DIVE · HAD TO WAIT', 140, 180, 52),
		tag(w0(132, 'sixth'), s1(132), '06.11.2026', 140, 180, 56, C.ink, true, 'TRIALS NEAR CHENNAI · NO PEOPLE INSIDE'),
		tag(w0(133, 'twenty'), s1(133) + 10, '2027', 140, 180, 72, C.amber, true, 'OFFICIALS SAY: THE FULL 6 KM DIVE'),
	],
};

const ch6: Part = {
	shots: [
		hero(S(134), 'H1_dive', 0.4),
		clip(S(135), 'PX_phone', CR.px),
		hero(S(137), 'H3_descent', 0),
		// real deep water (NOAA, public domain), then our seabed from 'Outside your window'
		clip(S(138), 'NOAA_dark', CR.noaa, 0, 'ILLUSTRATIVE FOOTAGE'),
		clip(S(139), 'NOAA_lights', CR.noaa, 0, 'ILLUSTRATIVE FOOTAGE'),
		hero(S(140), 'H3_seabed', 7.5),
		photo(pre(w0(141, 'seafloor')), 'geomar_nodules_wide.jpg', CR.geomar),
		photo(S(142), 'geomar_nodules_top.jpg', CR.geomar),
		shot(S(144), 'basin', (d, l) => <Basin dur={d} area={w0(144, 'patch') - S(144) + l} since={w0(144, 'two') - S(144) + l} robot={w0(145, 'robot') - S(144) + l} lead={l} />),
		clip(S(146), 'PX_churn', CR.px, 0, 'ILLUSTRATIVE FOOTAGE'),
		photo(S(149), 'pib_dom_crane.png', CR.pib),
		hero(S(150), 'H3_descent', 0.0),
		hero(S(153), 'H1_dive', 5.0),
		shot(S(155), 'ladder', (d, l) => (
			<Plate dur={d} seed="ladder">
				<DepthLadder china={w0(156, 'deepest') - S(155) + l} six={w0(158, 'six') - S(155) + l} />
			</Plate>
		)),
		clip(S(159), 'ISRO_hall', CR.isro),
		clip(S(160), 'ISRO_ansys', CR.isro),
		clip(S(161), 'ISRO_bead', CR.isro),
		clip(S(162), 'ISRO_console', CR.isro),
	],
	overlays: [
		tag(w0(136, 'cobalt'), s1(136), 'COBALT', 140, 180, 56, C.amber),
		tag(w0(136, 'nickel'), s1(136), 'NICKEL', 140, 270, 56, C.amber),
		cnt(w0(137, 'six'), w0(137, 'metres'), S(138), 6000, 'M', 140, 300, 120, C.ink),
		tag(w0(138, 'sunlight'), s1(138), 'NO SUNLIGHT', 140, 180, 56),
		tag(w0(139, 'lights'), s1(139), 'YOUR LIGHTS ONLY', 140, 180, 56, C.amber),
		tag(w0(140, 'freezing'), s1(140), 'NEAR FREEZING', 140, 760, 60, C.cyan, false, 'NOAA'),
		tag(w0(141, 'black'), s1(141) + 10, 'BLACK LUMPS', 140, 760, 56),
		tag(pre(w0(141, 'seafloor')) + 12, S(142), 'REAL NODULES · PACIFIC SEAFLOOR', 140, 860, 40, C.dim),
		tag(S(142) + 12, S(144), 'REAL NODULES · PACIFIC SEAFLOOR', 140, 860, 40, C.dim),
		tag(w0(143, 'nickel'), s1(143) + 10, 'NICKEL · COPPER · COBALT', 140, 180, 56, C.amber),
		tag(w0(144, 'two'), s1(144) + 10, 'SINCE 2002', 140, 180, 60, C.amber, true),
		tag(w0(146, 'independence'), s1(146), '15 AUG 2025 · THE PRIME MINISTER', 140, 180, 48, C.dim, true),
		tag(w0(147, 'samudra'), s1(148) + 10, 'SAMUDRA MANTHAN', 140, 700, 96, C.amber, false, 'THE CHURNING OF THE OCEAN'),
		tag(w0(149, 'four'), s1(149) + 10, '₹4,077 CRORE', 140, 700, 96, C.amber, true, 'DEEP OCEAN MISSION · SOURCE: PIB'),
		tag(w0(151, 'nobody'), s1(152), 'NO MINING YET', 140, 760, 64, C.amber),
		tag(w0(152, 'rules'), s1(152), 'THE RULES ARE STILL BEING WRITTEN', 140, 860, 44, C.dim),
		tag(w0(153, 'mining'), s1(153), 'NOT A MINING MACHINE', 140, 760, 56),
		tag(w0(154, 'eyes'), s1(154) + 10, 'A PAIR OF EYES', 140, 860, 64, C.cyan),
		tag(w0(157, 'behind'), s1(157), 'YES, INDIA IS BEHIND', 140, 900, 52, C.ink),
		tag(w0(159, 'how'), s1(159), 'BUT LOOK HOW', 140, 760, 56, C.green),
		tag(w0(160, 'designed'), s1(160), 'ISRO DESIGNED IT', 140, 760, 60, C.green),
		tag(w0(161, 'welded'), s1(161), 'ISRO WELDED IT', 140, 760, 60, C.green),
		cnt(w0(162, 'made'), w0(162, 'stronger'), s1(162) + 6, 40, 'KW', 140, 200, 110, C.amber, 15),
	],
};

const land: Part = {
	shots: [
		hero(S(163), 'H1_cutaway', 10.0),
		hero(S(164), 'H1_dive', 8.0),
		hero(S(166), 'H4_squeeze', 3.0, 'SIMPLIFIED'),
		hero(S(167), 'H1_dive', 0),
		hero(S(171), 'H2_seam', 0),
		clip(S(173), 'F01_crane', CR.dd),
		photo(S(174), 'pib_wet_foam.jpg', CR.pib, 'contain'),
		hero(S(175), 'H3_descent', 4.6),
		hero(S(176), 'H3_descent', 0),
		shot(S(181), 'endcard', (d) => <EndCard dur={d} />, {hard: true}),
	],
	overlays: [
		tag(w0(165, 'not'), s1(165), 'NOT TO SEA WITH PEOPLE · YET', 140, 760, 52),
		tag(w0(166, 'public'), s1(166), 'NO PUBLIC REPORT OF A FULL-PRESSURE TEST', 140, 760, 48),
		tag(w0(168, 'one'), s1(170) + 6, 'ONE DIVE', 140, 180, 64, C.amber),
		tag(w0(169, 'six'), s1(170) + 6, '6 KM', 140, 270, 64, C.amber),
		tag(w0(170, 'three'), s1(170) + 6, '3 INDIANS · 7 WELDS', 140, 360, 64, C.weld),
		tag(w0(171, 'only'), s1(171) + 10, 'ONLY AS STRONG AS ITS WEAKEST WELD', 140, 760, 56, C.weld),
		tag(w0(172, 'seven'), s1(172) + 6, '700 TRIES · NOT TOO MANY', 140, 860, 52, C.amber),
		tag(w0(174, 'test'), s1(174) + 6, 'WATCH FOR · THE 500 M TEST DIVE', 140, 760, 52, C.cyan),
		tag(w0(175, 'big'), s1(175) + 6, 'THEN · THE 6 KM DIVE', 140, 760, 56, C.amber),
		lab(pre(w0(177, 'subscribe')), S(179), 'subscribe', <SubscribePill press={w0(177, 'subscribe') - pre(w0(177, 'subscribe'))} />),
		lab(w0(179, 'is'), S(181), 'question', <Label at={0} text="IS THE DEEP SEA WORTH THIS EFFORT?" x={960} y={700} size={60} align="center" color={C.ink} sub="TELL ME IN THE COMMENTS" />),
		lab(w0(181, 'be'), Math.min(DURATION, s1(182) + 200), 'name', <Label at={0} text="BE PRACTICAL WITH KISHORE" x={960} y={820} size={56} align="center" color={C.ink} />),
		lab(w0(182, 'stay'), Math.min(DURATION, s1(182) + 200), 'stay', <Label at={0} text="STAY PRACTICAL" x={960} y={920} size={48} align="center" color={C.amber} />),
	],
};

export const a3: Part = {
	shots: [...ch4.shots, ...ch5.shots, ...ch6.shots, ...land.shots],
	overlays: [...ch4.overlays, ...ch5.overlays, ...ch6.overlays, ...land.overlays],
};
export {clip};
