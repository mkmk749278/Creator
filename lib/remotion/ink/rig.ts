// INK rig (PLAYBOOK §8.9): the maths of Creator's approved stick-man (`reference_stick.js`), typed and made data
// driven. Everything here is a pure function of time t (seconds) and a numeric seed: no state between frames.
//
// Figure space: origin on the ground under the hips, +x forward (the way the figure faces), +y down (SVG), units are
// pixels at scale 1. A standing adult man is about 340 units tall.

export type V2 = [number, number];

export const lerp = (a: number, b: number, p: number): number => a + (b - a) * p;
export const clamp = (x: number, a: number, b: number): number => Math.max(a, Math.min(b, x));
export const sstep = (a: number, b: number, x: number): number => {
	const p = clamp((x - a) / (b - a), 0, 1);
	return p * p * (3 - 2 * p);
};
export const add = (p: V2, v: V2): V2 => [p[0] + v[0], p[1] + v[1]];
export const sub = (p: V2, v: V2): V2 => [p[0] - v[0], p[1] - v[1]];
export const mul = (p: V2, k: number): V2 => [p[0] * k, p[1] * k];
export const lerp2 = (a: V2, b: V2, p: number): V2 => [lerp(a[0], b[0], p), lerp(a[1], b[1], p)];
export const len = (v: V2): number => Math.hypot(v[0], v[1]);
export const rot = (x: number, y: number, deg: number): V2 => {
	const a = (deg * Math.PI) / 180;
	const c = Math.cos(a);
	const s = Math.sin(a);
	return [x * c - y * s, x * s + y * c];
};
export const rotV = (v: V2, deg: number): V2 => rot(v[0], v[1], deg);

/** Creator's hash: deterministic 0..1 from a number. */
export const hash = (n: number): number => {
	const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
	return s - Math.floor(s);
};

/** Stable numeric seed from a string (FNV-1a). */
export const seedOf = (s: string): number => {
	let h = 2166136261;
	for (let i = 0; i < s.length; i++) {
		h ^= s.charCodeAt(i);
		h = Math.imul(h, 16777619);
	}
	return ((h >>> 0) % 100000) / 7.3;
};

/** Smooth 1D value noise (cosine-interpolated hash lattice), -1..1. Cheap and deterministic. */
export const vnoise = (x: number, seed: number): number => {
	const i = Math.floor(x);
	const f = x - i;
	const u = f * f * (3 - 2 * f);
	return lerp(hash(i + seed * 13.7), hash(i + 1 + seed * 13.7), u) * 2 - 1;
};

/** The 12 fps line boil (PLAYBOOK §8.9): a jitter vector that changes 12 times a second, per point id. */
export const boil = (t: number, id: number, amp: number): V2 => {
	const fr = Math.floor(t * 12);
	return [(hash(fr * 13.1 + id) - 0.5) * 2 * amp, (hash(fr * 7.7 + id + 50) - 0.5) * 2 * amp];
};

// ---------------------------------------------------------------- body build

export type Age = 'child' | 'adult' | 'old';
export type Build = {
	/** 1 = adult man (340 units). */
	height: number;
	/** Body width multiplier. */
	girth: number;
	/** Head size relative to the body (children have bigger heads). */
	head: number;
	age: Age;
	female: boolean;
};

export const defaultBuild: Build = {height: 1, girth: 1, head: 1, age: 'adult', female: false};

export const buildFor = (age: Age, female: boolean, height?: number, girth?: number): Build => ({
	height: height ?? (age === 'child' ? 0.6 : female ? 0.93 : 1),
	girth: girth ?? (female ? 0.92 : 1),
	head: age === 'child' ? 1.32 : 1,
	age,
	female,
});

export type Bones = {
	thigh: number;
	shin: number;
	ankle: number;
	torso: number;
	neck: number;
	upper: number;
	fore: number;
	headR: number;
	chestW: number;
	waistW: number;
	hipW: number;
	limbW: number;
};

export const bones = (b: Build): Bones => {
	const h = b.height;
	const g = b.girth;
	return {
		thigh: 84 * h,
		shin: 80 * h,
		ankle: 10 * h,
		torso: 108 * h,
		neck: 12 * h,
		upper: 60 * h,
		fore: 56 * h,
		headR: 22.5 * h * b.head,
		chestW: 46 * h * g * (b.female ? 0.92 : 1),
		waistW: 38 * h * g,
		hipW: 42 * h * g * (b.female ? 1.08 : 1),
		limbW: 15 * h * g,
	};
};

/** Rest hip height for a build (straight legs with a little knee give). */
export const restHip = (b: Build): number => {
	const k = bones(b);
	return -(k.thigh + k.shin + k.ankle - 4 * b.height);
};

// ---------------------------------------------------------------- pose

export type Face = {
	/** 0 closed … 1 open; dignified figures sit near 0.75. */
	eyes: number;
	/** Inner brow lift: 0 calm … 1 worried. */
	worry: number;
	/** Mouth curve: −1 down … +1 up. Dignified beats stay within ±0.25. */
	smile: number;
	/** Mouth open 0..1 (speaking, breath). */
	open: number;
};

export type Foot = {x: number; y: number; tilt: number};

export type Pose = {
	hip: V2;
	/** Torso lean forward in degrees. */
	lean: number;
	/** Head tilt in degrees (+ = chin down). */
	nod: number;
	/** Hand targets, shoulder-relative, in the torso's frame (rotated with the lean). */
	handF: V2;
	handB: V2;
	/** Elbow bend preference (direction the elbow points), figure space. */
	elbowF: V2;
	elbowB: V2;
	footF: Foot;
	footB: Foot;
	/** Knee bend preference (direction), figure space; forward by default. */
	knee: V2;
	/** Visible thigh length multiplier (foreshortening when the thigh points at the camera). */
	thighScale: number;
	face: Face;
	/** Eye/head target in figure space, or null to look straight ahead. */
	look: V2 | null;
	/** 0 frontal … 1 full profile. */
	turn: number;
	/** 0..1 how much the head follows the look target. */
	lookWeight: number;
	/** Wind on cloth, figure space units per second (secondary motion). */
	wind: V2;
};

export const dignified: Face = {eyes: 0.72, worry: 0.25, smile: -0.08, open: 0};

export const standPose = (b: Build): Pose => ({
	hip: [0, restHip(b)],
	lean: b.age === 'old' ? 9 : 1.5,
	nod: b.age === 'old' ? 6 : 2,
	handF: [5, 112 * b.height],
	handB: [-3, 113 * b.height],
	elbowF: [-0.4, 1],
	elbowB: [-0.4, 1],
	footF: {x: 13 * b.height, y: 0, tilt: 0},
	footB: {x: -14 * b.height, y: 0, tilt: 0},
	knee: [1, 0.05],
	thighScale: 1,
	face: dignified,
	look: null,
	turn: 0.62,
	lookWeight: 0.6,
	wind: [0, 0],
});

// ---------------------------------------------------------------- 2-bone IK (Creator's, typed)

export const ik = (a: V2, target: V2, l1: number, l2: number, pref: V2): {joint: V2; end: V2} => {
	const dx = target[0] - a[0];
	const dy = target[1] - a[1];
	const d = Math.hypot(dx, dy) || 1e-3;
	const dc = clamp(d, Math.abs(l1 - l2) + 1, l1 + l2 - 0.5);
	const end: V2 = [a[0] + (dx / d) * dc, a[1] + (dy / d) * dc];
	const base = Math.atan2(dy, dx);
	const ang = Math.acos(clamp((l1 * l1 + dc * dc - l2 * l2) / (2 * l1 * dc), -1, 1));
	const c1: V2 = [a[0] + l1 * Math.cos(base + ang), a[1] + l1 * Math.sin(base + ang)];
	const c2: V2 = [a[0] + l1 * Math.cos(base - ang), a[1] + l1 * Math.sin(base - ang)];
	const dot = (c: V2) => (c[0] - a[0]) * pref[0] + (c[1] - a[1]) * pref[1];
	return {joint: dot(c1) >= dot(c2) ? c1 : c2, end};
};

// ---------------------------------------------------------------- skeleton

export type Skeleton = {
	hip: V2;
	hipF: V2;
	hipB: V2;
	waist: V2;
	chest: V2;
	shoulder: V2;
	shF: V2;
	shB: V2;
	neck: V2;
	head: V2;
	/** Head rotation in degrees (lean + nod + look). */
	headRot: number;
	lean: number;
	elbowF: V2;
	handF: V2;
	elbowB: V2;
	handB: V2;
	kneeF: V2;
	ankleF: V2;
	kneeB: V2;
	ankleB: V2;
	footF: Foot;
	footB: Foot;
	/** Eye offset (unit-ish) toward the look target, head-local. */
	eye: V2;
	turn: number;
	face: Face;
	wind: V2;
	k: Bones;
	build: Build;
};

export const solve = (p: Pose, b: Build): Skeleton => {
	const k = bones(b);
	const hip = p.hip;
	const up = (d: number, extra = 0): V2 => add(hip, rot(0, -d, p.lean + extra));
	const shoulder = up(k.torso);
	const chest = up(k.torso * 0.72);
	const waist = up(k.torso * 0.2);
	const neck = up(k.torso + k.neck * 0.6);
	const shF = add(shoulder, rot(5 * b.height, 1, p.lean));
	const shB = add(shoulder, rot(-5 * b.height, -1, p.lean));
	const hipF = add(hip, [4 * b.height, 0]);
	const hipB = add(hip, [-4 * b.height, 0]);
	const armF = ik(shF, add(shF, rotV(p.handF, p.lean)), k.upper, k.fore, p.elbowF);
	const armB = ik(shB, add(shB, rotV(p.handB, p.lean)), k.upper, k.fore, p.elbowB);
	const thigh = k.thigh * p.thighScale;
	const ankleTarget = (f: Foot): V2 => [f.x, f.y - k.ankle];
	const legF = ik(hipF, ankleTarget(p.footF), thigh, k.shin, p.knee);
	const legB = ik(hipB, ankleTarget(p.footB), thigh, k.shin, p.knee);
	// head: follows the look target by lookWeight, clamped like Creator's rig
	const head0 = add(neck, rot(0, -k.headR * 1.25, p.lean * 0.6 + p.nod));
	let lookAng = 0;
	let eye: V2 = [0.35, 0.05];
	if (p.look) {
		const dx = p.look[0] - head0[0];
		const dy = p.look[1] - head0[1];
		const a = (Math.atan2(dy, Math.max(60, Math.abs(dx))) * 180) / Math.PI;
		lookAng = clamp(a * 0.5, -22, 20) * p.lookWeight;
		const m = Math.hypot(dx, dy) || 1;
		eye = [dx / m, dy / m];
	}
	const headRot = p.lean * 0.4 + p.nod + lookAng;
	const head = add(neck, rot(0, -k.headR * 1.25, p.lean * 0.5 + headRot * 0.5));
	return {
		hip,
		hipF,
		hipB,
		waist,
		chest,
		shoulder,
		shF,
		shB,
		neck,
		head,
		headRot,
		lean: p.lean,
		elbowF: armF.joint,
		handF: armF.end,
		elbowB: armB.joint,
		handB: armB.end,
		kneeF: legF.joint,
		ankleF: legF.end,
		kneeB: legB.joint,
		ankleB: legB.end,
		footF: p.footF,
		footB: p.footB,
		eye,
		turn: p.turn,
		face: p.face,
		wind: p.wind,
		k,
		build: b,
	};
};

// ---------------------------------------------------------------- walking (Creator's planted-foot walk)

export type Gait = {stride: number; stance: number; lift: number};
export const gaitFor = (b: Build): Gait => ({
	stride: (b.age === 'old' ? 170 : b.age === 'child' ? 150 : 230) * b.height,
	stance: 0.6,
	lift: (b.age === 'old' ? 12 : 20) * b.height,
});

/** One foot at walked distance d (offset 0 or 0.5): planted while in stance, a smooth arc while swinging. */
export const walkFoot = (d: number, off: number, g: Gait): Foot & {swing: number} => {
	const u = d / g.stride + off;
	const c = Math.floor(u);
	const l = u - c;
	if (l < g.stance) {
		return {x: (c + 0.3 - off) * g.stride, y: 0, tilt: 0, swing: 0};
	}
	const s = (l - g.stance) / (1 - g.stance);
	const e = s * s * (3 - 2 * s);
	return {x: (c + 0.3 + e - off) * g.stride, y: -g.lift * Math.sin(Math.PI * s), tilt: -16 * Math.sin(Math.PI * s), swing: Math.sin(Math.PI * s)};
};

/**
 * Distance phase for a clean stop: with stance 0.6 and feet half a cycle apart, both feet are planted when the
 * cycle fraction is in [0, 0.1) or [0.5, 0.6). Walks start at 0.05 of a cycle and move in half-cycle steps.
 */
export const PLANTED = 0.05;

export type Travel = (t: number) => number;

/** Smooth, eased moves: [{at, steps, dur}] → walked distance at t (each step = half a stride). */
export const shuffleTravel = (moves: {at: number; steps: number; dur: number}[], g: Gait): Travel => (t) => {
	let d = 0;
	for (const m of moves) {
		const p = clamp((t - m.at) / m.dur, 0, 1);
		const e = p * p * (3 - 2 * p);
		d += e * m.steps * g.stride * 0.5;
	}
	return d;
};

/**
 * A walk from t0 with a trapezoid speed profile: accelerate over `ramp` s, cruise at `speed`, decelerate over `ramp` s
 * and stop exactly at `dist` (or never stop when dist is Infinity). Distance after a ramp = v·ramp/2.
 */
export const steadyTravel = (speed: number, t0 = 0, dist = Infinity, ramp = 0.5): Travel => (t) => {
	const tt = t - t0;
	if (tt <= 0) {
		return 0;
	}
	const r = Number.isFinite(dist) ? Math.min(ramp, dist / speed) : ramp;
	const total = Number.isFinite(dist) ? dist / speed + r : Infinity;
	if (tt >= total) {
		return dist;
	}
	if (tt > total - r) {
		const left = total - tt;
		return dist - (speed * left * left) / (2 * r);
	}
	return tt < r ? (speed * tt * tt) / (2 * r) : speed * (tt - r / 2);
};
