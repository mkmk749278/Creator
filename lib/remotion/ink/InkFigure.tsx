import React from 'react';
import {random, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {InkAction, actionPose} from './actions';
import {COSTUMES, CostumeName} from './costumes';
import {Costume, InkStyle, Prop, drawFigure} from './draw';
import {Build, Pose, V2, buildFor, seedOf, solve, sub} from './rig';

/** The INK look (PLAYBOOK §8.9): bronze ink on charcoal, a soft ember rim where the figure is lit. */
export const inkPalette = {
	ink: '#D59B5F',
	inkSoft: 'rgba(213,155,95,0.55)',
	gold: colors.gold,
	skin: '#2A1F18',
	rim: colors.ember,
	shadow: 'rgba(0,0,0,0.55)',
} as const;

/** Ink cross-hatching for the side away from the light: one diagonal stroke per 7 px tile. */
const HATCH = `data:image/svg+xml,${encodeURIComponent(
	"<svg xmlns='http://www.w3.org/2000/svg' width='7' height='7'><path d='M-1 8L8 -1' stroke='#D59B5F' stroke-width='0.8' stroke-opacity='0.5'/></svg>",
)}`;

export type InkFigureProps = {
	/** What the figure does (data): wait, walk, ride… Defaults to a dignified wait. */
	action?: InkAction;
	/** A static pose override on top of the action. */
	pose?: Partial<Pose>;
	costume: Costume | CostumeName;
	age?: Build['age'];
	female?: boolean;
	build?: Partial<Build>;
	/** Ground point in the stage (px). */
	x: number;
	y: number;
	scale?: number;
	facing?: 1 | -1;
	/** Where the eyes and head go, in stage px. */
	look?: V2;
	seed: string;
	/** Light source in stage px (the rim light comes from it). */
	light?: V2;
	/** Rim light strength 0..1. */
	rim?: number;
	/** Time offset in seconds (figures in a crowd are never in step). */
	t0?: number;
	prop?: Prop;
	/** Wind on cloth, stage px per second. */
	wind?: V2;
	/** Extra second ink pass and finer boil (close shots). */
	detail?: boolean;
	shadow?: boolean;
	opacity?: number;
	/** Local frame override (to drive the figure from a parent clock). */
	frame?: number;
};

const femaleCostume = (c: Costume): boolean => c.bottom === 'nauvari' || c.bottom === 'saree' || c.top === 'blouse' || c.top === 'frock';

export const resolveCostume = (c: Costume | CostumeName): Costume => (typeof c === 'string' ? COSTUMES[c] : c);

export const InkFigure: React.FC<InkFigureProps> = (p) => {
	const cur = useCurrentFrame();
	const {fps} = useVideoConfig();
	const frame = p.frame ?? cur;
	const t = frame / fps + (p.t0 ?? 0);
	const costume = resolveCostume(p.costume);
	const female = p.female ?? femaleCostume(costume);
	const age = p.age ?? (costume.hair === 'child' || costume.hair === 'plait' ? 'child' : costume.hair === 'grey' || costume.hair === 'greyBun' ? 'old' : 'adult');
	const build: Build = {...buildFor(age, female), ...p.build};
	const seed = seedOf(p.seed);
	const scale = p.scale ?? 1;
	const facing = p.facing ?? 1;
	const action: InkAction = p.action ?? {type: 'wait', hands: 'clasp'};

	// travel is measured from the figure's own clock offset, so (x, y) is where it stands at frame 0
	const travel0 = actionPose(action, p.t0 ?? 0, build, seed).travel;
	const at = (tt: number) => {
		const r = actionPose(action, tt, build, seed);
		const pose: Pose = {...r.pose, ...p.pose};
		const X = p.x + (r.travel - travel0) * scale * facing;
		if (p.look) {
			pose.look = [((p.look[0] - X) / scale) * facing, (p.look[1] - p.y) / scale];
			pose.lookWeight = Math.max(pose.lookWeight, 0.85);
		}
		if (p.wind) {
			pose.wind = [(p.wind[0] / scale) * facing, p.wind[1] / scale];
		}
		return {S: solve(pose, build), X};
	};
	const now = at(t);
	const prev = at(t - 1 / 30);
	const vel: V2 = [(now.S.neck[0] - prev.S.neck[0]) * 30 + ((now.X - prev.X) * 30 * facing) / scale, (now.S.neck[1] - prev.S.neck[1]) * 30];

	// light direction (world), for the rim and for heavier lines on the shadow side
	const centre: V2 = [now.X, p.y - 200 * scale * build.height];
	const L = p.light ? sub(p.light, centre) : ([0.6, -0.8] as V2);
	const lm = Math.hypot(L[0], L[1]) || 1;
	const style: InkStyle = {
		ink: inkPalette.ink,
		inkSoft: inkPalette.inkSoft,
		gold: inkPalette.gold,
		skin: inkPalette.skin,
		// lines grow slower than the figure: ~2.2 px at scale 1, ~3.4 px at 2.4, never under 1.3 px far away
		lw: Math.max(2.2 / Math.sqrt(scale), 1.3 / scale),
		boilAmp: Math.max(0.9, 0.45 / scale),
		sketch: p.detail ?? scale > 1.4,
		shade: [(-L[0] / lm) * facing, -L[1] / lm],
	};
	const prims = drawFigure(now.S, costume, t, seed, style, vel, p.prop ?? 'none');

	// rim light: the silhouette's edge on the side facing the light, in ember, inside the figure, plus a soft glow;
	// form shade: a soft darkening inside the silhouette on the side away from the light
	const id = `ink-rim-${p.seed.replace(/[^a-zA-Z0-9_-]/g, '')}`;
	const rimPx = 2.6 * Math.max(0.6, Math.min(scale, 1.8));
	const rim = p.rim ?? 0.9;
	const dx = (-L[0] / lm) * rimPx;
	const dy = (-L[1] / lm) * rimPx;
	// the hatch tile travels with the figure (no shower-door slide) and boils with the 12 fps line
	const hx = (now.X % 7) - 7 + (Math.floor(t * 12) % 2) * 0.5;
	const hy = (p.y % 7) - 7;
	const shadowW = 46 * scale * build.height;

	return (
		<g opacity={p.opacity ?? 1}>
			<defs>
				<filter id={id} x="-30%" y="-15%" width="160%" height="130%" colorInterpolationFilters="sRGB">
					<feOffset in="SourceAlpha" dx={dx} dy={dy} result="moved" />
					<feComposite in="SourceAlpha" in2="moved" operator="out" result="edge" />
					<feGaussianBlur in="edge" stdDeviation={rimPx * 0.35} result="edgeSoft" />
					<feFlood floodColor={inkPalette.rim} floodOpacity={rim} />
					<feComposite in2="edgeSoft" operator="in" result="rimLight" />
					<feComposite in="rimLight" in2="SourceAlpha" operator="in" result="rimInside" />
					<feGaussianBlur in="rimLight" stdDeviation={rimPx * 1.6} result="glow" />
					<feComponentTransfer in="glow" result="glowSoft">
						<feFuncA type="linear" slope={0.55} />
					</feComponentTransfer>
					<feOffset in="SourceAlpha" dx={-dx * 4} dy={-dy * 4} result="toward" />
					<feComposite in="SourceAlpha" in2="toward" operator="out" result="far" />
					<feGaussianBlur in="far" stdDeviation={rimPx * 2.5} result="farSoft" />
					<feFlood floodColor="#000" floodOpacity={0.5} />
					<feComposite in2="farSoft" operator="in" />
					<feComposite in2="SourceAlpha" operator="in" result="shade" />
					<feImage href={HATCH} x={hx} y={hy} width={7} height={7} result="tile" />
					<feTile in="tile" result="hatch" />
					<feComposite in="hatch" in2="farSoft" operator="in" />
					<feComposite in2="SourceAlpha" operator="in" result="hatched" />
					<feMerge result="base">
						<feMergeNode in="glowSoft" />
						<feMergeNode in="SourceGraphic" />
						<feMergeNode in="shade" />
						<feMergeNode in="hatched" />
					</feMerge>
					<feBlend in="rimInside" in2="base" mode="screen" />
				</filter>
			</defs>
			{p.shadow === false ? null : (
				<ellipse cx={now.X} cy={p.y + 2 * scale} rx={shadowW} ry={shadowW * 0.16} fill={inkPalette.shadow} style={{filter: `blur(${4 * scale}px)`}} />
			)}
			<g filter={`url(#${id})`}>
				<g transform={`translate(${now.X.toFixed(2)} ${p.y.toFixed(2)}) scale(${(scale * facing).toFixed(4)} ${scale.toFixed(4)})`}>
					{prims.map((q, i) => (
						<path
							key={i}
							d={q.d}
							fill={q.fill}
							stroke={q.stroke}
							strokeWidth={q.w}
							strokeLinecap="round"
							strokeLinejoin="round"
							opacity={q.op}
							transform={q.dx !== undefined ? `translate(${q.dx.toFixed(2)} ${(q.dy ?? 0).toFixed(2)})` : undefined}
						/>
					))}
				</g>
			</g>
		</g>
	);
};

/** Seeded helper for scenes: a deterministic random in [a, b). */
export const rr = (seed: string, a = 0, b = 1): number => a + random(seed) * (b - a);
