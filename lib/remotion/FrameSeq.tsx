import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';

/**
 * A pre-rendered image sequence (Blender hero shots, PLAYBOOK §8.7) played on the film's 60 fps clock.
 * Sequences rendered every `step` frames (step 2 = 30 fps, to halve Cycles time) are blended: between two rendered
 * frames the next one fades in, so slow camera moves stay smooth at 60 fps. Frame f of the Sequence shows source
 * frame `from + f * rate`. Files: `${dir}/${prefix}${NNNN}.png`.
 */
export const FrameSeq: React.FC<{
	dir: string;
	prefix: string;
	last: number;
	step?: number;
	from?: number;
	rate?: number;
	style?: React.CSSProperties;
}> = ({dir, prefix, last, step = 2, from = 0, rate = 1, style}) => {
	const frame = useCurrentFrame();
	const src = Math.min(from + frame * rate, last);
	const a = Math.min(Math.floor(src / step) * step, last);
	const b = Math.min(a + step, last);
	const t = b === a ? 0 : (src - a) / step;
	const file = (n: number) => staticFile(`${dir}/${prefix}${String(n).padStart(4, '0')}.png`);
	const s: React.CSSProperties = {position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', ...style};
	return (
		<AbsoluteFill>
			<Img src={file(a)} style={s} />
			{t > 0.001 ? <Img src={file(b)} style={{...s, opacity: t}} /> : null}
		</AbsoluteFill>
	);
};
