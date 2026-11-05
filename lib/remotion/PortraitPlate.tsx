// Portrait plate (plan_v7 §2.5): a real person's photograph never floats as a print on a void. The portrait takes the
// frame's full height on one side, feathered into a real place from the same story on the other side (moving with
// depth parallax, softly out of focus), under one grade. Names ride as a lower third over the place.
import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {grades, Grade} from './Photo';
import {DepthPhoto, DepthKey} from './three/DepthPhoto';
import {ease} from './motion';

const src = (f: string): string => (f.startsWith('http') ? f : staticFile(f));

export const PortraitPlate: React.FC<{
	/** the person's photograph */
	file: string;
	/** a real place from the same story (needs <name>_depth.png for parallax; `flat` to skip) */
	place: string;
	placeKeys?: DepthKey[];
	flat?: boolean;
	side?: 'left' | 'right';
	/** share of the frame the portrait takes (0.42 – 0.6) */
	share?: number;
	/** where in the photo the face is, CSS object-position */
	focus?: string;
	grade?: Grade;
	/** portrait push: scale from → to over the shot */
	push?: [number, number];
	children?: React.ReactNode;
}> = ({file, place, placeKeys, flat = false, side = 'right', share = 0.5, focus = '50% 30%', grade = 'archive', push = [1.0, 1.07], children}) => {
	const frame = useCurrentFrame();
	const {durationInFrames, width} = useVideoConfig();
	const t = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp', easing: ease.camera});
	const scale = push[0] + (push[1] - push[0]) * t;
	const g = grades[grade];
	const w = width * share;
	const feather = side === 'right' ? 'linear-gradient(90deg, transparent 0%, #000 22%)' : 'linear-gradient(270deg, transparent 0%, #000 22%)';
	return (
		<AbsoluteFill style={{background: '#0b0b0c'}}>
			{/* the place: soft, darker, moving */}
			<AbsoluteFill style={{filter: 'blur(3px) brightness(0.62)'}}>
				{flat ? (
					<AbsoluteFill style={{transform: `scale(${1.08 + 0.05 * t}) translateX(${(side === 'right' ? 1 : -1) * 20 * t}px)`}}>
						<Img src={src(place)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: g.filter}} />
					</AbsoluteFill>
				) : (
					<DepthPhoto file={place} keys={placeKeys ?? [{f: 0, dolly: 0.02, x: side === 'right' ? 0.02 : -0.02}, {f: durationInFrames, dolly: 0.12, x: side === 'right' ? -0.01 : 0.01}]} depth={0.18} grade={grade} />
				)}
			</AbsoluteFill>
			{/* the person, full height, feathered into the place */}
			<div
				style={{
					position: 'absolute',
					top: 0,
					bottom: 0,
					[side]: 0,
					width: w,
					overflow: 'hidden',
					WebkitMaskImage: feather,
					maskImage: feather,
				}}
			>
				<Img
					src={src(file)}
					style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: focus, filter: g.filter, transform: `scale(${scale})`, transformOrigin: focus}}
				/>
				<AbsoluteFill style={{background: g.tint, mixBlendMode: 'overlay'}} />
			</div>
			{children}
		</AbsoluteFill>
	);
};
