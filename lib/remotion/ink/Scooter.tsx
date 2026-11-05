// A generic Indian step-through scooter of the 2000s, drawn in INK (no brand, no badge): leg shield, small wheels,
// a long seat for two, the rounded engine cowl. Anchor points let riders sit on it with the same rig.
import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {InkLine} from './InkStage';
import {inkPalette} from './InkFigure';
import {V2, add} from './rig';

/** Anchors in scooter space (origin on the ground at the scooter's middle, +x forward, units = figure units). */
export const SCOOTER = {
	frontWheel: [122, -46] as V2,
	rearWheel: [-112, -46] as V2,
	wheelR: 46,
	seatFront: [-28, -160] as V2,
	seatRear: [-118, -160] as V2,
	floor: [42, -54] as V2,
	floorFront: [74, -54] as V2,
	grip: [94, -212] as V2,
	pillionFoot: [-82, -76] as V2,
} as const;

const BODY = '#1B1A1D';

/** Suspension bounce (units) for a scooter riding at `speed` px/s over an Indian road: small, irregular, seeded. */
export const scooterBob = (t: number, speed = 1): number =>
	(Math.sin(t * 9.1) * 1.2 + Math.sin(t * 14.7 + 1.3) * 0.7 + Math.max(0, Math.sin(t * 2.3 + 0.4)) ** 12 * 5) * speed;

export const Scooter: React.FC<{x: number; y: number; scale?: number; facing?: 1 | -1; speed?: number; seed?: string; lampOn?: boolean}> = ({
	x,
	y,
	scale = 1,
	facing = 1,
	speed = 600,
	seed = 'scooter',
	lampOn = true,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const bob = scooterBob(t);
	// wheels turn with road speed (stage px/s → radians), frame-exact
	const ang = ((speed / scale) * t) / SCOOTER.wheelR;
	const P = (p: V2): V2 => p;
	const wheel = (c: V2, k: string) => {
		const spokes = [0, 1, 2, 3, 4].map((i) => {
			const a = ang + (i * 2 * Math.PI) / 5;
			return (
				<InkLine
					key={`${k}s${i}`}
					seed={`${seed}${k}s${i}`}
					w={1.6}
					opacity={0.8}
					pts={[add(c, [Math.cos(a) * 10, Math.sin(a) * 10]), add(c, [Math.cos(a) * 26, Math.sin(a) * 26])]}
				/>
			);
		});
		const treads = new Array(14).fill(0).map((_, i) => {
			const a = ang + (i * 2 * Math.PI) / 14;
			return <InkLine key={`${k}t${i}`} seed={`${seed}${k}t${i}`} w={1.2} opacity={0.5} pts={[add(c, [Math.cos(a) * 38, Math.sin(a) * 38]), add(c, [Math.cos(a) * 45, Math.sin(a) * 45])]} />;
		});
		return (
			<g key={k}>
				<circle cx={c[0]} cy={c[1]} r={SCOOTER.wheelR} fill="#0C0C0E" stroke={inkPalette.ink} strokeWidth={2.6} />
				<circle cx={c[0]} cy={c[1]} r={29} fill="#1E1D20" stroke={inkPalette.ink} strokeWidth={1.8} />
				{treads}
				{spokes}
				<circle cx={c[0]} cy={c[1]} r={7} fill={inkPalette.ink} opacity={0.8} />
			</g>
		);
	};
	return (
		<g transform={`translate(${x} ${y}) scale(${scale * facing} ${scale})`}>
			<ellipse cx={0} cy={2} rx={200} ry={14} fill="rgba(0,0,0,0.6)" style={{filter: 'blur(6px)'}} />
			{wheel(SCOOTER.rearWheel, 'rw')}
			{wheel(SCOOTER.frontWheel, 'fw')}
			<g transform={`translate(0 ${bob.toFixed(2)})`}>
				{/* front fork and fender */}
				<InkLine seed={`${seed}fork`} w={3} pts={[P([112, -168]), P([126, -100]), SCOOTER.frontWheel]} />
				<InkLine seed={`${seed}fender`} smooth closed fill={BODY} w={2.2} pts={[[84, -62], [94, -90], [122, -104], [152, -96], [170, -70], [162, -66], [146, -86], [122, -94], [100, -84], [92, -60]]} />
				{/* the rear cowl over the engine, the floorboard, the leg shield */}
				<InkLine
					seed={`${seed}cowl`}
					smooth
					closed
					fill={BODY}
					w={2.6}
					pts={[[-10, -60], [-8, -104], [-26, -138], [-90, -150], [-150, -140], [-186, -108], [-192, -78], [-174, -56], [-120, -50], [-50, -52]]}
				/>
				<InkLine seed={`${seed}cowlLine`} w={1.4} opacity={0.6} pts={[[-40, -134], [-110, -138], [-168, -118]]} />
				<InkLine seed={`${seed}vent`} w={1.2} opacity={0.5} pts={[[-150, -96], [-120, -98]]} />
				<InkLine seed={`${seed}vent2`} w={1.2} opacity={0.5} pts={[[-150, -86], [-120, -88]]} />
				<InkLine seed={`${seed}floor`} closed fill={BODY} w={2.4} pts={[[-12, -60], [92, -60], [96, -48], [-12, -46]]} />
				<InkLine seed={`${seed}shield`} smooth closed fill={BODY} w={2.6} pts={[[84, -58], [96, -100], [104, -150], [112, -176], [128, -180], [128, -150], [120, -100], [104, -54]]} />
				<InkLine seed={`${seed}horn`} smooth closed fill="#121214" w={1.4} opacity={0.9} pts={[[112, -150], [120, -152], [120, -128], [112, -126]]} />
				{/* seat, tail lamp, exhaust */}
				<InkLine seed={`${seed}seat`} smooth closed fill="#0F0F11" w={2.4} pts={[[-14, -146], [-22, -162], [-70, -168], [-150, -164], [-170, -152], [-150, -144], [-60, -142]]} />
				<InkLine seed={`${seed}rack`} w={1.8} opacity={0.8} pts={[[-150, -150], [-196, -144], [-200, -128]]} />
				<InkLine seed={`${seed}exh`} closed fill="#141416" w={1.8} pts={[[-120, -50], [-196, -44], [-200, -34], [-124, -38]]} />
				<rect x={-196} y={-112} width={10} height={14} fill="#FF3B2A" opacity={0.85} style={{filter: 'blur(0.6px)'}} />
				<circle cx={-191} cy={-105} r={16} fill="#FF3B2A" opacity={0.25} style={{filter: 'blur(8px)'}} />
				{/* steering column, handlebar and headlamp */}
				<InkLine seed={`${seed}col`} w={4} pts={[[120, -170], [114, -204]]} />
				<InkLine seed={`${seed}bar`} closed fill={BODY} w={2.4} pts={[[86, -206], [132, -214], [140, -202], [92, -196]]} />
				<InkLine seed={`${seed}lamp`} closed fill="#2A2A2E" w={2} pts={[[128, -218], [146, -216], [148, -198], [130, -198]]} />
				{lampOn ? (
					<>
						<circle cx={146} cy={-207} r={8} fill="#FFF0C8" />
						<polygon points="146,-216 520,-260 520,-60 146,-198" fill="#FFE7B0" opacity={0.08} style={{filter: 'blur(14px)'}} />
						<circle cx={146} cy={-207} r={26} fill="#FFE7B0" opacity={0.35} style={{filter: 'blur(10px)'}} />
					</>
				) : null}
				<InkLine seed={`${seed}mirror`} w={1.6} pts={[[98, -208], [90, -238]]} />
				<InkLine seed={`${seed}mirror2`} closed fill="#141416" w={1.6} pts={[[82, -248], [96, -250], [96, -236], [82, -234]]} />
			</g>
		</g>
	);
};
