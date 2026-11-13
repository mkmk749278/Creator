import json from '../../vo/timing.json';

// Every frame comes from the locked audio (vo/timing.json, PLAYBOOK §6.7): sentences by id, words by their text.
type Word = {s: number; w: string; start: number; end: number; startFrame: number; endFrame: number};
type Sentence = {id: number; text: string; start: number; end: number; startFrame: number; endFrame: number};
const T = json as unknown as {fps: number; durationInFrames: number; sentences: Sentence[]; words: Word[]};

export const FPS = T.fps;
export const DURATION = T.durationInFrames;
export const sentences = T.sentences;

const norm = (t: string) => t.toLowerCase().replace(/[^a-z0-9-]+/g, '');

/** Start frame of sentence `id` (a hair early: shots land before their word, never after). */
export const s0 = (id: number): number => Math.floor(T.sentences[id].start * FPS);
/** End frame of sentence `id`. */
export const s1 = (id: number): number => Math.ceil(T.sentences[id].end * FPS);

/** Start frame of the word in sentence `id` that begins `phrase` (its first word; `nth` for repeats). */
export const w0 = (id: number, phrase: string, nth = 0): number => {
	const ws = T.words.filter((w) => w.s === id);
	const q = norm(phrase.split(' ')[0]);
	const hits = ws.filter((w) => norm(w.w) === q || norm(w.w).startsWith(q));
	if (!hits[nth]) {
		throw new Error(`timing: "${phrase}" not in sentence ${id}: ${T.sentences[id].text}`);
	}
	return Math.floor(hits[nth].start * FPS);
};
/** End frame of the word `phrase`'s last word in sentence `id`. */
export const w1 = (id: number, phrase: string, nth = 0): number => {
	const parts = phrase.split(' ');
	const ws = T.words.filter((w) => w.s === id);
	const first = ws.findIndex((w, i) => norm(w.w).startsWith(norm(parts[0])) && ws.slice(0, i).filter((x) => norm(x.w).startsWith(norm(parts[0]))).length === nth);
	if (first < 0) {
		throw new Error(`timing: "${phrase}" not in sentence ${id}`);
	}
	return Math.ceil(ws[Math.min(ws.length - 1, first + parts.length - 1)].end * FPS);
};
/** Seconds → frames. */
export const sec = (s: number): number => Math.round(s * FPS);
