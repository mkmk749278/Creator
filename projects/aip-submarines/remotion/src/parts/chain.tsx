import React from 'react';
import {useCurrentFrame} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C, F} from '../theme';
import {ez, tw, useSpring} from './kit';

// Chapter 3–4 drawings on the plate (ILLUSTRATION): tanks, spoon and phone, the AIP chain, the balance,
// autorickshaws to scale, the trap loop, the refit calendar.

const T: React.FC<{x: number; y: number; s?: number; c?: string; o?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode}> = ({x, y, s = 44, c = C.ink, o = 1, a = 'middle', children}) => (
	<text x={x} y={y} textAnchor={a} fill={c} opacity={o} fontFamily={F.label} fontWeight={800} fontSize={s} style={{paintOrder: 'stroke'}} stroke="rgba(3,7,13,0.85)" strokeWidth={10}>
		{children}
	</text>
);

/** Germany's way: hydrogen held in metal tanks (amber gas inside steel cylinders); `empty` drains and fades them. */
export const Tanks: React.FC<{at: number; gas: number; empty?: number}> = ({at, gas, empty}) => {
	const f = useCurrentFrame();
	const k = tw(f, at, at + 30, 0, 1, ez.sweep);
	const g = tw(f, gas, gas + 20, 0, 1, ez.arrive);
	const e = empty === undefined ? 0 : tw(f, empty, empty + 30, 0, 1);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{Array.from({length: 5}).map((_, i) => {
				const x = 470 + i * 210;
				return (
					<g key={i} opacity={1 - 0.85 * e}>
						<rect x={x} y={330} width={150} height={420} rx={70} fill="rgba(10,16,24,0.9)" stroke={C.dim} strokeWidth={5} pathLength={1} strokeDasharray={`${k} 1`} />
						<rect x={x + 14} y={344 + 392 * (1 - g * (1 - e))} width={122} height={392 * g * (1 - e)} rx={56} fill={C.amber} opacity={0.55} />
						{g > 0.5 && e < 0.5 ? <T x={x + 75} y={560} s={52} c={C.ink}>H2</T> : null}
					</g>
				);
			})}
		</svg>
	);
};

/** One spoonful (about 7 g) and a phone that charges from it (OUR CALCULATION); `tonnes` grows a heap. */
export const SpoonPhone: React.FC<{spoon: number; grams: number; phone: number; tonnes: number}> = ({spoon, grams, phone, tonnes}) => {
	const f = useCurrentFrame();
	const sp = useSpring(spoon);
	const ch = tw(f, phone, phone + 90, 0.05, 1, ez.sweep);
	const tn = tw(f, tonnes, tonnes + 40, 0, 1, ez.arrive);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<g transform={`translate(560 560) scale(${sp})`} opacity={1 - 0.7 * tn}>
				<ellipse cx={0} cy={0} rx={150} ry={70} fill="#b8bec6" stroke="#e6ebf0" strokeWidth={4} />
				<path d="M140 -10 L420 -60 L425 -40 L150 20 Z" fill="#b8bec6" stroke="#e6ebf0" strokeWidth={3} />
				<ellipse cx={0} cy={-18} rx={118} ry={44} fill="#f2f2ef" />
				{Array.from({length: 40}).map((_, i) => (
					<circle key={i} cx={-100 + ((i * 37) % 200)} cy={-30 + ((i * 13) % 26)} r={3} fill="#ffffff" opacity={0.8} />
				))}
			</g>
			{f >= grams ? <T x={560} y={720} s={64} o={tw(f, grams, grams + 10, 0, 1) * (1 - tn)}>≈ 7 g</T> : null}
			<g transform="translate(1260 300)" opacity={tw(f, phone - 6, phone + 6, 0, 1) * (1 - 0.7 * tn)}>
				<rect x={0} y={0} width={260} height={500} rx={36} fill="#0b1118" stroke={C.ink} strokeWidth={6} />
				<rect x={70} y={170} width={120} height={200} rx={10} fill="none" stroke={C.ink} strokeWidth={5} />
				<rect x={100} y={156} width={60} height={14} rx={4} fill={C.ink} />
				<rect x={80} y={180 + 180 * (1 - ch)} width={100} height={180 * ch} rx={6} fill={C.green} />
				<T x={130} y={450} s={52} c={C.green}>
					{Math.round(ch * 100)}%
				</T>
			</g>
			{tn > 0 ? (
				<g opacity={tn}>
					<path d={`M560 ${830} Q960 ${830 - 420 * tn} 1360 830 Z`} fill="#eceeea" />
					{Array.from({length: 60}).map((_, i) => (
						<circle key={i} cx={600 + ((i * 97) % 720)} cy={820 - ((i * 53) % 200) * tn} r={4} fill="#ffffff" opacity={0.6} />
					))}
					<T x={960} y={330} s={84} c={C.amber}>
						TONNES
					</T>
				</g>
			) : null}
		</svg>
	);
};

type ChainCues = {h2: number; o2: number; cold: number; cell: number; acid: number; elec: number; water: number; back: number; hull?: number};

/** The AIP chain: powder reactor → hydrogen → fuel cell ← liquid oxygen; out come electricity and water. */
export const Chain: React.FC<{cue: ChainCues}> = ({cue}) => {
	const f = useCurrentFrame();
	const on = (a: number) => tw(f, a, a + 16, 0, 1, ez.arrive);
	const flow = (x1: number, y1: number, x2: number, y2: number, c: string, a: number, n = 6) => {
		const k = on(a);
		if (k <= 0) {
			return null;
		}
		return (
			<g>
				<line x1={x1} y1={y1} x2={x2} y2={y2} stroke={c} strokeOpacity={0.35 * k} strokeWidth={10} strokeLinecap="round" />
				{Array.from({length: n}).map((_, i) => {
					const t = ((f - a) / 50 + i / n) % 1;
					return <circle key={i} cx={x1 + (x2 - x1) * t} cy={y1 + (y2 - y1) * t} r={9} fill={c} opacity={k} />;
				})}
			</g>
		);
	};
	const cold = on(cue.cold);
	const hull = cue.hull === undefined ? 0 : tw(f, cue.hull, cue.hull + 40, 0, 1, ez.sweep);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{/* reactor with the powder */}
			<g>
				<rect x={180} y={420} width={260} height={260} rx={24} fill="rgba(10,16,24,0.9)" stroke={C.ink} strokeWidth={5} />
				<path d="M210 650 Q310 560 410 650 Z" fill="#eceeea" />
				<T x={310} y={740} s={40}>POWDER</T>
			</g>
			{flow(440, 520, 780, 520, C.amber, cue.h2)}
			<T x={610} y={490} s={40} c={C.amber} o={on(cue.h2)}>HYDROGEN</T>
			{/* liquid oxygen tank */}
			<g>
				<rect x={820} y={130} width={300} height={170} rx={80} fill="rgba(10,16,24,0.9)" stroke={C.frost} strokeWidth={5} opacity={on(cue.o2)} />
				{Array.from({length: 26}).map((_, i) => (
					<circle key={i} cx={840 + ((i * 47) % 260)} cy={140 + ((i * 29) % 150)} r={3 + (i % 3)} fill="#ffffff" opacity={cold * (0.4 + 0.4 * noise2D('fr' + i, f / 40, 0))} />
				))}
				<T x={970} y={110} s={40} c={C.frost} o={on(cue.o2)}>LIQUID OXYGEN</T>
			</g>
			{flow(970, 300, 970, 410, C.frost, cue.o2, 4)}
			{/* the fuel cell stack */}
			<g opacity={Math.max(0.25, on(cue.cell))}>
				{Array.from({length: 9}).map((_, i) => (
					<rect key={i} x={790 + i * 40} y={420} width={26} height={260} rx={4} fill={C.cyan} fillOpacity={0.15 + 0.35 * on(cue.elec)} stroke={C.cyan} strokeWidth={3} />
				))}
				<T x={970} y={740} s={44} c={C.cyan}>FUEL CELL</T>
				<T x={970} y={800} s={34} c={C.dim} o={on(cue.acid)}>PHOSPHORIC ACID</T>
			</g>
			{flow(1170, 520, 1520, 520, C.cyan, cue.elec, 8)}
			<T x={1345} y={490} s={40} c={C.cyan} o={on(cue.elec)}>ELECTRICITY</T>
			<g opacity={on(cue.elec)}>
				<rect x={1530} y={450} width={220} height={140} rx={16} fill="rgba(10,16,24,0.9)" stroke={C.green} strokeWidth={5} />
				<T x={1640} y={540} s={40} c={C.green}>BATTERY</T>
			</g>
			{/* water out, and back to the powder */}
			{flow(970, 680, 970, 860, C.frost, cue.water, 4)}
			{on(cue.water) > 0 ? <T x={1060} y={880} s={44} c={C.frost} a="start" o={on(cue.water)}>WATER</T> : null}
			{(() => {
				const k = tw(f, cue.back, cue.back + 50, 0, 1, ez.sweep);
				return k > 0 ? (
					<path d="M960 870 Q600 960 330 690" fill="none" stroke={C.frost} strokeWidth={8} strokeDasharray={`${k * 900} 900`} strokeLinecap="round" />
				) : null;
			})()}
			{hull > 0 ? (
				<g opacity={hull}>
					<rect x={110} y={60} width={1700} height={900} rx={450} fill="none" stroke={C.ink} strokeWidth={10} pathLength={1} strokeDasharray={`${hull} 1`} />
				</g>
			) : null}
		</svg>
	);
};

/** On paper: the edge (no stored hydrogen gas) against the price (weight, waste liquid). */
export const Balance: React.FC<{edge: number; price: number; weight: number; waste: number}> = ({edge, price, weight, waste}) => {
	const f = useCurrentFrame();
	const e = tw(f, edge, edge + 16, 0, 1, ez.arrive);
	const p = tw(f, price, price + 16, 0, 1, ez.arrive);
	const w = tw(f, weight, weight + 20, 0, 1, ez.arrive);
	const ws = tw(f, waste, waste + 20, 0, 1, ez.arrive);
	const tilt = (-6 * e + 5 * w + 4 * ws) * (Math.PI / 180);
	const lx = 960 - Math.cos(tilt) * 520;
	const ly = 330 - Math.sin(tilt) * 520;
	const rx = 960 + Math.cos(tilt) * 520;
	const ry = 330 + Math.sin(tilt) * 520;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<path d="M960 330 L960 820 M820 840 L1100 840" stroke={C.dim} strokeWidth={12} strokeLinecap="round" />
			<line x1={lx} y1={ly} x2={rx} y2={ry} stroke={C.ink} strokeWidth={10} strokeLinecap="round" />
			<circle cx={960} cy={330} r={18} fill={C.ink} />
			{[
				[lx, ly],
				[rx, ry],
			].map(([x, y], i) => (
				<g key={i}>
					<line x1={x} y1={y} x2={x} y2={y + 200} stroke={C.dim} strokeWidth={4} />
					<path d={`M${x - 170} ${y + 200} L${x + 170} ${y + 200} L${x + 120} ${y + 240} L${x - 120} ${y + 240} Z`} fill="rgba(10,16,24,0.9)" stroke={C.ink} strokeWidth={4} />
				</g>
			))}
			<g opacity={e}>
				<T x={lx} y={ly + 180} s={46} c={C.green}>NO H₂ GAS</T>
				<T x={lx} y={ly + 120} s={34} c={C.dim}>NOTHING TO LEAK</T>
			</g>
			<g opacity={p}>
				<T x={rx} y={ry - 30} s={40} c={C.dim}>THE PRICE</T>
			</g>
			<g opacity={w}>
				<rect x={rx - 120} y={ry + 120} width={110} height={80} fill="#3a3f46" stroke={C.ink} strokeWidth={3} />
				<T x={rx - 120} y={ry + 300} s={38} c={C.orange}>WEIGHT</T>
			</g>
			<g opacity={ws}>
				<rect x={rx + 10} y={ry + 100} width={110} height={100} rx={12} fill="#2a4a5a" stroke={C.frost} strokeWidth={3} />
				<T x={rx + 120} y={ry + 300} s={38} c={C.frost}>WASTE LIQUID</T>
			</g>
		</svg>
	);
};

/** Four autorickshaws end to end: about ten metres (claim C41). A generic three-wheeler, no brand. */
export const Rickshaws: React.FC<{at: number; x: number; y: number; w: number}> = ({at, x, y, w}) => (
	<g>
		{Array.from({length: 4}).map((_, i) => (
			<Rick key={i} at={at + i * 8} x={x + (w / 4) * i} y={y} w={w / 4} />
		))}
	</g>
);

const Rick: React.FC<{at: number; x: number; y: number; w: number}> = ({at, x, y, w}) => {
	const p = useSpring(at);
	const s = w / 260;
	return (
		<g transform={`translate(${x} ${y - (1 - p) * 40}) scale(${s})`} opacity={p}>
			<path d="M20 120 L20 40 Q30 0 90 0 L200 0 Q240 0 250 50 L255 120 Z" fill="#1f6b3a" stroke="#0a0d10" strokeWidth={6} />
			<path d="M20 60 L120 60 L120 120 L20 120 Z" fill="#e8b923" opacity={0.95} />
			<rect x={150} y={20} width={70} height={45} rx={8} fill="#0b1118" />
			<circle cx={60} cy={130} r={26} fill="#111" stroke="#666" strokeWidth={6} />
			<circle cx={215} cy={130} r={26} fill="#111" stroke="#666" strokeWidth={6} />
		</g>
	);
};

/** The trap loop: "can't trust it until it has been to sea" ⇄ "can't go to sea until a boat is cut open for it". */
export const TrapLoop: React.FC<{both: number; navy: number; engine: number; close: number; lock?: number; open?: number; reclose?: number}> = ({both, navy, engine, close, lock, open, reclose}) => {
	const f = useCurrentFrame();
	const b = tw(f, both, both + 20, 0, 1, ez.arrive);
	const n = tw(f, navy, navy + 16, 0, 1, ez.arrive);
	const e = tw(f, engine, engine + 16, 0, 1, ez.arrive);
	const cl = tw(f, close, close + 40, 0, 1, ez.sweep);
	const lk = lock === undefined ? 0 : tw(f, lock, lock + 16, 0, 1, ez.arrive);
	const op = open === undefined ? 0 : tw(f, open, open + 40, 0, 1, ez.sweep);
	const rc = reclose === undefined ? 0 : tw(f, reclose, reclose + 30, 0, 1, ez.sweep);
	const gapOpen = op * (1 - rc);
	const col = gapOpen > 0.5 ? C.green : C.red;
	const spin = cl >= 1 && gapOpen < 0.1 ? (f - close) * 1.2 : 0;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<g opacity={Math.max(b, n)}>
				<rect x={170} y={380} width={620} height={300} rx={20} fill="rgba(10,16,24,0.9)" stroke={n > 0.5 ? C.ink : C.dim} strokeWidth={5} />
				<T x={480} y={470} s={48}>THE NAVY</T>
				<T x={480} y={550} s={34} c={C.dim} o={n}>WON'T BET A WAR SUBMARINE</T>
				<T x={480} y={600} s={34} c={C.dim} o={n}>ON AN ENGINE NEVER AT SEA</T>
			</g>
			<g opacity={Math.max(b, e)}>
				<rect x={1130} y={380} width={620} height={300} rx={20} fill="rgba(10,16,24,0.9)" stroke={e > 0.5 ? C.amber : C.dim} strokeWidth={5} />
				<T x={1440} y={470} s={48} c={C.amber}>THE ENGINE</T>
				<T x={1440} y={550} s={34} c={C.dim} o={e}>CAN'T GO TO SEA UNTIL</T>
				<T x={1440} y={600} s={34} c={C.dim} o={e}>A BOAT IS CUT OPEN FOR IT</T>
			</g>
			<g fill="none" stroke={col} strokeWidth={9} strokeLinecap="round">
				<path d="M800 400 C 900 230, 1020 230, 1120 400" pathLength={1} strokeDasharray={`${Math.min(1, cl * 2) * (1 - 0.6 * gapOpen)} 1`} />
				<path d="M1120 660 C 1020 830, 900 830, 800 660" pathLength={1} strokeDasharray={`${Math.max(0, cl * 2 - 1)} 1`} />
				{cl >= 1 ? (
					<g transform={`rotate(${spin % 360} 960 530)`} opacity={gapOpen < 0.5 ? 0.5 : 0}>
						<circle cx={960} cy={530} r={80} strokeDasharray="20 18" strokeWidth={6} />
					</g>
				) : null}
			</g>
			{lk > 0 ? (
				<g transform={`translate(960 ${530 - (1 - lk) * 60})`} opacity={lk * (1 - gapOpen)}>
					<rect x={-46} y={-20} width={92} height={78} rx={10} fill={C.red} />
					<path d="M-28 -20 L-28 -50 Q0 -86 28 -50 L28 -20" fill="none" stroke={C.red} strokeWidth={12} />
				</g>
			) : null}
		</svg>
	);
};

/** The refit calendar: years across; a boat can be cut open only in its refit window, once in several years. */
export const RefitCalendar: React.FC<{at: number; windows: number; far: number}> = ({at, windows, far}) => {
	const f = useCurrentFrame();
	const k = tw(f, at, at + 30, 0, 1, ez.sweep);
	const w = tw(f, windows, windows + 20, 0, 1, ez.arrive);
	const fr = tw(f, far, far + 30, 0, 1, ez.sweep);
	const years = 12;
	const x0 = 220;
	const span = 1480;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<rect x={x0} y={480} width={span * k} height={100} fill="rgba(3,7,13,0.82)" stroke={C.dim} strokeWidth={2} />
			{Array.from({length: years + 1}).map((_, i) => (
				<line key={i} x1={x0 + (span / years) * i} x2={x0 + (span / years) * i} y1={580} y2={600} stroke={C.dim} strokeWidth={2} opacity={k} />
			))}
			{[1.5, 7.5].map((yr, i) => {
				const x = x0 + (span / years) * yr;
				const wx = x + (i === 1 ? 0 : 0) - (span / years) * 0.4 * fr * 0;
				return <rect key={i} x={wx} y={486} width={(span / years) * 0.9} height={88} fill={C.green} opacity={0.75 * w} />;
			})}
			<text x={x0} y={450} fill={C.dim} fontFamily={F.label} fontWeight={800} fontSize={36} opacity={k}>
				YEARS IN SERVICE
			</text>
			{fr > 0 ? (
				<g opacity={fr}>
					<path d={`M${x0 + (span / years) * 2.4} 650 L${x0 + (span / years) * 7.5} 650`} stroke={C.ink} strokeWidth={4} markerEnd="url(#ar)" />
					<text x={x0 + (span / years) * 5} y={710} textAnchor="middle" fill={C.ink} fontFamily={F.label} fontWeight={800} fontSize={44}>
						SEVERAL YEARS
					</text>
				</g>
			) : null}
		</svg>
	);
};
