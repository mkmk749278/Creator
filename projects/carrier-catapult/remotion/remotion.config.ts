import {Config} from '@remotion/cli/config';
import path from 'path';

// The shared toolkit in /lib/remotion imports remotion, react and three: resolve them from this film's node_modules.
Config.overrideWebpackConfig((c) => ({
	...c,
	resolve: {
		...c.resolve,
		modules: [path.resolve(process.cwd(), 'node_modules'), 'node_modules'],
	},
}));
Config.setVideoImageFormat('jpeg');
Config.setConcurrency(4);
Config.setChromiumOpenGlRenderer('swangle');
