// The film's art direction (word_map.md): colour means something.
export const C = {
	night: '#03070d', // the sea at night
	deep: '#061524', // under the waves
	steel: '#2a2f36',
	grid: '#3a4552',
	ink: '#eef3f8',
	dim: '#9fb0c2',
	amber: '#f2a93b', // fuel, hydrogen, the powder's energy
	cyan: '#4cc9f0', // current, sonar, data
	frost: '#bfe6ff', // liquid oxygen
	red: '#ff3b3b', // exposure only: the red marks, being found
	green: '#3fd27a', // proven, verified
	orange: '#ff8a3d', // stress, cuts, sparks
} as const;

export const F = {
	label: "'Inter Tight', 'Helvetica Neue', Arial, sans-serif",
	mono: "'JetBrains Mono', 'Courier New', monospace",
} as const;

export const W = 1920;
export const H = 1080;
export const FPS = 60;
