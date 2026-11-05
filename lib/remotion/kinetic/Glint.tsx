// A star glint on a stone's facet (PLAYBOOK §8.4, kinetic accents): a bright core and four soft rays that bloom and
// die in about two thirds of a second, turning slightly. Placed on a facet a render already lights, so it marks a
// real highlight rather than inventing one. Positions are in the 1920×1080 authoring frame.
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {ease, tween} from '../motion';

export const Glint: React.FC<{x: number; y: number; at: number; size?: number; dur?: number}> = ({x, y, at, size = 160, dur = 40}) => {
	const frame = useCurrentFrame();
	const up = tween(frame, at, at + dur * 0.35, 0, 1, ease.arrive);
	const down = tween(frame, at + dur * 0.35, at + dur, 1, 0, ease.leave);
	const k = up * down;
	if (k <= 0) {
		return null;
	}
	const rot = 12 + tween(frame, at, at + dur, 0, 18);
	const ray = (deg: number, len: number) => (
		<div
			style={{
				position: 'absolute',
				left: -len / 2,
				top: -1.5,
				width: len,
				height: 3,
				transform: `rotate(${deg}deg)`,
				background: 'linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.95) 50%, transparent 100%)',
				filter: 'blur(0.6px)',
			}}
		/>
	);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'screen'}}>
			<div style={{position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg) scale(${0.3 + 0.7 * k})`, opacity: k}}>
				{ray(0, size)}
				{ray(90, size)}
				{ray(45, size * 0.45)}
				{ray(-45, size * 0.45)}
				<div style={{position: 'absolute', left: -14, top: -14, width: 28, height: 28, borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(220,235,255,0.6) 35%, transparent 70%)'}} />
			</div>
		</AbsoluteFill>
	);
};
