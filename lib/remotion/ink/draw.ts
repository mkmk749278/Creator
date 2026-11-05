// INK drawing: a solved skeleton + a costume → ink primitives (SVG paths), pure.
// Each body part is a "mass": every shape's ink outline is drawn first, then every fill, so the shapes of one mass
// merge into one silhouette with one clean outline (a dhoti's two legs and its drape read as one cloth). The outline
// is drawn twice, the second copy nudged away from the light, so lines are thin where lit and heavy in shadow, as a
// brush would lay them.
import {Skeleton, V2, add, boil, clamp, hash, lerp, lerp2, mul, rot, rotV, sub} from './rig';

export type Headwear = 'bare' | 'turban' | 'pheta' | 'parsiCap' | 'millCap' | 'headCloth' | 'helmet';
export type Hair = 'short' | 'grey' | 'bald' | 'bun' | 'greyBun' | 'child' | 'plait';
export type Top = 'kurta' | 'vest' | 'shirt' | 'coat' | 'blouse' | 'tshirt' | 'frock' | 'none';
export type Bottom = 'dhoti' | 'dhotiShort' | 'trousers' | 'pyjama' | 'nauvari' | 'saree' | 'shorts' | 'skirt';
export type Prop = 'none' | 'pouch' | 'cane' | 'cap' | 'tiffin' | 'bundle';

/** Cloth tones from dark to light; the ink line does the drawing, tone only separates the masses. */
export type Tone = 'white' | 'light' | 'mid' | 'dark' | 'black' | 'maroon' | 'indigo' | 'ochre' | 'green';

export type Costume = {
	head: Headwear;
	hair: Hair;
	top: Top;
	topTone: Tone;
	bottom: Bottom;
	bottomTone: Tone;
	waistcoat?: boolean;
	/** Saree end: over the shoulder, or over the head (older women, the 1900s). */
	pallu?: 'shoulder' | 'head';
	/** Zari border on the saree (a gold line). */
	border?: boolean;
	/** A cloth (gamcha) over the shoulder. */
	gamcha?: boolean;
	moustache?: boolean;
	beard?: boolean;
	glasses?: boolean;
	/** Turban tail hanging behind (shamla). */
	tail?: boolean;
	headTone?: Tone;
	/** Shoes instead of bare feet or sandals. */
	shoes?: boolean;
};

export type InkStyle = {
	ink: string;
	inkSoft: string;
	gold: string;
	skin: string;
	/** Line width in figure units. */
	lw: number;
	/** Boil amplitude in figure units. */
	boilAmp: number;
	/** Second, thinner sketch pass (close shots). */
	sketch: boolean;
	/** Unit vector pointing away from the light, figure space (heavier lines on that side). */
	shade: V2;
};

export const toneFill: Record<Tone, string> = {
	white: '#302C27',
	light: '#262320',
	mid: '#1E1C1B',
	dark: '#161618',
	black: '#0A0A0C',
	maroon: '#2A1615',
	indigo: '#161925',
	ochre: '#2C2116',
	green: '#17201A',
};

export type Prim = {d: string; fill: string; stroke: string; w: number; op?: number; line?: boolean; dx?: number; dy?: number};

type Shape =
	| {kind: 'tube'; pts: V2[]; w: number}
	| {kind: 'poly'; pts: V2[]; smooth?: boolean}
	| {kind: 'ell'; c: V2; rx: number; ry: number; rot: number};

const f1 = (n: number): string => (Math.round(n * 10) / 10).toString();

export const smoothOpen = (pts: V2[]): string => {
	if (pts.length === 2) {
		return `M${f1(pts[0][0])} ${f1(pts[0][1])}L${f1(pts[1][0])} ${f1(pts[1][1])}`;
	}
	if (pts.length === 3) {
		// Creator's limb: a quadratic that passes through the middle joint
		const [a, b, c] = pts;
		const k: V2 = [2 * b[0] - (a[0] + c[0]) / 2, 2 * b[1] - (a[1] + c[1]) / 2];
		return `M${f1(a[0])} ${f1(a[1])}Q${f1(k[0])} ${f1(k[1])} ${f1(c[0])} ${f1(c[1])}`;
	}
	let d = `M${f1(pts[0][0])} ${f1(pts[0][1])}`;
	for (let i = 0; i < pts.length - 1; i++) {
		const p0 = pts[Math.max(0, i - 1)];
		const p1 = pts[i];
		const p2 = pts[i + 1];
		const p3 = pts[Math.min(pts.length - 1, i + 2)];
		const c1 = add(p1, mul(sub(p2, p0), 1 / 6));
		const c2 = sub(p2, mul(sub(p3, p1), 1 / 6));
		d += `C${f1(c1[0])} ${f1(c1[1])} ${f1(c2[0])} ${f1(c2[1])} ${f1(p2[0])} ${f1(p2[1])}`;
	}
	return d;
};

export const smoothClosed = (pts: V2[]): string => {
	const n = pts.length;
	let d = `M${f1(pts[0][0])} ${f1(pts[0][1])}`;
	for (let i = 0; i < n; i++) {
		const p0 = pts[(i - 1 + n) % n];
		const p1 = pts[i];
		const p2 = pts[(i + 1) % n];
		const p3 = pts[(i + 2) % n];
		const c1 = add(p1, mul(sub(p2, p0), 1 / 6));
		const c2 = sub(p2, mul(sub(p3, p1), 1 / 6));
		d += `C${f1(c1[0])} ${f1(c1[1])} ${f1(c2[0])} ${f1(c2[1])} ${f1(p2[0])} ${f1(p2[1])}`;
	}
	return d + 'Z';
};

const polyPath = (pts: V2[]): string => `M${pts.map((p) => `${f1(p[0])} ${f1(p[1])}`).join('L')}Z`;

export const ellPts = (c: V2, rx: number, ry: number, r: number, n = 14): V2[] =>
	new Array(n).fill(0).map((_, i) => {
		const a = (i / n) * Math.PI * 2;
		return add(c, rot(Math.cos(a) * rx, Math.sin(a) * ry, r));
	});

const norm = (v: V2): V2 => {
	const m = Math.hypot(v[0], v[1]) || 1;
	return [v[0] / m, v[1] / m];
};

/** Left-hand normal of a→b (for a figure facing +x and a limb pointing down, this is "forward"). */
const perp = (a: V2, b: V2): V2 => {
	const d = norm(sub(b, a));
	return [-d[1], d[0]].map((v) => -v) as V2;
};

/** Tighten the given corners of a closed smooth outline (adds two close neighbours so the curve turns sharply). */
const tight = (pts: V2[], corners: number[], k = 0.12): V2[] => {
	const out: V2[] = [];
	pts.forEach((p, i) => {
		if (!corners.includes(i)) {
			out.push(p);
			return;
		}
		const a = pts[(i - 1 + pts.length) % pts.length];
		const b = pts[(i + 1) % pts.length];
		out.push(lerp2(p, a, k), p, lerp2(p, b, k));
	});
	return out;
};

/** A drawing context: jitters points with the 12 fps boil and collects primitives in draw order. */
class Pen {
	prims: Prim[] = [];
	private id = 0;
	constructor(
		private t: number,
		private seed: number,
		public st: InkStyle,
	) {}
	j(p: V2, amp = this.st.boilAmp * 0.45): V2 {
		this.id += 1;
		return add(p, boil(this.t, this.seed * 31 + this.id, amp));
	}
	jp(pts: V2[], amp?: number): V2[] {
		return pts.map((p) => this.j(p, amp));
	}
	mass(shapes: Shape[], fill: string, outline = this.st.ink): void {
		const lw = this.st.lw;
		const [sx, sy] = this.st.shade;
		const ds = shapes.map((s) => {
			if (s.kind === 'tube') {
				return {d: smoothOpen(this.jp(s.pts)), tube: s.w};
			}
			if (s.kind === 'poly') {
				const pts = this.jp(s.pts);
				return {d: s.smooth === false ? polyPath(pts) : smoothClosed(pts), tube: 0};
			}
			return {d: smoothClosed(this.jp(ellPts(s.c, s.rx, s.ry, s.rot))), tube: 0};
		});
		for (const s of ds) {
			const o: Prim = s.tube ? {d: s.d, fill: 'none', stroke: outline, w: s.tube + lw * 2} : {d: s.d, fill: outline, stroke: outline, w: lw * 2};
			this.prims.push(o, {...o, dx: sx * lw * 0.85, dy: sy * lw * 0.85});
		}
		for (const s of ds) {
			this.prims.push(s.tube ? {d: s.d, fill: 'none', stroke: fill, w: s.tube} : {d: s.d, fill, stroke: 'none', w: 0});
		}
	}
	line(pts: V2[], w = this.st.lw * 0.75, color = this.st.ink, op?: number): void {
		this.prims.push({d: smoothOpen(this.jp(pts, this.st.boilAmp * 0.3)), fill: 'none', stroke: color, w, op, line: true});
	}
	dot(c: V2, rx: number, ry: number, color = this.st.ink, r = 0): void {
		this.prims.push({d: smoothClosed(ellPts(this.j(c, this.st.boilAmp * 0.15), rx, ry, r, 8)), fill: color, stroke: 'none', w: 0});
	}
}

/** Offset a polyline sideways by `o` (for borders). */
const offsetLine = (pts: V2[], o: number): V2[] =>
	pts.map((p, i) => {
		const a = pts[Math.max(0, i - 1)];
		const b = pts[Math.min(pts.length - 1, i + 1)];
		return add(p, mul(perp(a, b), o));
	});

/** A hanging cloth tail: from `base`, falling along `dir`, rippling, pushed by wind and by the body's velocity. */
const clothTail = (base: V2, dir: V2, length: number, n: number, t: number, wind: V2, vel: V2, phase: number, ripple = 1): V2[] => {
	const pts: V2[] = [base];
	const push: V2 = [clamp(wind[0] - vel[0] * 0.35, -900, 900), clamp(wind[1] - vel[1] * 0.25, -900, 900)];
	const strength = Math.hypot(push[0], push[1]);
	const freq = 3.2 + strength * 0.012;
	for (let i = 1; i <= n; i++) {
		const s = i / n;
		const wave = Math.sin(t * freq * 2 - i * 1.1 + phase) * s * length * 0.035 * ripple * (1 + strength * 0.004);
		const bend: V2 = mul(push, (s * s * length) / 900);
		const pd: V2 = [-dir[1], dir[0]];
		pts.push(add(base, add(mul(dir, length * s), add(mul(pd, wave), bend))));
	}
	return pts;
};

/** A hand: a tapered mitten along the forearm, the fingers curled a little toward the body. */
const handShape = (wrist: V2, elbow: V2, h: number, curl = 18): V2[] => {
	const d = rotV(norm(sub(wrist, elbow)), curl);
	const n: V2 = [-d[1], d[0]];
	const P = (a: number, b: number): V2 => add(wrist, add(mul(d, a * h), mul(n, b * h)));
	return [P(-1, 3.4), P(5, 3.8), P(10.5, 1.8), P(11, -0.6), P(8, -2.8), P(3, -3.6), P(-1, -3.2)];
};

/** A foot: heel, sole and toes, tilted with the step. */
const footShape = (ankle: V2, tilt: number, h: number, shoe: boolean): V2[] => {
	const s = shoe ? 1.1 : 1;
	const P = (x: number, y: number): V2 => add(ankle, rot(x * h * s, y * h, tilt));
	return [P(-4, -3), P(-6.5, 3), P(-5, 9), P(14, 9.5), P(17, 7), P(13, 3.5), P(4, -1)];
};

export const drawFigure = (S: Skeleton, C: Costume, t: number, seed: number, st: InkStyle, vel: V2, prop: Prop): Prim[] => {
	const pen = new Pen(t, seed, st);
	const k = S.k;
	const h = S.build.height;
	const g = S.build.girth;
	const fem = S.build.female;
	const up = rot(0, -1, S.lean);
	const fwd = rot(1, 0, S.lean);
	const T = (along: number, off: number): V2 => add(S.hip, add(mul(up, along * k.torso), mul(fwd, off)));
	const skin = st.skin;
	const top = toneFill[C.topTone];
	const bot = toneFill[C.bottomTone];

	// joints with the boil (Creator: jitter the joints once at 12 fps, build every shape from them)
	let jid = 0;
	const J = (p: V2, amp = st.boilAmp): V2 => add(p, boil(t, seed * 7 + ++jid * 5.1, amp));
	const kneeF = J(S.kneeF);
	const kneeB = J(S.kneeB);
	const ankleF = J(S.ankleF);
	const ankleB = J(S.ankleB);
	const elbowF = J(S.elbowF);
	const elbowB = J(S.elbowB);
	const handF = J(S.handF);
	const handB = J(S.handB);

	const longSleeve = C.top === 'kurta' || C.top === 'coat';
	const halfSleeve = C.top === 'shirt' || C.top === 'tshirt' || C.top === 'blouse' || C.top === 'frock';
	const armW = (fem ? 0.88 : 1) * g;
	const armMass = (sh: V2, el: V2, hd: V2, front: boolean): void => {
		if (longSleeve) {
			pen.mass([{kind: 'tube', pts: [sh, el, lerp2(el, hd, 0.86)], w: 12 * h * armW}], top);
			// a crease at the elbow, the cuff
			const ed = norm(sub(hd, el));
			pen.line([add(el, mul([-ed[1], ed[0]], 4 * h)), add(el, add(mul(ed, 3 * h), mul([-ed[1], ed[0]], -2 * h)))], st.lw * 0.5, st.inkSoft);
		} else if (halfSleeve) {
			pen.mass([{kind: 'tube', pts: [el, hd], w: 7.6 * h * armW}], skin);
			const mid = lerp2(sh, el, C.top === 'blouse' ? 0.42 : 0.82);
			pen.mass([{kind: 'tube', pts: [sh, el], w: 9.4 * h * armW}], skin);
			pen.mass([{kind: 'tube', pts: [sh, mid], w: 11.8 * h * armW}], top);
		} else {
			pen.mass(
				[
					{kind: 'tube', pts: [sh, el], w: 9.6 * h * armW},
					{kind: 'tube', pts: [el, hd], w: 7.6 * h * armW},
				],
				skin,
			);
		}
		pen.mass([{kind: 'poly', pts: handShape(hd, el, h * (fem ? 0.9 : 1), front ? 18 : 10)}], skin);
	};

	const legCloth = C.bottom === 'trousers' || C.bottom === 'pyjama';
	const legMass = (hp: V2, kn: V2, an: V2, tilt: number): void => {
		pen.mass([{kind: 'poly', pts: footShape(an, tilt, h, !!C.shoes)}], C.shoes ? toneFill.black : skin);
		if (legCloth) {
			const w = (C.bottom === 'pyjama' ? 16 : 14.5) * h * g;
			pen.mass([{kind: 'tube', pts: [hp, kn, an], w}], bot);
		} else {
			pen.mass(
				[
					{kind: 'tube', pts: [hp, kn], w: 12 * h * g},
					{kind: 'tube', pts: [kn, an], w: 9 * h * g},
				],
				skin,
			);
		}
	};

	// ---------------- back arm, legs
	armMass(S.shB, elbowB, handB, false);
	legMass(S.hipB, kneeB, ankleB, S.footB.tilt);
	legMass(S.hipF, kneeF, ankleF, S.footF.tilt);

	// ---------------- lower garment: the dhoti drape (also the nine-yard saree, worn the same way, kashta style)
	const drape = (hemF: number, width: number, fill: string, pleats: number): {hemLine: V2[]} => {
		const hf = lerp2(kneeF, ankleF, hemF);
		const hb = lerp2(kneeB, ankleB, hemF);
		const wf = T(0.13, k.hipW * 0.52);
		const wb = T(0.13, -k.hipW * 0.54);
		const pfT = perp(S.hipF, kneeF);
		const pbT = perp(S.hipB, kneeB);
		const pfS = perp(kneeF, ankleF);
		const pbS = perp(kneeB, ankleB);
		// the crotch of the drape rises as the legs part, so a stride never webs the cloth from knee to knee
		const spread = Math.abs(kneeF[0] - kneeB[0]) / (k.thigh * 0.9);
		const crotch: V2 = add(lerp2(S.hip, lerp2(kneeF, kneeB, 0.5), clamp(0.78 - spread * 0.45, 0.32, 0.78)), [0, 2 * h]);
		const hfFront = add(hf, mul(pfS, width * 0.56));
		const hfIn = add(hf, mul(pfS, -width * 0.4));
		const hbIn = add(hb, mul(pbS, width * 0.4));
		const hbBack = add(hb, mul(pbS, -width * 0.55));
		const outline = [
			wb,
			wf,
			add(lerp2(S.hipF, kneeF, 0.5), mul(pfT, width * 0.58)),
			add(kneeF, mul(pfT, width * 0.55)),
			hfFront,
			hfIn,
			add(lerp2(hfIn, kneeF, 0.5), mul(pfS, -width * 0.42)),
			crotch,
			add(lerp2(hbIn, kneeB, 0.5), mul(pbS, width * 0.42)),
			hbIn,
			hbBack,
			add(kneeB, mul(pbT, -width * 0.55)),
			add(lerp2(S.hipB, kneeB, 0.45), mul(pbT, -width * 0.58)),
		];
		pen.mass([{kind: 'poly', pts: tight(outline, [4, 5, 9, 10])}], fill);
		// the front pleats fall from the waist down the front leg; the back tuck runs between the legs
		const pleatTop = T(0.11, k.hipW * 0.3);
		for (let i = 0; i < pleats; i++) {
			const s = (i + 0.7) / (pleats + 0.6);
			const end = lerp2(hfFront, hfIn, 0.15 + s * 0.6);
			const mid = add(lerp2(pleatTop, end, 0.55), mul(pfT, (0.5 - s) * 3 * h));
			pen.line([add(pleatTop, [i * 2 * h, i * 3 * h]), mid, end], st.lw * 0.45, st.inkSoft, 0.7);
		}
		pen.line([wb, T(0.15, -k.hipW * 0.1), wf], st.lw * 0.5, st.inkSoft);
		pen.line([T(0.12, -k.hipW * 0.35), lerp2(T(0.1, -k.hipW * 0.3), crotch, 0.6), crotch], st.lw * 0.45, st.inkSoft, 0.7);
		pen.line([add(kneeB, mul(pbT, -width * 0.2)), add(lerp2(kneeB, hb, 0.25), mul(pbS, -width * 0.05))], st.lw * 0.4, st.inkSoft, 0.7);
		return {hemLine: [hbBack, hb, hbIn, hfIn, hf, hfFront]};
	};

	let hem: V2[] | null = null;
	if (C.bottom === 'dhoti') {
		hem = drape(0.6, 20 * h * g, bot, 3).hemLine;
	} else if (C.bottom === 'dhotiShort') {
		hem = drape(0.1, 19 * h * g, bot, 2).hemLine;
	} else if (C.bottom === 'nauvari') {
		hem = drape(0.78, 21 * h * g, bot, 3).hemLine;
	} else if (C.bottom === 'shorts') {
		drape(-0.3, 17 * h * g, bot, 0);
	} else if (C.bottom === 'saree' || C.bottom === 'skirt') {
		// a cloth cone from the waist to the ankles (or the knees for a child's skirt)
		const f = C.bottom === 'saree' ? 0.96 : 0.15;
		const hf = lerp2(kneeF, ankleF, f);
		const hb = lerp2(kneeB, ankleB, f);
		const lo = Math.max(hf[1], hb[1]) + 2 * h;
		const front: V2 = [Math.max(hf[0], hb[0]) + 12 * h, lo];
		const back: V2 = [Math.min(hf[0], hb[0]) - 12 * h, lo];
		const wf = T(0.16, k.hipW * 0.5);
		const wb = T(0.16, -k.hipW * 0.52);
		pen.mass([{kind: 'poly', pts: [wb, wf, add(lerp2(wf, front, 0.45), [7 * h, 0]), front, lerp2(front, back, 0.5), back, add(lerp2(wb, back, 0.45), [-6 * h, 0])]}], bot);
		if (C.bottom === 'saree') {
			for (let i = 0; i < 5; i++) {
				const top0 = T(0.13, k.hipW * (0.18 + i * 0.06));
				pen.line([top0, add(lerp2(top0, lerp2(front, back, 0.08 + i * 0.07), 0.5), [i * 0.6 * h, 0]), lerp2(front, back, 0.08 + i * 0.07)], st.lw * 0.5, st.inkSoft);
			}
			hem = [back, lerp2(back, front, 0.5), front];
		}
	}
	if (hem && C.border) {
		pen.line(offsetLine(hem, -3.5 * h), st.lw * 0.8, st.gold, 0.9);
	}

	// ---------------- torso garment
	const chestF = fem ? k.chestW * 0.56 : k.chestW * 0.5;
	const hemPts = (hemLen: number, flare: number): V2[] => {
		const pf = perp(S.hipF, kneeF);
		const pb = perp(S.hipB, kneeB);
		return [add(lerp2(S.hipF, kneeF, hemLen), mul(pf, k.hipW * 0.52 + flare)), add(lerp2(S.hipB, kneeB, hemLen), mul(pb, -k.hipW * 0.56 - flare))];
	};
	const torsoPts = (hemLen: number, flare = 0): V2[] => {
		const neckB = T(1.04, -k.chestW * 0.2);
		const neckF = T(1.03, k.chestW * 0.18);
		const shTop = T(1.02, 1 * h);
		const pts: V2[] = [neckB, shTop, neckF, T(0.88, chestF * 0.92), T(0.7, chestF), T(0.42, k.waistW * 0.5 + 1.5 * g), T(0.08, k.hipW * 0.5)];
		if (hemLen > 0) {
			pts.push(...hemPts(hemLen, flare));
		} else {
			pts.push(T(-0.07, k.hipW * 0.5), T(-0.07, -k.hipW * 0.52));
		}
		pts.push(T(0.08, -k.hipW * 0.53), T(0.42, -k.waistW * 0.48), T(0.72, -k.chestW * 0.5), T(0.92, -k.chestW * 0.44));
		return pts;
	};
	const folds = (hemLen: number): void => {
		const [hf, hb] = hemPts(hemLen, 0);
		pen.line([T(0.5, k.waistW * 0.3), lerp2(T(0.3, k.waistW * 0.2), hf, 0.4), lerp2(hf, hb, 0.25)], st.lw * 0.45, st.inkSoft);
		pen.line([T(0.6, -k.waistW * 0.1), lerp2(T(0.3, -k.waistW * 0.1), hb, 0.45), lerp2(hf, hb, 0.62)], st.lw * 0.45, st.inkSoft);
		// the side slit
		pen.line([lerp2(hf, hb, 0.5), add(lerp2(hf, hb, 0.5), mul(up, k.torso * 0.25))], st.lw * 0.45, st.inkSoft);
	};
	if (C.top === 'kurta') {
		pen.mass([{kind: 'poly', pts: torsoPts(0.82, 3 * h)}], top);
		folds(0.82);
		pen.line([T(1.02, k.chestW * 0.3), T(0.7, k.chestW * 0.36)], st.lw * 0.55, st.inkSoft);
		for (let i = 0; i < 3; i++) {
			pen.dot(T(0.96 - i * 0.09, k.chestW * 0.33), 1.1 * h, 1.1 * h, st.inkSoft);
		}
	} else if (C.top === 'coat') {
		pen.mass([{kind: 'poly', pts: torsoPts(1.08, 5 * h)}], top);
		folds(1.08);
		// the angrakha overlap across the chest, and a row of buttons
		pen.line([T(1.03, -k.chestW * 0.02), T(0.84, k.chestW * 0.26), T(0.55, k.chestW * 0.42)], st.lw * 0.6, st.inkSoft);
		for (let i = 0; i < 4; i++) {
			pen.dot(T(0.82 - i * 0.11, k.chestW * (0.3 + i * 0.035)), 1.3 * h, 1.3 * h, st.gold);
		}
	} else if (C.top === 'vest') {
		pen.mass([{kind: 'poly', pts: torsoPts(0)}], top);
		pen.mass([{kind: 'poly', pts: [T(1.05, -k.chestW * 0.16), T(1.03, k.chestW * 0.2), T(0.86, k.chestW * 0.1), T(0.9, -k.chestW * 0.06)]}], skin);
		pen.line([T(0.5, k.waistW * 0.35), T(0.15, k.waistW * 0.3)], st.lw * 0.45, st.inkSoft);
	} else if (C.top === 'shirt' || C.top === 'tshirt') {
		pen.mass([{kind: 'poly', pts: torsoPts(0)}], top);
		if (C.top === 'shirt') {
			pen.line([T(1.06, k.chestW * 0.02), T(0.96, k.chestW * 0.26), T(1.0, k.chestW * 0.1)], st.lw * 0.55, st.inkSoft);
			pen.line([T(0.96, k.chestW * 0.3), T(0.06, k.waistW * 0.44)], st.lw * 0.45, st.inkSoft);
			pen.line([T(0.6, -k.waistW * 0.2), T(0.12, -k.waistW * 0.1)], st.lw * 0.45, st.inkSoft);
		}
	} else if (C.top === 'frock') {
		pen.mass([{kind: 'poly', pts: torsoPts(0.55, 5 * h)}], top);
		pen.line([T(0.32, -k.waistW * 0.5), T(0.32, k.waistW * 0.52)], st.lw * 0.45, st.inkSoft);
	} else if (C.top === 'blouse') {
		pen.mass([{kind: 'poly', pts: torsoPts(0)}], skin);
		pen.mass(
			[{kind: 'poly', pts: [T(1.04, -k.chestW * 0.2), T(1.02, 1 * h), T(1.03, k.chestW * 0.18), T(0.88, chestF * 0.92), T(0.7, chestF), T(0.56, chestF * 0.9), T(0.58, -k.chestW * 0.48), T(0.78, -k.chestW * 0.5)]}],
			top,
		);
	}
	if (C.waistcoat) {
		pen.mass(
			[{kind: 'poly', pts: [T(1.0, -k.chestW * 0.18), T(0.98, k.chestW * 0.16), T(0.7, chestF + 1), T(0.4, k.waistW * 0.52 + 2), T(0.14, k.hipW * 0.52), T(0.12, -k.hipW * 0.5), T(0.46, -k.waistW * 0.52), T(0.8, -k.chestW * 0.5)]}],
			toneFill.black,
		);
		for (let i = 0; i < 4; i++) {
			pen.dot(T(0.86 - i * 0.16, k.chestW * 0.42), 1.3 * h, 1.3 * h, st.gold);
		}
	}

	// ---------------- saree pallu, gamcha (secondary motion from wind and the body's velocity)
	const sareeFill = toneFill[C.bottomTone];
	if (C.pallu) {
		const from = T(0.2, k.hipW * 0.46);
		const across = T(0.66, k.chestW * 0.2);
		const over = T(1.03, -k.chestW * 0.1);
		const tail = clothTail(T(0.94, -k.chestW * 0.42), rotV([-0.1, 1], S.lean * 0.5), k.torso * (C.pallu === 'head' ? 0.8 : 0.66), 5, t, S.wind, vel, seed);
		const band = [from, across, over, ...tail];
		pen.mass([{kind: 'tube', pts: band, w: 15 * h}], sareeFill);
		pen.line([lerp2(from, across, 0.4), across, lerp2(across, over, 0.7)], st.lw * 0.45, st.inkSoft);
		if (C.border) {
			pen.line(offsetLine(band, 6 * h).slice(1), st.lw * 0.7, st.gold, 0.85);
		}
	}
	if (C.gamcha) {
		const base = T(1.01, k.chestW * 0.08);
		const tail = clothTail(base, rotV([0.12, 1], S.lean), k.torso * 0.48, 4, t, S.wind, vel, seed + 3, 0.6);
		pen.mass([{kind: 'tube', pts: [T(1.03, -k.chestW * 0.28), ...tail], w: 9.5 * h}], toneFill.white);
		pen.line(offsetLine(tail.slice(-2), 0), st.lw * 0.45, st.inkSoft);
	}

	// ---------------- neck, head
	const R = k.headR;
	const head = J(S.head, st.boilAmp * 0.7);
	const hr = S.headRot;
	const H = (x: number, y: number): V2 => add(head, rot(x * R, y * R, hr));
	pen.mass([{kind: 'tube', pts: [S.neck, lerp2(S.neck, head, 0.6)], w: 11 * h * (fem ? 0.82 : 1)}], skin);

	const tr = S.turn;
	const fx = tr * 0.38;
	if ((C.hair === 'bun' || C.hair === 'greyBun') && C.pallu !== 'head') {
		pen.mass([{kind: 'ell', c: H(-0.9 + fx * 0.25, 0.08), rx: R * 0.32, ry: R * 0.28, rot: hr}], C.hair === 'greyBun' ? toneFill.white : toneFill.black);
	}
	if (C.hair === 'plait') {
		const tail = clothTail(H(-0.72, 0.3), rotV([-0.12, 1], -hr * 0.3), R * 2.2, 4, t, S.wind, vel, seed + 9, 0.25);
		pen.mass([{kind: 'tube', pts: tail, w: 5.5 * h}], toneFill.black);
	}
	// head: an egg, narrower at the chin, turned with the face
	pen.mass(
		[
			{
				kind: 'poly',
				pts: [H(0.05 + fx * 0.4, -1.06), H(0.6 + fx * 0.25, -0.8), H(0.8 + fx * 0.12, -0.2), H(0.72 + fx * 0.15, 0.42), H(0.36 + fx * 0.4, 0.95), H(-0.14 + fx * 0.3, 0.98), H(-0.64, 0.52), H(-0.86, -0.12), H(-0.62, -0.82)],
			},
		],
		skin,
	);

	const hairCol = C.hair === 'grey' || C.hair === 'greyBun' ? toneFill.white : toneFill.black;
	const covered = C.head !== 'bare' || C.pallu === 'head';
	if (!covered) {
		if (C.hair === 'bald') {
			pen.mass([{kind: 'poly', pts: [H(-0.86, -0.1), H(-0.74, -0.5), H(-0.32, -0.4), H(-0.5, 0.25)]}], hairCol);
		} else {
			const fringe = C.hair === 'child' ? 0.2 : 0;
			pen.mass(
				[{kind: 'poly', pts: [H(0.52 + fx * 0.3, -0.6 + fringe), H(0.63 + fx * 0.25, -0.86), H(0.05 + fx * 0.4, -1.12), H(-0.66, -0.88), H(-0.9, -0.12), H(-0.62, 0.3), H(-0.44, -0.1), H(-0.05 + fx * 0.3, -0.56)]}],
				hairCol,
			);
			// a parting and the comb lines
			pen.line([H(0.1 + fx * 0.35, -1.0), H(-0.3, -0.72), H(-0.6, -0.4)], st.lw * 0.4, st.inkSoft);
		}
	}

	// face (dignified: small eyes, held expressions, no grins)
	const F = S.face;
	const eyeY = -0.1;
	const look: V2 = [S.eye[0] * 0.07, S.eye[1] * 0.05];
	const eyes: {x: number; s: number}[] = [{x: fx + 0.25, s: 1}];
	if (tr < 0.85) {
		eyes.push({x: fx - 0.3 * (1 - tr * 0.55), s: 1 - tr * 0.35});
	}
	const er = R / (22.5 * h);
	for (const e of eyes) {
		const c = H(e.x + look[0], eyeY + look[1]);
		pen.dot(c, 1.45 * h * e.s * er, Math.max(0.3, 2.1 * F.eyes) * h * er, st.ink, hr);
		// upper lid line (gives the eye weight without making it big)
		pen.line([H(e.x - 0.1, eyeY - 0.08), H(e.x + 0.02, eyeY - 0.13), H(e.x + 0.12, eyeY - 0.07)], st.lw * 0.4, st.inkSoft);
		const side = e.x > fx ? -1 : 1;
		const by = eyeY - 0.32;
		pen.line([H(e.x - 0.14 * side, by + 0.02), H(e.x + 0.14 * side, by - F.worry * 0.14)], st.lw * 0.55);
		if (C.glasses) {
			const ring = ellPts(c, R * 0.17, R * 0.15, hr, 10);
			pen.line([...ring, ring[0]], st.lw * 0.4, st.inkSoft);
		}
	}
	if (tr > 0.2) {
		const nb = H(fx + 0.12 + 0.05 * tr, eyeY + 0.08);
		const tip = H(fx + 0.12 + 0.2 * tr, 0.3);
		const base = H(fx + 0.12 + 0.04 * tr, 0.36);
		pen.line([nb, lerp2(nb, tip, 0.7), tip, base], st.lw * 0.45);
	}
	if (tr > 0.3 && C.head !== 'helmet' && C.pallu !== 'head') {
		pen.line([H(fx - 0.5, -0.12), H(fx - 0.64, -0.04), H(fx - 0.6, 0.18), H(fx - 0.5, 0.22)], st.lw * 0.5, st.inkSoft);
	}
	const mw = 0.16 * (1 - tr * 0.3);
	const mx = fx + 0.12 * tr + 0.06;
	const my = 0.6;
	if (C.moustache) {
		// two short brush strokes falling away from the centre (never a lip shape)
		const mc = C.hair === 'grey' ? st.inkSoft : st.ink;
		pen.line([H(mx - 0.01, my - 0.1), H(mx - mw * 0.6, my - 0.08), H(mx - mw - 0.05, my + 0.0)], st.lw * 0.75, mc);
		pen.line([H(mx + 0.01, my - 0.1), H(mx + mw * 0.6, my - 0.08), H(mx + mw + 0.05, my + 0.0)], st.lw * 0.75, mc);
	}
	if (C.beard) {
		// a short beard along the jaw, below the mouth
		pen.mass([{kind: 'poly', pts: [H(fx - 0.58, 0.28), H(fx - 0.3, 0.62), H(mx - mw, my + 0.1), H(mx + mw + 0.04, my + 0.08), H(mx + 0.16, 0.98), H(fx - 0.06, 1.16), H(fx - 0.5, 0.82)]}], C.hair === 'grey' ? toneFill.white : toneFill.dark, st.inkSoft);
		for (let i = 0; i < 3; i++) {
			pen.line([H(fx - 0.38 + i * 0.18, 0.72), H(fx - 0.34 + i * 0.19, 1.0 + i * 0.04)], st.lw * 0.35, st.inkSoft);
		}
	}
	const sm = F.smile * 0.06;
	const mwm = C.moustache ? mw * 0.7 : mw;
	pen.line([H(mx - mwm, my + 0.02 - sm), H(mx, my + 0.02 + sm + F.open * 0.1), H(mx + mwm, my + 0.02 - sm)], st.lw * 0.42);

	// headwear
	const hw = C.headTone ? toneFill[C.headTone] : toneFill.white;
	if (C.pallu === 'head') {
		const tail = clothTail(H(-1.05, 0.5), rotV([-0.18, 1], S.lean), k.torso * 0.42, 3, t, S.wind, vel, seed + 5, 0.6);
		pen.mass(
			[
				{kind: 'poly', pts: [H(0.45 + fx * 0.3, -0.72), H(0.62 + fx * 0.25, -1.02), H(0.0, -1.32), H(-0.95, -1.02), H(-1.18, -0.1), H(-1.12, 0.6), H(-0.62, 0.66), H(-0.5, -0.05), H(-0.05 + fx * 0.3, -0.62)]},
				{kind: 'tube', pts: [H(-1.0, 0.1), ...tail], w: 16 * h},
			],
			sareeFill,
		);
		if (C.border) {
			pen.line([H(0.5 + fx * 0.3, -0.8), H(0.0, -1.2), H(-0.92, -0.92), H(-1.06, -0.1)], st.lw * 0.7, st.gold, 0.85);
		}
	} else if (C.head === 'turban' || C.head === 'pheta' || C.head === 'headCloth') {
		const tall = C.head === 'turban' ? 1.56 : C.head === 'pheta' ? 1.42 : 1.22;
		const wide = C.head === 'headCloth' ? 1.0 : 1.1;
		pen.mass(
			[{kind: 'poly', pts: [H(0.82 + fx * 0.15, -0.3), H(0.98 * wide + fx * 0.1, -0.86), H(0.62, -tall + 0.12), H(-0.12, -tall), H(-0.86 * wide, -tall + 0.24), H(-1.1 * wide, -0.7), H(-1.02, -0.18), H(-0.55, -0.3)]}],
			hw,
		);
		// the wraps cross over the forehead
		const n = C.head === 'headCloth' ? 2 : 4;
		for (let i = 0; i < n; i++) {
			const s = i / n;
			pen.line([H(0.86 + fx * 0.12, -0.36 - s * 0.55), H(0.1, -0.75 - s * 0.6), H(-0.98, -0.6 - s * 0.55)], st.lw * 0.5, st.inkSoft);
		}
		if (C.head !== 'headCloth') {
			pen.line([H(-1.0, -0.3), H(-0.2, -0.9), H(0.62, -tall + 0.15)], st.lw * 0.5, st.inkSoft);
		}
		if (C.head === 'pheta') {
			pen.mass([{kind: 'poly', pts: [H(0.3, -1.34), H(0.58, -1.8), H(0.74, -1.26)]}], hw);
		}
		if (C.tail || C.head === 'pheta') {
			const tail = clothTail(H(-0.98, -0.45), rotV([-0.22, 1], S.lean * 0.5), R * 2.5, 4, t, S.wind, vel, seed + 7, 0.7);
			pen.mass([{kind: 'tube', pts: tail, w: 8 * h}], hw);
		}
		if (C.head === 'headCloth') {
			pen.mass([{kind: 'ell', c: H(-1.02, -0.62), rx: R * 0.2, ry: R * 0.16, rot: hr + 30}], hw);
		}
	} else if (C.head === 'parsiCap') {
		// the tall, rigid black Parsi hat, higher at the back, with a slanted top
		pen.mass([{kind: 'poly', smooth: false, pts: [H(0.8 + fx * 0.15, -0.42), H(0.7 + fx * 0.15, -1.62), H(-0.62, -1.98), H(-0.96, -0.32)]}], toneFill.black);
		pen.line([H(0.78 + fx * 0.15, -0.56), H(-0.95, -0.46)], st.lw * 0.5, st.inkSoft);
		pen.line([H(0.42, -1.48), H(0.4, -0.72)], st.lw * 0.5, st.gold, 0.4);
	} else if (C.head === 'millCap') {
		pen.mass([{kind: 'poly', pts: [H(0.84 + fx * 0.15, -0.5), H(0.56, -1.14), H(-0.35, -1.22), H(-0.98, -0.55), H(0.0, -0.6)]}], hw);
		pen.mass([{kind: 'tube', pts: [H(0.7 + fx * 0.15, -0.52), H(1.34 + fx * 0.15, -0.38)], w: 3.6 * h}], hw);
		pen.line([H(0.6, -0.62), H(0.1, -1.14)], st.lw * 0.45, st.inkSoft);
	} else if (C.head === 'helmet') {
		pen.mass([{kind: 'poly', pts: [H(0.94 + fx * 0.15, -0.3), H(0.76, -1.1), H(-0.2, -1.38), H(-1.04, -0.86), H(-1.1, 0.1), H(-0.6, 0.14), H(-0.4, -0.38)]}], toneFill.dark);
		pen.line([H(0.94 + fx * 0.15, -0.36), H(1.08 + fx * 0.15, 0.05)], st.lw * 0.75, st.inkSoft);
		pen.line([H(-0.2, -1.3), H(-0.5, -0.4)], st.lw * 0.45, st.inkSoft);
	}

	// ---------------- front arm, props
	if (prop === 'cane') {
		const tip: V2 = [handF[0] + 24 * h, 0];
		pen.mass([{kind: 'tube', pts: [add(handF, [0, -9 * h]), tip], w: 3 * h}], toneFill.ochre);
	}
	const handsMid = lerp2(handF, handB, 0.5);
	if (prop === 'pouch') {
		// a small cloth pouch of savings, tied at the neck, held in both hands
		const c = add(handsMid, [5 * h, 4 * h]);
		pen.mass([{kind: 'poly', pts: [add(c, [-7 * h, -6 * h]), add(c, [7 * h, -6 * h]), add(c, [11 * h, 7 * h]), add(c, [0, 13 * h]), add(c, [-11 * h, 7 * h])]}], toneFill.ochre);
		pen.line([add(c, [-6 * h, -7 * h]), add(c, [0, -11 * h]), add(c, [6 * h, -7 * h])], st.lw * 0.55, st.gold, 0.85);
	} else if (prop === 'cap') {
		const c = add(handsMid, [6 * h, 2 * h]);
		pen.mass([{kind: 'poly', pts: [add(c, [-13 * h, -2 * h]), add(c, [13 * h, -4 * h]), add(c, [11 * h, 6 * h]), add(c, [-11 * h, 7 * h])]}], hw);
	} else if (prop === 'bundle') {
		const c = add(handsMid, [6 * h, 0]);
		pen.mass([{kind: 'ell', c, rx: 14 * h, ry: 10 * h, rot: -10}], toneFill.light);
		pen.line([add(c, [-4 * h, -10 * h]), add(c, [2 * h, -15 * h]), add(c, [6 * h, -9 * h])], st.lw * 0.55, st.inkSoft);
	}
	armMass(S.shF, elbowF, handF, true);
	if (prop === 'tiffin') {
		const c = add(handF, [2 * h, 20 * h]);
		pen.line([add(handF, [2 * h, 2 * h]), add(c, [0, -11 * h])], st.lw * 0.7);
		pen.mass([{kind: 'poly', smooth: false, pts: [add(c, [-8 * h, -10 * h]), add(c, [8 * h, -10 * h]), add(c, [8 * h, 14 * h]), add(c, [-8 * h, 14 * h])]}], toneFill.mid);
		pen.line([add(c, [-8 * h, -2 * h]), add(c, [8 * h, -2 * h])], st.lw * 0.5, st.inkSoft);
		pen.line([add(c, [-8 * h, 6 * h]), add(c, [8 * h, 6 * h])], st.lw * 0.5, st.inkSoft);
	}

	if (st.sketch) {
		// a second, thinner pass over the detail lines, as an ink artist re-traces a line
		const extra: Prim[] = pen.prims
			.filter((p, i) => p.line && hash(i + seed) < 0.5)
			.map((p) => ({...p, w: p.w * 0.5, op: 0.4, line: false, dx: 0.8, dy: -0.6}));
		pen.prims.push(...extra);
	}
	return pen.prims;
};

export {lerp};
