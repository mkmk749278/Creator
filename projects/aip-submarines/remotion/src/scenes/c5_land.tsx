import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {Battery} from '../parts/instruments';
import {Clip, Count, Credit, ez, Honesty, Label, Plate, tw, Underwater, useSpring} from '../parts/kit';
import {PatrolStrip, Silhouette} from '../parts/drawings';
import {TrapLoop} from '../parts/chain';
import {SeaMap, P} from '../parts/SeaMap';
import {SubUnderwater} from '../parts/Sub3D';
import {C, F} from '../theme';
import {s0, s1, w0} from '../timing';

// Chapter 5 · The way out (S154–168) and the landing (S169–183), word_map.md.
const pre = (f: number) => f - 9;
const VAG = 'INDIAN NAVY · INS VAGIR FILM';
const KHA = 'INS KHANDERI · FINANCIAL EXPRESS';

/** The boat slipping deeper into the dark, mast down: the landing image. */
const Deeper: React.FC<{dur: number}> = ({dur}) => {
	const f = useCurrentFrame();
	const k = tw(f, 0, dur, 0, 1);
	return (
		<AbsoluteFill>
			<Underwater depth={0.5 + 0.5 * k} />
			<SubUnderwater cam={[-10 + 25 * k + 6, 6 + 10 * k, 95]} look={[-10 + 25 * k, -4 * k, 0]} fov={34} x={-10 + 25 * k} depthTint={0.5 + 0.5 * k} />
		</AbsoluteFill>
	);
};

/** The next film: a depth gauge falling to 6,000 m and a titanium sphere drawn on the plate; then the end card. */
const NextFilm: React.FC<{dur: number; depth: number; sphere: number; card: number}> = ({dur, depth, sphere, card}) => {
	const f = useCurrentFrame();
	const sp = tw(f, sphere, sphere + 40, 0, 1, ez.sweep);
	const cd = tw(f, card, card + 30, 0, 1, ez.arrive);
	const logo = useSpring(card + 10);
	return (
		<AbsoluteFill>
			<Plate dur={dur} seed="next">
				<svg width={1920} height={1080} style={{position: 'absolute', opacity: 1 - cd}}>
					<circle cx={1300} cy={520} r={230} fill="none" stroke="#c9ced6" strokeWidth={10} pathLength={1} strokeDasharray={`${sp} 1`} />
					<circle cx={1300} cy={520} r={190} fill="rgba(201,206,214,0.08)" opacity={sp} />
					<circle cx={1240} cy={470} r={34} fill="none" stroke={C.cyan} strokeWidth={6} opacity={sp} />
				</svg>
				<div style={{opacity: 1 - cd}}>
					<Count a={depth} b={depth + 70} from={0} to={6000} x={200} y={380} size={150} unit="M DOWN" color={C.cyan} />
					<Label at={sphere} text="A TITANIUM SPHERE" x={1300} y={800} size={50} align="center" />
				</div>
			</Plate>
			{cd > 0 ? (
				<AbsoluteFill style={{background: `rgba(3,7,13,${0.92 * cd})`, alignItems: 'center', justifyContent: 'center'}}>
					<Img src={staticFile('brand/logo_square.png')} style={{width: 420, height: 420, opacity: logo, transform: `scale(${0.9 + 0.1 * logo})`, borderRadius: 24}} />
				</AbsoluteFill>
			) : null}
		</AbsoluteFill>
	);
};

export const ch5: Part = (() => {
	const shots: Part['shots'] = [];
	const overlays: Part['overlays'] = [];
	const add = (at: number, name: string, el: (d: number) => React.ReactNode, hard = false) => shots.push({at, name, el, hard});
	const over = (from: number, to: number, name: string, el: React.ReactNode) => overlays.push({from, to, name, el});

	// S154–156: how would you break the trap? one submarine: INS Khanderi (as reported, C12)
	const c154 = pre(s0(154));
	add(c154, 'trap again', (d) => (
		<Plate dur={d} seed="trap2">
			<TrapLoop both={-60} navy={-60} engine={-60} close={-60} lock={-60} />
		</Plate>
	));
	over(pre(w0(155, 'one')), pre(s0(156)), 'one sub', <Label at={0} text="START WITH ONE SUBMARINE" x={960} y={170} size={56} align="center" color={C.green} />);
	const c156 = pre(s0(156));
	add(c156, 'KHA bow', (d) => <Clip name="KHA_bow" dur={d} grade="day" />);
	over(pre(w0(156, 'I-N-S')), pre(s0(157)), 'khanderi', <Label at={0} text="INS KHANDERI" sub="AS REPORTED" x={170} y={190} size={72} />);
	over(c156, pre(s0(157)), 'credit kha', <Credit text={KHA} />);

	// S157–164: Hazira (Oct 2026), the Navy's tests, Mazagon Dock (early 2027), fitting mid-2027; who builds it
	const c157 = pre(s0(157));
	add(c157, 'map west coast', (d) => (
		<SeaMap
			dur={d}
			keys={[
				{f: 0, lon: 71.8, lat: 20.6, zoom: 6},
				{f: w0(159, 'Mazagon') - c157, lon: 71.6, lat: 20.1, zoom: 6.6},
				{f: w0(161, 'Ambernath') - c157, lon: 71.7, lat: 20.0, zoom: 7.0},
				{f: d, lon: 71.7, lat: 20.0, zoom: 7.3},
			]}
			pins={[
				{at: w0(157, 'Hazira') - c157, ll: P.hazira, label: 'HAZIRA', sub: "L&T'S YARD · GUJARAT"},
				{at: w0(159, 'Mazagon') - c157, ll: P.mumbai, label: 'MAZAGON DOCK', sub: 'MUMBAI', side: 'left'},
				{at: w0(161, 'Ambernath') - c157, ll: P.ambernath, label: 'AMBERNATH', sub: 'DRDO LAB · NMRL', color: C.cyan},
			]}
			routes={[{a: w0(159, 'goes') - c157, b: w0(159, 'Dock') - c157 + 20, from: P.hazira, to: P.mumbai, color: C.amber}]}
		/>
	));
	over(pre(w0(157, 'October')), pre(s0(158)), 'oct', <Label at={0} text="OCT 2026" sub="THE NEXT ROUND OF TESTS" x={120} y={230} size={64} mono />);
	over(pre(w0(158, 'powered')), pre(s0(159)), 'navy rules', <Label at={0} text="TESTED TO THE NAVY'S RULES" x={120} y={230} size={52} color={C.cyan} />);
	over(pre(w0(159, 'Early')), pre(s0(160)), 'early 27', <Label at={0} text="EARLY 2027" x={120} y={230} size={64} mono />);
	over(pre(w0(160, 'middle')), pre(s0(161)), 'mid 27', <Label at={0} text="FITTING: MID-2027" sub="THEN SEA TRIALS" x={120} y={230} size={60} mono color={C.green} />);
	over(pre(w0(162, 'Built')), pre(s0(163)), 'built lt', <Label at={0} text="BUILT BY L&T" x={120} y={230} size={56} color={C.amber} />);
	over(pre(w0(163, 'Fitted')), pre(s0(164)), 'fitted mdl', <Label at={0} text="FITTED BY MAZAGON DOCK" x={120} y={230} size={56} />);

	const c164 = pre(s0(164));
	add(c164, 'six boats', (d) => (
		<Plate dur={d} seed="six2">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{Array.from({length: 6}).map((_, i) => (
					<Silhouette key={i} x={220 + (i % 3) * 520} y={440 + Math.floor(i / 3) * 190} px={6} len={i === 0 ? 77.5 : 67.5} color={i === 0 ? C.amber : C.dim} at={w0(164, 'six') - c164 + i * 4} />
				))}
			</svg>
		</Plate>
	));
	over(pre(w0(164, 'six')), pre(s0(165)), 'all six', <Label at={0} text="ALL SIX KALVARI BOATS" sub="ONE REFIT AT A TIME · PLANNED" x={960} y={170} size={56} align="center" />);
	over(c164, pre(s0(165)), 'illus', <Honesty text="ILLUSTRATION" />);

	// S165–168: the sea is not waiting: China's Yuan class; Pakistan's Hangor (commissioned 30 Apr 2026, C16, C31)
	const c165 = pre(s0(165));
	add(c165, 'region map', (d) => (
		<SeaMap
			dur={d}
			dimIndia
			keys={[
				{f: 0, lon: 84, lat: 20, zoom: 0.9},
				{f: d, lon: 84.5, lat: 20.5, zoom: 0.96},
			]}
			pins={[
				{at: w0(167, 'Yuan') - c165, ll: [108, 26.5], label: "CHINA'S YUAN CLASS", sub: 'HAS AIP', color: C.ink, side: 'left'},
				{at: w0(168, 'Pakistan') - c165, ll: P.karachi, label: 'PAKISTAN · HANGOR CLASS', sub: 'APR 2026 · AIP, ITS NAVY SAYS', color: C.ink},
			]}
		/>
	));
	over(pre(w0(166, 'No')), pre(s0(167)), 'no wait', <Label at={0} text="THE SEA ISN'T WAITING" x={960} y={170} size={56} align="center" />);

	// S169–172: one boat, one set of trials; proven at sea; the trap opens
	const c169 = pre(s0(169));
	add(c169, 'KHA end', (d) => <Clip name="KHA_end" dur={d} grade="day" from={[1.0, 0, 0]} to={[1.12, 0, 0]} />);
	over(pre(w0(169, 'one')), pre(s0(170)), 'one boat', <Label at={0} text="ONE BOAT · ONE SET OF TRIALS" x={170} y={190} size={52} />);
	over(c169, pre(s0(171)), 'credit kha2', <Credit text={KHA} />);
	over(pre(w0(171, 'proven')), pre(s0(172)), 'proven', <Label at={0} text="✓ PROVEN AT SEA" x={960} y={480} size={84} align="center" color={C.green} />);
	const c172 = pre(s0(172));
	add(c172, 'trap opens', (d) => (
		<Plate dur={d} seed="open">
			<TrapLoop both={-60} navy={-60} engine={-60} close={-60} lock={-60} open={w0(172, 'opens') - c172} />
		</Plate>
	));
	over(pre(w0(172, 'every')), pre(s0(173)), 'every boat', <Label at={0} text="FOR EVERY BOAT AFTER IT" x={960} y={850 - 70} size={52} align="center" color={C.green} />);

	// S173–178: back to the night; the battery is low; the mast stays down; the boat slips deeper
	add(pre(s0(173)), 'H1a night again', (d) => <Clip name="H1a" dur={d} startAt={1} grade="none" />);
	add(pre(s0(174)), 'VAG ctrl again', (d) => <Clip name="VAG_consoles" dur={d} startAt={5} grade="red" />);
	over(pre(s0(174)), pre(s0(177)), 'credit vag', <Credit text={VAG} />);
	over(pre(w0(175, 'battery')), pre(s0(177)), 'bat low', <Battery x={1240} y={180} a={0} b={30} from={0.15} to={0.12} />);
	const c177 = pre(s0(177));
	add(c177, 'H1c mast stays down', (d) => <Clip name="H1c" dur={d} grade="none" />, true);
	over(c177, pre(s0(178)), 'strip last', (
		<PatrolStrip x={360} y={150} w={1200} draw={-60} marks={[0.5]} markAt={-60} markW={60} goneAt={w0(177, 'stays') - c177} label="" />
	));
	add(pre(s0(178)), 'deeper', (d) => <Deeper dur={d} />);
	over(c177, pre(s0(179)), 'recon', <Honesty text="RECONSTRUCTION" />);

	// S179–181: only a hope; if they fail, the trap closes again; the coming year
	const c179 = pre(s0(179));
	add(c179, 'IF', (d) => <Deeper dur={d} />);
	over(pre(w0(179, 'hope')), pre(s0(180)), 'if', <Label at={0} text="IF" x={960} y={420} size={160} align="center" color={C.amber} />);
	const c180 = pre(s0(180));
	add(c180, 'trap closes', (d) => (
		<Plate dur={d} seed="close">
			<TrapLoop both={-60} navy={-60} engine={-60} close={-60} open={-60} reclose={w0(180, 'closes') - c180} />
		</Plate>
	));
	over(pre(w0(181, 'coming')), pre(s0(182)), '2027', <Label at={0} text="THE NEXT 12 MONTHS" x={960} y={170} size={64} align="center" color={C.amber} />);

	// S182–183: next film, end card (the only logo)
	const c182 = pre(s0(182));
	add(c182, 'next film', (d) => <NextFilm dur={d} depth={w0(183, 'Six') - c182} sphere={w0(183, 'titanium') - c182} card={s1(183) - c182 + 12} />);
	return {shots, overlays};
})();

export {F};
