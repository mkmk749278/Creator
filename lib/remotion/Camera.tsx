import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ease} from './motion';

export type CamKey = {f: number; scale?: number; x?: number; y?: number; rotate?: number; tiltX?: number; tiltY?: number};

const at = (keys: CamKey[], frame: number, prop: keyof Omit<CamKey, 'f'>, rest: number): number => {
	const ks = keys.filter((k) => k[prop] !== undefined);
	if (ks.length === 0) {
		return rest;
	}
	if (ks.length === 1) {
		return ks[0][prop] as number;
	}
	return interpolate(
		frame,
		ks.map((k) => k.f),
		ks.map((k) => k[prop] as number),
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease.camera},
	);
};

/**
 * The virtual camera (PLAYBOOK §8.1): keyframed push/pan/tilt with eased curves, plus a seeded handheld drift so no
 * frame is ever perfectly still. Keyframe frames are local to the enclosing Sequence.
 */
export const Camera: React.FC<{
	keys: CamKey[];
	drift?: number;
	seed?: string;
	perspective?: number;
	children: React.ReactNode;
}> = ({keys, drift = 3, seed = 'cam', perspective = 1600, children}) => {
	const frame = useCurrentFrame();
	const scale = at(keys, frame, 'scale', 1);
	const x = at(keys, frame, 'x', 0) + drift * noise2D(seed + 'x', frame / 140, 0);
	const y = at(keys, frame, 'y', 0) + drift * noise2D(seed + 'y', 0, frame / 160);
	const rotate = at(keys, frame, 'rotate', 0) + (drift / 30) * noise2D(seed + 'r', frame / 200, 1);
	const tiltX = at(keys, frame, 'tiltX', 0);
	const tiltY = at(keys, frame, 'tiltY', 0);
	return (
		<AbsoluteFill style={{perspective, overflow: 'hidden'}}>
			<AbsoluteFill
				style={{
					transform: `translate(${x}px, ${y}px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) rotate(${rotate}deg) scale(${scale})`,
					transformOrigin: '50% 50%',
				}}
			>
				{children}
			</AbsoluteFill>
		</AbsoluteFill>
	);
};

/** Simple push-in over the whole Sequence (the default "never still" move). */
export const Push: React.FC<{
	from?: number;
	to?: number;
	dur: number;
	x?: [number, number];
	y?: [number, number];
	seed?: string;
	children: React.ReactNode;
}> = ({from = 1, to = 1.06, dur, x = [0, 0], y = [0, 0], seed, children}) => (
	<Camera
		seed={seed}
		keys={[
			{f: 0, scale: from, x: x[0], y: y[0]},
			{f: dur, scale: to, x: x[1], y: y[1]},
		]}
	>
		{children}
	</Camera>
);
