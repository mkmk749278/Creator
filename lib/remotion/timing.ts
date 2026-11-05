// Typed access to a film's VO timing (scripts/vo_timing.py → films/<slug>/vo/timing.json, PLAYBOOK §10.4).
// Scenes never type frame numbers by hand: they ask for a sentence or a word and get its frame.

export type TimedWord = {s: number; w: string; start: number; end: number; startFrame: number; endFrame: number};
export type TimedSentence = {
	id: number;
	block: number;
	chapter: string;
	text: string;
	tagged: string;
	start: number;
	end: number;
	startFrame: number;
	endFrame: number;
};
export type TimedChapter = {title: string; start: number; startFrame: number};
export type TimingJson = {
	fps: number;
	duration: number;
	durationInFrames: number;
	sentences: TimedSentence[];
	words: TimedWord[];
	chapters: TimedChapter[];
};

const norm = (t: string): string => t.toLowerCase().replace(/[^a-z0-9 ]+/g, '').replace(/\s+/g, ' ').trim();

export type Timing = ReturnType<typeof makeTiming>;

export const makeTiming = (json: TimingJson) => {
	const {sentences, words, chapters, fps} = json;
	const wordsOf = (id: number): TimedWord[] => words.filter((w) => w.s === id);

	/** The sentence whose text starts with (or contains) `text`, searching from sentence `after` on. */
	const sentence = (text: string, after = 0): TimedSentence => {
		const q = norm(text);
		const hit =
			sentences.find((s) => s.id >= after && norm(s.text).startsWith(q)) ??
			sentences.find((s) => s.id >= after && norm(s.text).includes(q));
		if (!hit) {
			throw new Error(`timing: no sentence matching "${text}" after #${after}`);
		}
		return hit;
	};

	/** Frame where `phrase` starts inside the sentence matching `inSentence` (phrase = one or more words). */
	const word = (inSentence: string, phrase: string, after = 0): TimedWord => {
		const s = sentence(inSentence, after);
		const ws = wordsOf(s.id);
		const q = norm(phrase).split(' ');
		for (let i = 0; i + q.length <= ws.length; i++) {
			if (q.every((p, k) => norm(ws[i + k].w) === p)) {
				return ws[i];
			}
		}
		throw new Error(`timing: no "${phrase}" in sentence #${s.id} "${s.text}"`);
	};

	/** Last frame of `phrase` inside the sentence (end of its last word). */
	const wordEnd = (inSentence: string, phrase: string, after = 0): number => {
		const s = sentence(inSentence, after);
		const first = word(inSentence, phrase, after);
		const ws = wordsOf(s.id);
		const i = ws.indexOf(first);
		return ws[i + norm(phrase).split(' ').length - 1].endFrame;
	};

	const chapter = (title: string): {start: number; end: number} => {
		const i = chapters.findIndex((c) => c.title === title);
		if (i < 0) {
			throw new Error(`timing: no chapter "${title}"`);
		}
		const end = i + 1 < chapters.length ? chapters[i + 1].startFrame : json.durationInFrames;
		return {start: chapters[i].startFrame, end};
	};

	return {fps, json, sentences, words, chapters, sentence, word, wordEnd, wordsOf, chapter};
};
