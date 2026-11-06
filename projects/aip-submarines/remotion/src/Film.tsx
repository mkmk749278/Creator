import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {Atmos, ez} from './parts/kit';
import {DURATION} from './timing';
import {open} from './scenes/c0_open';
import {ch12} from './scenes/c1_c2';
import {ch34} from './scenes/c3_c4';
import {ch5} from './scenes/c5_land';

// The film is a list of shots on frames from the locked audio (vo/timing.json). Each shot runs to the next shot's
// start; a dissolve (0.2 s) overlaps the previous shot unless the cut is hard (§9.4). Overlays (labels, gauges,
// tags) sit on top with their own word frames.

export type Shot = {at: number; el: (dur: number) => React.ReactNode; hard?: boolean; name: string};
export type Overlay = {from: number; to: number; el: React.ReactNode; name: string};
export type Part = {shots: Shot[]; overlays: Overlay[]};

const DISSOLVE = 12;
const parts: Part[] = [open, ch12, ch34, ch5];
const shots = parts.flatMap((p) => p.shots).sort((a, b) => a.at - b.at);
const overlays = parts.flatMap((p) => p.overlays);

const FadeIn: React.FC<{n: number; children: React.ReactNode}> = ({n, children}) => {
	const f = useCurrentFrame();
	const o = n === 0 ? 1 : interpolate(f, [0, n], [0, 1], {extrapolateRight: 'clamp', easing: ez.sweep});
	return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

// §9.4: a new framing about every 4 s. A shot longer than that is split into segments, each with its own framing;
// the camera eases between them in 18 frames (a visible move, never a jump).
const FRAMINGS: [number, number, number][] = [
	[1.0, 0, 0],
	[1.08, -30, -15],
	[1.04, 30, 12],
	[1.09, 20, -20],
	[1.03, -25, 15],
];
const SEG = 240;
const Reframe: React.FC<{dur: number; seed: number; children: React.ReactNode}> = ({dur, seed, children}) => {
	const f = useCurrentFrame();
	const n = Math.max(1, Math.round(dur / SEG));
	if (n === 1) {
		return <>{children}</>;
	}
	const len = dur / n;
	const i = Math.min(n - 1, Math.floor(f / len));
	const pick = (k: number) => FRAMINGS[(k + seed) % FRAMINGS.length];
	const a = pick(Math.max(0, i - 1));
	const b = pick(i);
	const t = i === 0 ? 1 : interpolate(f - i * len, [0, 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ez.cam});
	const v = a.map((x, j) => x + (b[j] - x) * t);
	return <AbsoluteFill style={{transform: `translate(${v[1]}px, ${v[2]}px) scale(${v[0]})`, transformOrigin: '50% 50%'}}>{children}</AbsoluteFill>;
};

export const Film: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		{shots.map((s, i) => {
			const end = i + 1 < shots.length ? shots[i + 1].at : DURATION;
			const pre = s.hard || i === 0 ? 0 : DISSOLVE;
			const from = s.at - pre;
			const dur = end - from + (i + 1 < shots.length && !shots[i + 1].hard ? 0 : 0);
			return (
				<Sequence key={s.name + i} from={from} durationInFrames={Math.max(1, end - from)} name={s.name}>
					<FadeIn n={pre}>
						<Reframe dur={end - from} seed={i}>{s.el(dur)}</Reframe>
					</FadeIn>
				</Sequence>
			);
		})}
		{overlays.map((o, i) => (
			<Sequence key={o.name + i} from={o.from} durationInFrames={Math.max(1, o.to - o.from)} name={o.name} layout="none">
				{o.el}
			</Sequence>
		))}
		<Atmos />
	</AbsoluteFill>
);
