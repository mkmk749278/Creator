// The archive table (plan_v7 §2.3): one physically lit desk (scripts/blender/archive_table.py) where every document
// of a film lies. A document is laid on the table's plane in centimetres and mapped to the screen with the plate's own
// perspective (a homography from the render's reference card), so it sits in the lamp's light (the light pass,
// multiplied over it) with a contact shadow, and moves with the table under one camera.
import {noise2D} from '@remotion/noise';
import React, {createContext, useContext} from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Camera, CamKey} from './Camera';
import {ease, pop, tween} from './motion';

export type TableMeta = {angle: string; px: [number, number]; card_cm: [number, number]; corners: [number, number][]};
type H = number[]; // 3×3 row-major homography

/** Solve the homography taking four (u, v) points to four (x, y) points (8×8 Gaussian elimination). */
export const homography = (src: [number, number][], dst: [number, number][]): H => {
	const A: number[][] = [];
	for (let i = 0; i < 4; i++) {
		const [u, v] = src[i];
		const [x, y] = dst[i];
		A.push([u, v, 1, 0, 0, 0, -u * x, -v * x, x]);
		A.push([0, 0, 0, u, v, 1, -u * y, -v * y, y]);
	}
	for (let c = 0; c < 8; c++) {
		let p = c;
		for (let r = c + 1; r < 8; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
		[A[c], A[p]] = [A[p], A[c]];
		for (let r = 0; r < 8; r++) {
			if (r === c) continue;
			const k = A[r][c] / A[c][c];
			for (let j = c; j < 9; j++) A[r][j] -= k * A[c][j];
		}
	}
	const h = A.map((row, i) => row[8] / row[i]);
	return [h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], 1];
};

const mul = (a: H, b: H): H => {
	const r: H = new Array(9).fill(0);
	for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) for (let k = 0; k < 3; k++) r[i * 3 + j] += a[i * 3 + k] * b[k * 3 + j];
	return r;
};
const apply = (h: H, x: number, y: number): [number, number] => {
	const w = h[6] * x + h[7] * y + h[8];
	return [(h[0] * x + h[1] * y + h[2]) / w, (h[3] * x + h[4] * y + h[5]) / w];
};
const css = (h: H): string => `matrix3d(${h[0]},${h[3]},0,${h[6]},${h[1]},${h[4]},0,${h[7]},0,0,1,0,${h[2]},${h[5]},0,${h[8]})`;

type Ctx = {plane: H; light: string};
const TableCtx = createContext<Ctx | null>(null);

/**
 * The table: the plate filling the frame, the camera over everything. `meta` is the plate's json (table_<angle>.json);
 * `dir` holds table_<angle>.png and table_<angle>_light.png. Children are <TableDoc>s.
 */
export const ArchiveTable: React.FC<{
	meta: TableMeta;
	dir: string;
	keys?: CamKey[];
	seed?: string;
	children?: React.ReactNode;
}> = ({meta, dir, keys = [{f: 0, scale: 1.02}, {f: 600, scale: 1.1}], seed = 'table', children}) => {
	const {width, height} = useVideoConfig();
	const k = Math.max(width / meta.px[0], height / meta.px[1]);
	const ox = (width - meta.px[0] * k) / 2;
	const oy = (height - meta.px[1] * k) / 2;
	const [cw, ch] = meta.card_cm;
	// plane (cm, x right, y toward the viewer's bottom, origin at the card centre) → screen px
	const card: [number, number][] = [
		[-cw / 2, -ch / 2],
		[cw / 2, -ch / 2],
		[cw / 2, ch / 2],
		[-cw / 2, ch / 2],
	];
	const plane = homography(card, meta.corners.map(([x, y]) => [ox + x * k, oy + y * k]));
	const file = (s: string) => staticFile(`${dir}/table_${meta.angle}${s}.png`);
	return (
		<AbsoluteFill style={{background: '#0A0907'}}>
			<Camera keys={keys} seed={seed} drift={1.5}>
				<Img src={file('')} style={{position: 'absolute', left: ox, top: oy, width: meta.px[0] * k, height: meta.px[1] * k}} />
				<TableCtx.Provider value={{plane, light: file('_light')}}>{children}</TableCtx.Provider>
			</Camera>
		</AbsoluteFill>
	);
};

/**
 * A document on the table: `w`×`h` cm, centred at (`x`, `y`) cm from the blotter's centre, turned `rot` degrees.
 * It drops onto the table at `at` (a short fall with its shadow tightening). Children are laid out in a box of
 * `w * ppcm` × `h * ppcm` px (ppcm defaults to 40: a 30 cm letter is 1,200 px wide to lay out).
 * `slide` brings it in from off the table instead of dropping: [dx, dy] cm.
 */
export const TableDoc: React.FC<{
	w: number;
	h: number;
	x?: number;
	y?: number;
	rot?: number;
	at?: number;
	slide?: [number, number];
	ppcm?: number;
	paper?: string;
	seed?: string;
	children?: React.ReactNode;
}> = ({w, h, x = 0, y = 0, rot = 0, at = 0, slide, ppcm = 40, paper = '#E9DEC4', seed = 'doc', children}) => {
	const ctx = useContext(TableCtx);
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	if (!ctx || frame < at - 1) return null;
	const p = pop(frame, fps, at, 120, 18);
	const s = slide ? tween(frame, at, at + 34, 1, 0, ease.arrive) : 0;
	const lift = slide ? 0 : 1 - p; // 0 on the table
	const drift = noise2D(seed, frame / 300, 0) * 0.25;
	const cx = x + (slide ? slide[0] * s : 0);
	const cy = y + (slide ? slide[1] * s : 0) - lift * 2.5;
	const a = ((rot + drift + (slide ? 4 * s : 0)) * Math.PI) / 180;
	const W = w * ppcm;
	const Hh = h * ppcm;
	// doc px → plane cm: rotate about the centre, then translate
	const toPlane: H = [Math.cos(a) / ppcm, -Math.sin(a) / ppcm, cx - (Math.cos(a) * W - Math.sin(a) * Hh) / (2 * ppcm), Math.sin(a) / ppcm, Math.cos(a) / ppcm, cy - (Math.sin(a) * W + Math.cos(a) * Hh) / (2 * ppcm), 0, 0, 1];
	const m = mul(ctx.plane, toPlane);
	const quad = [apply(m, 0, 0), apply(m, W, 0), apply(m, W, Hh), apply(m, 0, Hh)];
	const poly = quad.map(([qx, qy]) => `${qx.toFixed(1)}px ${qy.toFixed(1)}px`).join(',');
	const shadowPts = quad.map(([qx, qy]) => `${(qx + 8 + lift * 30).toFixed(1)},${(qy + 12 + lift * 40).toFixed(1)}`).join(' ');
	const op = slide ? 1 : Math.min(1, p * 2);
	return (
		<AbsoluteFill style={{opacity: op}}>
			{/* contact shadow: soft when the paper is in the air, tight on the table (a blurred polygon, never clipped) */}
			<svg width={width} height={height} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<filter id={`${seed}-sh`} x="-20%" y="-20%" width="140%" height="140%">
					<feGaussianBlur stdDeviation={5 + lift * 18} />
				</filter>
				<polygon points={shadowPts} fill="#000" opacity={0.6 - lift * 0.25} filter={`url(#${seed}-sh)`} />
			</svg>
			<div style={{position: 'absolute', left: 0, top: 0, width: W, height: Hh, transformOrigin: '0 0', transform: css(m), background: paper, overflow: 'hidden'}}>
				{children}
				{/* paper fibre and edge wear */}
				<svg style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'multiply', opacity: 0.3, pointerEvents: 'none'}}>
					<filter id={`${seed}-fib`}>
						<feTurbulence type="fractalNoise" baseFrequency="0.8 0.22" numOctaves={3} seed={11} />
						<feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0.55 0" />
					</filter>
					<rect width="100%" height="100%" filter={`url(#${seed}-fib)`} />
				</svg>
				<div style={{position: 'absolute', inset: 0, boxShadow: 'inset 0 0 60px rgba(90,60,25,0.35)', pointerEvents: 'none'}} />
			</div>
			{/* the lamp's light on the paper: the light pass, multiplied, clipped to the paper */}
			<AbsoluteFill style={{clipPath: `polygon(${poly})`, mixBlendMode: 'multiply'}}>
				<Img src={ctx.light} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(1.06) contrast(0.92)'}} />
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
