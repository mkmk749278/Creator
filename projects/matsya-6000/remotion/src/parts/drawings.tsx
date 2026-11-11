import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {Count, ez, Label, MarineSnow, tw, Underwater} from './kit';

// matsya-6000 drawings (word_map.md). Each sits on the steel plate (or in the deep), every value a function of the
// frame; facts on screen are claims rows (claims.csv) or labelled OUR CALCULATION / SIMPLIFIED / ILLUSTRATION.

const txt = (size: number, color: string = C.ink, weight = 800): React.CSSProperties => ({
	fontFamily: F.label,
	fontWeight: weight,
	fontSize: size,
	fill: color,
	letterSpacing: size * 0.02,
});

/** S9–10, S73–75: two weld cross-sections at true relative scale (6 px a millimetre): 20 mm, then 80 mm. */
export const WeldBars: React.FC<{show20: number; show80: number; grow?: number}> = ({show20, show80, grow}) => {
	const f = useCurrentFrame();
	const a = tw(f, show20, show20 + 24, 0, 1, ez.arrive);
	const b = tw(f, show80, show80 + 40, 0, 1, ez.sweep);
	const g = grow === undefined ? 0 : tw(f, grow, grow + 50, 0, 1, ez.sweep);
	const px = 6;
	const y = 540;
	const bar = (x: number, mm: number, k: number, hot: boolean) => (
		<g opacity={k}>
			<rect x={x} y={y - (mm * px) / 2} width={520} height={mm * px * k} fill={C.ti} opacity={0.9} />
			<rect x={x} y={y - (mm * px) / 2} width={520} height={mm * px * k} fill="none" stroke="#0a0d10" strokeWidth={3} />
			{/* the weld bead down the middle */}
			<rect x={x + 240} y={y - (mm * px) / 2} width={40} height={mm * px * k} fill={hot ? C.weld : '#8a8378'} opacity={hot ? 0.95 : 0.8} />
		</g>
	);
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{bar(260, 20, a, false)}
				{bar(1140, 80, b, true)}
				<text x={520} y={y + 140} textAnchor="middle" style={txt(64)} opacity={a}>20 MM</text>
				<text x={1400} y={y + 330} textAnchor="middle" style={txt(64, C.amber)} opacity={b}>80 MM</text>
				{g > 0 ? <text x={960} y={y + 20} textAnchor="middle" style={txt(110, C.amber)} opacity={g}>×4</text> : null}
			</svg>
		</AbsoluteFill>
	);
};

/** S19–21: a fingertip on the plate, an arrow down, then a buffalo standing on the nail (OUR CALCULATION). */
export const Fingernail: React.FC<{arrow: number; kg: number; buffalo: number}> = ({arrow, kg, buffalo}) => {
	const f = useCurrentFrame();
	const ar = tw(f, arrow, arrow + 30, 0, 1, ez.arrive);
	const bf = tw(f, buffalo, buffalo + 36, 0, 1, ez.arrive);
	const press = 1 - 0.02 * Math.sin(Math.min(1, Math.max(0, (f - buffalo) / 20)) * Math.PI);
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{/* finger from the right, nail up */}
				<g transform={`translate(0 ${(1 - press) * 300})`}>
					<path d="M760 800 C760 700 840 650 960 650 L1920 650 L1920 900 L960 900 C840 900 760 880 760 800 Z" fill="#c99877" stroke="#0a0d10" strokeWidth={4} />
					<path d="M800 760 C800 700 850 680 930 680 L1010 680 L1010 760 Z" fill="#efd8c8" stroke="#8a6a55" strokeWidth={3} />
				</g>
				{/* the arrow of water pressure */}
				<g opacity={ar * (1 - bf)}>
					<rect x={890} y={260 + (1 - ar) * 120} width={40} height={300} fill={C.amber} />
					<path d={`M850 ${560 + (1 - ar) * 120} L970 ${560 + (1 - ar) * 120} L910 ${650 + (1 - ar) * 120} Z`} fill={C.amber} />
				</g>
				{/* a buffalo silhouette standing on the nail */}
				<g opacity={bf} transform={`translate(905 ${672 - 4 * (1 - bf) * 60}) scale(${0.9 + 0.1 * bf})`}>
					<path
						d="M-210 -230 C-230 -300 -150 -350 -40 -345 L120 -345 C170 -350 200 -330 215 -300 L250 -300 C285 -300 300 -280 290 -255 L262 -232 C250 -222 232 -224 220 -232 L205 -232 L196 -150 L180 0 L150 0 L150 -120 L-120 -120 L-130 0 L-160 0 L-175 -150 L-200 -180 Z"
						fill="#1a1d21"
						stroke={C.dim}
						strokeWidth={3}
					/>
					<path d="M232 -300 C240 -330 270 -345 300 -330" stroke={C.dim} strokeWidth={10} fill="none" strokeLinecap="round" />
				</g>
			</svg>
			<Count a={kg} b={kg + 40} from={0} to={600} x={170} y={240} size={130} unit="KG" color={C.amber} />
			<Label at={buffalo} text="A FULL-GROWN BUFFALO" x={170} y={430} size={52} />
			<Label at={kg} text="ON ONE FINGERNAIL" x={170} y={160} size={40} color={C.dim} />
		</AbsoluteFill>
	);
};

/** S14–18: falling through the sea, the depth counter, a ring of pressure passing every "ten metres". */
export const Fall: React.FC<{dur: number; target: number; beats: number[]; race: number; bare?: boolean}> = ({dur, target, beats, race, bare}) => {
	const f = useCurrentFrame();
	// depth: 0 at the start; 10/20/30 m on the beats; then a race to 6,000
	// each beat takes over once it starts (r1 took the max of every beat, so it read 30 m from frame 0)
	let d = 0;
	beats.forEach((b, i) => {
		if (f >= b) {
			d = tw(f, b, b + 18, i * 10, (i + 1) * 10, ez.arrive);
		}
	});
	if (f >= race) {
		d = tw(f, race, dur, beats.length * 10, 6000, ez.sweep);
	}
	const deep = Math.min(1, d / 6000);
	return (
		<AbsoluteFill>
			{bare ? (
				// over real sea footage: the water darkens as the counter goes down
				<AbsoluteFill style={{background: `rgba(2,8,14,${Math.min(0.92, d / 160 + 0.88 * deep)})`}} />
			) : (
				<Underwater depth={0.2 + 0.8 * deep} />
			)}
			<MarineSnow speed={2 + 10 * deep} n={bare ? 90 : 170} />
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{beats.map((b, i) => {
					const k = tw(f, b, b + 40, 0, 1, ez.leave);
					return k > 0 && k < 1 ? <ellipse key={i} cx={960} cy={540} rx={200 + 900 * k} ry={60 + 260 * k} fill="none" stroke={C.amber} strokeWidth={6} opacity={1 - k} /> : null;
				})}
			</svg>
			<div style={{position: 'absolute', left: 140, top: 380, fontFamily: F.mono, fontWeight: 700, fontSize: 150, color: C.ink, textShadow: '0 4px 24px rgba(0,0,0,0.8)'}}>
				{Math.round(d).toLocaleString('en-IN')}
				<span style={{fontSize: 70, marginLeft: 18}}>M</span>
			</div>
			{f >= target ? <Label at={target} text="6,000 M" x={140} y={250} size={48} color={C.amber} /> : null}
		</AbsoluteFill>
	);
};

/** S42–46: a long tube and a ball under the same arrows; the tube's flat ends glow (where the push wins). */
export const TubeVsBall: React.FC<{tubeEnds: number; ring: number; corner?: number}> = ({tubeEnds, ring, corner}) => {
	const f = useCurrentFrame();
	const te = tw(f, tubeEnds, tubeEnds + 24, 0, 1, ez.arrive);
	const rg = tw(f, ring, ring + 90, 0, 1, ez.sweep);
	const arrows = (cx: number, cy: number, rx: number, ry: number, n: number) =>
		Array.from({length: n}).map((_, i) => {
			const a = (i / n) * Math.PI * 2;
			const x = cx + Math.cos(a) * (rx + 70);
			const y = cy + Math.sin(a) * (ry + 70);
			const ux = -Math.cos(a);
			const uy = -Math.sin(a);
			const wob = 6 * Math.sin(f / 9 + i);
			return <line key={i} x1={x - ux * wob} y1={y - uy * wob} x2={x + ux * 46} y2={y + uy * 46} stroke={C.amber} strokeWidth={8} strokeLinecap="round" markerEnd="url(#ah)" />;
		});
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<defs>
					<marker id="ah" markerWidth="5" markerHeight="5" refX="2.5" refY="2.5" orient="auto">
						<path d="M0 0 L5 2.5 L0 5 Z" fill={C.amber} />
					</marker>
				</defs>
				{/* tube */}
				<rect x={180} y={420} width={700} height={240} rx={18} fill="#3a4048" stroke={C.ti} strokeWidth={5} />
				<rect x={168} y={420} width={30} height={240} fill={C.amber} opacity={te * (0.6 + 0.4 * Math.sin(f / 6))} />
				<rect x={862} y={420} width={30} height={240} fill={C.amber} opacity={te * (0.6 + 0.4 * Math.sin(f / 6))} />
				{arrows(530, 540, 350, 120, 18)}
				{/* ball */}
				<circle cx={1400} cy={540} r={190} fill="#3a4048" stroke={C.ti} strokeWidth={5} />
				{arrows(1400, 540, 190, 190, 18)}
				<circle cx={1400} cy={540} r={196} fill="none" stroke={C.amber} strokeWidth={14} pathLength={1} strokeDasharray={`${rg} 1`} transform="rotate(-90 1400 540)" opacity={rg > 0 ? 0.9 : 0} />
				{corner !== undefined && f >= corner ? (
					<g opacity={tw(f, corner, corner + 20, 0, 1)}>
						<path d="M870 330 L930 330 L930 390" stroke={C.ink} strokeWidth={10} fill="none" />
						<line x1={850} y1={310} x2={950} y2={410} stroke={C.red} strokeWidth={10} />
					</g>
				) : null}
			</svg>
			<Label at={tubeEnds} text="FLAT ENDS" x={530} y={720} size={48} align="center" color={C.amber} />
			<Label at={ring} text="NO WEAK SIDE" x={1400} y={790} size={48} align="center" />
		</AbsoluteFill>
	);
};

/** S47–49: Alvin drawn (no clean-licence photo): the sphere's label changes from steel 1964 to titanium 1973, then two
 *  depth bars 2,440 m and 4,500 m (claim M29). */
export const Alvin: React.FC<{steel: number; ti: number; bars: number}> = ({steel, ti, bars}) => {
	const f = useCurrentFrame();
	const st = tw(f, steel, steel + 20, 0, 1);
	const tt = tw(f, ti, ti + 30, 0, 1, ez.sweep);
	const br = tw(f, bars, bars + 50, 0, 1, ez.sweep);
	const sph = tt > 0.5 ? C.ti : '#7a7f86';
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{/* the sub's outline, side on */}
				<g transform="translate(140 300)">
					<path d="M60 220 C60 120 160 80 300 80 L680 80 C780 80 860 140 860 220 C860 300 780 360 680 360 L300 360 C160 360 60 320 60 220 Z" fill="#e8e2d0" fillOpacity={0.12} stroke={C.ink} strokeWidth={4} />
					<rect x={420} y={20} width={140} height={70} rx={10} fill="none" stroke={C.ink} strokeWidth={4} />
					<line x1={860} y1={220} x2={940} y2={220} stroke={C.ink} strokeWidth={4} />
					<rect x={930} y={160} width={30} height={120} fill="none" stroke={C.ink} strokeWidth={4} />
					{/* the personnel sphere in the nose */}
					<circle cx={250} cy={230} r={110} fill={sph} fillOpacity={0.35 + 0.25 * st} stroke={sph} strokeWidth={8} />
				</g>
				<text x={390} y={760} textAnchor="middle" style={txt(56, '#9aa3ad')} opacity={st * (1 - tt)}>STEEL · 1964</text>
				<text x={390} y={760} textAnchor="middle" style={txt(56, C.ti)} opacity={tt}>TITANIUM · 1973</text>
				{/* depth bars */}
				<g opacity={br}>
					<rect x={1280} y={180} width={130} height={244 * 1.4 * br} fill="#7a7f86" />
					<rect x={1500} y={180} width={130} height={450 * 1.4 * br} fill={C.ti} />
					<text x={1345} y={180 + 244 * 1.4 * br + 60} textAnchor="middle" style={txt(46, C.dim)}>2,440 M</text>
					<text x={1565} y={180 + 450 * 1.4 * br + 60} textAnchor="middle" style={txt(46)}>4,500 M</text>
				</g>
			</svg>
			<Label at={steel} text="ALVIN" x={160} y={180} size={64} />
		</AbsoluteFill>
	);
};

/** S50–52: the 2021 test: a plain steel ball lowered on a cable from a ship's A-frame; a depth line to 600 m. */
export const SteelBall2021: React.FC<{dur: number; date: number; depth: number}> = ({dur, date, depth}) => {
	const f = useCurrentFrame();
	// the ball is already going down from frame 0 (r1 held still until the date: a 2 s freeze)
	const down = tw(f, date, dur, 0, 1, ez.sweep);
	const pre0 = tw(f, 0, date, 0, 1, (t) => t);
	const by = 300 + 70 * pre0 + 480 * down;
	return (
		<AbsoluteFill>
			<Underwater depth={0.2 + 0.5 * down} />
			<MarineSnow speed={1 + 3 * down} n={90} />
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{/* the ship's stern and A-frame above the surface line */}
				<rect x={0} y={0} width={1920} height={150} fill="#0b1824" />
				<path d="M560 150 L1360 150 L1300 220 L620 220 Z" fill="#1c252e" stroke={C.dim} strokeWidth={3} />
				<path d="M900 150 L940 40 L1020 40 L1060 150" stroke={C.dim} strokeWidth={10} fill="none" />
				<line x1={0} y1={220} x2={1920} y2={220} stroke="#6aa9c9" strokeWidth={2} opacity={0.6} />
				<line x1={980} y1={40} x2={980} y2={by - 70} stroke={C.ink} strokeWidth={3} />
				<circle cx={980} cy={by} r={70} fill="#5d6268" stroke="#9aa3ad" strokeWidth={5} />
				{/* depth ruler */}
				<line x1={1560} y1={220} x2={1560} y2={850} stroke={C.dim} strokeWidth={3} />
				{[0, 100, 200, 300, 400, 500, 600].map((m) => (
					<g key={m}>
						<line x1={1540} y1={220 + (m / 600) * 630} x2={1580} y2={220 + (m / 600) * 630} stroke={C.dim} strokeWidth={3} />
						<text x={1600} y={232 + (m / 600) * 630} style={txt(30, C.dim, 700)}>{m} M</text>
					</g>
				))}
			</svg>
			<Label at={date} text="OCTOBER 2021" x={140} y={300} size={52} />
			<Label at={depth} text="PLAIN STEEL · 600 M" x={140} y={390} size={52} color={C.amber} />
		</AbsoluteFill>
	);
};

/** S30–31 (SIMPLIFIED): a carbon-fibre cylinder; its layers part, a little more each dive. No implosion. */
export const CarbonHull: React.FC<{dur: number; part: number}> = ({dur, part}) => {
	const f = useCurrentFrame();
	const k = tw(f, part, dur, 0, 1, ez.sweep);
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{Array.from({length: 9}).map((_, i) => {
					const gap = k * (i % 3 === 1 ? 14 : 4) * (0.5 + random('g' + i));
					return <rect key={i} x={420} y={300 + i * 52 + gap * (i - 4)} width={1080} height={44} rx={6} fill={i % 2 ? '#2a2d31' : '#34383d'} stroke="#55595f" strokeWidth={2} />;
				})}
				{/* hairline separations growing */}
				{Array.from({length: 6}).map((_, i) => (
					<line key={i} x1={520 + i * 160} y1={340 + (i % 3) * 100} x2={520 + i * 160 + 120 * k} y2={340 + (i % 3) * 100} stroke={C.red} strokeWidth={3} opacity={k} />
				))}
			</svg>
			<Label at={0} text="CARBON FIBRE" x={420} y={210} size={52} />
		</AbsoluteFill>
	);
};

/** S67–68 (SIMPLIFIED): a weld bead in open air; O and N drift in, tiny holes open, a hairline crack runs. */
export const BeadInAir: React.FC<{atoms: number; holes: number; crack: number}> = ({atoms, holes, crack}) => {
	const f = useCurrentFrame();
	const at = tw(f, atoms, atoms + 60, 0, 1, ez.sweep);
	const ho = tw(f, holes, holes + 40, 0, 1, ez.arrive);
	const cr = tw(f, crack, crack + 40, 0, 1, ez.sweep);
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<rect x={0} y={560} width={1920} height={240} fill={C.ti} opacity={0.85} />
				<path d="M0 560 C320 470 640 470 960 520 C1280 470 1600 470 1920 560 L1920 640 L0 640 Z" fill={C.weld} opacity={0.9} />
				{Array.from({length: 26}).map((_, i) => {
					const x0 = random('ax' + i) * 1920;
					const y0 = 60 + random('ay' + i) * 260;
					const x = x0 + 40 * noise2D('n' + i, f / 80, 0);
					const y = y0 + at * (500 - y0 + 40 * random('d' + i));
					const o = i % 2 === 0;
					return (
						<g key={i} opacity={Math.min(1, at * 2)}>
							<circle cx={x} cy={y} r={26} fill={o ? '#ff6b6b' : '#6bb8ff'} opacity={0.9} />
							<text x={x} y={y + 11} textAnchor="middle" style={txt(30, '#0a0d10')}>{o ? 'O' : 'N'}</text>
						</g>
					);
				})}
				{Array.from({length: 22}).map((_, i) => (
					<circle key={i} cx={120 + random('hx' + i) * 1680} cy={600 + random('hy' + i) * 150} r={6 + 10 * random('hr' + i)} fill="#0a0d10" opacity={ho} />
				))}
				<path d="M300 760 L520 700 L700 744 L900 690 L1120 735 L1300 680" stroke="#0a0d10" strokeWidth={6} fill="none" pathLength={1} strokeDasharray={`${cr} 1`} />
			</svg>
			<Label at={atoms} text="OXYGEN · NITROGEN" x={140} y={160} size={52} />
			<Label at={holes} text="TINY HOLES" x={140} y={840} size={48} color={C.amber} />
		</AbsoluteFill>
	);
};

/** S106 (cutaway, 2 s): syntactic foam close up: hollow glass bubbles in hard plastic. */
export const Microspheres: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{background: '#c9a227'}}>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{Array.from({length: 180}).map((_, i) => {
					const x = random('mx' + i) * 1920 + 6 * noise2D('m' + i, f / 120, 0);
					const y = random('my' + i) * 1080;
					const r = 18 + 46 * random('mr' + i);
					return (
						<g key={i}>
							<circle cx={x} cy={y} r={r} fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.7)" strokeWidth={3} />
							<circle cx={x - r * 0.35} cy={y - r * 0.35} r={r * 0.2} fill="rgba(255,255,255,0.6)" />
						</g>
					);
				})}
			</svg>
		</AbsoluteFill>
	);
};

/** S130–132: the depth ladder on the plate: 4,025 · 5,002 · 6,000 · 10,909 m (claims M10, M17). */
export const DepthLadder: React.FC<{china: number; six: number}> = ({china, six}) => {
	const f = useCurrentFrame();
	const rows: [string, number, string, number][] = [
		['NAUTILE · RAJU RAMESH', 4025, C.dim, 0],
		['NAUTILE · J. P. SINGH', 5002, C.dim, 0],
		['MATSYA · GOAL', 6000, C.amber, six],
		['CHINA · FENDOUZHE', 10909, '#9aa3ad', china],
	];
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{rows.map(([name, m, col, at], i) => {
					const k = at === 0 ? 1 : tw(f, at, at + 40, 0, 1, ez.sweep);
					const y = 220 + i * 170;
					const w = (m / 11000) * 900 * k;
					return (
						<g key={name}>
							<rect x={720} y={y} width={w} height={90} fill={col} opacity={0.85} />
							<text x={690} y={y + 60} textAnchor="end" style={txt(38, C.ink)}>{name}</text>
							<text x={740 + w} y={y + 62} style={txt(44, col)} opacity={k}>{m.toLocaleString('en-IN')} M</text>
						</g>
					);
				})}
			</svg>
		</AbsoluteFill>
	);
};

/** S110: a block of the yellow buoyancy foam; a crack draws itself across its face on "crack" (illustration) */
export const FoamCrack: React.FC<{dur: number; crack: number; slide?: boolean}> = ({dur, crack, slide}) => {
	const f = useCurrentFrame();
	const k = tw(f, crack, crack + 40, 0, 1, ez.sweep);
	const turn = tw(f, 0, dur, -8, 6, (t) => t);
	// S109 "had to come from France, and it arrived late": the block slides in from the left and settles
	const sx = slide ? tw(f, 0, Math.min(dur, 120), -1500, 0, ez.arrive) : 0;
	const pts = [
		[700, 330], [760, 420], [735, 470], [820, 560], [800, 610], [890, 700], [870, 760],
	];
	const n = Math.max(2, Math.ceil(k * pts.length));
	const path = pts.slice(0, n).map((p, i) => `${i ? 'L' : 'M'}${p[0]} ${p[1]}`).join(' ');
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<g transform={`translate(${sx} 0) rotate(${turn * 0.3} 960 560) translate(${turn * 4} 0)`}>
					{/* the block: front face and top, foam yellow */}
					<path d="M560 320 L1300 320 L1380 260 L640 260 Z" fill="#e2b93b" stroke="#8a6d1c" strokeWidth={4} />
					<rect x={560} y={320} width={740} height={460} fill="#d4a92c" stroke="#8a6d1c" strokeWidth={4} />
					<path d="M1300 320 L1380 260 L1380 720 L1300 780 Z" fill="#b38b1f" stroke="#8a6d1c" strokeWidth={4} />
					{Array.from({length: 60}).map((_, i) => (
						<circle key={i} cx={580 + random('fx' + i) * 700} cy={340 + random('fy' + i) * 420} r={2 + 3 * random('fr' + i)} fill="#f2d775" opacity={0.6} />
					))}
					{k > 0 ? <path d={path} fill="none" stroke="#1a1408" strokeWidth={9} strokeLinejoin="round" strokeLinecap="round" /> : null}
					{k > 0 ? <path d={path} fill="none" stroke={C.red} strokeWidth={3} opacity={0.8 * k} strokeLinejoin="round" /> : null}
				</g>
			</svg>
		</AbsoluteFill>
	);
};

/** S20: the water's push on a real fingernail (over the macro clip): an arrow comes down on the nail, the count runs. */
export const NailPress: React.FC<{arrow: number; kg: number; tip?: number}> = ({arrow, kg, tip = 750}) => {
	const f = useCurrentFrame();
	const ar = tw(f, arrow, arrow + 30, 0, 1, ez.arrive);
	const y = (1 - ar) * 140;
	// the macro clip slides slowly: the arrow stays on the nail
	const x = interpolate(f, [0, 82, 152, 257], [805, 730, 624, 420], {extrapolateLeft: 'clamp', extrapolateRight: 'extend'});
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<g opacity={ar} transform={`translate(${x} ${tip - y})`}>
					<rect x={-22} y={-440} width={44} height={330} fill={C.amber} />
					<path d="M-66 -110 L66 -110 L0 0 Z" fill={C.amber} />
				</g>
			</svg>
			<Count a={kg} b={kg + 40} from={0} to={600} x={1180} y={240} size={130} unit="KG" color={C.amber} />
			<Label at={kg} text="ON ONE FINGERNAIL" x={1180} y={160} size={44} />
		</AbsoluteFill>
	);
};

/** S21: a full-grown buffalo on one fingernail, to scale (owner, r3: near to reality). World units are
 *  centimetres: the finger is 1.6 cm thick, the buffalo 1.4 m at the shoulder. The camera starts on the fingertip
 *  under a front hoof and pulls back until the whole animal stands over it. */
export const BuffaloTrueScale: React.FC<{dur: number; pull?: number}> = ({dur, pull = 54}) => {
	const f = useCurrentFrame();
	const t = tw(f, 4, 4 + pull, 0, 1, ez.sweep);
	const drift = tw(f, 4 + pull, Math.max(5 + pull, dur), 0, 1, (x) => x);
	const k = 30 * Math.pow(3.75 / 30, t) * (1 - 0.05 * drift); // px per cm
	const cx = 6 + (-26 - 6) * t;
	const cy = -8 + (-70 + 8) * t;
	const sx = 960 + (1290 - 960) * t;
	const sy = 700 + (600 - 700) * t;
	const sink = 0.35 * tw(f, 0, 14, 0, 1, ez.arrive); // the nail gives under the hoof
	const end = tw(f, 4 + pull - 8, 4 + pull + 14, 0, 1, ez.arrive);
	const body =
		'M-166 -118 C-152 -140 -112 -141 -82 -135 C-44 -130 -12 -141 14 -147 C36 -148 52 -138 64 -126 L80 -120 ' +
		'C97 -114 110 -100 117 -82 C121 -71 115 -62 104 -64 C92 -66 80 -74 71 -85 C61 -80 52 -70 45 -60 C41 -50 35 -46 27 -46 ' +
		'L13 -50 L9 -24 L10 -9 L12 0 L-2 0 L-2 -9 L-4 -25 L-9 -53 C-40 -57 -90 -59 -118 -66 L-121 -42 L-128 -23 L-126 -9 L-124 0 L-139 0 L-139 -9 ' +
		'L-142 -25 L-147 -47 C-159 -70 -170 -95 -166 -118 Z';
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<defs>
					<linearGradient id="bufBody" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor="#3d4046" />
						<stop offset="0.22" stopColor="#202226" />
						<stop offset="1" stopColor="#0d0f12" />
					</linearGradient>
					<linearGradient id="bufSkin" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor="#e2b391" />
						<stop offset="0.6" stopColor="#c58f6d" />
						<stop offset="1" stopColor="#8c5f47" />
					</linearGradient>
					<linearGradient id="bufNail" x1="0" y1="0" x2="1" y2="1">
						<stop offset="0" stopColor="#f6e6dc" />
						<stop offset="1" stopColor="#dcbcaa" />
					</linearGradient>
					<radialGradient id="bufShade" cx="0.5" cy="0.5" r="0.5">
						<stop offset="0" stopColor="rgba(0,0,0,0.75)" />
						<stop offset="1" stopColor="rgba(0,0,0,0)" />
					</radialGradient>
				</defs>
				<g transform={`translate(${sx} ${sy}) scale(${k}) translate(${-cx} ${-cy})`}>
					{/* ground shadow */}
					<ellipse cx={-64} cy={1} rx={130} ry={9} fill="url(#bufShade)" />
					{/* the hand lying on the plate, one finger out under the hoof */}
					<g transform={`translate(0 ${sink})`}>
						<path d="M11 -1.9 C13 -2.6 16 -3.2 19 -3.2 C24 -3.4 27 -3 30 -2.9 L70 -4.6 L70 0 L11 0 Z" fill="url(#bufSkin)" />
						<path d="M-3.6 -0.8 C-3.6 -1.5 -2.9 -1.62 -2 -1.62 L12 -1.9 L12 0 L-2.4 0 C-3.2 0 -3.6 -0.3 -3.6 -0.8 Z" fill="url(#bufSkin)" />
						<path d="M-3.2 -1.2 C-3.1 -1.62 -2.6 -1.7 -1.8 -1.7 L-0.9 -1.7 C-1.0 -1.2 -1.6 -0.95 -3.2 -1.2 Z" fill="url(#bufNail)" transform="translate(0.2 0)" />
						<rect x={-3.0} y={-1.78} width={2.3} height={0.2} rx={0.1} fill="url(#bufNail)" />
					</g>
					{/* far-side legs */}
					<path d="M-20 -56 L-23 -24 L-22 -9 L-20 0 L-33 0 L-33 -9 L-35 -25 L-38 -56 Z" fill="#090a0c" />
					<path d="M-104 -62 L-108 -40 L-114 -23 L-112 -9 L-110 0 L-124 0 L-124 -9 L-127 -25 L-130 -60 Z" fill="#090a0c" />
					{/* tail */}
					<path d="M-165 -116 C-174 -100 -174 -70 -171 -44" stroke="#15171a" strokeWidth={3} fill="none" strokeLinecap="round" />
					<ellipse cx={-171} cy={-38} rx={3} ry={8} fill="#0b0c0e" />
					{/* the far horn, the body, the near horn */}
					<path d="M86 -120 C82 -144 62 -160 40 -160 C58 -153 70 -140 76 -120 Z" fill="#6f6a60" />
					<path d={body} fill="url(#bufBody)" />
					<path d="M-150 -132 C-112 -141 -44 -129 14 -146" stroke="rgba(190,205,220,0.35)" strokeWidth={1.6} fill="none" strokeLinecap="round" />
					<path d="M79 -122 C73 -147 50 -164 26 -162 C46 -155 60 -142 67 -122 Z" fill="#a39c8c" />
					<path d="M62 -116 C54 -114 49 -108 50 -103 C56 -104 61 -109 62 -116 Z" fill="#0b0c0e" />
					<circle cx={92} cy={-103} r={1.8} fill="#0a0a0a" />
					<circle cx={92.5} cy={-103.5} r={0.5} fill="#b9c2cc" />
					<ellipse cx={112} cy={-72} rx={2} ry={1.4} fill="#050506" />
					{/* hooves */}
					<path d="M-2.6 -6 L12.6 -6 L13.4 0 L-3.4 0 Z" fill="#2c2a27" />
					<path d="M-139.6 -6 L-123.4 -6 L-122.6 0 L-140.4 0 Z" fill="#2c2a27" />
				</g>
				{/* where the finger is, once the camera is wide */}
				<g opacity={end}>
					<circle cx={sx + (5 - cx) * k} cy={sy + (-1 - cy) * k} r={46} fill="none" stroke={C.amber} strokeWidth={5} />
				</g>
			</svg>
			<Label at={4 + pull - 8} text="ONE FINGERNAIL" x={1420} y={930} size={44} color={C.amber} />
			<Count a={-60} b={-20} from={0} to={600} x={170} y={230} size={120} unit="KG" color={C.amber} />
			<Label at={0} text="A FULL-GROWN BUFFALO" x={170} y={400} size={44} />
			<Label at={0} text="DRAWN TO SCALE" x={170} y={160} size={40} color={C.dim} />
		</AbsoluteFill>
	);
};
