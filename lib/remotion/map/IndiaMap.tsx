// India map (PLAYBOOK §6.6, §8.5): India's official boundary from Natural Earth's India point-of-view file, filled and
// glowing; neighbours dimmed; city pins that drop in on a frame; routes drawn as glowing arcs with a moving head and a
// distance label. Everything is a pure function of the frame. Map units: 1 unit = 3 km (see indiaGeo.ts).
import React, {createContext, useContext, useMemo} from 'react';
import {interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {fontStacks} from '../fonts';
import {ease, pop, tween} from '../motion';
import {COUNTRIES, MAP_PROJ} from './indiaGeo';
import {PlateImage} from './PlateImage';

export type LonLat = [number, number];
export type MapPoint = [number, number];

/** Lambert azimuthal equal-area, the same projection as scripts/india_map.py: lon/lat → map units (y down). */
export const project = ([lon, lat]: LonLat): MapPoint => {
	const r = Math.PI / 180;
	const l = (lon - MAP_PROJ.lon0) * r;
	const p = lat * r;
	const p0 = MAP_PROJ.lat0 * r;
	const k = Math.sqrt(2 / (1 + Math.sin(p0) * Math.sin(p) + Math.cos(p0) * Math.cos(p) * Math.cos(l)));
	const x = MAP_PROJ.rKm * k * Math.cos(p) * Math.sin(l);
	const y = MAP_PROJ.rKm * k * (Math.cos(p0) * Math.sin(p) - Math.sin(p0) * Math.cos(p) * Math.cos(l));
	return [x / MAP_PROJ.kmPerUnit, -y / MAP_PROJ.kmPerUnit];
};

/** Places used in the film (city centres; Bombay = the Fort, as in claims T90). */
export const PLACES = {
	bombay: [72.83, 18.92] as LonLat,
	juhu: [72.83, 19.1] as LonLat,
	jamshedpur: [86.2, 22.8] as LonLat,
	karachi: [67.01, 24.86] as LonLat,
	ahmedabad: [72.58, 23.03] as LonLat,
	nagpur: [79.09, 21.15] as LonLat,
	kolkata: [88.36, 22.57] as LonLat,
	delhi: [77.21, 28.61] as LonLat,
	navsari: [72.95, 20.95] as LonLat,
	mayurbhanj: [86.73, 21.94] as LonLat,
	singur: [88.23, 22.81] as LonLat,
	sanand: [72.38, 22.99] as LonLat,
	dholera: [72.19, 22.25] as LonLat,
	bengaluru: [77.59, 12.97] as LonLat,
} as const;

export type MapCam = {x: number; y: number; zoom: number};
export type MapCamKey = MapCam & {f: number};

/** Eased map camera between keyframes (local frames): centre in map units, zoom in px per map unit. */
export const mapCam = (keys: MapCamKey[], frame: number): MapCam => {
	if (keys.length === 1) {
		return keys[0];
	}
	const fs = keys.map((k) => k.f);
	const o = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease.camera} as const;
	// zoom interpolates in log space so a zoom-out feels even
	return {
		x: interpolate(frame, fs, keys.map((k) => k.x), o),
		y: interpolate(frame, fs, keys.map((k) => k.y), o),
		zoom: Math.exp(interpolate(frame, fs, keys.map((k) => Math.log(k.zoom)), o)),
	};
};

/** A camera that frames the given places (with padding) in a 1920×1080 view. */
export const camFit = (places: LonLat[], pad = 260, f = 0): MapCamKey => {
	const pts = places.map(project);
	const xs = pts.map((p) => p[0]);
	const ys = pts.map((p) => p[1]);
	const w = Math.max(...xs) - Math.min(...xs);
	const h = Math.max(...ys) - Math.min(...ys);
	const zoom = Math.min((1920 - pad * 2) / Math.max(w, 1), (1080 - pad * 2) / Math.max(h, 1));
	return {f, x: (Math.max(...xs) + Math.min(...xs)) / 2, y: (Math.max(...ys) + Math.min(...ys)) / 2, zoom};
};

// graticule every 5° (projected curves): the blueprint under the map
const GRATICULE: string[] = (() => {
	const lines: string[] = [];
	for (let lon = 50; lon <= 110; lon += 5) {
		const pts: string[] = [];
		for (let lat = -5; lat <= 45; lat += 1) {
			const [x, y] = project([lon, lat]);
			pts.push(`${x.toFixed(1)} ${y.toFixed(1)}`);
		}
		lines.push(`M${pts.join('L')}`);
	}
	for (let lat = 0; lat <= 45; lat += 5) {
		const pts: string[] = [];
		for (let lon = 45; lon <= 115; lon += 1) {
			const [x, y] = project([lon, lat]);
			pts.push(`${x.toFixed(1)} ${y.toFixed(1)}`);
		}
		lines.push(`M${pts.join('L')}`);
	}
	return lines;
})();

export type MapStyle = 'today' | 'faint';

/** Real ground under every IndiaMap (plan_v7 §2.4): when a film provides satellite plates (all-India first, then
 *  detail plates), IndiaMap draws them in place of the flat land fills; detail plates fade in as the camera closes on
 *  them, feathered into the base, and the boundary file gives way to the real coast at close range. */
export type GroundPlate = {file: string; bounds: [number, number, number, number]; px?: number};
export const SatGround = createContext<{plates: GroundPlate[]; grade?: string} | null>(null);
const GROUND_GRADE = 'saturate(0.8) contrast(1.1) brightness(0.84) sepia(0.12)';
const FAINT_GRADE = 'saturate(0.45) sepia(0.45) contrast(1.08) brightness(1.0)';

export type IndiaMapProps = {
	cam: MapCam;
	/** 'today': India filled and glowing, neighbours dim. 'faint': all of today's borders drawn faintly (period routes). */
	style?: MapStyle;
	/** 0..1, how far India's fill and edge glow have come up (animate it in). */
	reveal?: number;
	/** Land tint for 'faint' maps (sepia for the 1930s). */
	land?: string;
	children?: React.ReactNode;
	id?: string;
};

/** The base map: graticule, neighbours, India. Children are drawn in map units on top (pins, routes). */
export const IndiaMap: React.FC<IndiaMapProps> = ({cam, style = 'today', reveal = 1, land = '#1F1A15', children, id = 'map'}) => {
	const frame = useCurrentFrame();
	const breathe = 0.85 + 0.15 * Math.sin(frame / 50);
	const tf = `translate(960 540) scale(${cam.zoom.toFixed(5)}) translate(${(-cam.x).toFixed(2)} ${(-cam.y).toFixed(2)})`;
	const others = useMemo(() => Object.entries(COUNTRIES).filter(([k]) => k !== 'IND'), []);
	const india = COUNTRIES.IND;
	const today = style === 'today';
	const ground = useContext(SatGround);
	if (ground && ground.plates.length) {
		return <GroundMap cam={cam} style={style} reveal={reveal} id={id} plates={ground.plates}>{children}</GroundMap>;
	}
	return (
		<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>
			<defs>
				<filter id={`${id}-glow`} x="-20%" y="-20%" width="140%" height="140%">
					<feGaussianBlur stdDeviation={10} />
				</filter>
				<radialGradient id={`${id}-fill`} cx="0.45" cy="0.42" r="0.7">
					<stop offset="0" stopColor="#3A2A1C" />
					<stop offset="0.6" stopColor="#261C14" />
					<stop offset="1" stopColor="#1A1410" />
				</radialGradient>
			</defs>
			<g transform={tf}>
				<g opacity={0.18}>
					{GRATICULE.map((d, i) => (
						<path key={i} d={d} fill="none" stroke={colors.muted} strokeWidth={0.8} vectorEffect="non-scaling-stroke" strokeDasharray="2 6" />
					))}
				</g>
				{/* coastlines: every country stroked thick first, then filled, so only the outer coast keeps its line */}
				{Object.entries(COUNTRIES).map(([code, ds]) =>
					ds.map((d, i) => (
						<path key={`c${code}${i}`} d={d} fill="none" stroke={today ? colors.muted : '#A88A63'} strokeOpacity={today ? 0.55 : 0.75} strokeWidth={today ? 2.4 : 2.6} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
					)),
				)}
				{others.map(([code, ds]) =>
					ds.map((d, i) => <path key={`f${code}${i}`} d={d} fill={today ? '#141518' : land} stroke="none" />),
				)}
				{!today ? india.map((d, i) => <path key={`fi${i}`} d={d} fill={land} stroke="none" />) : null}
				{/* land borders between countries: thin (today) or faint dashes (a period map) */}
				{others.map(([code, ds]) =>
					ds.map((d, i) => (
						<path
							key={`b${code}${i}`}
							d={d}
							fill="none"
							stroke={colors.muted}
							strokeOpacity={today ? 0.28 : 0.38}
							strokeWidth={0.9}
							strokeDasharray={today ? undefined : '4 5'}
							vectorEffect="non-scaling-stroke"
						/>
					)),
				)}
				{today ? (
					<>
						{/* the glow: a blurred bronze copy of India's edge */}
						<g filter={`url(#${id}-glow)`} opacity={0.75 * reveal * breathe}>
							{india.map((d, i) => (
								<path key={i} d={d} fill="none" stroke={colors.bronze} strokeWidth={10} vectorEffect="non-scaling-stroke" />
							))}
						</g>
						{india.map((d, i) => (
							<path key={`f${i}`} d={d} fill={`url(#${id}-fill)`} fillOpacity={0.25 + 0.75 * reveal} stroke="none" />
						))}
						{india.map((d, i) => (
							<path key={`s${i}`} d={d} fill="none" stroke={colors.gold} strokeOpacity={0.35 + 0.6 * reveal} strokeWidth={1.8} vectorEffect="non-scaling-stroke" strokeLinejoin="round" />
						))}
					</>
				) : (
					india.map((d, i) => (
						<path key={`s${i}`} d={d} fill="none" stroke={colors.muted} strokeOpacity={0.38} strokeWidth={0.9} strokeDasharray="4 5" vectorEffect="non-scaling-stroke" />
					))
				)}
				{children}
			</g>
		</svg>
	);
};

/** A city pin: drops in with a spring on frame `at`, a ring pulses out, the name in engraved capitals. */
export const MapPin: React.FC<{
	at: LonLat;
	from: number;
	cam: MapCam;
	label: string;
	sub?: string;
	side?: 'left' | 'right' | 'above' | 'below';
	color?: string;
	until?: number;
}> = ({at, from, cam, label, sub, side = 'right', color = colors.gold, until = 1e9}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const [x, y] = project(at);
	const p = pop(frame, fps, from, 170, 14);
	const o = Math.min(tween(frame, from, from + 8, 0, 1, ease.arrive), tween(frame, until - 15, until, 1, 0, ease.leave));
	if (frame < from) {
		return null;
	}
	const s = 1 / cam.zoom; // draw pins in screen pixels regardless of zoom
	const ring = ((frame - from) % 90) / 90;
	const lab = tween(frame, from + 6, from + 30, 0, 1, ease.arrive);
	const dx = side === 'left' ? -26 : side === 'right' ? 26 : 0;
	const dy = side === 'above' ? -30 : side === 'below' ? 40 : 7;
	const anchor = side === 'left' ? 'end' : side === 'right' ? 'start' : 'middle';
	return (
		<g transform={`translate(${x} ${y}) scale(${s})`} opacity={o}>
			<circle r={8 + ring * 34} fill="none" stroke={color} strokeWidth={2} opacity={(1 - ring) * 0.7} />
			<circle r={22} fill={color} opacity={0.25} style={{filter: 'blur(8px)'}} />
			<g transform={`translate(0 ${(1 - p) * -40}) scale(${0.4 + 0.6 * p})`}>
				<circle r={7.5} fill={color} stroke="#0D0E11" strokeWidth={2.5} />
				<circle r={2.6} fill="#FFF6DA" />
			</g>
			<g opacity={lab} transform={`translate(${dx + (side === 'left' ? 10 : side === 'right' ? -10 : 0) * (1 - lab)} ${dy})`}>
				<text
					textAnchor={anchor}
					fontFamily={fontStacks.display}
					fontWeight={700}
					fontSize={38}
					letterSpacing={`${0.16 + 0.1 * (1 - lab)}em`}
					fill={colors.ink}
					stroke="#0D0E11"
					strokeWidth={6}
					paintOrder="stroke"
				>
					{label}
				</text>
				{sub ? (
					<text
						y={38}
						textAnchor={anchor}
						fontFamily={fontStacks.text}
						fontWeight={700}
						fontSize={27}
						letterSpacing="0.14em"
						fill="#D8CDB8"
						stroke="#0D0E11"
						strokeWidth={5}
						paintOrder="stroke"
					>
						{sub}
					</text>
				) : null}
			</g>
		</g>
	);
};

/** Quadratic arc between two map points, bulging to one side by `bend` × length. */
const arcPoint = (a: MapPoint, b: MapPoint, bend: number, t: number): MapPoint => {
	const mx = (a[0] + b[0]) / 2;
	const my = (a[1] + b[1]) / 2;
	const dx = b[0] - a[0];
	const dy = b[1] - a[1];
	const c: MapPoint = [mx - dy * bend, my + dx * bend];
	const u = 1 - t;
	return [u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1]];
};

export type RouteHead = 'dot' | 'train' | 'plane';

/**
 * A glowing route through `stops`, drawn leg by leg from frame `from` over `dur` frames (eased per leg); a bright head
 * leads it. `label` (e.g. "1,400+ KM") rides the arc's middle once the line has passed it. Exposes the frames where
 * the head reaches each stop through `routeStopFrames()` for pins and SFX.
 */
export const MapRoute: React.FC<{
	stops: LonLat[];
	from: number;
	dur: number;
	cam: MapCam;
	color?: string;
	bend?: number;
	label?: string;
	labelAt?: number;
	head?: RouteHead;
	width?: number;
}> = ({stops, from, dur, cam, color = colors.gold, bend = -0.18, label, labelAt, head = 'dot', width = 3.2}) => {
	const frame = useCurrentFrame();
	const pts = stops.map(project);
	const legs = pts.length - 1;
	const lens = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
	const total = lens.reduce((a, b) => a + b, 0);
	const s = 1 / cam.zoom;
	// time is shared by distance so the head keeps one pace, each leg eased in and out (a stop at each city)
	let acc = 0;
	const legFrames = lens.map((l) => {
		const a = from + (acc / total) * dur;
		acc += l;
		return [a, from + (acc / total) * dur];
	});
	const N = 48;
	const drawn: string[] = [];
	legFrames.forEach(([a, b], i) => {
		const p = tween(frame, a, b, 0, 1, ease.sweep);
		if (p <= 0) {
			return;
		}
		const n = Math.max(2, Math.ceil(N * p));
		const segs: string[] = [];
		for (let k = 0; k <= n; k++) {
			const q = arcPoint(pts[i], pts[i + 1], bend, (k / n) * p);
			segs.push(`${q[0].toFixed(2)} ${q[1].toFixed(2)}`);
		}
		drawn.push(`M${segs.join('L')}`);
	});
	// the head rides the leg in progress (or rests at the last stop)
	let cur = -1;
	legFrames.forEach(([a], i) => {
		if (frame >= a) {
			cur = i;
		}
	});
	let headPt: MapPoint | null = null;
	let headAng = 0;
	if (cur >= 0) {
		const p = tween(frame, legFrames[cur][0], legFrames[cur][1], 0, 1, ease.sweep);
		const q0 = arcPoint(pts[cur], pts[cur + 1], bend, Math.max(0, p - 0.02));
		const q1 = arcPoint(pts[cur], pts[cur + 1], bend, Math.max(0.02, p));
		const q0b = p < 0.02 ? pts[cur] : q0;
		headPt = p < 0.02 ? pts[cur] : q1;
		headAng = (Math.atan2(q1[1] - q0b[1], q1[0] - q0b[0]) * 180) / Math.PI;
	}
	const done = frame >= from + dur;
	const headFade = done ? tween(frame, from + dur, from + dur + 30, 1, 0, ease.leave) : 1;
	// the label sits at the middle of the whole route
	const mid = (() => {
		let half = total / 2;
		for (let i = 0; i < legs; i++) {
			if (half <= lens[i]) {
				return arcPoint(pts[i], pts[i + 1], bend, half / lens[i]);
			}
			half -= lens[i];
		}
		return pts[pts.length - 1];
	})();
	const lStart = labelAt ?? from + dur * 0.55;
	const lp = tween(frame, lStart, lStart + 24, 0, 1, ease.arrive);
	const hp = headPt;
	return (
		<g>
			{drawn.map((d, i) => (
				<g key={i}>
					<path d={d} fill="none" stroke={color} strokeWidth={width * 5} strokeLinecap="round" opacity={0.22} vectorEffect="non-scaling-stroke" style={{filter: 'blur(6px)'}} />
					<path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
					<path d={d} fill="none" stroke="#FFF3D6" strokeWidth={width * 0.35} strokeLinecap="round" opacity={0.8} vectorEffect="non-scaling-stroke" />
				</g>
			))}
			{hp && headFade > 0 ? (
				<g transform={`translate(${hp[0]} ${hp[1]}) scale(${s}) rotate(${headAng})`} opacity={headFade}>
					<circle r={26} fill={color} opacity={0.35} style={{filter: 'blur(10px)'}} />
					{head === 'plane' ? (
						// a light monoplane seen from above: high wing, slim fuselage, tailplane
						<g fill="#FFF3D6" stroke="#0D0E11" strokeWidth={1.4}>
							<path d="M14 0 L-14 -1.6 L-14 1.6 Z" />
							<path d="M3 -19 L7 -19 L7 19 L3 19 Z" />
							<path d="M-11 -7 L-8 -7 L-8 7 L-11 7 Z" />
						</g>
					) : head === 'train' ? (
						<g fill="#FFF3D6" stroke="#0D0E11" strokeWidth={1.4}>
							<rect x={-12} y={-5} width={22} height={10} rx={2} />
							<rect x={-26} y={-4.5} width={12} height={9} rx={2} opacity={0.8} />
						</g>
					) : (
						<circle r={6} fill="#FFF3D6" />
					)}
				</g>
			) : null}
			{label && lp > 0 ? (
				<g transform={`translate(${mid[0]} ${mid[1]}) scale(${s})`} opacity={lp}>
					<g transform={`translate(0 ${-34 - 10 * (1 - lp)})`}>
						<rect x={-118} y={-30} width={236} height={46} rx={4} fill="rgba(10,10,12,0.72)" stroke={color} strokeOpacity={0.6} strokeWidth={1.4} />
						<text
							textAnchor="middle"
							y={4}
							fontFamily={fontStacks.numbers}
							fontWeight={700}
							fontSize={30}
							letterSpacing={`${0.06 + 0.08 * (1 - lp)}em`}
							fill={colors.gold}
						>
							{label}
						</text>
					</g>
				</g>
			) : null}
		</g>
	);
};

/** The frame at which a MapRoute's head reaches each stop (for pins and SFX). */
export const routeStopFrames = (stops: LonLat[], from: number, dur: number): number[] => {
	const pts = stops.map(project);
	const lens = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
	const total = lens.reduce((a, b) => a + b, 0);
	let acc = 0;
	return [from, ...lens.map((l) => Math.round(from + ((acc += l) / total) * dur))];
};

/** IndiaMap on real ground (see SatGround). */
const GroundMap: React.FC<{cam: MapCam; style: MapStyle; reveal: number; id: string; plates: GroundPlate[]; children?: React.ReactNode}> = ({
	cam,
	style,
	reveal,
	id,
	plates,
	children,
}) => {
	const frame = useCurrentFrame();
	const breathe = 0.85 + 0.15 * Math.sin(frame / 50);
	const tf = `translate(960 540) scale(${cam.zoom.toFixed(5)}) translate(${(-cam.x).toFixed(3)} ${(-cam.y).toFixed(3)})`;
	const india = COUNTRIES.IND;
	const others = useMemo(() => Object.entries(COUNTRIES).filter(([k]) => k !== 'IND'), []);
	const today = style === 'today';
	const lz = Math.log(cam.zoom);
	const lines = interpolate(lz, [Math.log(3), Math.log(7)], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const base = plates[0];
	const baseSharp = base.px ? base.px / (base.bounds[2] - base.bounds[0]) : 1;
	const outside = `M-5000 -5000H5000V5000H-5000Z ${india.join(' ')}`;
	return (
		<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0, background: '#07080A'}}>
			<defs>
				<filter id={`${id}-glow`} x="-20%" y="-20%" width="140%" height="140%">
					<feGaussianBlur stdDeviation={8} />
				</filter>
				<radialGradient id={`${id}-feather`} cx="0.5" cy="0.5" r="0.5">
					<stop offset="0.62" stopColor="#fff" />
					<stop offset="1" stopColor="#000" />
				</radialGradient>
				<mask id={`${id}-mask`} maskContentUnits="objectBoundingBox">
					<rect width={1} height={1} fill={`url(#${id}-feather)`} />
				</mask>
			</defs>
			<g transform={tf}>
				<g style={{filter: today ? GROUND_GRADE : FAINT_GRADE}} opacity={0.35 + 0.65 * reveal}>
					{plates.map((p, i) => {
						const [x0, y0, x1, y1] = p.bounds;
						// a detail plate only matters once the camera is near it
						const near = Math.abs(cam.x - (x0 + x1) / 2) < 960 / cam.zoom + (x1 - x0) && Math.abs(cam.y - (y0 + y1) / 2) < 540 / cam.zoom + (y1 - y0);
						const o = i === 0 ? 1 : near ? interpolate(lz, [Math.log(baseSharp * 0.9), Math.log(baseSharp * 3)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
						return o > 0.001 ? (
							<PlateImage key={p.file} href={staticFile(p.file)} x={x0} y={y0} width={x1 - x0} height={y1 - y0} preserveAspectRatio="none" opacity={o} mask={i === 0 ? undefined : `url(#${id}-mask)`} />
						) : null;
					})}
				</g>
				<path d={outside} fill="#05060A" fillOpacity={0.5 * lines} fillRule="evenodd" />
				{lines > 0.001 ? (
					<g opacity={lines}>
						{others.map(([code, ds]) =>
							ds.map((d, i) => (
								<path key={`b${code}${i}`} d={d} fill="none" stroke={colors.muted} strokeOpacity={0.4} strokeWidth={0.9} strokeDasharray={today ? undefined : '4 5'} vectorEffect="non-scaling-stroke" />
							)),
						)}
						{today ? (
							<g filter={`url(#${id}-glow)`} opacity={0.55 * reveal * breathe}>
								{india.map((d, i) => (
									<path key={i} d={d} fill="none" stroke={colors.bronze} strokeWidth={8} vectorEffect="non-scaling-stroke" />
								))}
							</g>
						) : null}
						{india.map((d, i) => (
							<path
								key={`s${i}`}
								d={d}
								fill="none"
								stroke={today ? colors.gold : '#C9B48E'}
								strokeOpacity={today ? 0.4 + 0.4 * reveal : 0.55}
								strokeWidth={today ? 1.6 : 1}
								strokeDasharray={today ? undefined : '4 5'}
								strokeLinejoin="round"
								vectorEffect="non-scaling-stroke"
							/>
						))}
					</g>
				) : null}
				{children}
			</g>
		</svg>
	);
};
