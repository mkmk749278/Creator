import {Easing, interpolate, spring} from 'remotion';

// Shared motion vocabulary (PLAYBOOK §6.3): eased curves and springs only, never linear camera or text moves.
export const ease = {
	/** Slow, cinematic in-out: camera pushes, pans. */
	camera: Easing.bezier(0.45, 0, 0.2, 1),
	/** Fast start, long settle: things arriving. */
	arrive: Easing.bezier(0.16, 1, 0.3, 1),
	/** Gentle out: things leaving. */
	leave: Easing.bezier(0.7, 0, 0.84, 0),
	/** Ink or highlighter sweep. */
	sweep: Easing.bezier(0.65, 0, 0.35, 1),
} as const;

/** Clamped, eased interpolation from frame a to b. */
export const tween = (
	frame: number,
	a: number,
	b: number,
	from: number,
	to: number,
	easing: (t: number) => number = ease.camera,
): number => interpolate(frame, [a, b], [from, to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing});

/** 0 → 1 → 0 envelope: fade in over `fadeIn` frames from `start`, out over `fadeOut` frames before `end`. */
export const envelope = (frame: number, start: number, end: number, fadeIn = 12, fadeOut = 12): number =>
	Math.min(tween(frame, start, start + fadeIn, 0, 1, ease.arrive), tween(frame, end - fadeOut, end, 1, 0, ease.leave));

/** Spring that starts at `start` (0 before). Damped by default: lands without wobble. */
export const pop = (frame: number, fps: number, start: number, stiffness = 120, damping = 18, mass = 1): number =>
	spring({frame: frame - start, fps, config: {stiffness, damping, mass}});
