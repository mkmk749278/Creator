#!/usr/bin/env node
// Review stills for a composition, bundled once (PLAYBOOK §10.6: look at every PNG before rendering).
// `npx remotion still` re-bundles per frame; this bundles once and renders every listed frame.
//
// Usage: node scripts/remotion_stills.mjs films/<slug>/remotion COMP OUT_DIR FRAMES [--scale 0.5]
//   FRAMES: comma list of frames or ranges with a step, e.g. "0,120,300" or "0-16000:300"
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';

const [project, comp, out, spec, ...rest] = process.argv.slice(2);
if (!spec) {
	console.error('usage: remotion_stills.mjs PROJECT COMP OUT FRAMES [--scale S]');
	process.exit(2);
}
const scale = rest[0] === '--scale' ? Number(rest[1]) : 0.5;
const req = createRequire(path.resolve(project, 'package.json'));
const {bundle} = req('@remotion/bundler');
const {selectComposition, renderStill} = req('@remotion/renderer');

const frames = spec.split(',').flatMap((p) => {
	const m = p.match(/^(\d+)-(\d+):(\d+)$/);
	if (!m) return [Number(p)];
	const [a, b, s] = m.slice(1).map(Number);
	const r = [];
	for (let f = a; f <= b; f += s) r.push(f);
	return r;
});

fs.mkdirSync(out, {recursive: true});
// lib/remotion sits outside the project: give it the project's node_modules (a gitignored link), since the webpack
// override alone did not reach its imports when bundling from Node.
const libModules = path.resolve(project, '../../../lib/remotion/node_modules');
if (!fs.existsSync(libModules)) fs.symlinkSync(path.relative(path.dirname(libModules), path.resolve(project, 'node_modules')), libModules);
// Same override as the film's remotion.config.ts: lib/remotion resolves its imports from the project's node_modules.
const webpackOverride = (config) => ({
	...config,
	resolve: {...config.resolve, modules: [path.resolve(project, 'node_modules'), 'node_modules']},
});
const serveUrl = await bundle({entryPoint: path.resolve(project, 'src/index.ts'), publicDir: path.resolve(project, 'public'), webpackOverride});
const composition = await selectComposition({serveUrl, id: comp, chromiumOptions: {gl: 'swangle'}});
for (const frame of frames) {
	const file = path.join(out, `${comp}_${String(frame).padStart(6, '0')}.jpg`);
	if (fs.existsSync(file)) continue;
	await renderStill({serveUrl, composition, frame, output: file, imageFormat: 'jpeg', jpegQuality: 88, scale, chromiumOptions: {gl: 'swangle'}});
	console.log('still', frame);
}
