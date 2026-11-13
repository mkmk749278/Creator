// The film's art direction (word_map.md): sea daylight and warm brass; colour means something.
export const C = {
	night: '#05080c', // behind the plate
	plate: '#1a1f25', // the steel inspection plate / drafting table
	grid: '#5b6b7c',
	ink: '#eef3f8',
	dim: '#a9b7c6',
	slot: '#ffcc1f', // caution yellow: the catapult slot, the motif
	amber: '#f2a93b', // steam and pressure
	copper: '#e08a4a', // the electric coils
	red: '#ff3b30', // signal red: the power spike only
	cyan: '#4cc9f0', // measured data (DOT&E, the programme count)
	green: '#3fd27a', // what India already has
	sea: '#1b5a7a',
	paper: '#e9e2d0', // the drafting paper
	pencil: '#2a3440',
} as const;

export const F = {
	label: "'Inter Tight', 'Helvetica Neue', Arial, sans-serif",
	mono: "'JetBrains Mono', 'Courier New', monospace",
} as const;

export const W = 1920;
export const H = 1080;
export const FPS = 60;
