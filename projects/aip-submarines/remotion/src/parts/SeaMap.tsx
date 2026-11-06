import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {COUNTRIES} from '../../../../../lib/remotion/map/indiaGeo';
import {project} from '../../../../../lib/remotion/map/IndiaMap';
import {C, F} from '../theme';
import {ez, tw} from './kit';
import bm from '../../../media/bm_plate.json';
import {PlateImage} from '../../../../../lib/remotion/map/PlateImage';

// Maps stand on real ground (§9.3, §9.8): NASA Blue Marble with bathymetry (public domain) reprojected into the
// map projection of India's official boundary (Natural Earth, India's point of view), India filled, neighbours dim.

type LonLat = [number, number];
export const P = {
	arabian: [65.5, 17.0] as LonLat,
	mumbai: [72.84, 18.95] as LonLat,
	hazira: [72.63, 21.09] as LonLat,
	ambernath: [73.19, 19.2] as LonLat,
	karachi: [67.0, 24.85] as LonLat,
	sanya: [109.5, 18.25] as LonLat,
};

type Key = {f: number; lon: number; lat: number; zoom: number};

const camAt = (keys: Key[], f: number) => {
	if (keys.length === 1) {
		return keys[0];
	}
	const fs = keys.map((k) => k.f);
	const o = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const, easing: ez.cam};
	return {
		lon: interpolate(f, fs, keys.map((k) => k.lon), o),
		lat: interpolate(f, fs, keys.map((k) => k.lat), o),
		zoom: Math.exp(interpolate(f, fs, keys.map((k) => Math.log(k.zoom)), o)),
	};
};

export type Pin = {at: number; ll: LonLat; label: string; sub?: string; color?: string; side?: 'left' | 'right'};
export type Route = {a: number; b: number; from: LonLat; to: LonLat; color?: string};

export const SeaMap: React.FC<{
	dur: number;
	mode?: 'arabian' | 'custom';
	keys?: Key[];
	pins?: Pin[];
	routes?: Route[];
	pulse?: {at: number; ll: LonLat};
	shelf?: number; // frame the shallow shelf highlight starts
	dimIndia?: boolean;
}> = ({dur, mode = 'custom', keys, pins = [], routes = [], pulse, shelf, dimIndia}) => {
	const f = useCurrentFrame();
	const ks: Key[] =
		keys ??
		(mode === 'arabian'
			? [
					{f: 0, lon: 72, lat: 18, zoom: 1.2},
					{f: dur, lon: 69, lat: 17.5, zoom: 1.5},
				]
			: [{f: 0, lon: 78, lat: 20, zoom: 1}]);
	const cam = camAt(ks, f);
	const [cx, cy] = project([cam.lon, cam.lat]);
	const z = cam.zoom * 1.1; // px per map unit (3 km)
	const tf = `translate(${960 - cx * z} ${540 - cy * z}) scale(${z})`;
	const b = bm.mapBounds;
	const pl = pulse ?? (mode === 'arabian' ? {at: 4, ll: P.arabian} : undefined);
	return (
		<AbsoluteFill style={{background: '#020a12'}}>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<defs>
					<filter id="indGlow" x="-10%" y="-10%" width="120%" height="120%">
						<feGaussianBlur stdDeviation="2.5" />
					</filter>
				</defs>
				<g transform={tf}>
					<PlateImage href={staticFile('assets/media/maps/bm_plate.jpg')} x={b[0]} y={b[1]} width={b[2] - b[0]} height={b[3] - b[1]} preserveAspectRatio="none" style={{filter: 'brightness(0.62) saturate(0.8)'}} />
					{Object.entries(COUNTRIES).map(([k, ds]) =>
						ds.map((d, i) => (
							<path
								key={k + i}
								d={d}
								fill={k === 'IND' ? (dimIndia ? 'rgba(242,169,59,0.06)' : 'rgba(242,169,59,0.13)') : 'rgba(2,6,10,0.38)'}
								stroke={k === 'IND' ? C.amber : 'rgba(200,210,220,0.35)'}
								strokeWidth={(k === 'IND' ? 2.2 : 1) / z}
							/>
						)),
					)}
					{shelf !== undefined ? <Shelf at={shelf} z={z} /> : null}
					{routes.map((r, i) => {
						const [x0, y0] = project(r.from);
						const [x1, y1] = project(r.to);
						const k = tw(f, r.a, r.b, 0, 1, ez.sweep);
						const mx = (x0 + x1) / 2 + (y1 - y0) * 0.25;
						const my = (y0 + y1) / 2 - (x1 - x0) * 0.25;
						return (
							<path key={i} d={`M${x0} ${y0} Q${mx} ${my} ${x1} ${y1}`} fill="none" stroke={r.color ?? C.cyan} strokeWidth={5 / z} pathLength={1} strokeDasharray={`${k} 1`} strokeLinecap="round" />
						);
					})}
				</g>
				{pl && f >= pl.at
					? (() => {
							const [px, py] = project(pl.ll);
							const sx = 960 + (px - cx) * z;
							const sy = 540 + (py - cy) * z;
							const age = ((f - pl.at) % 45) / 45;
							return (
								<g>
									<circle cx={sx} cy={sy} r={12} fill={C.cyan} />
									<circle cx={sx} cy={sy} r={14 + 70 * age} fill="none" stroke={C.cyan} strokeWidth={4} opacity={1 - age} />
								</g>
							);
						})()
					: null}
				{pins.map((p, i) => {
					const [px, py] = project(p.ll);
					const sx = 960 + (px - cx) * z;
					const sy = 540 + (py - cy) * z;
					const k = tw(f, p.at, p.at + 14, 0, 1, ez.arrive);
					if (k <= 0) {
						return null;
					}
					const left = p.side === 'left';
					return (
						<g key={i} opacity={k}>
							<circle cx={sx} cy={sy} r={11 * k} fill={p.color ?? C.amber} stroke="#000" strokeWidth={3} />
							<line x1={sx} y1={sy} x2={sx + (left ? -60 : 60)} y2={sy - 40} stroke={p.color ?? C.amber} strokeWidth={3} />
						</g>
					);
				})}
			</svg>
			{pins.map((p, i) => {
				const [px, py] = project(p.ll);
				const sx = 960 + (px - cx) * z;
				const sy = 540 + (py - cy) * z;
				const k = tw(f, p.at, p.at + 14, 0, 1, ez.arrive);
				if (k <= 0) {
					return null;
				}
				const left = p.side === 'left';
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: sx + (left ? -66 : 66),
							top: sy - 70,
							transform: left ? 'translateX(-100%)' : undefined,
							opacity: k,
							textAlign: left ? 'right' : 'left',
						}}
					>
						<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 46, color: p.color ?? C.ink, background: 'rgba(3,7,13,0.78)', padding: '4px 14px', whiteSpace: 'nowrap'}}>{p.label}</div>
						{p.sub ? (
							<div style={{fontFamily: F.label, fontWeight: 700, fontSize: 32, color: C.dim, background: 'rgba(3,7,13,0.78)', padding: '2px 14px', marginTop: 4, whiteSpace: 'nowrap', display: 'inline-block'}}>
								{p.sub}
							</div>
						) : null}
					</div>
				);
			})}
			<div style={{position: 'absolute', right: 80, bottom: 230, fontFamily: F.label, fontWeight: 700, fontSize: 26, color: C.dim, opacity: 0.85}}>
				NASA BLUE MARBLE · NATURAL EARTH
			</div>
			<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,${0.35 + 0.05 * noise2D('mv', f / 200, 0)}) 100%)`}} />
		</AbsoluteFill>
	);
};

/** The shallow shelf off India's west coast, shown as a soft cyan band along the coast (the bathymetry under it). */
const Shelf: React.FC<{at: number; z: number}> = ({at, z}) => {
	const f = useCurrentFrame();
	const k = tw(f, at, at + 30, 0, 1, ez.arrive);
	return (
		<path d={COUNTRIES.IND[0]} fill="none" stroke={C.cyan} strokeOpacity={0.45 * k} strokeWidth={34 / Math.sqrt(z)} strokeLinejoin="round" style={{filter: 'blur(6px)'}} />
	);
};

export const ImgPlate = Img;
