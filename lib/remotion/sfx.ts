// SFX cues (PLAYBOOK §10.2): every visual event exposes {frame, sfx, gainDb}. Systems return cues in their own local
// frames; the film shifts them by the Sequence start and merges them into its cues.ts, so picture and sound never drift.
export type SfxCue = {frame: number; sfx: string; gainDb: number; note?: string};

/** Shift a system's local cues to film frames. */
export const shiftCues = (cues: SfxCue[], from: number): SfxCue[] => cues.map((c) => ({...c, frame: c.frame + from}));
