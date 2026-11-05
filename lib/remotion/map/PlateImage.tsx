import React, {useState} from 'react';
import {continueRender, delayRender} from 'remotion';

/**
 * An SVG <image> is not waited on by Remotion: a frame could render before a large plate decoded and show the ground
 * blurred or missing (seen on the v7 720p cut, Dholera). Each plate holds the frame until its own load event.
 */
export const PlateImage: React.FC<React.SVGProps<SVGImageElement> & {href: string}> = (props) => {
	const [handle] = useState(() => delayRender(`sat plate ${props.href}`, {timeoutInMilliseconds: 120000}));
	const done = () => continueRender(handle);
	return <image {...props} onLoad={done} onError={done} />;
};
