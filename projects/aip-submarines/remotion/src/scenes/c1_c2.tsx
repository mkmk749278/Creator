import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {Battery, Ping, RedRing} from '../parts/instruments';
import {Clip, Count, Credit, ez, Honesty, Label, Plate, tw, Underwater} from '../parts/kit';
import {PatrolStrip, Silhouette} from '../parts/drawings';
import {AcousticLine, Cutaway, RadarScope, SeaFromAbove, SpeedDial, ThreeMachines, VerticalClip} from '../parts/schematics';
import {SubUnderwater} from '../parts/Sub3D';
import {SeaMap, P} from '../parts/SeaMap';
import {ProfileShot} from './c0_open';
import {C, F} from '../theme';
import {s0, w0} from '../timing';

// Chapter 1 · Caught breathing (S29–55) and Chapter 2 · The ghost myth (S56–78), word_map.md.
const pre = (f: number) => f - 9;
const VAG = 'INDIAN NAVY · INS VAGIR FILM';
const P8 = 'INDIAN NAVY · P-8I';

/** The patrol strip on the plate: the film's motif. */
const StripShot: React.FC<{dur: number; strip: React.ComponentProps<typeof PatrolStrip>; extra?: React.ReactNode}> = ({dur, strip, extra}) => (
	<Plate dur={dur} seed={'strip' + strip.markAt}>
		<PatrolStrip {...strip} />
		{extra}
	</Plate>
);

/** Under water, the boat; a sonar ping finds it. */
const SonarShot: React.FC<{dur: number; ping: number}> = ({dur, ping}) => {
	const f = useCurrentFrame();
	const k = tw(f, 0, dur, 0, 1);
	return (
		<AbsoluteFill>
			<Underwater depth={0.5} />
			<SubUnderwater cam={[10 - 20 * k, -4, 110]} look={[0, 0, 0]} fov={36} depthTint={0.5} />
			<Ping x={1700} y={300} start={ping} max={1500} />
		</AbsoluteFill>
	);
};

const MARKS = [0.07, 0.21, 0.36, 0.5, 0.64, 0.79, 0.93];

export const ch12: Part = (() => {
	const shots: Part['shots'] = [];
	const overlays: Part['overlays'] = [];
	const add = (at: number, name: string, el: (d: number) => React.ReactNode, hard = false) => shots.push({at, name, el, hard});
	const over = (from: number, to: number, name: string, el: React.ReactNode) => overlays.push({from, to, name, el});

	// S29–32: the hunter. P-8I real footage (vertical source in its frame).
	add(pre(s0(29)), 'P8I ramp', (d) => <VerticalClip name="P8I_ramp" dur={d} />);
	add(pre(w0(30, 'switch')), 'P8I takeoff', (d) => <VerticalClip name="P8I_takeoff" dur={d} />, true);
	add(pre(s0(32)), 'P8I flight', (d) => <VerticalClip name="P8I_flight" dur={d} />);
	add(pre(w0(32, 'hours')), 'P8I sea', (d) => <VerticalClip name="P8I_sea" dur={d} />);
	over(pre(s0(29)), pre(s0(33)), 'credit p8', <Credit text={P8} />);
	over(pre(w0(31, 'hunter')), pre(s0(32)), 'hunter', <Label at={0} text="THE HUNTER" x={1380} y={300} size={60} color={C.red} />);
	over(pre(w0(32, 'P-Eight-I')), pre(s0(33)), 'p8i label', <Label at={0} text="P-8I" sub="INDIAN NAVY · SUB HUNTER" x={1380} y={300} size={72} />);
	over(pre(w0(32, 'hours')), pre(s0(33)), 'hours', <Label at={0} text="HOURS OUT AT SEA" x={1380} y={560} size={48} color={C.cyan} />);

	// S33–38: what it looks for
	add(pre(s0(33)), 'sea above', (d) => <SeaFromAbove dur={d} cross={w0(33, 'submarine') - pre(s0(33))} fade={w0(34, 'leaves') - pre(s0(33))} />);
	add(pre(w0(35, 'mast')), 'TRI masts', (d) => <Clip name="TRI_masts" dur={d} from={[1.5, -200, 60]} to={[1.6, -230, 60]} grade="day" />, true);
	add(pre(s0(36)), 'TRI wake', (d) => <Clip name="TRI_wake" dur={d} from={[1.05, 0, 0]} to={[1.12, 0, 0]} grade="day" />, true);
	over(pre(s0(36)), pre(s0(37)), 'credit tri', <Credit text="INS KALVARI SEA TRIALS" />);
	over(pre(w0(35, 'mast')), pre(s0(36)), 'mast lab', <Label at={0} text="A MAST" x={1240} y={260} size={60} />);
	over(pre(w0(36, 'wake')), pre(s0(37)), 'wake lab', <Label at={0} text="A WAKE" x={1240} y={260} size={60} />);
	add(pre(s0(37)), 'radar scope', (d) => <RadarScope dot={w0(37, 'dot') - pre(s0(37))} />, true);
	over(pre(w0(37, 'dot')), pre(s0(38)), 'radar lab', <Label at={0} text="A DOT ON RADAR" x={1240} y={170} size={52} />);
	add(pre(s0(38)), 'acoustic', (d) => <AcousticLine spike={w0(38, 'diesel') - pre(s0(38))} />, true);
	over(pre(w0(38, 'diesel')), pre(s0(39)), 'noise lab', <Label at={0} text="DIESEL NOISE" x={960} y={170} size={60} align="center" color={C.cyan} />);

	// S39–41: back inside
	add(pre(s0(39)), 'VAG valves', (d) => <Clip name="VAG_valves" dur={d} grade="day" />, true);
	over(pre(s0(39)), pre(s0(42)), 'credit vag', <Credit text={VAG} />);
	add(pre(w0(41, 'raise')), 'VAG surf mast', (d) => <Clip name="VAG_surf" dur={d} startAt={6} grade="night" />);

	// S42–45: everything runs on one battery (cutaway, SIMPLIFIED)
	const c42 = pre(s0(42));
	add(c42, 'cutaway', (d) => (
		<Plate dur={d} seed="cut" from={[1.0, 0, 0]} to={[1.06, 0, 0]}>
			<Cutaway
				dur={d}
				lit={{
					battery: w0(42, 'battery') - c42,
					motor: w0(43, 'motor') - c42,
					lights: w0(43, 'lights') - c42,
					air: w0(43, 'air') - c42,
					computers: w0(43, 'computers') - c42,
					diesels: w0(44, 'engines') - c42,
				}}
				airAt={w0(44, 'need') - c42}
				cutAirAt={w0(45, 'none') - c42}
			/>
		</Plate>
	));
	over(c42, pre(s0(46)), 'simpl', <Honesty text="SIMPLIFIED · ILLUSTRATION" />);
	over(pre(w0(44, 'need')), pre(s0(46)), 'needs air', <Label at={0} text="NEED AIR" x={1180} y={170} size={56} color={C.frost} />);

	// S46–49: how long? a few days; the makers say about four, at a crawl
	const c46 = pre(s0(46));
	add(c46, 'battery days', (d) => (
		<Plate dur={d} seed="days">
			<Battery x={170} y={330} a={w0(47, 'few') - c46} b={w0(48, 'four') - c46} from={1} to={0.15} scale={1.3} />
			<Count a={w0(47, 'few') - c46} b={w0(48, 'four') - c46} from={0} to={4} x={1000} y={300} size={170} unit="DAYS" color={C.ink} />
			<SpeedDial x={1450} y={760} keys={[[0, 0.06]]} at={w0(48, 'crawl') - c46 - 6} />
		</Plate>
	));
	over(pre(w0(48, 'Kalvari')), pre(s0(49)), 'kalvari lab', <Label at={0} text="KALVARI CLASS" sub="THE MAKERS SAY ABOUT 4 DAYS" x={170} y={640} size={56} />);
	over(pre(w0(48, 'crawl')), pre(s0(49)), 'crawl', <Label at={0} text="AT A CRAWL" x={1060} y={500} size={52} color={C.green} />);
	add(pre(s0(49)), 'TRI side', (d) => <Clip name="TRI_side" dur={d} from={[1.0, 0, 0]} to={[1.12, 0, 0]} grade="day" />);
	add(pre(w0(49, 'raise')), 'VAG surfacing', (d) => <Clip name="VAG_surf" dur={d} startAt={2} grade="night" />);
	over(pre(s0(49)), pre(s0(50)), 'credit 49', <Credit text="INS KALVARI SEA TRIALS · INDIAN NAVY" />);
	over(pre(w0(49, 'hours')), pre(s0(50)), 'hours lab', <Label at={0} text="FOR HOURS" x={1300} y={240} size={60} color={C.red} />);

	// S50–55: the patrol strip (motif)
	const c50 = pre(s0(50));
	add(c50, 'strip', (d) => (
		<StripShot
			dur={d}
			strip={{x: 260, y: 420, w: 1400, draw: w0(50, 'strip') - c50, marks: MARKS, markAt: w0(51, 'red') - c50, days: 28, label: 'YOUR PATROL · 4 WEEKS', fewerAt: w0(54, 'Fewer') - c50, shrinkAt: w0(55, 'Shorter') - c50}}
			extra={<StripSenses c={c50} />}
		/>
	));
	over(pre(w0(54, 'Fewer')), pre(s0(55)), 'fewer', <Label at={0} text="FEWER" x={960} y={700} size={72} align="center" color={C.green} />);
	over(pre(w0(55, 'Shorter')), pre(s0(56)), 'shorter', <Label at={0} text="SHORTER" x={960} y={700} size={72} align="center" color={C.green} />);
	over(c50, pre(s0(56)), 'strip illus', <Honesty text="ILLUSTRATION" />);

	// S56–57: AIP, a second engine that needs no outside air
	const c56 = pre(s0(56));
	add(c56, 'profile aip', (d) => <ProfileShot dur={d} plugAt={w0(57, 'second') - c56} />);
	over(pre(w0(57, 'second')), pre(s0(58)), 'second eng', <Label at={0} text="A SECOND ENGINE" x={960} y={220} size={64} align="center" color={C.amber} />);
	over(pre(w0(57, 'air')), pre(s0(58)), 'no air', <Label at={0} text="NO OUTSIDE AIR" x={960} y={760} size={52} align="center" color={C.frost} />);

	// S58–60: three kinds; India chose the fuel cell
	const c58 = pre(s0(58));
	add(c58, 'three machines', (d) => (
		<Plate dur={d} seed="three">
			<ThreeMachines at={[w0(59, 'Stirling') - c58, w0(59, 'steam') - c58, w0(59, 'fuel') - c58]} keep={w0(60, 'chose') - c58} />
		</Plate>
	));
	over(pre(w0(60, 'India')), pre(s0(61)), 'india chose', <Label at={0} text="INDIA'S CHOICE" x={1560} y={190} size={52} align="center" color={C.cyan} />);
	over(c58, pre(s0(61)), 'illus58', <Honesty text="ILLUSTRATION" />);

	// S61–63: four days becomes two weeks (DRDO's land-trial figure)
	const c61 = pre(s0(61));
	add(c61, 'strip aip', (d) => (
		<StripShot
			dur={d}
			strip={{x: 260, y: 520, w: 1400, draw: -60, marks: MARKS, markAt: -60, days: 28, label: 'YOUR PATROL · 4 WEEKS', spreadTo: [0.48, 0.97], spreadAt: w0(62, 'two') - c61}}
			extra={
				<>
					<Count a={w0(62, 'four') - c61} b={w0(62, 'four') - c61 + 1} from={4} to={4} x={330} y={220} size={130} unit="DAYS" color={C.dim} />
					<Count a={w0(62, 'two') - c61} b={w0(62, 'weeks') - c61 + 20} from={4} to={14} x={1050} y={220} size={150} unit="DAYS" color={C.green} />
				</>
			}
		/>
	));
	over(pre(w0(63, 'D-R-D-O')), pre(s0(64)), 'drdo fig', <Label at={0} text="DRDO · LAND TRIALS" x={960} y={760} size={48} align="center" color={C.amber} />);

	// S64–65: so, a ghost? not quite
	const c64 = pre(s0(64));
	add(c64, 'ghost q', (d) => <ProfileShot dur={d} plugAt={-40} ghostAt={-40} backAt={w0(65, 'Not') - c64} />);
	over(c64, pre(w0(65, 'Not')), 'ghost?', <Label at={0} text="A GHOST?" x={960} y={220} size={80} align="center" />);
	over(pre(w0(65, 'Not')), pre(s0(66)), 'not quite', <Label at={0} text="NOT QUITE" x={960} y={220} size={80} align="center" color={C.red} />);

	// S66–68: crawl for weeks, not run; a sprint drains the battery
	const c66 = pre(s0(66));
	add(c66, 'dial', (d) => (
		<Plate dur={d} seed="dial">
			<SpeedDial x={620} y={560} keys={[[0, 0.08], [w0(67, 'run') - c66, 0.95], [w0(68, 'Push') - c66, 0.95]]} />
			<Battery x={1080} y={430} a={w0(68, 'draining') - c66} b={w0(68, 'fast') - c66 + 30} from={0.9} to={0.18} scale={1.2} appear={w0(68, 'back') - c66} />
		</Plate>
	));
	over(pre(w0(66, 'crawl')), pre(w0(67, 'run')), 'weeks', <Label at={0} text="CRAWL FOR WEEKS" x={960} y={170} size={60} align="center" color={C.green} />);
	over(pre(w0(67, 'run')), pre(s0(69)), 'no run', <Label at={0} text="NOT RUN" x={960} y={170} size={60} align="center" color={C.red} />);

	// S69–71: still found: active sonar; still seen: the mast
	add(pre(s0(69)), 'sonar', (d) => <SonarShot dur={d} ping={w0(70, 'Active') - pre(s0(69))} />);
	over(pre(w0(70, 'sonar')), pre(s0(71)), 'sonar lab', <Label at={0} text="ACTIVE SONAR" x={170} y={200} size={60} color={C.cyan} />);
	add(pre(s0(71)), 'TRI masts seen', (d) => <Clip name="TRI_masts" dur={d} startAt={4} from={[1.4, -150, 40]} to={[1.55, -180, 40]} grade="day" />);
	over(pre(s0(71)), pre(s0(72)), 'seen ring', <RedRing x={1060} y={470} at={w0(71, 'seen') - pre(s0(71))} r={160} />);

	// S72–74: what it buys: fewer red marks; whether you come home
	const c72 = pre(s0(72));
	add(c72, 'strip fewer', (d) => (
		<StripShot dur={d} strip={{x: 260, y: 460, w: 1400, draw: -60, marks: MARKS, markAt: -60, days: 28, label: 'YOUR PATROL', fewerAt: w0(72, 'fewer') - c72, shrinkAt: w0(73, 'exposed') - c72}} />
	));
	add(pre(s0(74)), 'VAG sunset', (d) => <Clip name="VAG_sunset" dur={d} grade="none" />);
	over(pre(s0(74)), pre(s0(75)), 'credit sunset', <Credit text={VAG} />);

	// S75–78: why not nuclear? to scale (C34); the shallow coast (C40)
	const c75 = pre(s0(75));
	add(c75, 'to scale', (d) => (
		<Plate dur={d} seed="scale">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<Silhouette x={220} y={420} px={12.5} len={111} color={C.dim} at={w0(75, 'nuclear') - c75} />
				<Silhouette x={220} y={760} px={12.5} len={67.5} color={C.ink} at={w0(76, 'India') - c75 - 30} />
			</svg>
			<ScaleLabels c={c75} />
		</Plate>
	));
	over(c75, pre(s0(78)), 'scale tag', <Honesty text="TO SCALE · ILLUSTRATION" />);
	const c78 = pre(s0(78));
	add(c78, 'coast map', (d) => (
		<SeaMap dur={d} keys={[{f: 0, lon: 72, lat: 17, zoom: 2.0}, {f: d, lon: 72.5, lat: 17.5, zoom: 2.6}]} shelf={w0(78, 'shallow') - c78} pins={[]} />
	));
	add(pre(w0(78, 'small')), 'KAL sea', (d) => <Clip name="KAL_sea" dur={d} grade="day" />);
	over(pre(w0(78, 'shallow')), pre(w0(78, 'small')), 'shallow', <Label at={0} text="SHALLOW COASTAL WATERS" x={1000} y={240} size={52} color={C.cyan} />);
	over(pre(w0(78, 'small')), pre(s0(79)), 'right tool', <Label at={0} text="SMALL · QUIET · DIESEL" x={170} y={240} size={56} />);
	over(pre(w0(78, 'small')), pre(s0(79)), 'credit kal', <Credit text="INS KALVARI · INDIAN NAVY / MDL" />);
	return {shots, overlays};
})();

function StripSenses({c}: {c: number}) {
	const heard = w0(52, 'heard') - c;
	const seen = w0(52, 'seen') - c;
	const radar = w0(52, 'radar') - c;
	return (
		<>
			<Label at={heard} text="HEARD" x={460} y={620} size={56} color={C.red} />
			<Label at={seen} text="SEEN" x={840} y={620} size={56} color={C.red} />
			<Label at={radar} text="ON RADAR" x={1160} y={620} size={56} color={C.red} />
		</>
	);
}

function ScaleLabels({c}: {c: number}) {
	return (
		<>
			<Label at={w0(75, 'nuclear') - c} text="NUCLEAR · INS ARIHANT ≈ 111 M" x={180} y={210} size={48} color={C.dim} />
			<Label at={w0(77, 'bigger') - c} text="BIGGER" x={1300} y={300} size={52} />
			<Label at={w0(77, 'costly') - c} text="COSTLIER" x={1300} y={380} size={52} />
			<Label at={w0(77, 'few') - c} text="FEW" x={1300} y={460} size={52} />
			<Label at={w0(76, 'India') - c - 30} text="DIESEL · KALVARI 67.5 M" x={180} y={570} size={48} />
		</>
	);
}

export {F, P};
