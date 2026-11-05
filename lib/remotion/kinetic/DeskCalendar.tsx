// The 2008 desk calendar (chapter 7): one tear-off calendar on a desk; at each frame in `tears` the top month rips
// along its perforation, lifts, curls and falls away, showing the next. Months: January, March, October, November.
// Each page carries the real 2008 day grid (weekday of the 1st computed, not typed).
import React from 'react';
import {random, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors} from '../brand';
import {fontStacks} from '../fonts';
import {ease, tween} from '../motion';
import {SfxCue} from '../sfx';

const MONTHS = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'];
const DAYS_2008 = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

/** Weekday of the 1st of a month (0 = Sunday), Zeller's congruence. */
const weekday1 = (year: number, month: number): number => {
	let m = month + 1;
	let y = year;
	if (m < 3) {
		m += 12;
		y -= 1;
	}
	const k = y % 100;
	const j = Math.floor(y / 100);
	const h = (1 + Math.floor((13 * (m + 1)) / 5) + k + Math.floor(k / 4) + Math.floor(j / 4) + 5 * j) % 7; // 0 = Saturday
	return (h + 6) % 7;
};

export const calendarCues = (tears: number[]): SfxCue[] => tears.flatMap((f) => [
	{frame: f, sfx: 'paper_tear', gainDb: -6},
	{frame: f + 34, sfx: 'paper_flutter', gainDb: -16},
]);

const PW = 620;
const PH = 640;

const Page: React.FC<{month: number; year: number; accent?: boolean}> = ({month, year, accent}) => {
	const first = weekday1(year, month);
	const cells: (number | null)[] = [...new Array(first).fill(null), ...new Array(DAYS_2008[month]).fill(0).map((_, i) => i + 1)];
	return (
		<div
			style={{
				position: 'absolute',
				inset: 0,
				background: 'linear-gradient(180deg, #EFE6D4 0%, #E6DAC2 100%)',
				borderRadius: 6,
				boxShadow: 'inset 0 0 40px rgba(120,90,50,0.25)',
				overflow: 'hidden',
			}}
		>
			{/* perforation along the top */}
			<div style={{position: 'absolute', top: 54, left: 0, right: 0, height: 0, borderTop: '3px dotted rgba(90,70,40,0.45)'}} />
			<div style={{position: 'absolute', top: 92, left: 0, right: 0, textAlign: 'center', fontFamily: fontStacks.display, fontWeight: 700, fontSize: 92, letterSpacing: '0.08em', color: accent ? '#8A3B16' : '#2A2018'}}>
				{MONTHS[month]}
			</div>
			<div style={{position: 'absolute', top: 210, left: 0, right: 0, textAlign: 'center', fontFamily: fontStacks.numbers, fontWeight: 700, fontSize: 40, letterSpacing: '0.3em', color: '#8A5426'}}>
				{year}
			</div>
			<div style={{position: 'absolute', top: 290, left: 60, right: 60, display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', rowGap: 10, fontFamily: fontStacks.text, fontWeight: 600, fontSize: 24, color: '#4A3C2C', textAlign: 'center'}}>
				{['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((d, i) => (
					<div key={`h${i}`} style={{color: i === 0 ? '#9A4A22' : '#8E7A60', fontSize: 20}}>
						{d}
					</div>
				))}
				{cells.map((c, i) => (
					<div key={i} style={{color: i % 7 === 0 ? '#9A4A22' : undefined}}>
						{c ?? ''}
					</div>
				))}
			</div>
			{/* paper grain */}
			<div style={{position: 'absolute', inset: 0, background: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.018) 0px, rgba(0,0,0,0.018) 1px, transparent 1px, transparent 3px)'}} />
		</div>
	);
};

export const DeskCalendar: React.FC<{tears: number[]; months?: number[]; year?: number; x?: number; y?: number; scale?: number}> = ({
	tears,
	months = [0, 2, 9, 10],
	year = 2008,
	x = 960,
	y = 560,
	scale = 1,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<div style={{position: 'absolute', left: x - (PW * scale) / 2, top: y - (PH * scale) / 2, width: PW * scale, height: PH * scale}}>
			<div style={{position: 'absolute', inset: 0, transform: `scale(${scale})`, transformOrigin: '0 0', width: PW, height: PH, perspective: 1600}}>
				{/* the stand behind, and the stack's thickness */}
				<div style={{position: 'absolute', left: -20, right: -20, top: -24, height: 70, background: 'linear-gradient(180deg, #2A2420, #16120F)', borderRadius: 8, border: `2px solid ${colors.bronze}`}} />
				{[3, 2, 1].map((k) => (
					<div key={k} style={{position: 'absolute', inset: 0, transform: `translate(${k * 3}px, ${k * 4}px)`, background: '#CFC2A8', borderRadius: 6, boxShadow: '0 4px 10px rgba(0,0,0,0.4)'}} />
				))}
				{/* pages, last month at the bottom of the stack */}
				{months
					.map((m, i) => ({m, i}))
					.reverse()
					.map(({m, i}) => {
						const at = i < tears.length ? tears[i] : Infinity;
						const age = (frame - at) / fps;
						if (age > 2.2) {
							return null;
						}
						let tf = '';
						let shadow = 0;
						if (age > 0) {
							// rip: the page lifts from the bottom, hinged on the perforation, then lets go and falls
							const lift = tween(frame, at, at + 14, 0, 1, ease.arrive);
							const fall = Math.max(0, age - 0.22);
							const dir = random(`cal${i}`) < 0.5 ? -1 : 1;
							const rx = -38 * lift - fall * 120;
							const tx = dir * (fall * 380 + fall * fall * 120);
							const ty = -40 * lift + fall * fall * 1500;
							const rz = dir * (lift * 4 + fall * 140);
							tf = `translate(${tx}px, ${ty}px) rotateZ(${rz}deg) rotateX(${rx}deg)`;
							shadow = lift;
						}
						return (
							<div
								key={m}
								style={{
									position: 'absolute',
									inset: 0,
									transformOrigin: '50% 54px',
									transform: tf,
									boxShadow: `0 ${8 + 30 * shadow}px ${20 + 40 * shadow}px rgba(0,0,0,${0.45 + 0.2 * shadow})`,
									borderRadius: 6,
								}}
							>
								<Page month={m} year={year} accent={m === 10} />
							</div>
						);
					})}
				{/* binding rings over the top */}
				{new Array(6).fill(0).map((_, k) => (
					<div key={k} style={{position: 'absolute', top: -18, left: 70 + k * 96, width: 18, height: 52, borderRadius: 9, border: `4px solid ${colors.bronze}`, background: 'transparent', boxShadow: '0 3px 6px rgba(0,0,0,0.6)'}} />
				))}
			</div>
		</div>
	);
};
