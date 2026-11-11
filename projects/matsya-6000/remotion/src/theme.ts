// The film's art direction (word_map.md): colour means something.
export const C = {
	night: '#02060b', // the deep
	deep: '#05131f', // water with a little light
	plate: '#2b3036', // the steel inspection plate
	grid: '#3a4552',
	ink: '#eef3f8',
	dim: '#9fb0c2',
	amber: '#f2a93b', // pressure and squeeze
	hot: '#ffd9a0', // a weld being laid (white-hot)
	weld: '#ff8a3d', // the weld cooling
	cyan: '#4cc9f0', // inspection: X-ray, sound, data
	green: '#3fd27a', // certified, verified
	red: '#ff3b3b', // Titan's failure only
	ti: '#c9c4bb', // bare titanium
} as const;

export const F = {
	label: "'Inter Tight', 'Helvetica Neue', Arial, sans-serif",
	mono: "'JetBrains Mono', 'Courier New', monospace",
} as const;

export const W = 1920;
export const H = 1080;
export const FPS = 60;
