// Renders stills at the given frames from one bundle (fast audit sheets, §13.1): node tools/stills.mjs OUTDIR scale f1 f2 ...
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
import fs from 'fs';

const [out, scale, ...frames] = process.argv.slice(2);
fs.mkdirSync(out, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => ({...c, resolve: {...c.resolve, modules: [path.resolve('node_modules'), 'node_modules']}})});
const composition = await selectComposition({serveUrl, id: 'AIP'});
for (const f of frames) {
	try {
		await renderStill({serveUrl, composition, frame: Number(f), output: `${out}/f${String(f).padStart(5, '0')}.png`, scale: Number(scale), chromiumOptions: {gl: 'swangle'}, timeoutInMilliseconds: 120000});
	} catch (e) {
		console.log(`FAIL ${f}: ${String(e).slice(0, 200)}`);
	}
}
console.log('done');
