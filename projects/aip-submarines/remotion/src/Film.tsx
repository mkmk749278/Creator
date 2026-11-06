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

export const Film: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		{shots.map((s, i) => {
			const end = i + 1 < shots.length ? shots[i + 1].at : DURATION;
			const pre = s.hard || i === 0 ? 0 : DISSOLVE;
			const from = s.at - pre;
			const dur = end - from + (i + 1 < shots.length && !shots[i + 1].hard ? 0 : 0);
			return (
				<Sequence key={s.name + i} from={from} durationInFrames={Math.max(1, end - from)} name={s.name}>
					<FadeIn n={pre}>{s.el(dur)}</FadeIn>
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
