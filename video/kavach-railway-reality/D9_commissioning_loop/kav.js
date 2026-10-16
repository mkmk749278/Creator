/* The Kavach Railway Reality: shared helpers for every scene. Copy into each scene folder next to cues.js.
   Everything is a pure function of time: no Date.now, no unseeded random, no state carried between frames. */
(function () {
  const C = window.CUES;
  // time (s, inside the scene) of the word at `frac` (0..1) through line `id`, by its share of the line's characters
  window.word = (id, frac) => { const c = C.cues[id]; return c.at + (c.to - c.at) * Math.min(1, Math.max(0, frac)); };
  // time of a phrase inside a line: first occurrence of `needle` in the VO text
  window.at = (id, needle, after = 0) => {
    const c = C.cues[id], i = c.vo.indexOf(needle);
    if (i < 0) throw new Error(`cue text not found: ${id} "${needle}"`);
    return c.at + (c.to - c.at) * (i / c.vo.length) + after;
  };
  window.mulberry32 = (s) => () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  // film grain: a pre-rendered texture jumped to a new offset every frame (deterministic in t)
  window.grain = (tl, sel, dur) => {
    const n = Math.ceil(dur * 12);
    for (let i = 0; i <= n; i++) { const r = mulberry32(i * 7919 + 13); tl.set(sel, { backgroundPosition: `${Math.floor(r() * 512)}px ${Math.floor(r() * 512)}px` }, i / 12); }
  };
})();
