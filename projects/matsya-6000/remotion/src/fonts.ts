import {loadFont} from '@remotion/fonts';
import {continueRender, delayRender, staticFile} from 'remotion';

let started = false;
// Vendored OFL fonts (public/fonts), never fetched at render time (PLAYBOOK §10.2).
export const loadFilmFonts = (): void => {
	if (started) {
		return;
	}
	started = true;
	const h = delayRender('fonts');
	Promise.all([
		...['500', '700', '800'].map((w) => loadFont({family: 'Inter Tight', url: staticFile(`fonts/inter-tight-latin-${w}-normal.woff2`), weight: w})),
		...['500', '700'].map((w) => loadFont({family: 'JetBrains Mono', url: staticFile(`fonts/jetbrains-mono-latin-${w}-normal.woff2`), weight: w})),
	]).then(() => continueRender(h));
};
