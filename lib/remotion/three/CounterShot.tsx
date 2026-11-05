import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {ease} from '../motion';
import {DepthKey, DepthPhoto} from './DepthPhoto';

/**
 * The 1924 bank counter (RECONSTRUCTION, scripts/blender/counter.py): the plate on DepthPhoto for a real dolly, and the
 * jewel case as its own layer so it can slide into the lamp pool (plan_v6 §1: the counter seen from the same low angle,
 * four times in the film).
 *
 * The case layer is a full-frame PNG rendered from the same camera, so it lines up with the plate at dolly 0. As the
 * camera dollies, a point at the case's depth grows by (1 − z) / (1 − dolly − z), z being its displacement toward the
 * camera (DepthPhoto: (depth − 0.5) × relief); the layer is scaled by that factor, times the plate's overscan, about
 * the frame centre. Keep pans at 0 in counter shots (the layer follows dolly only).
 */
const OVERSCAN = 1.18; // DepthPhoto's Plate overscan
const CASE_DEPTH = 0.7; // depth-map value at the case (mean over the case in counter_case_depth.png)

const valAt = (keys: DepthKey[], frame: number): number => {
	const ks = keys.filter((k) => k.dolly !== undefined);
	if (ks.length === 0) return 0;
	if (ks.length === 1) return ks[0].dolly as number;
	return interpolate(frame, ks.map((k) => k.f), ks.map((k) => k.dolly as number), {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: ease.camera,
	});
};

export const CounterShot: React.FC<{
	dir: string;
	keys: DepthKey[];
	relief?: number;
	/** Case: null = no case; otherwise the frames over which it slides in (from below, toward the lamp pool). */
	caseIn?: {from: number; to: number} | null;
	/** 0..1 extra light on the case (when it opens, the light spills out). */
	glow?: number;
}> = ({dir, keys, relief = 0.18, caseIn = {from: 0, to: 1}, glow = 0}) => {
	const frame = useCurrentFrame();
	const dolly = valAt(keys, frame);
	const z = (CASE_DEPTH - 0.5) * relief;
	const k = OVERSCAN * ((1 - z) / (1 - dolly - z));
	const slide = caseIn ? interpolate(frame, [caseIn.from, caseIn.to], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease.arrive}) : 1;
	return (
		<AbsoluteFill>
			<DepthPhoto file={`${dir}/counter_plate.png`} depthFile={`${dir}/counter_plate_depth.png`} keys={keys} depth={relief} grade="modern" drift={0.002} />
			{caseIn ? (
				<AbsoluteFill style={{transform: `scale(${k})`, transformOrigin: '50% 50%'}}>
				<AbsoluteFill
					style={{
						transform: `translateY(${slide * 260}px) scale(${1 + slide * 0.35})`,
						transformOrigin: '50% 72%',
						opacity: interpolate(slide, [0, 0.85, 1], [1, 1, 0]),
					}}
				>
					<Img src={staticFile(`${dir}/counter_case.png`)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
					{glow > 0 ? (
						<AbsoluteFill
							style={{
								background: `radial-gradient(ellipse 9% 7% at 50% 74%, rgba(255,250,240,${0.9 * glow}) 0%, rgba(255,214,160,${0.35 * glow}) 45%, rgba(0,0,0,0) 100%)`,
								mixBlendMode: 'screen',
							}}
						/>
					) : null}
				</AbsoluteFill>
				</AbsoluteFill>
			) : null}
		</AbsoluteFill>
	);
};
