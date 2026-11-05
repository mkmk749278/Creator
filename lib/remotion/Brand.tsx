import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';

/** The logo bug (PLAYBOOK §6.5): the medallion at ~60% opacity, ~5% of frame height, top-right, all film long. */
export const LogoBug: React.FC<{opacity?: number}> = ({opacity = 0.6}) => {
	const frame = useCurrentFrame();
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<Img
				src={staticFile('brand/medallion_512.png')}
				style={{
					position: 'absolute',
					top: 40,
					right: 48,
					width: 58,
					height: 58,
					opacity,
					filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.6))',
					transform: `rotate(${Math.sin(frame / 600) * 2}deg)`,
				}}
			/>
		</AbsoluteFill>
	);
};

/** An honesty label (PLAYBOOK §9.4): RECONSTRUCTION / ILLUSTRATION / ARCHIVE, small, top-left. */
export const HonestyTag: React.FC<{text: 'RECONSTRUCTION' | 'ILLUSTRATION' | 'ARCHIVE' | 'ILLUSTRATIVE FOOTAGE' | 'COLOURISED'}> = ({text}) => (
	<AbsoluteFill style={{pointerEvents: 'none'}}>
		<div
			style={{
				position: 'absolute',
				top: 46,
				left: 52,
				fontFamily: "'Inter', sans-serif",
				fontWeight: 600,
				fontSize: 17,
				letterSpacing: '0.32em',
				color: 'rgba(255,255,255,0.72)',
				padding: '7px 12px',
				background: 'rgba(0,0,0,0.35)',
				borderLeft: '2px solid #C57D3C',
			}}
		>
			{text}
		</div>
	</AbsoluteFill>
);
