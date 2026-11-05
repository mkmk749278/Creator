import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {pop, tween} from './motion';

/** Colour grades by era (PLAYBOOK §6.1: one colour temperature per era). CSS filters + a tint layer. */
export const grades = {
	archive: {filter: 'sepia(0.55) contrast(1.12) brightness(0.92) saturate(0.85)', tint: 'rgba(197,125,60,0.10)'},
	furnace: {filter: 'sepia(0.35) contrast(1.18) brightness(0.9) saturate(1.1)', tint: 'rgba(255,138,61,0.14)'},
	aviation: {filter: 'sepia(0.35) contrast(1.1) brightness(0.95) saturate(0.8) hue-rotate(-8deg)', tint: 'rgba(90,130,170,0.12)'},
	steel: {filter: 'contrast(1.1) brightness(0.9) saturate(0.7)', tint: 'rgba(120,135,150,0.10)'},
	night: {filter: 'contrast(1.15) brightness(0.8) saturate(0.85)', tint: 'rgba(40,60,90,0.18)'},
	cyan: {filter: 'contrast(1.08) brightness(0.92) saturate(0.85)', tint: 'rgba(60,170,190,0.10)'},
	modern: {filter: 'contrast(1.06) brightness(0.95) saturate(0.95)', tint: 'rgba(0,0,0,0)'},
} as const;
export type Grade = keyof typeof grades;

const src = (file: string): string => (file.startsWith('http') ? file : staticFile(file));

/** A full-bleed photo (cover), graded. Put it inside a Camera for movement. */
export const FullPhoto: React.FC<{file: string; grade?: Grade; position?: string; fit?: 'cover' | 'contain'}> = ({
	file,
	grade = 'archive',
	position = '50% 50%',
	fit = 'cover',
}) => {
	const g = grades[grade];
	return (
		<AbsoluteFill style={{background: '#0b0b0c'}}>
			{fit === 'contain' ? (
				// Blurred copy fills the frame behind a contained image, so a portrait never sits on flat black.
				<Img src={src(file)} style={{position: 'absolute', inset: -60, width: 'calc(100% + 120px)', height: 'calc(100% + 120px)', objectFit: 'cover', filter: `${g.filter} blur(28px) brightness(0.45)`}} />
			) : null}
			<Img src={src(file)} style={{width: '100%', height: '100%', objectFit: fit, objectPosition: position, filter: g.filter}} />
			<AbsoluteFill style={{background: g.tint, mixBlendMode: 'overlay'}} />
		</AbsoluteFill>
	);
};

/** Full-bleed footage, graded, muted unless asked. */
export const Footage: React.FC<{file: string; grade?: Grade; startFrom?: number; rate?: number; volume?: number; position?: string}> = ({
	file,
	grade = 'modern',
	startFrom = 0,
	rate = 1,
	volume = 0,
	position = '50% 50%',
}) => {
	const g = grades[grade];
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<OffthreadVideo
				src={src(file)}
				startFrom={startFrom}
				playbackRate={rate}
				volume={volume}
				style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: position, filter: g.filter}}
			/>
			<AbsoluteFill style={{background: g.tint, mixBlendMode: 'overlay'}} />
		</AbsoluteFill>
	);
};

/**
 * An archive photo as a physical print on the dark desk: cream border, soft shadow, a slow 3D sway, dropped in with a
 * spring at `at`. Used for portraits and documents-as-objects (PLAYBOOK §8.2–8.3).
 */
export const Print: React.FC<{
	file: string;
	at?: number;
	width?: number;
	x?: number;
	y?: number;
	rotate?: number;
	grade?: Grade;
	border?: number;
	seed?: string;
	caption?: string;
}> = ({file, at = 0, width = 760, x = 0, y = 0, rotate = -2, grade = 'archive', border = 18, seed = 'print', caption}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = pop(frame, fps, at, 90, 16);
	const sway = noise2D(seed, frame / 220, 0);
	const g = grades[grade];
	const drop = (1 - p) * 120;
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', perspective: 1400}}>
			<div
				style={{
					width,
					padding: border,
					paddingBottom: caption ? border * 3 : border,
					background: 'linear-gradient(160deg, #EFE6D2 0%, #E2D5BA 60%, #D6C6A5 100%)',
					boxShadow: `0 ${30 + drop / 3}px ${60 + drop / 2}px rgba(0,0,0,${0.55 * p}), 0 4px 10px rgba(0,0,0,0.35)`,
					transform: `translate(${x}px, ${y - drop}px) rotateX(${8 + sway * 3}deg) rotateY(${-6 + sway * 4}deg) rotate(${rotate + sway}deg) scale(${0.94 + 0.06 * p})`,
					opacity: Math.min(1, p * 1.6),
				}}
			>
				<div style={{position: 'relative', overflow: 'hidden'}}>
					<Img src={src(file)} style={{width: '100%', display: 'block', filter: g.filter}} />
					<AbsoluteFill style={{background: g.tint, mixBlendMode: 'overlay'}} />
					<AbsoluteFill style={{boxShadow: 'inset 0 0 60px rgba(60,40,20,0.45)'}} />
				</div>
				{caption ? (
					<div style={{fontFamily: "'Cinzel', serif", fontSize: 22, letterSpacing: '0.18em', color: '#4A3B28', marginTop: border * 0.9, textAlign: 'center'}}>
						{caption}
					</div>
				) : null}
			</div>
		</AbsoluteFill>
	);
};

/**
 * The desk the prints and papers lie on (plan_v7 §2.3): the film's rendered archive table (scripts/blender/
 * archive_table.py, `assets/media/table/table_top.png`), never a void. `grid` is kept for old call sites and ignored.
 * The plate drifts very slowly so the frame is never still; the lamp's pool is warmed a touch.
 */
export const Desk: React.FC<{light?: string; grid?: boolean; plate?: string}> = ({light = 'rgba(255,170,90,0.16)', plate = 'assets/media/table/table_top.png'}) => {
	const frame = useCurrentFrame();
	const lx = 50 + noise2D('desk', frame / 400, 0) * 4;
	const dx = noise2D('deskx', frame / 600, 0) * 14;
	const dy = noise2D('desky', 0, frame / 650) * 10;
	return (
		<AbsoluteFill style={{background: '#0A0907', overflow: 'hidden'}}>
			<AbsoluteFill style={{transform: `translate(${dx}px, ${dy}px) scale(1.14)`}}>
				<Img src={src(plate)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.82)'}} />
			</AbsoluteFill>
			<AbsoluteFill style={{background: `radial-gradient(ellipse 55% 60% at ${lx}% 45%, ${light} 0%, rgba(0,0,0,0) 70%)`, mixBlendMode: 'screen'}} />
		</AbsoluteFill>
	);
};

/** Fade a layer in and out (for dissolves between stacked shots inside one Sequence). */
export const Fade: React.FC<{from: number; to: number; inF?: number; outF?: number; children: React.ReactNode}> = ({
	from,
	to,
	inF = 18,
	outF = 18,
	children,
}) => {
	const frame = useCurrentFrame();
	const o = Math.min(tween(frame, from, from + inF, 0, 1), tween(frame, to - outF, to, 1, 0));
	return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};
