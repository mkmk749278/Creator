// INK cast for 1900–1930 India (and 2008 for the scooter family). Clothing references: period photographs of Bombay
// crowds and Jamshedpur workers (PLAYBOOK §11.5): dhoti and kurta, turbans and the Maharashtrian pheta, the
// nine-yard (nauvari) saree, the worker's vest and cap with a gamcha, the Parsi black hat with a long white coat.
import {Costume, Tone} from './draw';

export const COSTUMES = {
	/** Steelworker: mill cap, vest, short dhoti, a gamcha over the shoulder. */
	workerCap: {head: 'millCap', hair: 'short', top: 'vest', topTone: 'light', bottom: 'dhotiShort', bottomTone: 'white', gamcha: true, moustache: true, headTone: 'mid'},
	/** Steelworker with a head cloth. */
	workerCloth: {head: 'headCloth', hair: 'short', top: 'vest', topTone: 'white', bottom: 'dhotiShort', bottomTone: 'light', moustache: true, headTone: 'white'},
	/** Worker in a kurta and dhoti, turban. */
	workerKurta: {head: 'turban', hair: 'short', top: 'kurta', topTone: 'light', bottom: 'dhoti', bottomTone: 'white', moustache: true, headTone: 'ochre'},
	/** Woman worker: saree over the head. */
	workerWoman: {head: 'bare', hair: 'bun', top: 'blouse', topTone: 'mid', bottom: 'saree', bottomTone: 'maroon', pallu: 'head'},
	/** Townsman: turban, kurta, dhoti. */
	dhotiKurta: {head: 'turban', hair: 'short', top: 'kurta', topTone: 'white', bottom: 'dhoti', bottomTone: 'white', moustache: true, headTone: 'light'},
	/** Bombay clerk: pheta, dark coat, dhoti. */
	clerk: {head: 'pheta', hair: 'short', top: 'coat', topTone: 'dark', bottom: 'dhoti', bottomTone: 'white', moustache: true, headTone: 'maroon'},
	/** An old man: turban, grey beard, spectacles, kurta, dhoti (give him the cane). */
	elder: {head: 'turban', hair: 'grey', top: 'kurta', topTone: 'white', bottom: 'dhoti', bottomTone: 'white', beard: true, glasses: true, headTone: 'white'},
	/** Parsi gentleman: the tall black hat, a long white coat, white trousers. */
	parsi: {head: 'parsiCap', hair: 'short', top: 'coat', topTone: 'white', bottom: 'pyjama', bottomTone: 'white', moustache: true, glasses: true, shoes: true},
	/** Young man: bare head, kurta and waistcoat, dhoti. */
	youngMan: {head: 'bare', hair: 'short', top: 'kurta', topTone: 'light', bottom: 'dhoti', bottomTone: 'white', waistcoat: true, moustache: true},
	/** Woman in a nine-yard saree, the end over the shoulder, a zari border. */
	nauvari: {head: 'bare', hair: 'bun', top: 'blouse', topTone: 'dark', bottom: 'nauvari', bottomTone: 'green', pallu: 'shoulder', border: true},
	/** Older woman in a nine-yard saree, the end over her head. */
	nauvariElder: {head: 'bare', hair: 'greyBun', top: 'blouse', topTone: 'mid', bottom: 'nauvari', bottomTone: 'maroon', pallu: 'head', border: true},
	/** Boy, 1900s: short hair, kurta, shorts. */
	boy: {head: 'bare', hair: 'child', top: 'kurta', topTone: 'white', bottom: 'shorts', bottomTone: 'mid'},
	/** Girl, 1900s: plait, frock (a long one). */
	girl: {head: 'bare', hair: 'plait', top: 'frock', topTone: 'ochre', bottom: 'skirt', bottomTone: 'ochre'},
	// ---------------- 2008
	father2008: {head: 'helmet', hair: 'short', top: 'shirt', topTone: 'light', bottom: 'trousers', bottomTone: 'dark', moustache: true, shoes: true},
	mother2008: {head: 'bare', hair: 'bun', top: 'blouse', topTone: 'maroon', bottom: 'saree', bottomTone: 'indigo', pallu: 'shoulder', border: true, shoes: true},
	boy2008: {head: 'bare', hair: 'child', top: 'tshirt', topTone: 'ochre', bottom: 'shorts', bottomTone: 'dark', shoes: true},
	girl2008: {head: 'bare', hair: 'plait', top: 'frock', topTone: 'green', bottom: 'skirt', bottomTone: 'green', shoes: true},
} satisfies Record<string, Costume>;

export type CostumeName = keyof typeof COSTUMES;

const TONES: Tone[] = ['white', 'light', 'mid', 'ochre', 'maroon', 'indigo', 'green'];

/** A seeded variation of a costume (cloth tones, moustache): a crowd never looks cloned. */
export const vary = (c: Costume, r: (k: string) => number): Costume => {
	const pick = (k: string, base: Tone, pool: Tone[]): Tone => (r(k) < 0.45 ? base : pool[Math.floor(r(k + 'p') * pool.length)]);
	return {
		...c,
		topTone: pick('top', c.topTone, c.top === 'vest' || c.top === 'kurta' ? ['white', 'light', 'mid'] : TONES),
		bottomTone: pick('bot', c.bottomTone, c.bottom === 'nauvari' || c.bottom === 'saree' ? ['maroon', 'green', 'indigo', 'ochre'] : ['white', 'light']),
		headTone: c.headTone ? pick('head', c.headTone, ['white', 'light', 'ochre', 'maroon']) : c.headTone,
		moustache: c.moustache && r('m') < 0.85,
	};
};
