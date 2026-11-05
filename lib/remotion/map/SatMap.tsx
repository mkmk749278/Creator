// Satellite map (plan_v7 §2.4): real ground under every map. Plates are images in the film's map projection
// (scripts/bluemarble_india.py for all-India, scripts/sat_crop.py for Sentinel-2 close-ups), placed by their bounds in
// map units, so India's official boundary (PLAYBOOK §6.6), the pins and the routes of IndiaMap.tsx sit exactly on
// them. The camera is the same MapCam as IndiaMap; `tilt` leans the ground away from the lens like a slow aerial shot.
import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {colors} from '../brand';
import {ease} from '../motion';
import {COUNTRIES} from './indiaGeo';
import {MapCam} from './IndiaMap';
import {PlateImage} from './PlateImage';

export type SatPlate = {
	file: string;
	/** [x0, y0, x1, y1] in map units (the plate's json `mapBounds`) */
	bounds: [number, number, number, number];
	/** plate pixels across; with bounds this gives the zoom at which the plate is sharp */
	px?: number;
	/** override: fade the plate in between these zooms (px per map unit) */
	fade?: [number, number];
};

export type SatGrade = 'night' | 'day' | 'archive' | 'cyan';

const GRADE: Record<SatGrade, {filter: string; tint: string}> = {
	// the channel look: deep charcoal sea, warm earth, a touch of bronze
	night: {filter: 'saturate(0.82) contrast(1.1) brightness(0.86) sepia(0.1)', tint: 'rgba(197,125,60,0.08)'},
	day: {filter: 'saturate(0.92) contrast(1.06) brightness(0.92)', tint: 'rgba(0,0,0,0)'},
	archive: {filter: 'saturate(0.35) sepia(0.45) contrast(1.15) brightness(0.82)', tint: 'rgba(197,125,60,0.14)'},
	cyan: {filter: 'saturate(0.7) contrast(1.1) brightness(0.8) hue-rotate(-6deg)', tint: 'rgba(60,170,190,0.10)'},
};

const src = (f: string): string => (f.startsWith('http') ? f : staticFile(f));



export const SatMap: React.FC<{
	cam: MapCam;
	plates: SatPlate[];
	/** degrees the ground leans back (0 = straight down) */
	tilt?: number;
	/** 0..1: how much the land outside India is dimmed */
	dimOutside?: number;
	/** India's official boundary: 'today' (gold line), 'faint' (dashed, period maps) or 'none' */
	boundary?: 'today' | 'faint' | 'none';
	grade?: SatGrade;
	children?: React.ReactNode;
	id?: string;
}> = ({cam, plates, tilt = 0, dimOutside = 0.45, boundary = 'today', grade = 'night', children, id = 'sat'}) => {
	const frame = useCurrentFrame();
	const tf = `translate(960 540) scale(${cam.zoom.toFixed(5)}) translate(${(-cam.x).toFixed(3)} ${(-cam.y).toFixed(3)})`;
	const india = COUNTRIES.IND;
	const others = useMemo(() => Object.entries(COUNTRIES).filter(([k]) => k !== 'IND'), []);
	const g = GRADE[grade];
	const breathe = 0.85 + 0.15 * Math.sin(frame / 50);
	// The boundary file is drawn for country-scale views (Natural Earth 1:10m): close in, the real coast is the line.
	const lines = interpolate(Math.log(cam.zoom), [Math.log(3), Math.log(7)], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const dim = dimOutside * lines;
	// a huge rectangle with India cut out (even-odd): the dim outside India
	const outside = `M-5000 -5000H5000V5000H-5000Z ${india.join(' ')}`;
	// tilted ground needs overscan so its far edge never shows
	const over = 1 + tilt / 40;
	return (
		<AbsoluteFill style={{background: '#07080A', overflow: 'hidden', perspective: 1400, perspectiveOrigin: '50% 30%'}}>
			<AbsoluteFill style={{transform: `rotateX(${tilt}deg) scale(${over})`, transformOrigin: '50% 60%'}}>
				<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>
					<defs>
						<filter id={`${id}-glow`} x="-20%" y="-20%" width="140%" height="140%">
							<feGaussianBlur stdDeviation={8} />
						</filter>
						{/* soft edges for detail plates, so a Sentinel-2 close-up melts into the all-India plate */}
						<radialGradient id={`${id}-feather`} cx="0.5" cy="0.5" r="0.5">
							<stop offset="0.62" stopColor="#fff" />
							<stop offset="1" stopColor="#000" />
						</radialGradient>
						<mask id={`${id}-mask`} maskContentUnits="objectBoundingBox">
							<rect width={1} height={1} fill={`url(#${id}-feather)`} />
						</mask>
					</defs>
					<g transform={tf}>
						<g style={{filter: g.filter}}>
							{plates.map((p, i) => {
								const [x0, y0, x1, y1] = p.bounds;
								// The base plate (i = 0) is always on. A detail plate fades in as the base starts to go soft
								// (past its own sharp zoom) and is fully in well before it fills the frame.
								const base = plates[0];
								const baseSharp = base.px ? base.px / (base.bounds[2] - base.bounds[0]) : 1;
								const [za, zb] = p.fade ?? [baseSharp * 0.9, baseSharp * 3];
								const o = i === 0 || za <= 0 ? 1 : interpolate(Math.log(cam.zoom), [Math.log(za), Math.log(zb)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
								return o > 0.001 ? (
									<PlateImage
										key={p.file}
										href={src(p.file)}
										x={x0}
										y={y0}
										width={x1 - x0}
										height={y1 - y0}
										preserveAspectRatio="none"
										opacity={o}
										mask={i === 0 ? undefined : `url(#${id}-mask)`}
									/>
								) : null;
							})}
						</g>
						<path d={outside} fill="#05060A" fillOpacity={dim} fillRule="evenodd" />
						{boundary !== 'none' && lines > 0.001 ? (
							<g opacity={lines}>
								{others.map(([code, ds]) =>
									ds.map((d, i) => (
										<path key={`b${code}${i}`} d={d} fill="none" stroke={colors.muted} strokeOpacity={0.35} strokeWidth={0.9} strokeDasharray={boundary === 'faint' ? '4 5' : undefined} vectorEffect="non-scaling-stroke" />
									)),
								)}
								{boundary === 'today' ? (
									<g filter={`url(#${id}-glow)`} opacity={0.55 * breathe}>
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
										stroke={boundary === 'today' ? colors.gold : colors.muted}
										strokeOpacity={boundary === 'today' ? 0.75 : 0.5}
										strokeWidth={boundary === 'today' ? 1.6 : 1}
										strokeDasharray={boundary === 'faint' ? '4 5' : undefined}
										strokeLinejoin="round"
										vectorEffect="non-scaling-stroke"
									/>
								))}
							</g>
						) : null}
						{children}
					</g>
				</svg>
				<AbsoluteFill style={{background: g.tint, mixBlendMode: 'overlay', pointerEvents: 'none'}} />
			</AbsoluteFill>
			{/* haze toward the far edge of tilted ground, like air over a real landscape */}
			{tilt > 0 ? (
				<AbsoluteFill style={{background: `linear-gradient(180deg, rgba(14,16,20,${Math.min(0.85, tilt / 40)}) 0%, rgba(14,16,20,0) 45%)`}} />
			) : null}
		</AbsoluteFill>
	);
};

/** Ease a tilt between keys (local frames). */
export const tiltAt = (frame: number, keys: {f: number; t: number}[]): number =>
	keys.length === 1 ? keys[0].t : interpolate(frame, keys.map((k) => k.f), keys.map((k) => k.t), {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease.camera});

/** Plate helper from a sat_crop.py / bluemarble_india.py json. */
export const plate = (file: string, meta: {mapBounds: number[]; px: number[]}, fade?: [number, number]): SatPlate => ({
	file,
	bounds: meta.mapBounds as [number, number, number, number],
	px: meta.px[0],
	fade,
});

