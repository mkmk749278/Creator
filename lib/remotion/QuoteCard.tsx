import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {colors} from './brand';
import {fontStacks} from './fonts';
import {Camera} from './Camera';
import {Paper} from './Document';
import {Desk} from './Photo';
import {ease, tween} from './motion';

/**
 * An attributed quote on period paper (PLAYBOOK §8.3, §9): the words verbatim from claims.csv, typeset (never a
 * facsimile of a real document), with an attribution line and an optional highlighter that sweeps the key phrase as
 * the voice reaches it. `lines` are the quote broken by hand for the page; `mark` is the index of the line to
 * highlight, swept from `markFrom` to `markTo` (local frames). The camera eases in so the marked line ends at least a
 * third of the frame wide (Creator lesson: readable on a phone).
 */
export const QuoteCard: React.FC<{
	lines: string[];
	attribution: string;
	at?: number;
	mark?: number;
	markFrom?: number;
	markTo?: number;
	tone?: 'cream' | 'newsprint' | 'card';
	seed?: string;
}> = ({lines, attribution, at = 0, mark, markFrom = 0, markTo = 0, tone = 'cream', seed = 'quote'}) => {
	const frame = useCurrentFrame();
	const sweep = tween(frame, markFrom, markTo, 0, 1, ease.sweep);
	return (
		<AbsoluteFill style={{background: '#0E0F12'}}>
			<Desk />
			<Camera seed={seed} drift={2} keys={[{f: at, scale: 0.96, y: 30}, {f: at + 400, scale: 1.08, y: -10}]}>
				<Paper at={at} width={1380} tone={tone} seed={seed}>
					<div style={{padding: '86px 100px 70px', fontFamily: fontStacks.quote, color: '#2E2418'}}>
						<div style={{fontSize: 120, lineHeight: 0.6, color: colors.bronze, opacity: 0.7, height: 54}}>“</div>
						{lines.map((l, i) => (
							<div key={i} style={{position: 'relative', fontSize: 56, lineHeight: 1.42, fontStyle: 'italic', whiteSpace: 'nowrap', width: 'fit-content'}}>
								{i === mark ? (
									<span
										style={{
											position: 'absolute',
											left: -8,
											top: '12%',
											height: '78%',
											width: `calc(${sweep * 100}% + 16px)`,
											background: colors.gold,
											opacity: 0.45,
											borderRadius: 6,
											mixBlendMode: 'multiply',
										}}
									/>
								) : null}
								<span style={{position: 'relative'}}>{l}</span>
							</div>
						))}
						<div style={{marginTop: 34, fontFamily: fontStacks.display, fontSize: 26, letterSpacing: '0.28em', fontStyle: 'normal', color: '#5A4426'}}>— {attribution}</div>
					</div>
				</Paper>
			</Camera>
		</AbsoluteFill>
	);
};
