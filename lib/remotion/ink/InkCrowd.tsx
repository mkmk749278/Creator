import React from 'react';
import {random} from 'remotion';
import {InkAction, Hands} from './actions';
import {COSTUMES, CostumeName, vary} from './costumes';
import {Costume, Prop} from './draw';
import {InkFigure, InkFigureProps} from './InkFigure';
import {V2} from './rig';

export type CrowdMember = Omit<InkFigureProps, 'seed'> & {seed?: string};

export type InkCrowdProps = {
	seed: string;
	/** Explicit members (drawn with the generated ones, depth-sorted together). */
	members?: CrowdMember[];
	/** Generated members: how many, on which ground band, at what depth scales. */
	count?: number;
	area?: {x0: number; x1: number; yFar: number; yNear: number};
	scaleFar?: number;
	scaleNear?: number;
	/** Costume pool (names or costumes); each member gets a seeded variation of one. */
	cast?: (CostumeName | Costume)[];
	/** Action for member i (data), or a pool to pick from. */
	action?: ((i: number, r: (k: string) => number) => InkAction) | InkAction[];
	hands?: Hands[];
	facing?: 1 | -1 | 'mixed';
	/** Everyone faces this x (a door, a window): overrides `facing`. */
	faceToward?: number;
	look?: V2;
	light?: V2;
	wind?: V2;
	props?: Prop[];
	rim?: number;
	/** Fade far figures into the dark (atmospheric depth), 0..1. */
	haze?: number;
};

/** Places and varies many INK figures: seeded positions, costumes, builds, timing; drawn far to near. */
export const InkCrowd: React.FC<InkCrowdProps> = (p) => {
	const r = (i: number) => (k: string) => random(`${p.seed}-${i}-${k}`);
	const gen: CrowdMember[] = [];
	const n = p.count ?? 0;
	const area = p.area ?? {x0: 0, x1: 1920, yFar: 700, yNear: 1000};
	const cast = p.cast ?? (['dhotiKurta', 'workerCap', 'nauvari', 'elder'] as CostumeName[]);
	for (let i = 0; i < n; i++) {
		const ri = r(i);
		// stratified x so the crowd covers the band without clumps, depth random inside it
		const x = area.x0 + ((i + 0.15 + ri('x') * 0.7) / n) * (area.x1 - area.x0);
		const depth = ri('d');
		const y = area.yFar + depth * (area.yNear - area.yFar);
		const scale = (p.scaleFar ?? 0.5) + depth * ((p.scaleNear ?? 1) - (p.scaleFar ?? 0.5));
		const base = cast[Math.floor(ri('c') * cast.length)];
		const costume = vary(typeof base === 'string' ? COSTUMES[base] : base, ri);
		const action: InkAction =
			typeof p.action === 'function'
				? p.action(i, ri)
				: p.action && p.action.length
					? p.action[Math.floor(ri('a') * p.action.length)]
					: {type: 'wait', hands: p.hands ? p.hands[Math.floor(ri('h') * p.hands.length)] : 'clasp'};
		const facing = p.faceToward !== undefined ? (x < p.faceToward ? 1 : -1) : p.facing === 'mixed' ? (ri('f') < 0.5 ? 1 : -1) : (p.facing ?? 1);
		gen.push({
			costume,
			action,
			x,
			y,
			scale,
			facing,
			look: p.look,
			light: p.light,
			wind: p.wind,
			rim: p.rim,
			t0: ri('t') * 20,
			prop: p.props ? p.props[Math.floor(ri('p') * p.props.length)] : 'none',
			build: {height: 0.94 + ri('ht') * 0.12, girth: 0.9 + ri('g') * 0.2},
			opacity: 1 - (p.haze ?? 0) * (1 - depth),
		});
	}
	const all = [...gen, ...(p.members ?? [])].sort((a, b) => a.y - b.y);
	return (
		<g>
			{all.map((m, i) => (
				<InkFigure key={i} {...m} seed={m.seed ?? `${p.seed}-${i}`} />
			))}
		</g>
	);
};
