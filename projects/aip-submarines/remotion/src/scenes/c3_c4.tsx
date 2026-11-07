import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {Clip, Count, Credit, ez, Honesty, Label, Plate, tw} from '../parts/kit';
import {PlugDrawing, Silhouette, SubSide} from '../parts/drawings';
import {Balance, Chain, Rickshaws, RefitCalendar, SpoonPhone, Tanks, TrapLoop} from '../parts/chain';
import {ProfileShot, UnderShot} from './c0_open';
import {C, F} from '../theme';
import {s0, w0} from '../timing';

// Chapter 3 · India's powder (S79–109), Chapter 4 · Cut it in half (S110–122) and the trap (S123–153).
const pre = (f: number) => f - 9;
const VAG = 'INDIAN NAVY · INS VAGIR FILM';

/** The boat on the plate, side-on, with dimension lines; compartments fill; a plug floats beside. */
const HullPlan: React.FC<{dur: number; dim?: number; full?: number; plug?: number; longer?: number; rick?: number}> = ({dur, dim, full, plug, longer, rick}) => {
	const f = useCurrentFrame();
	const px = 21;
	const L = longer === undefined ? 67.5 : 67.5 + 10 * tw(f, longer, longer + 40, 0, 1, ez.sweep);
	const x0 = 960 - (L * px) / 2;
	const dk = dim === undefined ? 0 : tw(f, dim, dim + 40, 0, 1, ez.sweep);
	const fk = full === undefined ? 0 : tw(f, full, full + 60, 0, 1);
	const pk = plug === undefined ? 0 : tw(f, plug, plug + 20, 0, 1, ez.arrive);
	return (
		<Plate dur={dur} seed={'plan' + (dim ?? 0)}>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<SubSide x={x0} y={470} px={px} len={L} a={-40} draw={30} plug={longer !== undefined ? {at: 33 - 10, len: 10 * tw(f, longer, longer + 40, 0, 1), glow: 1} : undefined} />
				{fk > 0
					? Array.from({length: 14}).map((_, i) => {
							const x = x0 + (4 + i * 4.2) * px;
							const on = tw(fk, i / 14, i / 14 + 0.08, 0, 1);
							return <rect key={i} x={x} y={470 - 2.2 * px} width={3.6 * px} height={4.4 * px} rx={4} fill={i % 3 === 0 ? C.cyan : i % 3 === 1 ? C.amber : C.dim} opacity={0.5 * on} />;
						})
					: null}
				{dk > 0 ? (
					<g opacity={dk} stroke={C.ink} strokeWidth={3}>
						<line x1={x0} y1={620} x2={x0 + L * px * dk} y2={620} />
						<line x1={x0} y1={600} x2={x0} y2={640} />
						<line x1={x0 + L * px} y1={600} x2={x0 + L * px} y2={640} opacity={dk >= 1 ? 1 : 0} />
					</g>
				) : null}
				{pk > 0 ? (
					<g transform={`translate(960 ${830 + (1 - pk) * 40})`} opacity={pk}>
						<rect x={-105} y={-65} width={210} height={130} rx={60} fill="rgba(242,169,59,0.25)" stroke={C.amber} strokeWidth={4} strokeDasharray="12 8" />
					</g>
				) : null}
				{rick !== undefined ? <Rickshaws at={rick} x={960 + (33 - 10 - 67.5 / 2) * px - 5 * px + 0} y={720} w={10 * px} /> : null}
			</svg>
		</Plate>
	);
};

export const ch34: Part = (() => {
	const shots: Part['shots'] = [];
	const overlays: Part['overlays'] = [];
	const add = (at: number, name: string, el: (d: number) => React.ReactNode, hard = false) => shots.push({at, name, el, hard});
	const over = (from: number, to: number, name: string, el: React.ReactNode) => overlays.push({from, to, name, el});
	const tag = (from: number, to: number, t = 'ILLUSTRATION') => over(from, to, 'tag' + from, <Honesty text={t} />);

	// S79–80: so India built its own, its own way
	const c79 = pre(s0(79));
	add(c79, 'profile own way', (d) => <ProfileShot dur={d} plugAt={-30} />);
	over(pre(w0(79, 'India')), pre(s0(81)), 'india aip', <Label at={0} text="INDIA'S OWN AIP" x={960} y={220} size={64} align="center" color={C.amber} />);
	tag(c79, pre(s0(81)));

	// S81–82: Germany's hydrogen in metal tanks; India's carries none
	const c81 = pre(s0(81));
	add(c81, 'tanks', (d) => (
		<Plate dur={d} seed="tanks">
			<Tanks at={0} gas={w0(81, 'hydrogen') - c81} empty={w0(82, 'no') - c81} />
		</Plate>
	));
	over(pre(w0(81, 'Germany')), pre(s0(82)), 'germany', <Label at={0} text="GERMANY: HYDROGEN IN METAL TANKS" x={960} y={170} size={50} align="center" />);
	over(pre(w0(82, 'no')), pre(s0(83)), 'india none', <Label at={0} text="INDIA: NO HYDROGEN GAS" x={960} y={170} size={56} align="center" color={C.green} />);
	tag(c81, pre(s0(83)));

	// S83–86: H3, the powder; water; hydrogen
	const c83 = pre(s0(83));
	add(c83, 'H3 powder', (d) => <Clip name="H3" dur={d} from={[1.0, 0, 0]} to={[1.05, 0, 0]} grade="none" />);
	over(pre(w0(83, 'dry')), pre(s0(85)), 'white powder', <Label at={0} text="A DRY WHITE POWDER" x={170} y={190} size={52} />);
	over(pre(w0(84, 'Sodium')), pre(s0(86)), 'nabh4', <Label at={0} text="SODIUM BOROHYDRIDE" sub="NaBH₄" x={170} y={300} size={60} color={C.ink} />);
	over(pre(w0(85, 'water')), pre(s0(86)), 'add water', <Label at={0} text="+ WATER" x={1300} y={190} size={56} color={C.frost} />);
	over(pre(w0(85, 'hydrogen')), pre(s0(87)), 'h2 out', <Label at={0} text="→ HYDROGEN" x={1300} y={300} size={56} color={C.amber} />);
	over(pre(w0(86, 'much')), pre(s0(87)), 'as needed', <Label at={0} text="ONLY AS MUCH AS NEEDED" x={960} y={760} size={46} align="center" color={C.dim} />);
	tag(c83, pre(s0(87)));

	// S87–90: a spoonful charges a phone (OUR CALCULATION); tonnes
	const c87 = pre(s0(87));
	add(c87, 'spoon phone', (d) => (
		<Plate dur={d} seed="spoon">
			<SpoonPhone spoon={w0(88, 'spoonful') - c87} grams={w0(88, 'seven') - c87} phone={w0(88, 'charge') - c87} tonnes={w0(90, 'tonnes') - c87} />
		</Plate>
	));
	over(c87, pre(s0(91)), 'calc', <Honesty text="OUR CALCULATION · ON PAPER" />);
	over(pre(w0(88, 'One')), pre(s0(90)), 'spoonful', <Label at={0} text="ONE SPOONFUL" x={360} y={300} size={52} />);

	// S91–99: the chain
	const c91 = pre(s0(91));
	add(c91, 'chain', (d) => (
		<Plate dur={d} seed="chain" from={[1.0, 0, 0]} to={[1.04, 0, 0]}>
			<Chain
				cue={{
					h2: w0(91, 'hydrogen') - c91,
					o2: w0(91, 'oxygen') - c91,
					cold: w0(92, 'cold') - c91,
					cell: w0(93, 'fuel') - c91,
					acid: w0(93, 'acid') - c91,
					elec: w0(96, 'electricity') - c91,
					water: w0(98, 'Water') - c91,
					back: w0(99, 'flows') - c91,
					hull: w0(100, 'sealed') - c91,
				}}
			/>
		</Plate>
	));
	over(pre(w0(94, 'flame')), pre(s0(96)), 'no flame', <Label at={0} text="NO FLAME · NO EXPLOSION" x={960} y={950 - 160} size={46} align="center" color={C.green} />);
	over(pre(w0(100, 'sealed')), pre(s0(101)), 'sealed', <Label at={0} text="A SEALED STEEL TUBE" x={960} y={40 + 80} size={48} align="center" />);
	tag(c91, pre(s0(101)), 'SIMPLIFIED · ILLUSTRATION');

	// S101–102: the Defence Secretary, October 2026 (C14 context; quoted words only)
	const c101 = pre(s0(101));
	// review r1: the quote sat on a sailor's face and read as the Secretary himself; it now sits on the sealed hull drawing
	add(c101, 'sealed chain quote', (d) => (
		<Plate dur={d} seed="chainq" from={[1.06, 0, 0]} to={[1.12, 0, 0]}>
			<div style={{opacity: 0.25, filter: 'blur(3px)'}}>
				<Chain cue={{h2: -200, o2: -200, cold: -200, cell: -200, acid: -200, elec: -200, water: -200, back: -200, hull: -200}} />
			</div>
		</Plate>
	));
	// review r4: the date sat on the oxygen tube, "Defence Secretary" had no picture, and the card hid half of two labels;
	// the drawing now sits further back and the speaker gets his own line on his words.
	over(pre(w0(101, 'October')), pre(s0(103)), 'oct', <Label at={0} text="OCT 2026" x={960} y={250} size={60} mono align="center" />);
	over(pre(w0(101, 'Defence')), pre(s0(103)), 'speaker', <Label at={0} text="INDIA'S DEFENCE SECRETARY" x={960} y={360} size={52} align="center" />);
	over(pre(w0(102, 'strict')), pre(s0(103)), 'quote', <Label at={0} text="“STRICT SAFETY CULTURE”" sub="“NO COMPROMISE”" x={960} y={540} size={64} color={C.amber} align="center" />);

	// S103–106: the balance
	const c103 = pre(s0(103));
	add(c103, 'balance', (d) => (
		<Plate dur={d} seed="bal">
			<Balance edge={w0(103, 'edge') - c103} price={w0(105, 'price') - c103} weight={w0(106, 'Weight') - c103} waste={w0(106, 'salty') - c103} />
		</Plate>
	));
	over(pre(w0(106, 'pump')), pre(s0(107)), 'pump out', <Label at={0} text="HELD ON BOARD, OR PUMPED OUT" x={960} y={170} size={44} align="center" color={C.frost} />);
	tag(c103, pre(s0(107)));

	// S107–109: powder in, power out, under water for weeks (three hard cuts)
	add(pre(s0(107)), 'H3 again', (d) => <Clip name="H3" dur={d} startAt={6} from={[1.08, 0, 0]} to={[1.14, 0, 0]} grade="none" />, true);
	over(pre(s0(107)), pre(s0(108)), 'powder in', <Label at={0} text="POWDER IN" x={960} y={480} size={96} align="center" />);
	const c108 = pre(s0(108));
	add(c108, 'stack glow', (d) => (
		<Plate dur={d} seed="glow">
			<Chain cue={{h2: -100, o2: -100, cold: -100, cell: -100, acid: 9999, elec: -100, water: 9999, back: 9999}} />
		</Plate>
	), true);
	over(c108, pre(s0(109)), 'power out', <Label at={0} text="POWER OUT" x={960} y={170} size={96} align="center" color={C.cyan} />);
	add(pre(s0(109)), 'under weeks', (d) => <UnderShot dur={d} push={9999} />, true);
	over(pre(s0(109)), pre(s0(110)), 'weeks', <Label at={0} text="UNDER WATER, FOR WEEKS" x={960} y={760} size={64} align="center" color={C.green} />);

	// S110–113: 67 metres, every metre full; where does it go?
	const c110 = pre(s0(110));
	add(c110, 'hull plan', (d) => <HullPlan dur={d} dim={w0(111, 'sixty-seven') - c110} full={w0(112, 'every') - c110} plug={w0(113, 'plant') - c110} />);
	over(pre(w0(111, 'sixty-seven')), pre(s0(112)), '67m', <Label at={0} text="≈ 67 M" sub="KALVARI CLASS" x={960} y={660} size={72} align="center" mono />);
	over(pre(w0(112, 'full')), pre(s0(113)), 'full', <Label at={0} text="EVERY METRE FULL" x={960} y={180} size={56} align="center" />);
	over(pre(w0(113, 'plant')), pre(s0(114)), 'plant', <Label at={0} text="THE NEW PLANT?" x={960} y={180} size={56} align="center" color={C.amber} />);
	tag(c110, pre(s0(114)));

	// S114–117: H4 dry dock; Mazagon Dock real; the plug's four parts; slides in, joined
	const c114 = pre(s0(114));
	add(c114, 'H4 open', (d) => <Clip name="H4" dur={d} grade="none" from={[1.0, 0, 0]} to={[1.03, 0, 0]} />);
	const maz = pre(w0(115, 'Mazagon'));
	add(maz, 'LCH dock', (d) => <Clip name="LCH_dock" dur={d} grade="day" />, true);
	over(maz, pre(w0(115, 'hull')), 'mazagon', <Label at={0} text="MAZAGON DOCK" sub="MUMBAI" x={170} y={190} size={64} />);
	over(maz, pre(w0(115, 'hull')), 'credit lch', <Credit text="INS VAGIR LAUNCH · MAZAGON DOCK" />);
	add(pre(w0(115, 'hull')), 'H4 cut', (d) => <Clip name="H4" dur={d} startAt={(pre(w0(115, 'hull')) - c114) / 60} grade="none" from={[1.03, 0, 0]} to={[1.06, 0, 0]} />, true);
	const c116 = pre(s0(116));
	add(c116, 'plug parts', (d) => (
		<Plate dur={d} seed="parts">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<PlugDrawing x={960} y={480} s={1.5} a={-60} parts={[w0(116, 'powder') - c116, w0(116, 'oxygen') - c116, w0(116, 'fuel') - c116, w0(116, 'waste') - c116]} />
			</svg>
		</Plate>
	));
	over(c116, pre(s0(117)), 'new section', <Label at={0} text="A NEW SECTION" x={960} y={150} size={56} align="center" color={C.amber} />);
	const c117 = pre(s0(117));
	add(c117, 'H4 slide', (d) => <Clip name="H4" dur={d} startAt={(700 - (w0(117, 'slides') - c117)) / 60} grade="none" from={[1.0, 0, 0]} to={[1.04, 0, 0]} />);
	over(pre(w0(117, 'joined')), pre(s0(118)), 'joined', <Label at={0} text="JOINED" x={960} y={170} size={64} align="center" color={C.orange} />);
	tag(c114, maz);
	tag(pre(w0(115, 'hull')), pre(s0(118)));

	// S118–120: ten metres longer; four autorickshaws
	const c118 = pre(s0(118));
	add(c118, 'longer', (d) => <HullPlan dur={d} longer={w0(118, 'ten') - c118} rick={w0(120, 'four') - c118} />);
	over(pre(w0(118, 'ten')), pre(s0(119)), '+10', <Label at={0} text="≈ 10 M LONGER" sub="AS REPORTED" x={960} y={180} size={64} align="center" color={C.amber} mono />);
	const c119 = pre(s0(119));
	add(c119, 'ten metres', (d) => (
		<Plate dur={d} seed="ten">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<rect x={360} y={300} width={1200} height={280} rx={40} fill="rgba(242,169,59,0.22)" stroke={C.amber} strokeWidth={5} strokeDasharray="16 10" />
				<line x1={360} x2={1560} y1={620} y2={620} stroke={C.ink} strokeWidth={4} />
				<Rickshaws at={w0(120, 'four') - c119} x={360} y={700} w={1200} />
			</svg>
			<Label at={0} text="10 M" x={960} y={400} size={90} align="center" color={C.amber} mono />
		</Plate>
	));
	over(pre(w0(120, 'four')), pre(s0(121)), 'ricks', <Label at={0} text="≈ 4 AUTORICKSHAWS" x={960} y={150} size={60} align="center" color={C.green} />);
	tag(c118, pre(s0(121)), 'TO SCALE · ILLUSTRATION');

	// S121–122: trust a cut hull? Naval Group signs off
	const c121 = pre(s0(121));
	// The clip runs out about 4 s in (0.5x), so a steady linear push and pan carries the rest to the cut (r4: an eased
	// move went still for 2 s under "signs off the design").
	add(c121, 'H4 weld', (d) => <Clip name="H4" dur={d} startAt={13.8} grade="none" from={[1.06, 50, 0]} to={[1.24, -90, 0]} ease={(t) => t} />);
	over(pre(w0(122, 'Naval')), pre(s0(123)), 'naval group', <Label at={0} text="NAVAL GROUP" sub="FRANCE · THE ORIGINAL DESIGNER" x={170} y={190} size={60} />);
	over(pre(w0(122, 'signs')), pre(s0(123)), 'signs off', <Label at={0} text="✓ SIGNS OFF THE DESIGN" x={170} y={420} size={50} color={C.green} />);
	tag(c121, pre(s0(123)));

	// S123–129: on land, yes: 08 MAR 2021, two modes; never at sea
	const c123 = pre(s0(123));
	add(c123, 'land rig', (d) => (
		<Plate dur={d} seed="rig">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<PlugDrawing x={960} y={470} s={1.3} a={-80} onLand={-60} />
			</svg>
		</Plate>
	));
	over(pre(w0(127, 'Yes')), pre(s0(130)), 'yes', <Label at={0} text="ON LAND: YES" x={170} y={170} size={60} color={C.green} />);
	over(pre(w0(128, 'eighth')), pre(s0(130)), 'date', <Label at={0} text="08 MAR 2021" sub="DRDO LAND PROTOTYPE" x={1250} y={170} size={64} mono />);
	over(pre(w0(128, 'endurance')), pre(s0(129)), 'endur', <Label at={0} text="✓ ENDURANCE MODE" x={420} y={760} size={46} color={C.green} />);
	over(pre(w0(128, 'maximum')), pre(s0(129)), 'maxp', <Label at={0} text="✓ MAXIMUM POWER MODE" x={1000} y={760} size={46} color={C.green} />);
	over(pre(w0(129, 'never')), pre(s0(130)), 'never', <Label at={0} text="AT SEA: NEVER" x={960} y={760} size={64} align="center" color={C.red} />);
	tag(c123, pre(s0(130)));

	// S130–133: six submarines, sea-proven
	const c130 = pre(s0(130));
	add(c130, 'six', (d) => (
		<Plate dur={d} seed="six">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{Array.from({length: 6}).map((_, i) => (
					<Silhouette key={i} x={220 + (i % 3) * 520} y={420 + Math.floor(i / 3) * 170} px={6} len={70} color={C.ink} at={i * 5} opacity={1} />
				))}
			</svg>
		</Plate>
	));
	over(pre(w0(131, 'proven')), pre(s0(134)), 'sea proven', <Label at={0} text="AIP PROVEN AT SEA" sub="THE NAVY'S REQUIREMENT" x={960} y={160} size={64} align="center" color={C.cyan} />);
	over(pre(w0(132, 'shore')), pre(s0(133)), 'not shore', <Label at={0} text="✗ NOT ON SHORE" x={500} y={800} size={52} color={C.red} />);
	over(pre(w0(133, 'sea')), pre(s0(134)), 'at sea', <Label at={0} text="✓ AT SEA" x={1150} y={800} size={52} color={C.green} />);
	tag(c130, pre(s0(134)));

	// S134–137: L&T with Navantia turned down (reports); Germany at sea ~20 years
	const c134 = pre(s0(134));
	add(c134, 'bid', (d) => <Plate dur={d} seed="bid" />);
	over(pre(w0(134, 'L')), pre(s0(136)), 'lt', <Label at={0} text="L&T" x={560} y={400} size={84} />);
	over(pre(w0(134, 'Navantia')), pre(s0(136)), 'nav', <Label at={0} text="NAVANTIA" sub="SPAIN" x={1000} y={400} size={84} />);
	over(pre(w0(134, 'turned')), pre(s0(136)), 'rej', <Label at={0} text="TURNED DOWN" sub="AS REPORTED" x={960} y={640} size={60} align="center" color={C.red} />);
	over(pre(w0(135, 'shore')), pre(s0(136)), 'shore', <Label at={0} text="SHOWN ON SHORE, NOT AT SEA" x={960} y={200} size={46} align="center" color={C.dim} />);
	const c136 = pre(s0(136));
	add(c136, 'german at sea', (d) => (
		<Plate dur={d} seed="ger2">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<Silhouette x={430} y={560} px={15} len={65} color={C.dim} at={0} />
			</svg>
			<Count a={w0(136, 'about') - c136} b={w0(136, 'years') - c136 + 10} from={0} to={20} x={960} y={160} size={140} unit="YEARS AT SEA" color={C.ink} align="center" />
		</Plate>
	));
	over(pre(w0(137, 'German')), pre(s0(138)), 'ger lean', <Label at={0} text="THE NAVY LEANED GERMAN" x={960} y={800} size={50} align="center" />);
	tag(c134, pre(s0(138)));

	// S138–140: bad? no. nobody has proven it at sea yet
	const c138 = pre(s0(138));
	add(c138, 'plug no', (d) => (
		<Plate dur={d} seed="no">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<PlugDrawing x={960} y={470} s={1.2} a={-80} onLand={-60} />
			</svg>
		</Plate>
	));
	over(pre(w0(139, 'No')), pre(s0(140)), 'no', <Label at={0} text="NO" x={960} y={170} size={96} align="center" color={C.green} />);
	over(pre(w0(140, 'nobody')), pre(s0(141)), 'not yet', <Label at={0} text="NOT PROVEN AT SEA · YET" x={960} y={170} size={56} align="center" color={C.amber} />);

	// S141–148: the trap loop (signature) and its lock
	const c141 = pre(s0(141));
	add(c141, 'trap loop', (d) => (
		<Plate dur={d} seed="trap" from={[1.0, 0, 0]} to={[1.06, 0, 0]}>
			<TrapLoop both={w0(141, 'both') - c141} navy={w0(142, 'Navy') - c141} engine={w0(143, 'engine') - c141} close={w0(144, 'Both') - c141} lock={w0(146, 'lock') - c141} />
		</Plate>
	));
	over(pre(w0(145, 'trap')), pre(s0(146)), 'trap', <Label at={0} text="A TRAP" x={960} y={150} size={80} align="center" color={C.red} />);
	const c147 = pre(s0(147));
	add(c147, 'refit', (d) => (
		<Plate dur={d} seed="refit">
			<RefitCalendar at={0} windows={w0(147, 'refit') - c147} far={w0(148, 'several') - c147} />
		</Plate>
	));
	over(pre(w0(147, 'refit')), pre(s0(149)), 'refit lab', <Label at={0} text="ONLY IN A BIG REFIT" sub="MONTHS OUT OF SERVICE" x={960} y={170} size={56} align="center" color={C.green} />);

	// S149–153: 2025, INS Kalvari's refit went ahead without it (C11)
	const c149 = pre(s0(149));
	add(c149, 'KAL above', (d) => <Clip name="KAL_above" dur={d} grade="day" from={[1.0, 0, 0]} to={[1.1, 0, 0]} />); // INS Kalvari herself (review r1: the Vagir shot was captioned Kalvari)
	over(pre(w0(149, 'twenty')), pre(s0(154)), '2025', <Label at={0} text="2025" x={170} y={170} size={96} mono />);
	over(pre(w0(150, 'Kalvari')), pre(s0(151)), 'ins kalvari', <Label at={0} text="INS KALVARI" sub="IN REFIT IN 2025" x={170} y={320} size={56} />);
	over(pre(w0(151, 'engine')), pre(s0(152)), 'not ready', <Label at={0} text="AIP NOT READY" x={170} y={320} size={56} color={C.amber} />);
	add(pre(s0(152)), 'TRI out to sea', (d) => <Clip name="TRI_side" dur={d} grade="day" from={[1.0, 0, 0]} to={[1.1, 0, 0]} />);
	over(pre(w0(152, 'without')), pre(s0(154)), 'without', <Label at={0} text="OUT WITHOUT IT" x={170} y={320} size={56} color={C.red} />);
	over(pre(w0(153, 'window')), pre(s0(154)), 'window', <Label at={0} text="THE WINDOW CLOSED" x={960} y={700} size={64} align="center" color={C.red} />);
	over(c149, pre(s0(152)), 'credit kal', <Credit text="INS KALVARI · INDIAN NAVY / MDL" />);
	over(pre(s0(152)), pre(s0(154)), 'credit tri', <Credit text="INS KALVARI SEA TRIALS" />);
	return {shots, overlays};
})();

export {AbsoluteFill, F};
