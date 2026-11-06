import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {Battery, CutLine, Exhaust, RadarSweep, RedRing} from '../parts/instruments';
import {Cam, Clip, Credit, ez, Honesty, Label, Plate, tw, Underwater} from '../parts/kit';
import {PatrolStrip, PlugDrawing, Silhouette, SubSide} from '../parts/drawings';
import {SubUnderwater} from '../parts/Sub3D';
import {SeaMap} from '../parts/SeaMap';
import {C, F} from '../theme';
import {s0, w0} from '../timing';

// Cold open (0:00–1:15), word_map.md. Frames come from the locked audio; cutaways start 9 frames (0.15 s) early.
const pre = (f: number) => f - 9;

const VAG = 'INDIAN NAVY · INS VAGIR FILM';

/** The boat under the waves, camera gliding alongside; push to the fin on "Indian submarine". */
export const UnderShot: React.FC<{dur: number; push: number}> = ({dur, push}) => {
	const f = useCurrentFrame();
	const k = tw(f, 0, dur, 0, 1);
	const pk = tw(f, push, push + 90, 0, 1);
	return (
		<AbsoluteFill>
			<Underwater depth={0.2} />
			<SubUnderwater cam={[70 - 40 * k - 20 * pk, -10 + 6 * pk, 120 - 50 * pk]} look={[-4 + 12 * pk, 1.5 * pk, 0]} fov={30 - 6 * pk} x={-6 + 10 * k} depthTint={0.25} />
		</AbsoluteFill>
	);
};

/** The boat in profile under water, the AIP module glowing mid-hull ("There is a cure"), then the ghost. */
export const ProfileShot: React.FC<{dur: number; plugAt: number; ghostAt?: number; goneAt?: number; backAt?: number}> = ({dur, plugAt, ghostAt, goneAt, backAt}) => {
	const f = useCurrentFrame();
	const k = tw(f, 0, dur, 0, 1);
	const plug = tw(f, plugAt, plugAt + 30, 0, 1, ez.arrive);
	let ghost = 0;
	if (ghostAt !== undefined) {
		ghost = tw(f, ghostAt, ghostAt + 40, 0, 0.7);
	}
	if (goneAt !== undefined) {
		ghost = Math.max(ghost, tw(f, goneAt, goneAt + 40, 0.7, 1));
	}
	if (backAt !== undefined) {
		ghost = ghost * (1 - tw(f, backAt, backAt + 6, 0, 1));
	}
	return (
		<AbsoluteFill>
			<Underwater depth={0.35} />
			<SubUnderwater cam={[-6 + 10 * k, -3, 84 - 10 * k]} look={[-4 + 8 * k, 0, 0]} fov={34} plug={plug * (1 - ghost)} ghost={ghost} depthTint={0.4} />
		</AbsoluteFill>
	);
};

/** "Both were right": the two halves face each other on the plate. */
const TwoSides: React.FC<{dur: number; navyQ: number; indiaQ: number; both: number; loop: number}> = ({dur, navyQ, indiaQ, both, loop}) => {
	const f = useCurrentFrame();
	const navyDim = tw(f, navyQ, navyQ + 12, 1, 0.35) * (1 - tw(f, indiaQ, indiaQ + 12, 0, 1)) + tw(f, indiaQ, indiaQ + 12, 0, 1);
	const indiaDim = f < indiaQ ? 1 : tw(f, indiaQ, indiaQ + 12, 1, 0.35);
	const g = tw(f, both, both + 16, 0, 1, ez.arrive);
	const lp = tw(f, loop, loop + 40, 0, 1, ez.sweep);
	const col = (base: string) => (g > 0.5 ? C.green : base);
	return (
		<Plate dur={dur} seed="two">
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<g opacity={Math.max(navyDim, g)}>
					<Silhouette x={250} y={500} px={8} color={col(C.ink)} />
					<text x={520} y={720} textAnchor="middle" fill={col(C.ink)} fontFamily={F.label} fontWeight={800} fontSize={54}>
						THE NAVY
					</text>
				</g>
				<g opacity={Math.max(indiaDim, g)}>
					<PlugDrawing x={1400} y={480} s={0.9} a={-60} />
					<text x={1400} y={720} textAnchor="middle" fill={col(C.amber)} fontFamily={F.label} fontWeight={800} fontSize={54}>
						INDIA&apos;S MACHINE
					</text>
				</g>
				{lp > 0 ? (
					<g opacity={0.55 * lp} fill="none" stroke={C.dim} strokeWidth={5} strokeDasharray="14 12">
						<path d="M780 380 C 900 260, 1060 260, 1150 360" pathLength={1} strokeDasharray={`${lp} 1`} />
						<path d="M1150 620 C 1060 720, 900 720, 790 620" pathLength={1} strokeDasharray={`${lp} 1`} />
					</g>
				) : null}
			</svg>
		</Plate>
	);
};

/** "India built this machine… It has run on land.": the plug drawn on the plate, then set on its land test bed. */
const PlugBuild: React.FC<{dur: number; land: number}> = ({dur, land}) => (
	<Plate dur={dur} seed="plug" from={[1.0, 0, 0]} to={[1.1, 0, -10]}>
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<PlugDrawing x={960} y={500} s={1.4} a={4} onLand={land} />
		</svg>
	</Plate>
);

/** "Yet the Navy leaned towards a German design for its next submarines." */
const GermanDesign: React.FC<{dur: number; german: number; six: number}> = ({dur, german, six}) => (
	<Plate dur={dur} seed="ger">
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<Silhouette x={430} y={430} px={15} len={65} color={C.dim} at={german - 20} />
			{Array.from({length: 6}).map((_, i) => (
				<Silhouette key={i} x={260 + (i % 3) * 480} y={720 + Math.floor(i / 3) * 110} px={5.4} len={65} color={C.ink} at={six + i * 5} />
			))}
		</svg>
	</Plate>
);

export const open: Part = (() => {
	const shots: Part['shots'] = [];
	const overlays: Part['overlays'] = [];
	const add = (at: number, name: string, el: (d: number) => React.ReactNode, hard = false) => shots.push({at, name, el, hard});
	const over = (from: number, to: number, name: string, el: React.ReactNode) => overlays.push({from, to, name, el});

	// S0–1: the night sea; "Arabian Sea" → the map cutaway
	add(0, 'H1a night sea', (d) => <Clip name="H1a" dur={d} from={[1.02, 0, 0]} to={[1.06, 0, 0]} grade="none" />, true);
	const arab = pre(w0(1, 'Arabian'));
	add(arab, 'map Arabian Sea', (d) => <SeaMap dur={d} mode="arabian" />, true);
	add(arab + 62, 'H1a back', (d) => <Clip name="H1a" dur={d} startAt={(arab + 62) / 60} from={[1.06, 0, 0]} to={[1.08, 0, 0]} grade="none" />);

	// S2: under the waves; "Indian submarine" → push to the fin; "battery" → the gauge
	const s2 = s0(2);
	add(s2, 'T1 under', (d) => <UnderShot dur={d} push={w0(2, 'Indian') - s2} />);
	const bat = pre(w0(2, 'battery'));
	over(bat, s0(3), 'battery', <Battery x={1240} y={180} a={0} b={60} from={0.24} to={0.12} appear={0} />);

	// S3–6: the control room, real (INS Vagir)
	add(pre(s0(3)), 'VAG ctrl', (d) => <Clip name="VAG_ctrl" dur={d} grade="red" />);
	add(pre(s0(4)), 'VAG consoles', (d) => <Clip name="VAG_consoles" dur={d} startAt={1.0} grade="red" />);
	add(pre(s0(5)), 'VAG periscope', (d) => <Clip name="VAG_peri" dur={d} grade="red" />);
	over(pre(s0(3)), pre(w0(6, 'Raise')), 'credit vag', <Credit text={VAG} />);

	// S6–9: "Raise" → hard cut to the mast; it breaks the surface on "mast rises"
	const raise = pre(w0(6, 'Raise'));
	add(raise, 'H1b mast', (d) => <Clip name="H1b" dur={d} from={[1.0, 0, 0]} to={[1.04, 0, 0]} grade="none" />, true);
	over(raise, raise + 1, 'label recon', <></>);
	const diesel = pre(w0(8, 'diesel'));
	add(diesel, 'VAG machinery', (d) => <Clip name="VAG_mach" dur={d} grade="day" />);
	over(diesel, s0(9), 'credit vag2', <Credit text={VAG} />);
	const s9 = pre(s0(9));
	add(s9, 'H1b wide', (d) => <Clip name="H1b" dur={d} startAt={(diesel - raise) / 60} from={[1.0, 0, 0]} to={[1.03, 0, 0]} grade="none" />);
	over(s9, pre(s0(10)), 'exhaust', <Exhaust x={1010} y={300} start={0} />);
	over(s9, pre(s0(10)), 'radar', <RadarSweep cx={1010} cy={420} r={520} blip={w0(9, 'easier') - s9} bx={1010} by={360} lock={w0(9, 'find') - s9} />);
	over(raise, diesel, 'recon', <Honesty text="RECONSTRUCTION" />);
	over(s9, pre(s0(10)), 'recon2', <Honesty text="RECONSTRUCTION" />);

	// S10–13: a machine built to disappear
	add(pre(s0(10)), 'VAG underwater', (d) => <Clip name="VAG_under" dur={d} grade="none" />);
	add(pre(s0(11)), 'VAG night boat', (d) => <Clip name="VAG_dusk" dur={d} grade="night" from={[1.1, 0, 0]} to={[1.25, 0, 20]} />);
	over(pre(s0(10)), pre(s0(12)), 'credit vag3', <Credit text={VAG} />);
	over(pre(s0(11)), pre(s0(12)), 'danger ring', <RedRing x={960} y={520} at={w0(11, 'dangerous') - pre(s0(11))} r={170} />);
	const s12 = pre(s0(12));
	add(s12, 'strip teaser', (d) => (
		<Plate dur={d} seed="strip0">
			<PatrolStrip x={210} y={470} w={1500} draw={0} marks={[0.18, 0.43, 0.68, 0.93]} markAt={w0(12, 'every') - s12} days={12} label="EVERY FEW DAYS" />
		</Plate>
	));
	const s13 = pre(s0(13));
	add(s13, 'TRI surfaced', (d) => <Clip name="TRI_surf" dur={d} from={[1.0, 0, 0]} to={[1.18, -40, 10]} grade="day" />);
	over(s13, pre(s0(14)), 'show ring', <RedRing x={1010} y={560} at={w0(13, 'show') - s13} r={200} />);
	over(s13, pre(s0(14)), 'credit tri', <Credit text="INS KALVARI SEA TRIALS · MAZAGON DOCK" />);

	// S14–18: the cure has a name; the ghost maker
	const s14 = pre(s0(14));
	add(s14, 'T1 profile cure', (d) => (
		<ProfileShot dur={d} plugAt={w0(14, 'cure') - s14} ghostAt={w0(17, 'ghost') - s14} goneAt={w0(18, 'invisible') - s14} />
	));
	over(pre(w0(16, 'A-I-P')), pre(s0(17)), 'aip letters', <AipTitle a={0} words={[w0(16, 'air'), w0(16, 'independent'), w0(16, 'propulsion')].map((x) => x - pre(w0(16, 'A-I-P')))} />);
	over(pre(w0(17, 'ghost')), pre(s0(19)), 'ghost quote', <Label at={0} text="“THE GHOST MAKER”" x={960} y={230} size={72} align="center" sub="ONLINE" />);
	over(pre(w0(18, 'invisible')), pre(s0(19)), 'invisible', <Label at={0} text="“INVISIBLE”" x={960} y={760} size={64} align="center" color={C.dim} sub="HEADLINES" />);
	over(s14, pre(s0(19)), 'illus', <Honesty text="ILLUSTRATION" />);

	// S19–20: "But here's the catch." the real hull at Mazagon; "cut … in two" → the cut line
	const s19 = pre(s0(19));
	add(s19, 'VAG shed', (d) => <Clip name="VAG_shed" dur={d} from={[1.0, 0, 0]} to={[1.07, 0, 0]} grade="day" />, true);
	const cut = w0(20, 'cut') - s19;
	over(s19, pre(s0(21)), 'cut line', <CutLine d="M640 560 C 625 700, 600 860, 570 1070" a={cut} b={w0(20, 'two') - s19} len={680} tip={(k) => [640 - 70 * k, 560 + 510 * k]} />);
	over(s19, pre(s0(21)), 'credit shed', <Credit text={VAG} />);
	over(s19 + cut, pre(s0(21)), 'two label', <Label at={0} text="CUT IN TWO" x={700} y={420} size={60} color={C.orange} />);

	// S21–24: India built it; it ran on land; the Navy leaned German
	const s21 = pre(s0(21));
	add(s21, 'plug drawing', (d) => <PlugBuild dur={d} land={w0(23, 'run') - s21} />);
	over(pre(w0(22, 'India')), pre(s0(24)), 'drdo', <Label at={0} text="DRDO · NMRL" x={960} y={180} size={56} align="center" color={C.amber} />);
	over(pre(w0(23, 'land')), pre(s0(24)), 'on land', <Label at={0} text="ON LAND" x={960} y={800} size={56} align="center" />);
	const s24 = pre(s0(24));
	add(s24, 'german', (d) => <GermanDesign dur={d} german={w0(24, 'German') - s24} six={w0(24, 'next') - s24} />);
	over(pre(w0(24, 'German')), pre(s0(25)), 'german label', <Label at={0} text="A GERMAN DESIGN" x={960} y={170} size={60} align="center" />);
	over(pre(w0(24, 'next')), pre(s0(25)), 'p75i', <Label at={0} text="NEXT SIX SUBMARINES" x={960} y={620} size={44} align="center" color={C.dim} />);
	over(s21, pre(s0(29)), 'illus2', <Honesty text="ILLUSTRATION" />);

	// S25–28: was the Navy wrong, or India's machine? Both were right.
	const s25 = pre(s0(25));
	add(s25, 'two sides', (d) => (
		<TwoSides dur={d} navyQ={w0(25, 'Navy') - s25} indiaQ={w0(26, "India's") - s25} both={w0(27, 'both') - s25} loop={w0(28, 'see') - s25} />
	));
	over(pre(w0(27, 'both')), pre(s0(29)), 'both right', <Label at={0} text="BOTH RIGHT" x={960} y={200} size={72} align="center" color={C.green} />);
	return {shots, overlays};
})();

/** A-I-P: three letters land, then each word lands under its letter. */
function AipTitle({a, words}: {a: number; words: number[]}) {
	const f = useCurrentFrame();
	const L = ['A', 'I', 'P'];
	const W = ['AIR', 'INDEPENDENT', 'PROPULSION'];
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-start', paddingTop: 170}}>
			<div style={{display: 'flex', gap: 120}}>
				{L.map((l, i) => {
					const p = tw(f, a + i * 5, a + i * 5 + 14, 0, 1, ez.arrive);
					const wp = tw(f, words[i] - 4, words[i] + 10, 0, 1, ez.arrive);
					return (
						<div key={l} style={{textAlign: 'center', opacity: p, transform: `translateY(${(1 - p) * 30}px)`}}>
							<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 190, color: C.amber, lineHeight: 1, textShadow: '0 0 40px rgba(242,169,59,0.45)'}}>{l}</div>
							<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 46, color: C.ink, opacity: wp, letterSpacing: 2, marginTop: 10, background: 'rgba(3,7,13,0.7)', padding: '4px 12px'}}>
								{W[i]}
							</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
}

export {Cam};
