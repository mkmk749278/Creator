import React from 'react';
import {Composition} from 'remotion';
import {Film} from './Film';
import {DURATION, FPS} from './timing';
import {loadFilmFonts} from './fonts';

loadFilmFonts();

export const Root: React.FC = () => (
	<Composition id="AIP" component={Film} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
);
