// Prints every shot's start and length (after the 4 s reframing, segments count as new framings) for the §9.4 audit.
import {open} from '../src/scenes/c0_open';
import {ch12} from '../src/scenes/c1_c2';
import {ch34} from '../src/scenes/c3_c4';
import {ch5} from '../src/scenes/c5_land';
import {DURATION, FPS} from '../src/timing';

const shots = [open, ch12, ch34, ch5].flatMap((p) => p.shots).sort((a, b) => a.at - b.at);
let long = 0;
const rows: string[] = [];
shots.forEach((s, i) => {
	const end = i + 1 < shots.length ? shots[i + 1].at : DURATION;
	const len = (end - s.at) / FPS;
	const segs = Math.max(1, Math.ceil((end - s.at) / 270));
	const seg = len / segs;
	if (seg > 5) long++;
	rows.push(`${(s.at / FPS).toFixed(2).padStart(7)}  ${len.toFixed(2).padStart(6)}s  x${segs} ${seg > 5 ? 'LONG' : seg < 0.5 ? 'SHORT' : ''}  ${s.name}`);
});
console.log(rows.join('\n'));
console.log(`${shots.length} shots; mean ${(DURATION / FPS / shots.length).toFixed(2)} s; segments over 5 s: ${long}`);

if (process.argv.includes('--json')) {
	const mids = shots.map((s, i) => {
		const end = i + 1 < shots.length ? shots[i + 1].at : DURATION;
		return {at: s.at, end, mid: Math.round((s.at + end) / 2), name: s.name};
	});
	require('fs').writeFileSync('/tmp/claude-0/shots.json', JSON.stringify(mids));
}
