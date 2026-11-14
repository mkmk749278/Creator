import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {ez, tw} from './kit';

// The film's drawings (word_map.md, R): each sits on the drafting plate (kit Plate) and moves only on its words.
// Every cue is a frame inside the shot (the scene passes word frame − shot start + lead).

const ink = C.ink;
const T: React.FC<{x: number; y: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'; weight?: number; mono?: boolean; o?: number; children: React.ReactNode}> = ({
	x,
	y,
	size = 44,
	color = ink,
	anchor = 'start',
	weight = 800,
	mono,
	o = 1,
	children,
}) => (
	<text x={x} y={y} fontSize={size} fill={color} textAnchor={anchor} fontFamily={mono ? F.mono : F.label} fontWeight={weight} opacity={o} style={{letterSpacing: mono ? 0 : 1}}>
		{children}
	</text>
);

const Svg: React.FC<{children: React.ReactNode}> = ({children}) => (
	<AbsoluteFill>
		<svg width={1920} height={1080} viewBox="0 0 1920 1080">
			<defs>
				<filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
					<feGaussianBlur stdDeviation="6" result="b" />
					<feMerge>
						<feMergeNode in="b" />
						<feMergeNode in="SourceGraphic" />
					</feMerge>
				</filter>
				<pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
					<line x1="0" y1="0" x2="0" y2="14" stroke={C.dim} strokeWidth="3" strokeOpacity="0.5" />
				</pattern>
			</defs>
			{children}
		</svg>
	</AbsoluteFill>
);

// ---------------------------------------------------------------- the carrier in plan (deck seen from above)
const DECK_X0 = 260;
const DECK_X1 = 1660; // 262 m → 1400 px: 5.34 px a metre
export const PX_M = (DECK_X1 - DECK_X0) / 262;
const deckPath = (cy: number) => {
	const hw = 165;
	const x0 = DECK_X0;
	const x1 = DECK_X1;
	return `M${x0 + 30} ${cy - hw * 0.8} L${x1 - 260} ${cy - hw} Q${x1 - 60} ${cy - hw * 0.95} ${x1} ${cy - 40} L${x1} ${cy + 40} Q${x1 - 60} ${cy + hw * 0.95} ${x1 - 260} ${cy + hw} L${x0 + 30} ${cy + hw * 0.8} Q${x0} ${cy} ${x0 + 30} ${cy - hw * 0.8} Z`;
};
const RAMP_X = DECK_X1 - 37 * PX_M;

/** S10: the deck plan; the slot draws from the stern and stops dead at the ramp; a tiny 17 m track beside it.
 *  `oldAt` (S2, viewer review r3 fix 1): the first Vikrant of 1961 slides in above at the same scale: a flat deck, no
 *  ramp, its steam catapult glowing at the bow; today's slot is then drawn dashed (missing). */
export const DeckPlan: React.FC<{slotAt: number; slotEnd: number; modelAt?: number; oldAt?: number}> = ({slotAt, slotEnd, modelAt, oldAt}) => {
	const f = useCurrentFrame();
	const cy = oldAt === undefined ? 520 : 600;
	const k = tw(f, slotAt, slotEnd, 0, 1, ez.sweep);
	const x0 = DECK_X0 + 150;
	const xs = x0 + (RAMP_X - 6 - x0) * k;
	const stop = tw(f, slotEnd, slotEnd + 10, 0, 1, ez.arrive);
	const m = modelAt === undefined ? 0 : tw(f, modelAt, modelAt + 24, 0, 1, ez.arrive);
	const o = oldAt === undefined ? 0 : tw(f, oldAt, oldAt + 30, 0, 1, ez.arrive);
	const oc = oldAt === undefined ? 0 : tw(f, oldAt + 24, oldAt + 54, 0, 1, ez.sweep);
	// the 1961 ship: about 213 m, a straight flat deck with an angled landing deck to port
	const oy = 285;
	const oL = 213 * PX_M;
	const ox0 = DECK_X0;
	const ox1 = DECK_X0 + oL;
	const old = `M${ox0 + 20} ${oy - 48} L${ox0 + oL * 0.32} ${oy - 52} L${ox0 + oL * 0.62} ${oy - 92} L${ox0 + oL * 0.78} ${oy - 92} L${ox0 + oL * 0.8} ${oy - 52} L${ox1 - 80} ${oy - 46} Q${ox1 - 10} ${oy - 30} ${ox1} ${oy} Q${ox1 - 10} ${oy + 30} ${ox1 - 80} ${oy + 46} L${ox0 + 20} ${oy + 48} Q${ox0} ${oy} ${ox0 + 20} ${oy - 48} Z`;
	return (
		<Svg>
			{o > 0 ? (
				<g opacity={o} transform={`translate(${(1 - o) * -80} 0)`}>
					<path d={old} fill="#3a3326" stroke={C.amber} strokeWidth={3} />
					<line x1={ox0 + oL * 0.3} y1={oy + 10} x2={ox0 + oL * 0.75} y2={oy - 70} stroke={C.amber} strokeOpacity={0.45} strokeWidth={3} strokeDasharray="20 16" />
					<rect x={ox0 + oL * 0.66} y={oy + 52} width={150} height={30} fill="#3a3326" stroke={C.amber} strokeWidth={2} />
					<line x1={ox1 - 70 - 48 * PX_M * oc} y1={oy - 16} x2={ox1 - 70} y2={oy - 16} stroke={C.slot} strokeWidth={12} strokeLinecap="round" filter="url(#glow)" />
					<T x={ox0 + 420} y={oy - 110} size={46} color={C.slot}>FIRST VIKRANT · 1961</T>
					<T x={ox0 + 40} y={oy + 90} size={34} color={C.amber}>FLAT DECK · STEAM CATAPULT AT THE BOW</T>
				</g>
			) : null}
			<path d={deckPath(cy)} fill="#2b3138" stroke={C.dim} strokeWidth={3} />
			<rect x={RAMP_X} y={cy - 150} width={DECK_X1 - RAMP_X} height={300} fill="url(#hatch)" />
			<line x1={DECK_X0 + 80} y1={cy} x2={DECK_X1 - 10} y2={cy} stroke={ink} strokeOpacity={0.35} strokeWidth={4} strokeDasharray="30 22" />
			<rect x={DECK_X0 + 640} y={cy + 164} width={240} height={46} fill="#3a424b" stroke={C.dim} strokeWidth={2} />
			<T x={RAMP_X + 20} y={cy + 210} size={36} color={C.dim}>RAMP</T>
			{o > 0 ? <T x={DECK_X0 + 40} y={cy + 230} size={40} color={ink} o={o}>VIKRANT · TODAY</T> : null}
			{k > 0 ? (
				<line x1={x0} y1={cy} x2={xs} y2={cy} stroke={C.slot} strokeWidth={12} strokeLinecap="round" strokeDasharray={oldAt === undefined ? undefined : '34 22'} strokeOpacity={oldAt === undefined ? 1 : 0.8} filter="url(#glow)" />
			) : null}
			{stop > 0 ? <line x1={RAMP_X - 6} y1={cy - 46 * stop} x2={RAMP_X - 6} y2={cy + 46 * stop} stroke={C.slot} strokeWidth={10} /> : null}
			{m > 0 ? (
				<g opacity={m}>
					<line x1={DECK_X0 + 520} y1={cy + 230} x2={DECK_X0 + 520 + 17 * PX_M} y2={cy + 230} stroke={C.slot} strokeWidth={14} strokeLinecap="round" filter="url(#glow)" />
					<T x={DECK_X0 + 520 + 17 * PX_M + 30} y={cy + 244} size={42} color={C.slot}>TEST MODEL · SAME SCALE</T>
				</g>
			) : null}
		</Svg>
	);
};

// ---------------------------------------------------------------- an Indian home's electricity meter
/** a digital meter (the kind on Indian walls): the kWh window counts from a to b between frames f0 and f1 */
export const Meter: React.FC<{x: number; y: number; scale?: number; a: number; b: number; f0: number; f1: number; label?: string; hot?: boolean}> = ({x, y, scale = 1, a, b, f0, f1, label, hot}) => {
	const f = useCurrentFrame();
	const v = tw(f, f0, f1, a, b, (t) => t);
	const pulse = f >= f0 && f <= f1 ? (Math.floor(f / 4) % 2 === 0 ? 1 : 0.25) : 0.15;
	return (
		<g transform={`translate(${x} ${y}) scale(${scale})`}>
			<rect x={-190} y={-260} width={380} height={520} rx={28} fill="#d9dde0" stroke="#7a8590" strokeWidth={6} />
			<rect x={-150} y={-200} width={300} height={110} rx={10} fill="#1c2a22" />
			<text x={130} y={-122} fontFamily={F.mono} fontWeight={700} fontSize={58} fill="#9effa8" textAnchor="end">
				{v.toFixed(1).padStart(6, '0')}
			</text>
			<text x={0} y={-50} fontFamily={F.label} fontWeight={800} fontSize={34} fill="#30383f" textAnchor="middle">kWh · UNITS</text>
			<circle cx={-100} cy={40} r={16} fill={hot ? C.red : '#e6442e'} opacity={pulse} />
			<text x={-70} y={52} fontFamily={F.label} fontWeight={700} fontSize={28} fill="#30383f">IMP/kWh</text>
			<rect x={-150} y={110} width={300} height={90} rx={8} fill="#c4c9cd" />
			{label ? (
				<text x={0} y={300} fontFamily={F.label} fontWeight={800} fontSize={46} fill={ink} textAnchor="middle">
					{label}
				</text>
			) : null}
		</g>
	);
};

export const MeterSolo: React.FC<{a: number; b: number; f0: number; f1: number; label?: string}> = (p) => (
	<Svg>
		<Meter x={960} y={520} {...p} />
	</Svg>
);

// ---------------------------------------------------------------- the ramp, side on
const rampCurve = (x0: number, y0: number, len: number, deg: number) => {
	const n = 30;
	const R = len / ((Math.max(0.01, deg) * Math.PI) / 180);
	const pts: string[] = [];
	for (let i = 0; i <= n; i++) {
		const th = ((deg * Math.PI) / 180) * (i / n);
		pts.push(`${x0 + R * Math.sin(th)},${y0 - R * (1 - Math.cos(th))}`);
	}
	return pts;
};

/** S18–22: the ramp in side elevation, no moving parts; S31–32: a heavy, slow aircraft cannot leave it */
export const RampSide: React.FC<{heavyAt?: number; dropAt?: number; noPartsAt?: number}> = ({heavyAt, dropAt, noPartsAt}) => {
	const f = useCurrentFrame();
	const y0 = 480;
	const pts = rampCurve(900, y0, 600, 14);
	const last = pts[pts.length - 1].split(',').map(Number);
	const deck = `M100 ${y0} L900 ${y0} L${pts.join(' L')} L${last[0]} ${y0 + 160} L100 ${y0 + 160} Z`;
	const h = heavyAt === undefined ? -1 : tw(f, heavyAt, (dropAt ?? heavyAt + 90) , 0, 1, ez.cam);
	const fall = dropAt === undefined ? 0 : tw(f, dropAt, dropAt + 50, 0, 1, (t) => t * t);
	const px = 300 + (last[0] - 300) * Math.max(0, h);
	const py = px < 900 ? y0 : y0 - (last[1] < y0 ? (y0 - last[1]) * ((px - 900) / (last[0] - 900)) : 0);
	const np = noPartsAt === undefined ? 0 : tw(f, noPartsAt, noPartsAt + 20, 0, 1, ez.arrive);
	return (
		<Svg>
			<path d={`M60 ${y0 + 160} L1860 ${y0 + 160}`} stroke={C.sea} strokeWidth={6} />
			<path d={deck} fill="#2b3138" stroke={C.dim} strokeWidth={4} />
			<polyline points={pts.join(' ')} fill="none" stroke={ink} strokeWidth={6} />
			{np > 0 ? <T x={1100} y={y0 + 100} size={40} color={C.dim} o={np}>NO MOVING PARTS</T> : null}
			{h >= 0 ? (
				<g transform={`translate(${px} ${py + fall * 260}) rotate(${-8 + fall * 35})`}>
					<path d="M-150 -40 L120 -40 Q170 -30 175 -10 L120 0 L-150 0 Z" fill="#7d8790" stroke={ink} strokeWidth={3} />
					<path d="M-40 -40 L-10 -95 L30 -95 L20 -40 Z" fill="#7d8790" stroke={ink} strokeWidth={3} />
					<ellipse cx={-10} cy={-80} rx={80} ry={14} fill="#c9ced3" stroke={ink} strokeWidth={3} />
					<rect x={-150} y={-90} width={30} height={50} fill="#7d8790" stroke={ink} strokeWidth={3} />
				</g>
			) : null}
		</Svg>
	);
};

// ---------------------------------------------------------------- what each one sees: radar circles from above
export const Radar: React.FC<{heliAt: number; planeAt: number; contactAt: number}> = ({heliAt, planeAt, contactAt}) => {
	const f = useCurrentFrame();
	const cx = 960;
	const cy = 520;
	const r1 = 150 * tw(f, heliAt, heliAt + 30, 0, 1, ez.arrive);
	const r2 = 360 * tw(f, planeAt, planeAt + 90, 0, 1, ez.cam);
	const c = tw(f, contactAt, contactAt + 12, 0, 1, ez.arrive);
	const sweep = (f * 3) % 360;
	return (
		<Svg>
			<rect width={1920} height={1080} fill="#0b2232" opacity={0.85} />
			{r2 > 0 ? (
				<g>
					<circle cx={cx} cy={cy} r={r2} fill={C.cyan} fillOpacity={0.08} stroke={C.cyan} strokeWidth={4} />
					<line x1={cx} y1={cy} x2={cx + r2 * Math.cos((sweep * Math.PI) / 180)} y2={cy + r2 * Math.sin((sweep * Math.PI) / 180)} stroke={C.cyan} strokeOpacity={0.6} strokeWidth={3} />
					<T x={cx + r2 * 0.72} y={cy - r2 * 0.74} size={38} color={C.cyan}>PLANE</T>
				</g>
			) : null}
			{r1 > 0 ? (
				<g>
					<circle cx={cx} cy={cy} r={r1} fill={C.amber} fillOpacity={0.12} stroke={C.amber} strokeWidth={4} />
					<T x={cx - r1 - 20} y={cy - r1 * 0.6} size={38} color={C.amber} anchor="end">HELICOPTER</T>
				</g>
			) : null}
			{[0, 1, 2].map((i) => {
				const ph = ((f + i * 40) % 120) / 120;
				return <circle key={i} cx={cx} cy={cy} r={20 + 120 * ph} fill="none" stroke={ink} strokeOpacity={0.35 * (1 - ph)} strokeWidth={3} />;
			})}
			<path d={`M${cx - 30} ${cy + 8} L${cx + 26} ${cy + 8} L${cx + 40} ${cy} L${cx + 26} ${cy - 8} L${cx - 30} ${cy - 8} Z`} fill={ink} />
			{c > 0 ? (
				<g opacity={c}>
					<circle cx={cx + 290} cy={cy + 130} r={14} fill={C.red} />
					<circle cx={cx + 290} cy={cy + 130} r={14 + 30 * ((f % 40) / 40)} fill="none" stroke={C.red} strokeWidth={3} opacity={1 - (f % 40) / 40} />
				</g>
			) : null}
		</Svg>
	);
};

// ---------------------------------------------------------------- the pressure cooker (drawn: no real clip exists)
export const Cooker: React.FC<{buildAt: number; burstAt: number}> = ({buildAt, burstAt}) => {
	const f = useCurrentFrame();
	const tremble = f >= buildAt && f < burstAt ? 3 * Math.sin(f * 1.7) : 0;
	const lift = tw(f, burstAt, burstAt + 8, 0, 34, ez.arrive) * (1 - tw(f, burstAt + 40, burstAt + 70, 0, 1));
	const puff = tw(f, burstAt, burstAt + 40, 0, 1, (t) => t);
	return (
		<Svg>
			<g transform="translate(960 470) scale(1.15)">
				<ellipse cx={0} cy={210} rx={300} ry={40} fill="#000" opacity={0.35} />
				<path d="M-260 -60 L260 -60 L240 200 Q0 240 -240 200 Z" fill="#b9bfc4" stroke="#5d666e" strokeWidth={6} />
				<rect x={-280} y={-100} width={560} height={50} rx={14} fill="#9aa2a9" stroke="#5d666e" strokeWidth={6} />
				<rect x={260} y={-92} width={300} height={34} rx={14} fill="#1d1f22" />
				<rect x={-34} y={-150} width={68} height={56} rx={8} fill="#6f7880" />
				<g transform={`translate(${tremble} ${-lift})`}>
					<rect x={-26} y={-200} width={52} height={52} rx={10} fill="#3a3f45" stroke="#1d1f22" strokeWidth={4} />
				</g>
				{puff > 0
					? [0, 1, 2, 3, 4].map((i) => (
							<circle key={i} cx={(i - 2) * 30 * puff} cy={-200 - 260 * puff * (0.6 + i * 0.12)} r={40 + 90 * puff} fill="#f2efe8" opacity={0.55 * (1 - puff)} />
						))
					: null}
			</g>
		</Svg>
	);
};

// ---------------------------------------------------------------- one boiler, two jobs
export const SteamSplit: React.FC<{propAt: number; slotAt: number; redAt: number}> = ({propAt, slotAt, redAt}) => {
	const f = useCurrentFrame();
	const a = tw(f, propAt, propAt + 30, 0, 1, ez.arrive);
	const b = tw(f, slotAt, slotAt + 30, 0, 1, ez.arrive);
	const red = tw(f, redAt, redAt + 20, 0, 1, ez.arrive);
	const flow = -(f * 6) % 60;
	const shake = red > 0.5 ? 2.5 * Math.sin(f * 2.3) : 0;
	return (
		<Svg>
			<g transform={`translate(${shake} 0)`}>
				<rect x={240} y={420} width={420} height={300} rx={26} fill="#3a3330" stroke={C.amber} strokeWidth={5} />
				<T x={450} y={590} size={46} anchor="middle">BOILER</T>
				<circle cx={600} cy={460} r={34} fill="#e9e5dc" stroke="#7a6a50" strokeWidth={5} />
				<line x1={600} y1={460} x2={600 + 26 * Math.cos(Math.PI * (1.15 - 0.95 * red))} y2={460 - 26 * Math.sin(Math.PI * (1.15 - 0.95 * red))} stroke={red > 0.6 ? C.red : '#111'} strokeWidth={6} />
			</g>
			<path d="M660 520 C 900 520, 900 300, 1080 300" fill="none" stroke={C.amber} strokeWidth={22} strokeOpacity={0.25 + 0.75 * a} />
			<path d="M660 520 C 900 520, 900 300, 1080 300" fill="none" stroke="#fff3d6" strokeWidth={8} strokeDasharray="20 40" strokeDashoffset={flow} opacity={a} />
			<path d="M660 620 C 900 620, 900 800, 1080 800" fill="none" stroke={C.amber} strokeWidth={22} strokeOpacity={0.25 + 0.75 * b} />
			<path d="M660 620 C 900 620, 900 800, 1080 800" fill="none" stroke="#fff3d6" strokeWidth={8} strokeDasharray="20 40" strokeDashoffset={flow} opacity={b} />
			<g opacity={0.3 + 0.7 * a}>
				<circle cx={1190} cy={300} r={70} fill="none" stroke={ink} strokeWidth={6} />
				{[0, 1, 2].map((i) => (
					<path key={i} d="M0 0 C 20 -30, 50 -40, 66 -10 Z" fill={ink} transform={`translate(1190 300) rotate(${i * 120 + f * 4 * a})`} />
				))}
				<T x={1300} y={316} size={46}>PROPELLERS</T>
			</g>
			<g opacity={0.3 + 0.7 * b}>
				<rect x={1100} y={786} width={300} height={28} fill={C.slot} filter="url(#glow)" />
				<T x={1430} y={816} size={46}>CATAPULT</T>
			</g>
		</Svg>
	);
};

// ---------------------------------------------------------------- the first Vikrant becomes a ramp ship (side elevation)
export const Elevation61: React.FC<{sealAt: number; liftAt: number}> = ({sealAt, liftAt}) => {
	const f = useCurrentFrame();
	const seal = tw(f, sealAt, sealAt + 40, 0, 1, ez.sweep);
	const lift = tw(f, liftAt, liftAt + 45, 0, 1, ez.sweep);
	const y0 = 520;
	const x0 = 260;
	const x1 = 1660;
	const rampLen = 340;
	// viewer review r3 fix 6: the change must read at a glance: the slot strikes out, the ramp rises in caution yellow
	const pts = rampCurve(x1 - rampLen, y0, rampLen, 15 * lift);
	const end = pts[pts.length - 1].split(',').map(Number);
	const hull = `M${x0} ${y0} L${x1 - rampLen} ${y0} L${pts.join(' L')} Q${end[0] + 40} ${y0 + 80} ${end[0] - 60} ${y0 + 230} L${x0 + 120} ${y0 + 230} Q${x0 + 20} ${y0 + 200} ${x0} ${y0} Z`;
	return (
		<Svg>
			<rect x={0} y={y0 + 170} width={1920} height={400} fill={C.sea} opacity={0.35} />
			<path d={hull} fill="#3a4048" stroke={ink} strokeWidth={4} />
			<rect x={x0 + 700} y={y0 - 120} width={160} height={120} fill="#4a525c" stroke={ink} strokeWidth={3} />
			<rect x={x0 + 740} y={y0 - 190} width={60} height={70} fill="#4a525c" stroke={ink} strokeWidth={3} />
			<line x1={x1 - 520} y1={y0 - 6} x2={x1 - 30} y2={y0 - 6} stroke={C.slot} strokeWidth={10} opacity={1 - 0.75 * seal} filter="url(#glow)" />
			<T x={x1 - 520} y={y0 - 40} size={44} color={C.slot} o={1 - 0.6 * seal}>STEAM CATAPULT</T>
			{seal > 0 ? <line x1={x1 - 530} y1={y0 - 34} x2={x1 - 530 + 380 * seal} y2={y0 - 34} stroke={C.red} strokeWidth={8} strokeLinecap="round" /> : null}
			{seal > 0.6 ? <T x={x1 - 520} y={y0 + 70} size={44} color={C.red} o={tw(seal, 0.6, 1, 0, 1)}>REMOVED</T> : null}
			{lift > 0 ? <polyline points={pts.join(' ')} fill="none" stroke={C.slot} strokeWidth={10} strokeLinecap="round" filter="url(#glow)" opacity={lift} /> : null}
			<T x={x1 - rampLen + 40} y={y0 - 120} size={56} color={C.slot} o={lift}>A RAMP</T>
		</Svg>
	);
};

// ---------------------------------------------------------------- the new Vikrant in cutaway: full under the ramp
export const HullCut: React.FC<{turbAt: number; fillAt: number}> = ({turbAt, fillAt}) => {
	const f = useCurrentFrame();
	const y0 = 430;
	const x0 = 200;
	const x1 = 1720;
	const rampLen = 230;
	const pts = rampCurve(x1 - rampLen, y0, rampLen, 14);
	const end = pts[pts.length - 1].split(',').map(Number);
	const hull = `M${x0} ${y0} L${x1 - rampLen} ${y0} L${pts.join(' L')} Q${end[0] + 30} ${y0 + 120} ${end[0] - 90} ${y0 + 330} L${x0 + 140} ${y0 + 330} Q${x0 + 20} ${y0 + 290} ${x0} ${y0} Z`;
	const fill = tw(f, fillAt, fillAt + 50, 0, 1, ez.sweep);
	const cells: React.ReactNode[] = [];
	let k = 0;
	for (let cx = x1 - rampLen - 60; cx < end[0] - 70; cx += 62) {
		for (let cy = y0 + 20; cy < y0 + 300; cy += 56) {
			const order = k / 28;
			const o = Math.max(0, Math.min(1, fill * 1.6 - order));
			cells.push(<rect key={`${cx}-${cy}`} x={cx} y={cy} width={56} height={50} fill={k % 3 === 0 ? '#6b5a44' : k % 3 === 1 ? '#555e68' : '#4b4f55'} stroke="#20252a" strokeWidth={2} opacity={o} />);
			k++;
		}
	}
	return (
		<Svg>
			<rect x={0} y={y0 + 250} width={1920} height={400} fill={C.sea} opacity={0.35} />
			<path d={hull} fill="#20262c" stroke={ink} strokeWidth={4} />
			{[0, 1, 2].map((i) => (
				<line key={i} x1={x0 + 40} y1={y0 + 80 + i * 80} x2={x1 - rampLen - 40} y2={y0 + 80 + i * 80} stroke={C.dim} strokeOpacity={0.35} strokeWidth={2} />
			))}
			{[0, 1, 2, 3].map((i) => {
				const o = tw(f, turbAt + i * 14, turbAt + i * 14 + 16, 0, 1, ez.arrive);
				return (
					<g key={i}>
						<rect x={620 + i * 120} y={y0 + 200} width={96} height={60} rx={10} fill={C.amber} fillOpacity={0.15 + 0.75 * o} stroke={C.amber} strokeWidth={3} filter={o > 0.5 ? 'url(#glow)' : undefined} />
					</g>
				);
			})}
			<T x={620} y={y0 + 300} size={36} color={C.amber}>4 GAS TURBINES</T>
			{cells}
			<T x={x1 - rampLen - 60} y={y0 - 40} size={36} color={C.dim} o={fill}>NO ROOM BELOW</T>
		</Svg>
	);
};

// ---------------------------------------------------------------- S1: the ceiling fan's motor, unrolled
/** coils on a ring open along a seam and unroll into a straight line, which settles into a deck slot; a lit patch
 *  runs down it (SIMPLIFIED) */
export const FanUnroll: React.FC<{glowAt: number; openAt: number; unrollEnd: number; dropAt: number; runAt?: number; patchAt?: number; jetAt?: number}> = ({
	glowAt,
	openAt,
	unrollEnd,
	dropAt,
	runAt,
	patchAt,
	jetAt,
}) => {
	const f = useCurrentFrame();
	const n = 36;
	const R = 230;
	const u = tw(f, openAt, unrollEnd, 0, 1, ez.sweep);
	const drop = tw(f, dropAt, dropAt + 40, 0, 1, ez.sweep);
	const glow = tw(f, glowAt, glowAt + 20, 0, 1, ez.arrive);
	const chase = (f * 0.12) % n;
	const len = 1500;
	const lineY = 540 + 230 * drop;
	const run = runAt === undefined ? -1 : ((f - runAt) * 0.012) % 1.4;
	const patch = patchAt !== undefined && f >= patchAt ? Math.min(1, (f - patchAt) / 150) : -1;
	const coils = [];
	for (let i = 0; i < n; i++) {
		const th = -Math.PI / 2 + (i / n) * Math.PI * 2;
		const cx = 960 + R * Math.cos(th);
		const cy = 540 + R * Math.sin(th);
		const lx = 960 - len / 2 + (i / (n - 1)) * len;
		const x = cx + (lx - cx) * u;
		const y = cy + (lineY - cy) * u;
		const rot = ((th * 180) / Math.PI + 90) * (1 - u);
		let lit = glow * (u < 0.05 ? (Math.abs(i - chase) < 3 || Math.abs(i - chase - n) < 3 ? 1 : 0.25) : 0.25);
		if (run >= 0 && u > 0.95) {
			lit = Math.abs(i / (n - 1) - run) < 0.08 ? 1 : 0.2;
		}
		if (patch >= 0) {
			lit = Math.abs(i / (n - 1) - patch) < 0.06 ? 1 : 0.15;
		}
		coils.push(
			<g key={i} transform={`translate(${x} ${y}) rotate(${rot})`}>
				<rect x={-14} y={-34} width={28} height={68} rx={8} fill={C.copper} stroke="#7a4a20" strokeWidth={3} />
				<rect x={-14} y={-34} width={28} height={68} rx={8} fill="#ffd9a0" opacity={lit} filter={lit > 0.6 ? 'url(#glow)' : undefined} />
			</g>,
		);
	}
	const shuttleX = 960 - len / 2 + len * Math.max(0, patch);
	return (
		<Svg>
			{drop > 0 ? (
				<g opacity={drop}>
					<rect x={960 - len / 2 - 60} y={lineY - 60} width={len + 120} height={50} fill="#2b3138" />
					<rect x={960 - len / 2 - 60} y={lineY + 46} width={len + 120} height={50} fill="#2b3138" />
					<rect x={960 - len / 2 - 60} y={lineY - 14} width={len + 120} height={28} fill={C.slot} opacity={0.25} />
					<T x={960 - len / 2 - 60} y={lineY - 80} size={36} color={C.dim}>UNDER THE DECK · ABOUT 100 M</T>
				</g>
			) : null}
			{u < 0.02 ? <circle cx={960} cy={540} r={R - 50} fill="#2b3138" stroke={C.dim} strokeWidth={4} /> : null}
			{coils}
			{jetAt !== undefined && f >= jetAt && patch >= 0 ? (
				<g transform={`translate(${shuttleX} ${lineY - 70})`}>
					<rect x={-40} y={-10} width={80} height={20} fill={ink} />
					<path d="M-130 -60 L110 -60 L150 -40 L110 -20 L-130 -20 Z" fill="#7d8790" stroke={ink} strokeWidth={3} />
				</g>
			) : null}
		</Svg>
	);
};

// ---------------------------------------------------------------- the working, on screen (OUR CALCULATION)
export const Working: React.FC<{at: number[]}> = ({at}) => {
	const f = useCurrentFrame();
	const lines: [string, string][] = [
		['½ × 30,000 kg × (66.7 m/s)²', ink],
		['≈ 67 MJ  ÷ 3.6 MJ a unit', ink],
		['≈ 19 UNITS', C.slot],
		['98 units a month → about 6 DAYS', ink],
		['× ₹6.5 a unit ≈ ₹120 · UNDER ₹200', C.green],
	];
	return (
		<Svg>
			{lines.map(([t, c], i) => {
				const o = tw(f, at[i] ?? 99999, (at[i] ?? 99999) + 14, 0, 1, ez.arrive);
				return (
					<g key={i} opacity={o} transform={`translate(${(1 - o) * 30} 0)`}>
						<T x={260} y={300 + i * 130} size={i === 2 || i === 4 ? 76 : 64} color={c} mono weight={700}>
							{t}
						</T>
					</g>
				);
			})}
		</Svg>
	);
};

// ---------------------------------------------------------------- the same energy, two speeds
export const TwoMeters: React.FC<{homeAt: number; catAt: number}> = ({homeAt, catAt}) => (
	<Svg>
		<Meter x={560} y={480} a={0} b={19} f0={homeAt} f1={homeAt + 3600} label="YOUR HOME · 6 DAYS" />
		<Meter x={1360} y={480} a={0} b={19} f0={catAt} f1={catAt + 180} label="CATAPULT · 3 SECONDS" hot />
	</Svg>
);

// ---------------------------------------------------------------- the spike against Vikrant's four engines
export const EngineBars: React.FC<{barsAt: number; spikeAt: number}> = ({barsAt, spikeAt}) => {
	const f = useCurrentFrame();
	const base = 860;
	const pxMW = 7; // 100 MW = 700 px
	const spike = tw(f, spikeAt, spikeAt + 30, 0, 49, ez.arrive);
	return (
		<Svg>
			<line x1={300} y1={base} x2={1620} y2={base} stroke={C.dim} strokeWidth={3} />
			{[0, 1, 2, 3].map((i) => {
				const o = tw(f, barsAt + i * 8, barsAt + i * 8 + 18, 0, 1, ez.arrive);
				return (
					<g key={i} opacity={o}>
						<rect x={360 + i * 230} y={base - 22 * pxMW * o} width={170} height={22 * pxMW * o} fill={C.cyan} fillOpacity={0.55} stroke={C.cyan} strokeWidth={4} />
						<T x={445 + i * 230} y={base + 54} size={34} anchor="middle" color={C.dim}>22 MW</T>
					</g>
				);
			})}
			<T x={360} y={base - 22 * pxMW - 30} size={40} color={C.cyan}>VIKRANT'S 4 ENGINES · 88 MW</T>
			{f >= spikeAt ? (
				<g>
					<rect x={1360} y={base - spike * pxMW} width={170} height={spike * pxMW} fill={C.red} fillOpacity={0.85} filter="url(#glow)" />
					<line x1={340} y1={base - 49 * pxMW} x2={1560} y2={base - 49 * pxMW} stroke={C.red} strokeWidth={3} strokeDasharray="14 10" opacity={tw(f, spikeAt + 20, spikeAt + 34, 0, 1)} />
					<T x={1445} y={base - spike * pxMW - 24} size={56} anchor="middle" color={C.red} mono weight={700}>
						{`${Math.round(spike)} MW`}
					</T>
				</g>
			) : null}
		</Svg>
	);
};

// ---------------------------------------------------------------- China: a full-length track on land
export const LandTrack: React.FC<{drawAt: number}> = ({drawAt}) => {
	const f = useCurrentFrame();
	const k = tw(f, drawAt, drawAt + 70, 0, 1, ez.sweep);
	return (
		<Svg>
			<rect x={0} y={560} width={1920} height={520} fill="#3d3a30" opacity={0.6} />
			<line x1={240} y1={680} x2={240 + 1440 * k} y2={680} stroke={C.slot} strokeWidth={14} strokeLinecap="round" filter="url(#glow)" />
			<T x={240} y={760} size={40} color={C.dim} o={k}>A FULL-SIZE TEST TRACK, ON LAND</T>
			<g transform={`translate(${240 + 1440 * k} 650)`} opacity={k}>
				<path d="M-170 -50 L100 -50 L150 -30 L100 -10 L-170 -10 Z" fill="#7d8790" stroke={ink} strokeWidth={3} />
			</g>
		</Svg>
	);
};

// ---------------------------------------------------------------- the American testers' numbers (SOURCE: US DOT&E)
export const DoteBars: React.FC<{lineAt: number; b1At: number; b2At: number}> = ({lineAt, b1At, b2At}) => {
	const f = useCurrentFrame();
	const base = 880;
	const px = 600 / 4166;
	const l = tw(f, lineAt, lineAt + 24, 0, 1, ez.arrive);
	const b1 = tw(f, b1At, b1At + 24, 0, 181, ez.arrive);
	const b2 = tw(f, b2At, b2At + 24, 0, 614, ez.arrive);
	return (
		<Svg>
			<line x1={300} y1={base} x2={1620} y2={base} stroke={C.dim} strokeWidth={3} />
			<g opacity={l}>
				<line x1={300} y1={base - 4166 * px} x2={1620} y2={base - 4166 * px} stroke={C.green} strokeWidth={5} strokeDasharray="20 12" />
				<T x={300} y={base - 4166 * px - 24} size={46} color={C.green}>NAVY'S GOAL · 4,166 LAUNCHES</T>
			</g>
			{b1 > 0 ? (
				<g>
					<rect x={520} y={base - b1 * px} width={260} height={b1 * px} fill={C.cyan} fillOpacity={0.7} />
					<T x={650} y={base - b1 * px - 20} size={56} anchor="middle" color={C.cyan} mono weight={700}>{Math.round(b1)}</T>
					<T x={650} y={base + 56} size={40} anchor="middle" color={C.dim}>2020</T>
				</g>
			) : null}
			{b2 > 0 ? (
				<g>
					<rect x={1000} y={base - b2 * px} width={260} height={b2 * px} fill={C.cyan} fillOpacity={0.7} />
					<T x={1130} y={base - b2 * px - 20} size={56} anchor="middle" color={C.cyan} mono weight={700}>{Math.round(b2)}</T>
					<T x={1130} y={base + 56} size={40} anchor="middle" color={C.dim}>2022</T>
				</g>
			) : null}
			<T x={1620} y={base + 120} size={30} anchor="end" color={C.dim}>LAUNCHES BETWEEN SERIOUS FAILURES</T>
		</Svg>
	);
};

// ---------------------------------------------------------------- a document on the drafting table (the film's one pose)
// Viewer review r3 fix 5: the card fills about 70% of the frame; the line the voice reads is large, the rest small;
// the source sits on one line. On a TV at 720p the marked line is ~50 px, the others ~32 px.
const DocCard: React.FC<{at: number; lines: string[]; mark?: number; markAt?: number; head: string; stamp?: string; width: number; tilt: number; big?: number; headSize?: number}> = ({
	at,
	lines,
	mark,
	markAt,
	head,
	stamp,
	width,
	tilt,
	big = 78,
	headSize = 40,
}) => {
	const f = useCurrentFrame();
	const p = tw(f, at, at + 22, 0, 1, ez.arrive);
	const hi = markAt === undefined ? 0 : tw(f, markAt, markAt + 14, 0, 1, ez.arrive);
	return (
		<div
			style={{
				width,
				background: C.paper,
				boxShadow: '0 40px 90px rgba(0,0,0,0.6)',
				transform: `translateY(${(1 - p) * 60}px) rotate(${tilt * (1 - p) * 8 + tilt}deg)`,
				opacity: p,
				padding: '56px 70px 50px',
			}}
		>
			<div style={{fontFamily: F.label, fontWeight: 800, fontSize: headSize, color: C.pencil, letterSpacing: 1.5, borderBottom: `4px solid ${C.pencil}`, paddingBottom: 16, marginBottom: 30, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{head}</div>
			{lines.map((l, i) => {
				const on = mark === undefined || i === mark;
				return (
					<div
						key={i}
						style={{
							fontFamily: F.label,
							fontWeight: on ? 800 : 700,
							fontSize: mark === undefined ? Math.round(big * 0.8) : on ? big : 48,
							color: on ? C.pencil : '#4a5560',
							lineHeight: 1.22,
							marginBottom: 16,
							display: 'inline-block',
							width: '100%',
							background: i === mark ? `linear-gradient(90deg, rgba(255,204,31,0.8) ${hi * 100}%, transparent ${hi * 100}%)` : undefined,
						}}
					>
						{l}
					</div>
				);
			})}
			{stamp ? <div style={{marginTop: 22, fontFamily: F.label, fontWeight: 700, fontSize: 34, color: '#5d5d5d', whiteSpace: 'nowrap'}}>{stamp}</div> : null}
		</div>
	);
};

export const Doc: React.FC<{at: number; lines: string[]; mark?: number; markAt?: number; head: string; stamp?: string; big?: number}> = (p) => (
	<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
		<DocCard {...p} width={1480} tilt={-1.2} />
	</AbsoluteFill>
);

/** two documents side by side (S148–150: the White House memo and the maker's reply, one split, r3 fix 5) */
export const DocPair: React.FC<{a: React.ComponentProps<typeof Doc>; b: React.ComponentProps<typeof Doc>}> = ({a, b}) => (
	<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'row', gap: 40}}>
		<DocCard {...a} width={690} tilt={-1.6} big={a.big ?? 60} headSize={32} />
		<DocCard {...b} width={690} tilt={1.4} big={b.big ?? 60} headSize={32} />
	</AbsoluteFill>
);

// ---------------------------------------------------------------- S3: seventeen metres beside a hundred (one pull-back)
const Rafale: React.FC<{s: number}> = ({s}) => (
	<g transform={`scale(${s})`}>
		<path d="M75 0 L20 -5 L-10 -54 L-40 -54 L-30 -6 L-75 -6 L-75 6 L-30 6 L-40 54 L-10 54 L20 5 Z" fill="#9aa3ab" stroke={ink} strokeWidth={2 / s} />
		<path d="M45 -3 L35 -22 L28 -22 L32 -3 Z M45 3 L35 22 L28 22 L32 3 Z" fill="#9aa3ab" stroke={ink} strokeWidth={1.5 / s} />
	</g>
);
export const ScaleCompare: React.FC<{dur: number; longAt: number; jetAt: number}> = ({dur, longAt, jetAt}) => {
	const f = useCurrentFrame();
	const pxm = 15; // px a metre at the end of the pull-back (100 m = 1500 px)
	const zoom = 1 + 0.6 * (1 - tw(f, 0, Math.min(dur, longAt + 120), 0, 1, ez.cam));
	const L = tw(f, longAt, longAt + 90, 0, 100, ez.sweep);
	const j = tw(f, jetAt, jetAt + 30, 0, 1, ez.arrive);
	const x0 = 210;
	return (
		<Svg>
			<g transform={`translate(${x0} 700) scale(${zoom}) translate(${-x0} -700)`}>
				<line x1={x0} y1={760} x2={x0 + 17 * pxm} y2={760} stroke={C.slot} strokeWidth={12} strokeLinecap="round" filter="url(#glow)" />
				<T x={x0} y={830} size={34 / zoom + 6} color={C.slot}>17 M · 400 KG</T>
				{L > 0 ? (
					<g>
						<line x1={x0} y1={560} x2={x0 + L * pxm} y2={560} stroke={C.slot} strokeWidth={12} strokeLinecap="round" opacity={0.85} />
						<T x={x0} y={470} size={40} color={ink} o={L / 100}>ABOUT 100 M · 30 TONNES</T>
					</g>
				) : null}
				{j > 0 ? (
					<g transform={`translate(${x0 + 700} ${560 - (1 - j) * 140})`} opacity={j}>
						<Rafale s={2.0} />
					</g>
				) : null}
			</g>
		</Svg>
	);
};

// ---------------------------------------------------------------- what China had / what India has
export const ChinaIndia: React.FC<{trackAt: number; shipAt: number}> = ({trackAt, shipAt}) => {
	const f = useCurrentFrame();
	const t = tw(f, trackAt, trackAt + 40, 0, 1, ez.sweep);
	const s = tw(f, shipAt, shipAt + 30, 0, 1, ez.arrive);
	const ship = (x: number, dotted: boolean) => (
		<path
			d={`M${x} 700 L${x + 560} 700 Q${x + 620} 700 ${x + 640} 740 L${x + 600} 800 L${x + 60} 800 Z`}
			fill={dotted ? 'none' : '#3a4048'}
			stroke={ink}
			strokeWidth={4}
			strokeDasharray={dotted ? '16 12' : undefined}
		/>
	);
	return (
		<Svg>
			<line x1={960} y1={140} x2={960} y2={940} stroke={C.dim} strokeOpacity={0.4} strokeWidth={3} />
			<T x={480} y={210} size={60} anchor="middle">CHINA</T>
			<T x={1440} y={210} size={60} anchor="middle">INDIA</T>
			<line x1={180} y1={460} x2={180 + 600 * t} y2={460} stroke={C.slot} strokeWidth={12} strokeLinecap="round" filter="url(#glow)" />
			<line x1={1140} y1={460} x2={1740} y2={460} stroke={C.dim} strokeOpacity={0.4 * t} strokeWidth={6} strokeDasharray="10 14" />
			<T x={180} y={530} size={34} color={C.dim} o={t}>TEST TRACK ON LAND</T>
			<T x={1140} y={530} size={34} color={C.dim} o={t}>NOT YET</T>
			<g opacity={s}>
				{ship(160, false)}
				{ship(1120, true)}
				<T x={160} y={870} size={34} color={C.dim}>A SHIP WAITING</T>
				<T x={1120} y={870} size={34} color={C.dim}>NOT APPROVED</T>
			</g>
		</Svg>
	);
};

/** S171–173: the plan's two catapults (a dotted ship) and the ship close to approval (a ramp) */
export const TwoShips: React.FC<{slotsAt: number; rampAt: number}> = ({slotsAt, rampAt}) => {
	const f = useCurrentFrame();
	const a = tw(f, slotsAt, slotsAt + 24, 0, 1, ez.arrive);
	const b = tw(f, rampAt, rampAt + 24, 0, 1, ez.arrive);
	const pts = rampCurve(1430, 760, 200, 14);
	return (
		<Svg>
			<g opacity={a}>
				<path d="M260 420 L1460 420 Q1620 420 1660 480 L1560 560 L340 560 Z" fill="none" stroke={ink} strokeWidth={4} strokeDasharray="16 12" />
				<line x1={900} y1={438} x2={1500} y2={438} stroke={C.slot} strokeWidth={8} filter="url(#glow)" />
				<line x1={900} y1={462} x2={1500} y2={462} stroke={C.slot} strokeWidth={8} filter="url(#glow)" />
				<T x={260} y={390} size={36} color={C.dim}>THE PLAN: TWO ELECTRIC CATAPULTS</T>
			</g>
			<g opacity={b}>
				<path d={`M260 760 L1430 760 L${pts.join(' L')} L1560 900 L340 900 Z`} fill="#3a4048" stroke={ink} strokeWidth={4} />
				<T x={260} y={960} size={36} color={C.dim}>CLOSE TO APPROVAL: A REPEAT VIKRANT</T>
			</g>
		</Svg>
	);
};

/** S180–185: the honest sum: jets ordered (tick), a small test model, a dotted ship */
export const ThreeItems: React.FC<{tickAt: number; smallAt: number; dotAt: number}> = ({tickAt, smallAt, dotAt}) => {
	const f = useCurrentFrame();
	const a = tw(f, tickAt, tickAt + 20, 0, 1, ez.arrive);
	const b = tw(f, smallAt, smallAt + 20, 0, 1, ez.arrive);
	const c = tw(f, dotAt, dotAt + 20, 0, 1, ez.arrive);
	return (
		<Svg>
			{/* r3 fix 4: all three inside the title-safe area (x 230–1690 even at the camera's closest framing) */}
			<g transform="translate(470 440)">
				<Rafale s={2.4} />
				<path d="M-60 170 L-20 210 L70 120" fill="none" stroke={C.green} strokeWidth={14} strokeLinecap="round" opacity={a} />
				<T x={0} y={300} size={46} anchor="middle">JETS</T>
				<T x={0} y={356} size={40} anchor="middle" color={C.green}>ORDERED</T>
			</g>
			<g opacity={b} transform="translate(960 440)">
				<line x1={-50} y1={0} x2={50} y2={0} stroke={C.slot} strokeWidth={14} strokeLinecap="round" filter="url(#glow)" />
				<T x={0} y={300} size={46} anchor="middle">CATAPULT</T>
				<T x={0} y={356} size={40} anchor="middle" color={C.slot}>A TEST MODEL</T>
			</g>
			<g opacity={c} transform="translate(1450 440)">
				<path d="M-190 -40 L150 -40 Q195 -40 212 0 L178 50 L-172 50 Z" fill="none" stroke={ink} strokeWidth={4} strokeDasharray="14 10" />
				<T x={0} y={300} size={46} anchor="middle">SHIP</T>
				<T x={0} y={356} size={40} anchor="middle" color={C.dim}>NOT APPROVED</T>
			</g>
		</Svg>
	);
};

/** S189: what is missing, three slots filling */
export const ThreeSlots: React.FC<{at: number[]; words: string[]}> = ({at, words}) => {
	const f = useCurrentFrame();
	return (
		<Svg>
			{words.map((w, i) => {
				const o = tw(f, at[i], at[i] + 18, 0, 1, ez.arrive);
				return (
					<g key={w}>
						<rect x={210 + i * 520} y={420} width={460} height={220} rx={14} fill={C.slot} fillOpacity={0.1 + 0.25 * o} stroke={C.slot} strokeWidth={5} strokeDasharray={o > 0.5 ? undefined : '16 12'} />
						<T x={440 + i * 520} y={550} size={58} anchor="middle" o={o}>{w}</T>
					</g>
				);
			})}
		</Svg>
	);
};

/** S199–202: three dates to watch */
export const Watch: React.FC<{at: number[]; items: [string, string][]}> = ({at, items}) => {
	const f = useCurrentFrame();
	return (
		<Svg>
			{items.map(([a, b], i) => {
				const o = tw(f, at[i], at[i] + 18, 0, 1, ez.arrive);
				return (
					<g key={a} opacity={o} transform={`translate(${(1 - o) * 40} 0)`}>
						<circle cx={300} cy={330 + i * 190} r={22} fill={C.slot} />
						<T x={360} y={346 + i * 190} size={60}>{a}</T>
						<T x={360} y={400 + i * 190} size={38} color={C.dim}>{b}</T>
					</g>
				);
			})}
		</Svg>
	);
};

/** S206: a ramp, or a catapult? */
export const RampOrCatapult: React.FC<{at: number}> = ({at}) => {
	const f = useCurrentFrame();
	const o = tw(f, at, at + 24, 0, 1, ez.arrive);
	const pts = rampCurve(760, 620, 160, 14);
	return (
		<Svg>
			<g opacity={o} transform="translate(0 -110)">
				<path d={`M160 620 L760 620 L${pts.join(' L')} L880 720 L220 720 Z`} fill="#3a4048" stroke={ink} strokeWidth={4} />
				<T x={520} y={820} size={56} anchor="middle">A RAMP</T>
				<path d="M1040 620 L1700 620 Q1760 620 1780 660 L1740 720 L1100 720 Z" fill="#3a4048" stroke={ink} strokeWidth={4} />
				<line x1={1300} y1={612} x2={1720} y2={612} stroke={C.slot} strokeWidth={10} filter="url(#glow)" />
				<T x={1400} y={820} size={56} anchor="middle">A CATAPULT</T>
				<T x={960} y={980} size={46} anchor="middle" color={C.slot}>₹40,000 CRORE: YOUR CHOICE?</T>
			</g>
		</Svg>
	);
};

/** S9–10: the 1961 slot on the old deck, drawn over the archive (a thin glowing line) */
export const SlotLine: React.FC<{at: number; end: number; x0: number; y0: number; x1: number; y1: number}> = ({at, end, x0, y0, x1, y1}) => {
	const f = useCurrentFrame();
	const k = tw(f, at, end, 0, 1, ez.sweep);
	if (k <= 0) {
		return null;
	}
	return (
		<Svg>
			<line x1={x0} y1={y0} x2={x0 + (x1 - x0) * k} y2={y0 + (y1 - y0) * k} stroke={C.slot} strokeWidth={10} strokeLinecap="round" filter="url(#glow)" />
		</Svg>
	);
};

/** S207–208: the next film as a question: a submarine whose sonar reaches ahead and to the sides, but not behind */
export const SubBlind: React.FC = () => {
	const f = useCurrentFrame();
	const cx = 960;
	const cy = 560;
	return (
		<Svg>
			<rect width={1920} height={1080} fill="#071a26" opacity={0.85} />
			{[0, 1, 2, 3].map((i) => {
				const ph = ((f + i * 30) % 120) / 120;
				const r = 120 + 520 * ph;
				return <path key={i} d={`M ${cx + r * Math.cos(2.4)} ${cy - r * Math.sin(2.4)} A ${r} ${r} 0 1 1 ${cx + r * Math.cos(-2.4)} ${cy - r * Math.sin(-2.4)}`} fill="none" stroke={C.cyan} strokeOpacity={0.55 * (1 - ph)} strokeWidth={4} />;
			})}
			<path d={`M${cx - 520} ${cy} L${cx - 760} ${cy - 150} L${cx - 760} ${cy + 150} Z`} fill={C.red} fillOpacity={0.12} />
			<T x={cx - 760} y={cy - 190} size={40} color={C.red}>BEHIND: SILENCE</T>
			<path d={`M${cx - 200} ${cy - 30} L${cx + 160} ${cy - 30} Q${cx + 230} ${cy} ${cx + 160} ${cy + 30} L${cx - 200} ${cy + 30} Q${cx - 240} ${cy} ${cx - 200} ${cy - 30} Z`} fill="#2b3138" stroke={ink} strokeWidth={4} />
			<rect x={cx - 20} y={cy - 70} width={70} height={42} rx={8} fill="#2b3138" stroke={ink} strokeWidth={4} />
		</Svg>
	);
};

// ---------------------------------------------------------------- r4 (viewer review r3): new drawings

/** S26–29 (fix 7): the ramp takes its price from the load: the jet's stack (airframe, fuel, weapons) shrinks on
 *  "lighter", "fuel", "weapons"; on "published" the missing part becomes a dashed box with a question mark. */
export const RampLoad: React.FC<{lighterAt: number; fuelAt: number; weapAt: number; qAt: number}> = ({lighterAt, fuelAt, weapAt, qAt}) => {
	const f = useCurrentFrame();
	const y0 = 640;
	const pts = rampCurve(760, y0, 420, 14);
	const last = pts[pts.length - 1].split(',').map(Number);
	const deck = `M120 ${y0} L760 ${y0} L${pts.join(' L')} L${last[0]} ${y0 + 150} L120 ${y0 + 150} Z`;
	const l = tw(f, lighterAt, lighterAt + 30, 0, 1, ez.arrive);
	const fu = tw(f, fuelAt, fuelAt + 24, 0, 1, ez.arrive);
	const we = tw(f, weapAt, weapAt + 24, 0, 1, ez.arrive);
	const q = tw(f, qAt, qAt + 20, 0, 1, ez.arrive);
	const base = 820;
	const X = 1380;
	const W = 300;
	const air = 260;
	const fuel = 180 - 70 * Math.max(l * 0.5, fu);
	const weap = 150 - 60 * Math.max(l * 0.5, we);
	const full = 260 + 180 + 150;
	const now = air + fuel + weap;
	const seg = (y: number, h: number, c: string, label: string, hot: number) => (
		<g>
			<rect x={X} y={y - h} width={W} height={h} fill={c} fillOpacity={0.35 + 0.4 * hot} stroke={c} strokeWidth={4} />
			<T x={X + W / 2} y={y - h / 2 + 16} size={40} anchor="middle" color={ink}>{label}</T>
		</g>
	);
	return (
		<Svg>
			<path d={`M60 ${y0 + 150} L1300 ${y0 + 150}`} stroke={C.sea} strokeWidth={6} />
			<path d={deck} fill="#2b3138" stroke={C.dim} strokeWidth={4} />
			<polyline points={pts.join(' ')} fill="none" stroke={ink} strokeWidth={6} />
			<g transform={`translate(420 ${y0})`}>
				<path d="M-150 -40 L120 -40 Q170 -30 175 -10 L120 0 L-150 0 Z" fill="#7d8790" stroke={ink} strokeWidth={3} />
				<path d="M-40 -40 L-10 -95 L30 -95 L20 -40 Z" fill="#7d8790" stroke={ink} strokeWidth={3} />
				<rect x={-150} y={-90} width={30} height={50} fill="#7d8790" stroke={ink} strokeWidth={3} />
				{/* the engines push: the only force on a ramp */}
				<path d={`M-160 -22 L${-200 - 40 * Math.abs(Math.sin(f / 5))} -22`} stroke={C.amber} strokeWidth={14} strokeLinecap="round" opacity={0.9} />
			</g>
			<T x={420} y={y0 - 140} size={40} anchor="middle" color={C.amber}>ITS OWN ENGINES</T>
			<T x={X + W / 2} y={base - full - 40} size={40} anchor="middle" color={C.dim}>WHAT IT CAN LIFT</T>
			{seg(base, air, '#7d8790', 'THE JET', 0)}
			{seg(base - air, fuel, C.amber, 'FUEL', fu)}
			{seg(base - air - fuel, weap, C.red, 'WEAPONS', we)}
			{l > 0 ? (
				<rect x={X} y={base - full} width={W} height={full - now} fill="none" stroke={C.slot} strokeWidth={4} strokeDasharray="14 10" opacity={l} />
			) : null}
			{q > 0 ? (
				<g opacity={q}>
					<T x={X + W / 2} y={base - full + (full - now) / 2 + 34} size={96} anchor="middle" color={C.slot} mono weight={700}>?</T>
				</g>
			) : null}
			<line x1={X - 30} y1={base} x2={X + W + 30} y2={base} stroke={C.dim} strokeWidth={4} />
		</Svg>
	);
};

/** S123: every 45 seconds, for years: a dial sweeps (time-lapse) and each turn throws one launch; on "years" the
 *  count runs away. */
export const Cycle45: React.FC<{yearsAt: number}> = ({yearsAt}) => {
	const f = useCurrentFrame();
	const per = 72; // one 45-second turn shown in 1.2 s
	const turns = f / per;
	const ang = (turns % 1) * Math.PI * 2;
	const n = Math.floor(turns) + 1;
	const flash = 1 - Math.min(1, (f % per) / 18);
	const cx = 640;
	const cy = 500;
	const r = 230;
	return (
		<Svg>
			<circle cx={cx} cy={cy} r={r} fill="#14191f" stroke={C.dim} strokeWidth={6} />
			{Array.from({length: 9}).map((_, i) => {
				const a = (i / 9) * Math.PI * 2 - Math.PI / 2;
				return <line key={i} x1={cx + (r - 30) * Math.cos(a)} y1={cy + (r - 30) * Math.sin(a)} x2={cx + (r - 6) * Math.cos(a)} y2={cy + (r - 6) * Math.sin(a)} stroke={C.dim} strokeWidth={5} />;
			})}
			<path d={`M${cx} ${cy - r + 14} A ${r - 14} ${r - 14} 0 ${ang > Math.PI ? 1 : 0} 1 ${cx + (r - 14) * Math.sin(ang)} ${cy - (r - 14) * Math.cos(ang)}`} fill="none" stroke={C.slot} strokeWidth={16} strokeLinecap="round" filter="url(#glow)" />
			<line x1={cx} y1={cy} x2={cx + (r - 50) * Math.sin(ang)} y2={cy - (r - 50) * Math.cos(ang)} stroke={ink} strokeWidth={8} strokeLinecap="round" />
			<T x={cx} y={cy + 100} size={60} anchor="middle" mono weight={700}>45 S</T>
			<line x1={1060} y1={420} x2={1060 + 640} y2={420} stroke={C.slot} strokeWidth={14} strokeLinecap="round" opacity={0.25 + 0.75 * flash} filter="url(#glow)" />
			<T x={1060} y={380} size={40} color={C.dim}>A LAUNCH EVERY TURN</T>
			<T x={1060} y={560} size={110} mono weight={700} color={C.slot}>{n.toLocaleString('en-IN')}</T>
			<T x={1060} y={630} size={40} color={C.dim}>{f < yearsAt ? 'LAUNCHES' : 'AND AGAIN · FOR YEARS'}</T>
		</Svg>
	);
};

/** S190–192: the other side, as a queue at one counter: submarines and the Army step ahead; the carrier waits. */
export const Queue: React.FC<{passAt: number; waitAt: number}> = ({passAt, waitAt}) => {
	const f = useCurrentFrame();
	const k = tw(f, passAt, passAt + 60, 0, 1, ez.cam);
	const w = tw(f, waitAt, waitAt + 24, 0, 1, ez.arrive);
	const y = 480;
	// slots in the line, nearest the counter first
	const slot = (i: number) => 1300 - i * 380;
	const carrierX = slot(0) + (slot(2) - slot(0)) * k;
	const subX = slot(1) + (slot(0) - slot(1)) * k;
	const armyX = slot(2) + (slot(1) - slot(2)) * k;
	const hop = (x: number) => -Math.sin(Math.min(1, Math.max(0, k)) * Math.PI) * 40 * (x === carrierX ? 0 : 1);
	return (
		<Svg>
			<line x1={180} y1={y + 70} x2={1720} y2={y + 70} stroke={C.dim} strokeWidth={4} />
			<rect x={1580} y={y - 260} width={150} height={330} fill="#2b3138" stroke={ink} strokeWidth={4} />
			<T x={1655} y={y - 280} size={40} anchor="middle" color={C.slot}>FIRST</T>
			<g transform={`translate(${carrierX} ${y})`} opacity={1 - 0.45 * w}>
				<path d="M-170 0 L120 0 Q160 0 172 30 L150 62 L-150 62 Z" fill="#3a4048" stroke={ink} strokeWidth={4} />
				<rect x={-20} y={-50} width={50} height={50} fill="#3a4048" stroke={ink} strokeWidth={3} />
				<T x={0} y={130} size={40} anchor="middle">CARRIER</T>
			</g>
			<g transform={`translate(${subX} ${y + hop(subX)})`}>
				<path d="M-160 20 L120 20 Q170 40 120 60 L-160 60 Q-190 40 -160 20 Z" fill="#2d3c4a" stroke={C.cyan} strokeWidth={4} />
				<rect x={-30} y={-10} width={60} height={32} rx={6} fill="#2d3c4a" stroke={C.cyan} strokeWidth={3} />
				<T x={0} y={130} size={40} anchor="middle" color={C.cyan}>SUBMARINES</T>
			</g>
			<g transform={`translate(${armyX} ${y + hop(armyX)})`}>
				<rect x={-130} y={10} width={260} height={52} rx={18} fill="#3d4630" stroke={C.green} strokeWidth={4} />
				<rect x={-60} y={-24} width={110} height={36} rx={8} fill="#3d4630" stroke={C.green} strokeWidth={3} />
				<line x1={50} y1={-8} x2={160} y2={-8} stroke={C.green} strokeWidth={8} />
				<T x={0} y={130} size={40} anchor="middle" color={C.green}>THE ARMY</T>
			</g>
			{w > 0 ? <T x={carrierX} y={y - 90} size={52} anchor="middle" color={C.slot} o={w}>WAITS</T> : null}
		</Svg>
	);
};

/** S178–179: the price of the catapult and the wires alone: the ship around them is only a dashed outline. */
export const PriceShip: React.FC<{priceAt: number; wiresAt: number; shipAt: number}> = ({priceAt, wiresAt, shipAt}) => {
	const f = useCurrentFrame();
	const p = tw(f, priceAt, priceAt + 50, 0, 1.321, ez.sweep);
	const wi = tw(f, wiresAt, wiresAt + 24, 0, 1, ez.arrive);
	const sh = tw(f, shipAt, shipAt + 30, 0, 1, ez.arrive);
	const cy = 540;
	return (
		<Svg>
			<path d={`M260 ${cy - 110} L1400 ${cy - 130} Q1600 ${cy - 120} 1660 ${cy} Q1600 ${cy + 120} 1400 ${cy + 130} L260 ${cy + 110} Q230 ${cy} 260 ${cy - 110} Z`} fill="none" stroke={ink} strokeOpacity={0.5} strokeWidth={4} strokeDasharray="18 14" />
			<line x1={980} y1={cy - 40} x2={1560} y2={cy - 40} stroke={C.slot} strokeWidth={12} strokeLinecap="round" filter="url(#glow)" />
			<line x1={980} y1={cy + 40} x2={1560} y2={cy + 40} stroke={C.slot} strokeWidth={12} strokeLinecap="round" filter="url(#glow)" />
			<T x={980} y={cy - 70} size={36} color={C.slot}>CATAPULTS</T>
			<g opacity={wi}>
				{[0, 1, 2].map((i) => (
					<line key={i} x1={420 + i * 60} y1={cy - 90} x2={420 + i * 60} y2={cy + 90} stroke={C.cyan} strokeWidth={6} />
				))}
				<T x={390} y={cy - 110} size={36} color={C.cyan}>ARRESTING WIRES</T>
			</g>
			<T x={260} y={300} size={110} mono weight={700} color={C.slot}>{`$${p.toFixed(3)} BN`}</T>
			<T x={260} y={360} size={36} color={C.dim}>US ESTIMATE FOR FRANCE · ONE SHIP'S SET · 2021</T>
			<T x={1660} y={cy + 200} size={44} anchor="end" color={ink} o={sh}>THE SHIP: NOT INCLUDED</T>
		</Svg>
	);
};
