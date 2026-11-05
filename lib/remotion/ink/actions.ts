// INK actions: data → pose at time t. A scene says what a figure does ({type: 'wait', hands: 'clasp'}) and the rig
// gives every frame: breathing, weight shifts, blinks, glances, planted-foot walks and shuffles, seated rides.
// Pure functions of (t, build, seed).
import {
	Build,
	Face,
	Pose,
	V2,
	add,
	clamp,
	gaitFor,
	hash,
	lerp,
	lerp2,
	restHip,
	rot,
	rotV,
	sstep,
	standPose,
	steadyTravel,
	sub,
	vnoise,
	walkFoot,
	bones,
} from './rig';

export type Hands =
	| 'hang'
	| 'clasp'
	| 'behind'
	| 'folded'
	| 'cap'
	| 'pouch'
	| 'offer'
	| 'cane'
	| 'childHand'
	| 'chest';

export type Mood = 'dignified' | 'tired' | 'hopeful' | 'warm' | 'worried' | 'resolute';

export const moods: Record<Mood, Face> = {
	dignified: {eyes: 0.72, worry: 0.22, smile: -0.06, open: 0},
	tired: {eyes: 0.55, worry: 0.45, smile: -0.18, open: 0},
	hopeful: {eyes: 0.82, worry: 0.1, smile: 0.12, open: 0},
	warm: {eyes: 0.7, worry: 0, smile: 0.22, open: 0},
	worried: {eyes: 0.8, worry: 0.75, smile: -0.2, open: 0},
	resolute: {eyes: 0.68, worry: 0, smile: 0, open: 0},
};

type Move = {at: number; steps: number; dur: number};

export type InkAction =
	| {type: 'stand'; hands?: Hands; mood?: Mood}
	| {
			type: 'wait';
			hands?: Hands;
			mood?: Mood;
			/** Queue shuffles: at time `at` take `steps` steps forward over `dur` s, moving `dist` units in all. */
			shuffle?: (Move & {dist: number})[];
			/** Occasional glances away and down (default true). */
			glance?: boolean;
	  }
	| {type: 'walk'; speed?: number; start?: number; dist?: number; hands?: Hands; mood?: Mood}
	| {type: 'ride'; seat: V2; bar: V2; floor: V2; bob?: number; mood?: Mood}
	| {type: 'pillion'; seat: V2; floor: V2; hold?: V2; bob?: number; mood?: Mood}
	| {type: 'perch'; floor: V2; bar: V2; bob?: number; mood?: Mood}
	| {type: 'lap'; seat: V2; bob?: number; mood?: Mood}
	| {type: 'pose'; pose: Partial<Pose>};

/** Hand targets per variant (adult units, shoulder-relative in the torso frame) and the elbow directions. */
const handSets: Record<Hands, {f: V2; b: V2; ef: V2; eb: V2}> = {
	hang: {f: [5, 112], b: [-3, 113], ef: [-0.4, 1], eb: [-0.4, 1]},
	clasp: {f: [24, 86], b: [31, 88], ef: [-1, 0.35], eb: [-1, 0.35]},
	behind: {f: [-24, 92], b: [-14, 92], ef: [-1, 0.5], eb: [-1, 0.5]},
	folded: {f: [22, 44], b: [27, 50], ef: [0.15, 1], eb: [0.15, 1]},
	cap: {f: [24, 74], b: [29, 77], ef: [-0.7, 1], eb: [-0.7, 1]},
	pouch: {f: [21, 72], b: [26, 75], ef: [-0.7, 1], eb: [-0.7, 1]},
	offer: {f: [50, 52], b: [53, 57], ef: [-0.3, 1], eb: [-0.3, 1]},
	cane: {f: [30, 96], b: [-3, 113], ef: [-0.8, 0.6], eb: [-0.4, 1]},
	childHand: {f: [12, 116], b: [-3, 113], ef: [-0.4, 1], eb: [-0.4, 1]},
	chest: {f: [20, 38], b: [-3, 113], ef: [0.2, 1], eb: [-0.4, 1]},
};

const scaled = (v: V2, h: number): V2 => [v[0] * h, v[1] * h];

/** Seeded blink: 0 open … 1 closed. One blink every 2.8–5.4 s, 150 ms long. */
export const blinkAt = (t: number, seed: number): number => {
	const period = 2.8 + hash(seed * 3.1) * 2.6;
	const k = Math.floor(t / period);
	const at = k * period + hash(seed + k * 7.3) * period * 0.7;
	return Math.max(0, 1 - Math.abs(t - at) / 0.075);
};

/** Glance schedule: every 5–9 s the figure looks away (back down the line, or down) for about 1.6 s. */
const glanceAt = (t: number, seed: number): {w: number; kind: number} => {
	const period = 5 + hash(seed * 1.7) * 4;
	const k = Math.floor(t / period);
	const at = k * period + 1 + hash(seed + k * 3.9) * (period - 3);
	const w = Math.min(sstep(at, at + 0.35, t), 1 - sstep(at + 1.4, at + 1.8, t));
	return {w, kind: hash(seed + k * 11.1)};
};

/** Shoulder-relative (torso-frame) hand target for a point given in figure space. */
export const reach = (hip: V2, lean: number, b: Build, target: V2, front: boolean): V2 => {
	const k = bones(b);
	const sh = add(add(hip, rot(0, -k.torso, lean)), rot(front ? 5 * b.height : -5 * b.height, front ? 1 : -1, lean));
	return rotV(sub(target, sh), -lean);
};

export type ActionResult = {pose: Pose; travel: number};

export const actionPose = (a: InkAction, t: number, b: Build, seed: number): ActionResult => {
	const base = standPose(b);
	const h = b.height;
	if (a.type === 'pose') {
		return {pose: {...base, ...a.pose}, travel: 0};
	}
	const mood = moods[('mood' in a && a.mood) || 'dignified'];
	const blink = blinkAt(t, seed);
	const face: Face = {...mood, eyes: mood.eyes * (1 - blink)};
	const breath = Math.sin((2 * Math.PI * t) / (3.6 + hash(seed) * 1.4) + seed);

	if (a.type === 'stand' || a.type === 'wait') {
		const hs = handSets[a.hands ?? 'hang'];
		const sway = vnoise(t * 0.32 + seed, seed) * 2.4 * h;
		const pose: Pose = {
			...base,
			hip: [base.hip[0] + sway, base.hip[1] + breath * 0.6 * h],
			lean: base.lean + breath * 0.5 + vnoise(t * 0.2, seed + 4) * 1.2,
			handF: add(scaled(hs.f, h), [0, breath * 1.2 * h]),
			handB: add(scaled(hs.b, h), [0, breath * 1.2 * h]),
			elbowF: hs.ef,
			elbowB: hs.eb,
			face,
			nod: base.nod + vnoise(t * 0.25, seed + 9) * 2,
		};
		// a weight shift every ~7 s: the back foot lifts and replants a little to one side
		const wp = 6.5 + hash(seed * 2.3) * 3;
		const wk = Math.floor(t / wp);
		const wat = wk * wp + hash(seed + wk) * (wp - 1);
		const ws = sstep(wat, wat + 0.5, t) - sstep(wat + 0.5, wat + 0.9, t);
		pose.footB = {...pose.footB, y: -5 * h * Math.sin(Math.PI * clamp((t - wat) / 0.6, 0, 1)), x: pose.footB.x + 3 * h * ws};
		pose.hip = add(pose.hip, [ws * 3 * h, 0]);
		let travel = 0;
		if (a.type === 'wait') {
			// shuffles: step-through stepping, each foot moves `dist`, the hip glides
			for (const m of a.shuffle ?? []) {
				const p = clamp((t - m.at) / m.dur, 0, 1);
				travel += m.dist * (p * p * (3 - 2 * p));
			}
			if (a.shuffle && a.shuffle.length) {
				let dF = 0;
				let dB = 0;
				let liftF = 0;
				let liftB = 0;
				for (const m of a.shuffle) {
					const n = Math.max(2, m.steps);
					for (let i = 0; i < n; i++) {
						const s0 = m.at + (m.dur * i) / n;
						const s1 = m.at + (m.dur * (i + 1)) / n;
						const p = clamp((t - s0) / (s1 - s0), 0, 1);
						const e = p * p * (3 - 2 * p);
						const per = m.dist / Math.ceil(n / 2);
						// back foot steps first, then the front foot
						if (i % 2 === 0) {
							dB += per * e;
							liftB = Math.max(liftB, Math.sin(Math.PI * p));
						} else {
							dF += per * e;
							liftF = Math.max(liftF, Math.sin(Math.PI * p));
						}
					}
				}
				pose.footF = {x: pose.footF.x + dF - travel, y: -14 * h * liftF, tilt: -12 * liftF};
				pose.footB = {x: pose.footB.x + dB - travel, y: -14 * h * liftB + pose.footB.y, tilt: -12 * liftB};
				const moving = a.shuffle.reduce((m, s) => Math.max(m, sstep(s.at - 0.2, s.at + 0.2, t) - sstep(s.at + s.dur - 0.2, s.at + s.dur + 0.3, t)), 0);
				pose.lean += moving * 4;
				pose.hip = add(pose.hip, [0, -moving * 3 * h]);
			}
			if (a.glance !== false) {
				const g = glanceAt(t, seed);
				if (g.w > 0) {
					const away: V2 = g.kind < 0.5 ? [-420 * h, -40 * h] : [90 * h, 40 * h];
					pose.look = away;
					pose.lookWeight = g.w;
					pose.nod += g.kind >= 0.5 ? 9 * g.w : 0;
				}
			}
		}
		return {pose, travel};
	}

	if (a.type === 'walk') {
		const g = gaitFor(b);
		const speed = (a.speed ?? (b.age === 'old' ? 120 : b.age === 'child' ? 150 : 190)) * h;
		// no start: an endless steady walk (travel 0 at t = 0); with a start: ramps up from standing
		const travelFn = a.start === undefined ? (tt: number) => speed * tt : steadyTravel(speed, a.start, a.dist ?? Infinity, 0.6);
		const d = travelFn(t) + g.stride * 0.05;
		const sp = (travelFn(t + 0.02) - travelFn(t - 0.02)) / 0.04 / speed;
		const u = d / g.stride;
		const F = walkFoot(d, 0, g);
		const B = walkFoot(d, 0.5, g);
		const hs = handSets[a.hands ?? 'hang'];
		const swing = a.hands === undefined || a.hands === 'hang' ? 22 * sp * Math.cos(2 * Math.PI * u) : 0;
		const bob = 4.5 * h * sp * Math.cos(4 * Math.PI * u);
		const pose: Pose = {
			...base,
			hip: [0, restHip(b) + 3 * h * sp + bob],
			lean: base.lean + 4 * sp + breath * 0.3,
			footF: {x: F.x - (d - g.stride * 0.05), y: F.y, tilt: F.tilt},
			footB: {x: B.x - (d - g.stride * 0.05), y: B.y, tilt: B.tilt},
			handF: add(rotV(scaled(hs.f, h), a.hands === 'cane' ? 0 : swing), [0, 0]),
			handB: rotV(scaled(hs.b, h), -swing),
			elbowF: hs.ef,
			elbowB: hs.eb,
			face,
			nod: base.nod + 3,
		};
		// a held object bobs with the steps
		if (a.hands && a.hands !== 'hang') {
			pose.handF = add(pose.handF, [0, bob * 0.6]);
			pose.handB = add(pose.handB, [0, bob * 0.6]);
		}
		return {pose, travel: d - g.stride * 0.05};
	}

	// seated actions on a vehicle: targets are in figure space; `bob` is the vehicle's vertical bounce
	const bob = 'bob' in a && a.bob ? a.bob : 0;
	if (a.type === 'ride') {
		const hip: V2 = add(a.seat, [0, bob]);
		const lean = 10 + breath * 0.4;
		return {
			pose: {
				...base,
				hip,
				lean,
				handF: reach(hip, lean, b, a.bar, true),
				handB: reach(hip, lean, b, add(a.bar, [-4 * h, 2 * h]), false),
				elbowF: [-0.2, 1],
				elbowB: [-0.2, 1],
				footF: {x: a.floor[0] + 8 * h, y: a.floor[1], tilt: 0},
				footB: {x: a.floor[0] - 6 * h, y: a.floor[1], tilt: 0},
				knee: [0.6, -1],
				face,
				nod: -2,
			},
			travel: 0,
		};
	}
	if (a.type === 'pillion') {
		// side-saddle: the thighs point at the camera (foreshortened), the shins hang down the scooter's side
		const hip: V2 = add(a.seat, [0, bob * 1.15]);
		const lean = 2 + breath * 0.5;
		const hold = a.hold ?? add(a.seat, [40 * h, -60 * h]);
		return {
			pose: {
				...base,
				hip,
				lean,
				handF: reach(hip, lean, b, hold, true),
				handB: reach(hip, lean, b, add(hold, [8 * h, 14 * h]), false),
				elbowF: [0.2, 1],
				elbowB: [0.2, 1],
				footF: {x: a.floor[0], y: a.floor[1], tilt: 0},
				footB: {x: a.floor[0] - 10 * h, y: a.floor[1], tilt: 0},
				knee: [1, -0.2],
				thighScale: 0.42,
				turn: 0.35,
				face,
			},
			travel: 0,
		};
	}
	if (a.type === 'perch') {
		// a child standing on the footboard in front of the rider, hands on the handlebar
		const hip: V2 = add([a.floor[0], a.floor[1] - (bones(b).thigh + bones(b).shin + bones(b).ankle - 6 * h)], [0, bob * 0.9]);
		const lean = 6;
		return {
			pose: {
				...base,
				hip,
				lean,
				handF: reach(hip, lean, b, a.bar, true),
				handB: reach(hip, lean, b, add(a.bar, [-3 * h, 0]), false),
				elbowF: [-0.3, 1],
				elbowB: [-0.3, 1],
				footF: {x: a.floor[0] + 6 * h, y: a.floor[1], tilt: 0},
				footB: {x: a.floor[0] - 8 * h, y: a.floor[1], tilt: 0},
				face,
				nod: -4,
			},
			travel: 0,
		};
	}
	// lap: a small child seated across the lap, legs forward
	const hip: V2 = add(a.seat, [0, bob * 1.2]);
	const k = bones(b);
	return {
		pose: {
			...base,
			hip,
			lean: -4 + breath * 0.6,
			handF: [10 * h, 60 * h],
			handB: [14 * h, 64 * h],
			elbowF: [0.3, 1],
			elbowB: [0.3, 1],
			footF: {x: hip[0] + k.thigh * 0.9 + 6, y: hip[1] + k.shin * 0.85, tilt: 0},
			footB: {x: hip[0] + k.thigh * 0.85, y: hip[1] + k.shin * 0.9, tilt: 0},
			knee: [0.2, -1],
			face,
			turn: 0.45,
		},
		travel: 0,
	};
};

export {lerp, lerp2};
