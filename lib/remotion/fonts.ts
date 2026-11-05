import {loadFont} from '@remotion/fonts';
import {continueRender, delayRender, staticFile} from 'remotion';
import {fonts} from './brand';

// Vendored OFL fonts from the project's public/fonts (PLAYBOOK §10.2): never fetched from a CDN at render time.
const LATIN = 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD';
const EXT = 'U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF';

let started = false;

export const loadBrandFonts = (): void => {
	if (started) {
		return;
	}
	started = true;
	const handle = delayRender('Loading brand fonts');
	const f = (family: string, file: string, weight: string, unicodeRange?: string, style = 'normal') =>
		loadFont({family, url: staticFile(`fonts/${file}`), weight, unicodeRange, style});
	Promise.all([
		...['400', '600', '700'].map((w) => f(fonts.display, `cinzel-latin-${w}-normal.woff2`, w)),
		// v8 (2026-10-29): one serif system. EB Garamond (OFL) carries every label, caption, counter and quote beside
		// Cinzel's capitals; its latin-ext subset has the rupee sign (used only for present-day sums).
		...['400', '500', '600', '700'].flatMap((w) => [
			...['normal', 'italic'].map((st) => f(fonts.quote, `eb-garamond-latin-${w}-${st}.woff2`, w, LATIN, st)),
			f(fonts.quote, `eb-garamond-latin-ext-${w}-normal.woff2`, w, EXT),
		]),
	])
		.then(() => continueRender(handle))
		.catch((err: unknown) => {
			throw err;
		});
};

export const fontStacks = {
	display: `'${fonts.display}', serif`,
	text: `'${fonts.text}', Georgia, serif`,
	numbers: `'${fonts.numbers}', Georgia, serif`,
	quote: `'${fonts.quote}', Georgia, serif`,
} as const;
