// Blast furnace cutaway (chapter 3, "Iron ore, limestone, and coke, a kind of baked coal, go in at the top. Hot air
// blasts in at the bottom. And out comes iron, as a glowing liquid."). A 2.5D section of a 1910s steel-shelled furnace
// of the American (Pittsburgh) type, drawn from period sections (films/tata-history/scenes/design-reference.md): bell
// and hopper top fed by a skip incline, gas offtakes, a firebrick-lined stack, belly, bosh and hearth, the mantle on
// columns, the hot-blast main into a bustle pipe and tuyeres, a cinder notch and an iron notch over a cast-house runner.
// Every event (each charge, the blast, the tap) has a frame the scene sets; the SFX list comes from the same frames.
import {noise2D} from '@remotion/noise';
import React, {useMemo} from 'react';
import {interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {fontStacks} from '../fonts';
import {ease, tween} from '../motion';
import {SfxCue} from '../sfx';

type P = [number, number];

/** Event frames (local). Defaults fit the VO line at about 155 wpm. */
export type FurnaceTimeline = {ore: number; limestone: number; coke: number; blast: number; tap: number};
export const furnaceDefaults: FurnaceTimeline = {ore: 40, limestone: 110, coke: 180, blast: 340, tap: 480};

export const furnaceCues = (tl: FurnaceTimeline = furnaceDefaults): SfxCue[] => [
	{frame: 0, sfx: 'furnace_roar_bed', gainDb: -16},
	{frame: tl.ore - 30, sfx: 'skip_car_winch', gainDb: -18},
	{frame: tl.ore, sfx: 'ore_rumble_drop', gainDb: -10},
	{frame: tl.limestone, sfx: 'stone_rumble_drop', gainDb: -12},
	{frame: tl.coke, sfx: 'coke_rattle_drop', gainDb: -12},
	{frame: tl.blast, sfx: 'hot_blast_whoosh', gainDb: -8},
	{frame: tl.tap, sfx: 'tap_hole_burst', gainDb: -6},
	{frame: tl.tap + 10, sfx: 'molten_pour_sizzle', gainDb: -10},
];

// ---------------------------------------------------------------- geometry (furnace units: axis x = 0, ground y = 0)
const HEARTH_R = 112;
const HEARTH_TOP = -205;
const HEARTH_BOT = -40;
const BELLY_R = 168;
const BELLY_Y = -370;
const THROAT_R = 112;
const THROAT_Y = -1040;
const TOP_Y = -1105;
const LINING = 42;
const SHELL = 7;
const STOCKLINE = -1010;
const ELL = 0.2; // ellipse ratio for rings seen from slightly above

/** Inner radius of the working profile at height y. */
const innerR = (y: number): number => {
	if (y >= HEARTH_TOP) {
		return HEARTH_R;
	}
	if (y >= BELLY_Y) {
		return interpolate(y, [BELLY_Y, HEARTH_TOP], [BELLY_R, HEARTH_R]);
	}
	if (y >= THROAT_Y) {
		return interpolate(y, [THROAT_Y, BELLY_Y], [THROAT_R, BELLY_R]);
	}
	return THROAT_R;
};

const PROFILE_Y = [TOP_Y, THROAT_Y, BELLY_Y, HEARTH_TOP, HEARTH_BOT];
const side = (sgn: 1 | -1, off: number): P[] => PROFILE_Y.map((y) => [sgn * (innerR(y) + off), y] as P);
const pathOf = (pts: P[], close = false): string => `M${pts.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join('L')}${close ? 'Z' : ''}`;

const INTERIOR = pathOf([...side(-1, 0), ...side(1, 0).reverse()], true);
const LINING_L = pathOf([...side(-1, 0), ...side(-1, LINING).reverse()], true);
const LINING_R = pathOf([...side(1, 0), ...side(1, LINING).reverse()], true);
const SHELL_L = pathOf([...side(-1, LINING), ...side(-1, LINING + SHELL).reverse()], true);
const SHELL_R = pathOf([...side(1, LINING), ...side(1, LINING + SHELL).reverse()], true);

const MATERIAL = {
	ore: {fill: '#6E3420', edge: '#B8673F', label: 'IRON ORE'},
	limestone: {fill: '#8E8A80', edge: '#D9D2C2', label: 'LIMESTONE'},
	coke: {fill: '#232326', edge: '#6F6A64', label: 'COKE'},
} as const;
type Mat = keyof typeof MATERIAL;
const ORDER: Mat[] = ['ore', 'coke', 'limestone', 'coke'];

type Lump = {u: number; v: number; r: number; rot: number; sides: number; seed: number};

const lumpPath = (cx: number, cy: number, r: number, rot: number, sides: number, seed: number): string => {
	const pts: P[] = [];
	for (let i = 0; i < sides; i++) {
		const a = rot + (i / sides) * Math.PI * 2;
		const rr = r * (0.72 + random(`lp${seed}-${i}`) * 0.4);
		pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.86]);
	}
	return pathOf(pts, true);
};

const LAYER_H = 64;
const DESCENT = 9; // units per second: the burden sinks slowly

export type BlastFurnaceProps = {
	timeline?: FurnaceTimeline;
	/** Camera centre in furnace units and zoom (px per unit); the scene animates it. */
	cam: {x: number; y: number; zoom: number};
	labels?: boolean;
};

export const BlastFurnace: React.FC<BlastFurnaceProps> = ({timeline = furnaceDefaults, cam, labels = true}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const tl = timeline;
	const blast = tween(frame, tl.blast, tl.blast + 40, 0.25, 1, ease.arrive);
	const tapOpen = tween(frame, tl.tap, tl.tap + 18, 0, 1, ease.arrive);
	const heat = 0.75 + 0.25 * blast;
	const flick = (k: string, s = 18) => 0.85 + 0.15 * noise2D(k, frame / s, 0);

	// burden layers: lumps in bands that sink; squeezed by the profile; they soften and glow in the bosh
	const lumps = useMemo(() => {
		const out: {mat: Mat; lumps: Lump[]}[] = [];
		for (let k = 0; k < 14; k++) {
			const mat = ORDER[k % ORDER.length];
			const n = mat === 'coke' ? 34 : 40;
			const ls: Lump[] = [];
			for (let i = 0; i < n; i++) {
				ls.push({
					u: random(`u${k}-${i}`) * 2 - 1,
					v: random(`v${k}-${i}`),
					r: (mat === 'coke' ? 13 : 10) + random(`r${k}-${i}`) * 7,
					rot: random(`o${k}-${i}`) * 6.28,
					sides: 6 + Math.floor(random(`s${k}-${i}`) * 3),
					seed: k * 100 + i,
				});
			}
			out.push({mat, lumps: ls});
		}
		return out;
	}, []);
	const sink = (t * DESCENT) % (LAYER_H * ORDER.length);

	// charge cascades at the top: each event drops a burst of lumps from the bell onto the stockline
	const cascade = (mat: Mat, at: number) => {
		const age = (frame - at) / fps;
		if (age < 0 || age > 1.6) {
			return null;
		}
		return new Array(26).fill(0).map((_, i) => {
			const delay = random(`cd${mat}${i}`) * 0.45;
			const a = age - delay;
			if (a < 0) {
				return null;
			}
			const x0 = (random(`cx${mat}${i}`) - 0.5) * 70;
			const vy = 80 + random(`cv${mat}${i}`) * 60;
			const y = TOP_Y + 20 + vy * a + 0.5 * 900 * a * a;
			const yStop = STOCKLINE - 6 + random(`cs${mat}${i}`) * 20;
			const yy = Math.min(y, yStop);
			const x = x0 * (1 + Math.min(a, 0.5) * 2.4);
			const o = Math.min(1, (1.6 - age) * 2.5);
			const m = MATERIAL[mat];
			return <path key={`${mat}${i}`} d={lumpPath(x, yy, 9 + random(`cr${mat}${i}`) * 5, i, 7, i + 999)} fill={m.fill} stroke={m.edge} strokeWidth={1.2} opacity={o} />;
		});
	};
	const bellDrop = Math.max(
		...[tl.ore, tl.limestone, tl.coke].map((at) => tween(frame, at - 6, at + 6, 0, 1, ease.arrive) - tween(frame, at + 40, at + 60, 0, 1, ease.camera)),
	);
	// the skip car climbs the incline before each charge
	const skipP = Math.max(...[tl.ore, tl.limestone, tl.coke].map((at) => (frame >= at - 50 && frame <= at + 10 ? tween(frame, at - 50, at - 4, 0, 1, ease.camera) : frame > at + 10 && frame < at + 40 ? tween(frame, at + 10, at + 40, 1, 0, ease.camera) : 0)));
	const skipFrom: P = [720, -10];
	const skipTo: P = [150, -1150];
	const skipAt: P = [skipFrom[0] + (skipTo[0] - skipFrom[0]) * skipP, skipFrom[1] + (skipTo[1] - skipFrom[1]) * skipP];

	const iron = HEARTH_BOT - 4; // iron pool bottom
	const ironLevel = interpolate(frame, [tl.tap, tl.tap + 260], [HEARTH_BOT - 70, HEARTH_BOT - 38], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const slagLevel = ironLevel - 34;

	const tf = `translate(960 540) scale(${cam.zoom.toFixed(5)}) translate(${(-cam.x).toFixed(2)} ${(-cam.y).toFixed(2)})`;
	const z = 1 / cam.zoom;
	const lab = (text: string, at: number, anchor: P, to: P, until = 1e9) => {
		const o = Math.min(tween(frame, at, at + 18, 0, 1, ease.arrive), tween(frame, until - 18, until, 1, 0, ease.leave));
		if (!labels || o <= 0) {
			return null;
		}
		const lp = tween(frame, at, at + 26, 0, 1, ease.sweep);
		const mid: P = [anchor[0] + (to[0] - anchor[0]) * lp, anchor[1] + (to[1] - anchor[1]) * lp];
		return (
			<g opacity={o}>
				<path d={pathOf([anchor, mid])} stroke={colors.gold} strokeWidth={1.6 * z} fill="none" />
				<circle cx={to[0]} cy={to[1]} r={4 * z * lp} fill={colors.gold} />
				<text
					x={anchor[0] + (anchor[0] < to[0] ? -14 * z : 14 * z)}
					y={anchor[1] + 9 * z}
					textAnchor={anchor[0] < to[0] ? 'end' : 'start'}
					fontFamily={fontStacks.text}
					fontWeight={700}
					fontSize={30 * z}
					letterSpacing="0.22em"
					fill={colors.ink}
					stroke="#0D0E11"
					strokeWidth={6 * z}
					paintOrder="stroke"
				>
					{text}
				</text>
			</g>
		);
	};

	// tuyeres: four visible on the back half, at the top of the hearth
	const tuyeres = [-0.75, -0.25, 0.25, 0.75];
	const BUSTLE_Y = -268;
	const BUSTLE_R = BELLY_R + 120;

	return (
		<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>
			<defs>
				<pattern id="bf-brick" width={28} height={14} patternUnits="userSpaceOnUse">
					<rect width={28} height={14} fill="#3A2318" />
					<path d="M0 0.5H28M0 7.5H28M7 0.5V7.5M21 7.5V14" stroke="#1A0F0A" strokeWidth={1.4} />
				</pattern>
				<linearGradient id="bf-heat" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#000" stopOpacity={0} />
					<stop offset="0.45" stopColor="#7A1E08" stopOpacity={0.25 * heat} />
					<stop offset="0.72" stopColor="#E0541A" stopOpacity={0.55 * heat} />
					<stop offset="0.86" stopColor="#FFB04A" stopOpacity={0.85 * heat} />
					<stop offset="1" stopColor="#FFE7B0" stopOpacity={0.9 * heat} />
				</linearGradient>
				<radialGradient id="bf-iron" cx="0.5" cy="0.4" r="0.7">
					<stop offset="0" stopColor="#FFF6D8" />
					<stop offset="0.5" stopColor="#FFC25A" />
					<stop offset="1" stopColor="#E5641E" />
				</radialGradient>
				<linearGradient id="bf-back" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#120C0A" />
					<stop offset="0.5" stopColor="#24160F" />
					<stop offset="1" stopColor="#120C0A" />
				</linearGradient>
				<clipPath id="bf-inside">
					<path d={INTERIOR} />
				</clipPath>
				<filter id="bf-blur8">
					<feGaussianBlur stdDeviation={8} />
				</filter>
				<filter id="bf-blur3">
					<feGaussianBlur stdDeviation={3} />
				</filter>
			</defs>
			<g transform={tf}>
				{/* cast-house floor and the foundation */}
				<rect x={-2400} y={0} width={5200} height={900} fill="#0F0E0F" />
				<path d={pathOf([[-2400, 0], [2800, 0]])} stroke={colors.bronze} strokeWidth={2 * z} />
				<rect x={-HEARTH_R - LINING - 40} y={HEARTH_BOT} width={(HEARTH_R + LINING + 40) * 2} height={-HEARTH_BOT} fill="url(#bf-brick)" stroke={colors.bronze} strokeWidth={1.6 * z} />

				{/* skip incline and the car */}
				<path d={pathOf([skipFrom, skipTo])} stroke={colors.bronze} strokeWidth={3 * z} />
				<path d={pathOf([[skipFrom[0] + 22, skipFrom[1]], [skipTo[0] + 22, skipTo[1]]])} stroke={colors.bronze} strokeWidth={1.6 * z} opacity={0.7} />
				{new Array(16).fill(0).map((_, i) => {
					const p = i / 15;
					const x = skipFrom[0] + (skipTo[0] - skipFrom[0]) * p;
					const y = skipFrom[1] + (skipTo[1] - skipFrom[1]) * p;
					return <path key={i} d={pathOf([[x, y], [x + 30, Math.min(0, y + 40)], [x + 30, 0]])} stroke={colors.bronze} strokeWidth={1.1 * z} opacity={0.22} fill="none" />;
				})}
				<g transform={`translate(${skipAt[0]} ${skipAt[1]}) rotate(-63)`}>
					<path d="M-26 -16 L26 -16 L20 16 L-20 16 Z" fill="#1C1A1A" stroke={colors.gold} strokeWidth={1.6 * z} />
				</g>

				{/* the dust catcher: the downcomer's gas drops its dust here before going on to fire the stoves */}
				<path d={pathOf([[-690, -560], [-690, -380], [-650, -300], [-650, 0], [-590, 0], [-590, -300], [-550, -380], [-550, -560]], true)} fill="#1C1A1B" stroke={colors.bronze} strokeWidth={1.4 * z} />
				<ellipse cx={-620} cy={-560} rx={70} ry={14} fill="#1C1A1B" stroke={colors.bronze} strokeWidth={1.4 * z} />
				{/* the mantle on columns, the hot-blast main and the bustle pipe ring (back half) */}
				{[-1, 1].map((s) => (
					<path key={`col${s}`} d={pathOf([[s * (BELLY_R + LINING + 30), BELLY_Y + 10], [s * (BELLY_R + LINING + 50), 0]])} stroke={colors.bronze} strokeWidth={10} opacity={0.75} />
				))}
				<ellipse cx={0} cy={BUSTLE_Y} rx={BUSTLE_R} ry={BUSTLE_R * ELL} fill="none" stroke="#3A2A20" strokeWidth={26} />
				<ellipse cx={0} cy={BUSTLE_Y} rx={BUSTLE_R} ry={BUSTLE_R * ELL} fill="none" stroke={colors.bronze} strokeWidth={1.5 * z} />
				{/* hot-blast main from the stoves (off to the left) */}
				<path d={pathOf([[-900, BUSTLE_Y - 60], [-BUSTLE_R - 60, BUSTLE_Y - 60], [-BUSTLE_R, BUSTLE_Y]])} stroke="#3A2A20" strokeWidth={34} fill="none" strokeLinejoin="round" />
				<path d={pathOf([[-900, BUSTLE_Y - 60], [-BUSTLE_R - 60, BUSTLE_Y - 60], [-BUSTLE_R, BUSTLE_Y]])} stroke={colors.bronze} strokeWidth={1.5 * z} fill="none" />
				{/* the blast flowing: bright dashes racing along the main and round the ring */}
				<g opacity={blast > 0.3 ? (blast - 0.3) / 0.7 : 0}>
					<path
						d={pathOf([[-900, BUSTLE_Y - 60], [-BUSTLE_R - 60, BUSTLE_Y - 60], [-BUSTLE_R, BUSTLE_Y]])}
						stroke="#FFD39A"
						strokeWidth={8}
						fill="none"
						strokeDasharray="40 60"
						strokeDashoffset={-frame * 3.2 /* v9: 14 px a frame on an 80 px dash read as a 13 fps stutter */}
						filter="url(#bf-blur3)"
					/>
					<ellipse cx={0} cy={BUSTLE_Y} rx={BUSTLE_R} ry={BUSTLE_R * ELL} fill="none" stroke="#FFD39A" strokeWidth={7} strokeDasharray="30 50" strokeDashoffset={-frame * 2.8} filter="url(#bf-blur3)" />
				</g>

				{/* back tuyeres: their pipes run behind the furnace; only the glowing nozzles show on the back wall */}
				{tuyeres.map((u, i) => {
					const xr = u * BUSTLE_R;
					const yr = BUSTLE_Y - Math.sqrt(Math.max(0, 1 - u * u)) * BUSTLE_R * ELL;
					const xh = u * (HEARTH_R + LINING);
					return <path key={`tp${i}`} d={pathOf([[xr, yr], [xr * 0.85, HEARTH_TOP - 10], [xh, HEARTH_TOP + 14]])} stroke="#3A2A20" strokeWidth={14} fill="none" strokeLinejoin="round" />;
				})}
				{/* back wall of the cut furnace, then the burden inside it */}
				<path d={INTERIOR} fill="url(#bf-back)" />
				<g clipPath="url(#bf-inside)">
					{lumps.map((layer, k) => {
						const yTop = STOCKLINE + ((k * LAYER_H + sink) % (LAYER_H * 14)) - 40;
						if (yTop > HEARTH_TOP + 30) {
							return null;
						}
						const m = MATERIAL[layer.mat];
						return layer.lumps.map((l, i) => {
							const y = yTop + l.v * LAYER_H;
							const r = innerR(y) - 8;
							const x = l.u * r;
							// in the bosh the ore and stone soften into glowing drops; coke stays solid down to the tuyeres
							const melt = layer.mat === 'coke' ? 0 : tween(y, BELLY_Y - 60, HEARTH_TOP, 0, 1, ease.camera);
							const glow = tween(y, BELLY_Y - 200, HEARTH_TOP, 0, 1, ease.camera) * heat;
							if (melt >= 1) {
								return null;
							}
							return (
								<path
									key={`${k}-${i}`}
									d={lumpPath(x, y, l.r * (1 - melt * 0.6), l.rot, l.sides, l.seed)}
									fill={glow > 0.4 ? (layer.mat === 'coke' ? '#5A2412' : '#C2521C') : m.fill}
									stroke={glow > 0.2 ? '#FF9A45' : m.edge}
									strokeWidth={1.3}
									opacity={1 - melt}
								/>
							);
						});
					})}
					{/* the heat of the lower furnace, brighter with the blast */}
					<rect x={-BELLY_R} y={-900} width={BELLY_R * 2} height={900 + HEARTH_BOT} fill="url(#bf-heat)" style={{mixBlendMode: 'screen'}} />
					{/* drops of iron and slag raining from the bosh into the hearth */}
					{new Array(30).fill(0).map((_, i) => {
						const life = 0.9 + random(`dl${i}`) * 0.6;
						const ph = ((t + random(`dp${i}`) * life) % life) / life;
						const x = (random(`dx${i}`) - 0.5) * HEARTH_R * 1.6;
						const y = HEARTH_TOP - 60 + ph * (slagLevel - HEARTH_TOP + 60);
						return <circle key={i} cx={x} cy={y} r={2.6 + random(`dr${i}`) * 2} fill="#FFD9A0" opacity={0.85 * Math.sin(Math.PI * ph) * heat} />;
					})}
					{/* raceways: fierce glow in front of each tuyere when the blast is on */}
					{tuyeres.map((u, i) => (
						<ellipse key={i} cx={u * HEARTH_R} cy={HEARTH_TOP + 18} rx={40 + 20 * blast} ry={22 + 8 * blast} fill="#FFF0C0" opacity={0.25 + 0.6 * blast * flick(`rw${i}`, 6)} filter="url(#bf-blur8)" />
					))}
					{tuyeres.map((u, i) => (
						<g key={`tn${i}`}>
							<ellipse cx={u * HEARTH_R * 0.92} cy={HEARTH_TOP + 16} rx={9} ry={6} fill="#1A120D" stroke={colors.bronze} strokeWidth={1.2 * z} />
							<ellipse cx={u * HEARTH_R * 0.92} cy={HEARTH_TOP + 16} rx={6} ry={4} fill="#FFE7B0" opacity={0.3 + 0.7 * blast} />
						</g>
					))}
					{/* the hearth: slag floating on molten iron */}
					<rect x={-HEARTH_R} y={slagLevel} width={HEARTH_R * 2} height={ironLevel - slagLevel} fill="#E8A63C" opacity={0.92} />
					<rect x={-HEARTH_R} y={ironLevel} width={HEARTH_R * 2} height={iron - ironLevel + 8} fill="url(#bf-iron)" />
					<path d={pathOf([[-HEARTH_R, slagLevel], [HEARTH_R, slagLevel]])} stroke="#FFE2A0" strokeWidth={2} opacity={0.8} />
					<path d={pathOf([[-HEARTH_R, ironLevel], [HEARTH_R, ironLevel]])} stroke="#FFF6D8" strokeWidth={2} />
				</g>

				{/* the cut: firebrick lining in section, the steel shell, the top */}
				<path d={LINING_L} fill="url(#bf-brick)" stroke={colors.bronze} strokeWidth={1.6 * z} />
				<path d={LINING_R} fill="url(#bf-brick)" stroke={colors.bronze} strokeWidth={1.6 * z} />
				<path d={SHELL_L} fill="#1E1C1D" stroke={colors.gold} strokeWidth={1.8 * z} />
				<path d={SHELL_R} fill="#1E1C1D" stroke={colors.gold} strokeWidth={1.8 * z} />
				{/* rims: the cut rings read as a cylinder */}
				{[TOP_Y, THROAT_Y, BELLY_Y, HEARTH_TOP].map((y, i) => (
					<ellipse key={i} cx={0} cy={y} rx={innerR(y) + LINING + SHELL} ry={(innerR(y) + LINING + SHELL) * ELL} fill="none" stroke={colors.bronze} strokeWidth={1.2 * z} opacity={0.45} strokeDasharray={`${8 * z} ${6 * z}`} />
				))}
				{/* the front half of the bustle ring, and the two front tuyeres coming down to the shell */}
				<path d={`M${-BUSTLE_R} ${BUSTLE_Y} A ${BUSTLE_R} ${BUSTLE_R * ELL} 0 0 0 ${BUSTLE_R} ${BUSTLE_Y}`} fill="none" stroke="#3A2A20" strokeWidth={26} />
				<path d={`M${-BUSTLE_R} ${BUSTLE_Y} A ${BUSTLE_R} ${BUSTLE_R * ELL} 0 0 0 ${BUSTLE_R} ${BUSTLE_Y}`} fill="none" stroke={colors.bronze} strokeWidth={1.5 * z} />
				<path
					d={`M${-BUSTLE_R} ${BUSTLE_Y} A ${BUSTLE_R} ${BUSTLE_R * ELL} 0 0 0 ${BUSTLE_R} ${BUSTLE_Y}`}
					fill="none"
					stroke="#FFD39A"
					strokeWidth={7}
					strokeDasharray="30 50"
					strokeDashoffset={frame * 2.8}
					filter="url(#bf-blur3)"
					opacity={blast > 0.3 ? (blast - 0.3) / 0.7 : 0}
				/>
				{[-1, 1].map((sg) => {
					const xr = sg * BUSTLE_R * 0.62;
					const yr = BUSTLE_Y + Math.sqrt(1 - 0.62 * 0.62) * BUSTLE_R * ELL;
					const xh = sg * (HEARTH_R + LINING + SHELL + 4);
					return (
						<g key={`ft${sg}`}>
							<path d={pathOf([[xr, yr], [xr * 0.9, HEARTH_TOP - 4], [xh, HEARTH_TOP + 16]])} stroke="#3A2A20" strokeWidth={14} fill="none" strokeLinejoin="round" />
							<path d={pathOf([[xr, yr], [xr * 0.9, HEARTH_TOP - 4], [xh, HEARTH_TOP + 16]])} stroke={blast > 0.4 ? '#FFB45E' : colors.bronze} strokeWidth={2 * z} fill="none" opacity={0.6 + 0.4 * blast} />
							<circle cx={xh} cy={HEARTH_TOP + 16} r={9} fill="#FFE7B0" opacity={0.25 + 0.6 * blast} filter="url(#bf-blur3)" />
						</g>
					);
				})}
				{/* top: hopper, bell, gas offtakes and downcomers */}
				<path d={pathOf([[-THROAT_R - LINING - SHELL, TOP_Y], [-60, TOP_Y - 70], [60, TOP_Y - 70], [THROAT_R + LINING + SHELL, TOP_Y]])} fill="#1E1C1D" stroke={colors.gold} strokeWidth={1.8 * z} />
				<path d={pathOf([[-48, TOP_Y - 70], [-70, TOP_Y - 150], [70, TOP_Y - 150], [48, TOP_Y - 70]])} fill="#191717" stroke={colors.gold} strokeWidth={1.8 * z} />
				<g transform={`translate(0 ${bellDrop * 34})`}>
					<path d={pathOf([[0, TOP_Y - 64], [-46, TOP_Y - 20], [46, TOP_Y - 20]], true)} fill="#2A2626" stroke={colors.gold} strokeWidth={1.8 * z} />
					<path d={pathOf([[0, TOP_Y - 64], [0, TOP_Y - 190]])} stroke={colors.gold} strokeWidth={2.4 * z} />
				</g>
				{/* gas offtakes rise from the top, the downcomer falls to the dust catcher on the left */}
				{[-1, 1].map((sg) => (
					<g key={`up${sg}`}>
						<path d={pathOf([[sg * 70, TOP_Y - 30], [sg * 92, TOP_Y - 230]])} stroke="#2A2422" strokeWidth={22} strokeLinecap="round" />
						<path d={pathOf([[sg * 70, TOP_Y - 30], [sg * 92, TOP_Y - 230]])} stroke={colors.bronze} strokeWidth={1.3 * z} />
					</g>
				))}
				<path d={pathOf([[92, TOP_Y - 230], [0, TOP_Y - 262], [-92, TOP_Y - 230], [-620, -560]])} stroke="#2A2422" strokeWidth={26} fill="none" strokeLinejoin="round" />
				<path d={pathOf([[92, TOP_Y - 230], [0, TOP_Y - 262], [-92, TOP_Y - 230], [-620, -560]])} stroke={colors.bronze} strokeWidth={1.3 * z} fill="none" strokeLinejoin="round" />
				{/* top gas drifting out (it went on to fire the stoves) */}
				{new Array(10).fill(0).map((_, i) => {
					const ph = ((t * 0.35 + i / 10) % 1);
					const s = i % 2 ? 1 : -1;
					return <circle key={`g${i}`} cx={s * (110 + ph * 120)} cy={TOP_Y - 260 - ph * 120} r={18 + ph * 40} fill="#5A4A40" opacity={0.18 * Math.sin(Math.PI * ph)} filter="url(#bf-blur8)" />;
				})}
				{cascade('ore', tl.ore)}
				{cascade('limestone', tl.limestone)}
				{cascade('coke', tl.coke)}

				{/* the cinder notch (left) and the iron notch (right) */}
				<rect x={-HEARTH_R - LINING - SHELL - 30} y={slagLevel - 6} width={34} height={14} fill="#2A2422" stroke={colors.bronze} strokeWidth={1.2 * z} />
				<rect x={HEARTH_R + LINING + SHELL - 4} y={HEARTH_BOT - 46} width={40} height={16} fill="#2A2422" stroke={colors.bronze} strokeWidth={1.2 * z} />
				{/* the tap: iron bursts from the notch, arcs into the runner and flows to the ladle */}
				{tapOpen > 0 ? (
					<g>
						{(() => {
							const sx = HEARTH_R + LINING + SHELL + 36;
							const sy = HEARTH_BOT - 38;
							const len = tween(frame, tl.tap, tl.tap + 50, 0, 1, ease.arrive);
							const stream = `M${sx} ${sy} Q ${sx + 60} ${sy - 8} ${sx + 90} ${-6}`;
							const runEnd = 160 + 260 * len;
							return (
								<>
									<path d={stream} stroke="#FFE7B0" strokeWidth={18 * tapOpen} fill="none" filter="url(#bf-blur8)" opacity={0.8} />
									<path d={stream} stroke="#FFF6D8" strokeWidth={8 * tapOpen} fill="none" strokeLinecap="round" />
									<path d={pathOf([[sx + 90, -4], [sx + runEnd, -4]])} stroke="#FFC25A" strokeWidth={10} strokeLinecap="round" />
									<path d={pathOf([[sx + 90, -4], [sx + runEnd, -4]])} stroke="#FFE7B0" strokeWidth={30} strokeLinecap="round" opacity={0.35} filter="url(#bf-blur8)" />
									<rect x={sx + 380} y={-70} width={130} height={70} fill="#1E1C1D" stroke={colors.gold} strokeWidth={1.6 * z} />
									<rect x={sx + 386} y={-70 + 64 * (1 - len * 0.7)} width={118} height={64 * len * 0.7} fill="url(#bf-iron)" opacity={len > 0.6 ? 1 : 0} />
									{new Array(40).fill(0).map((_, i) => {
										const life = 0.5 + random(`sp${i}`) * 0.7;
										const age = ((t - tl.tap / fps + random(`sq${i}`) * life) % life) / life;
										if (t < tl.tap / fps) {
											return null;
										}
										const ang = -Math.PI * (0.15 + random(`sa${i}`) * 0.7);
										const v = 160 + random(`sv${i}`) * 260;
										const x = sx + 20 + Math.cos(ang) * v * age * life;
										const y = sy + Math.sin(ang) * v * age * life + 0.5 * 700 * (age * life) ** 2;
										return <circle key={i} cx={x} cy={y} r={2.2} fill={i % 3 ? '#FFD08A' : '#FFF6D8'} opacity={(1 - age) * tapOpen} />;
									})}
								</>
							);
						})()}
					</g>
				) : null}
				{/* labels: the materials as the voice names them, the blast, the iron */}
				{lab(MATERIAL.ore.label, tl.ore, [-360, TOP_Y - 150], [-40, STOCKLINE - 30], tl.blast - 40)}
				{lab(MATERIAL.limestone.label, tl.limestone, [380, TOP_Y - 70], [30, STOCKLINE - 4], tl.blast - 40)}
				{lab(MATERIAL.coke.label, tl.coke, [-360, TOP_Y + 40], [-10, STOCKLINE + 26], tl.blast - 40)}
				{lab('HOT AIR', tl.blast, [-600, BUSTLE_Y - 170], [-BUSTLE_R - 40, BUSTLE_Y - 60], tl.tap)}
				{lab('LIQUID IRON', tl.tap + 20, [HEARTH_R + 520, -170], [HEARTH_R + LINING + SHELL + 200, -8])}
			</g>
		</svg>
	);
};

/** A camera path for the cutaway that follows the line: the top, then the whole furnace, the tuyeres, the tap. */
export const furnaceCamKeys = (tl: FurnaceTimeline = furnaceDefaults) => [
	{f: 0, x: -40, y: -1080, zoom: 1.25},
	{f: tl.coke + 40, x: -60, y: -1000, zoom: 1.12},
	{f: tl.blast - 30, x: 40, y: -560, zoom: 0.7},
	{f: tl.blast + 60, x: -150, y: -300, zoom: 0.98},
	{f: tl.tap - 10, x: 60, y: -300, zoom: 0.98},
	{f: tl.tap + 90, x: 240, y: -310, zoom: 1.06},
	{f: tl.tap + 400, x: 260, y: -300, zoom: 1.12},
];

export const camAt = (keys: {f: number; x: number; y: number; zoom: number}[], frame: number) => {
	const fs = keys.map((k) => k.f);
	const o = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease.camera} as const;
	return {
		x: interpolate(frame, fs, keys.map((k) => k.x), o),
		y: interpolate(frame, fs, keys.map((k) => k.y), o),
		zoom: Math.exp(interpolate(frame, fs, keys.map((k) => Math.log(k.zoom)), o)),
	};
};
