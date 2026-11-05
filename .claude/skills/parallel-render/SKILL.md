---
name: parallel-render
description: Render a documentary's review cut or 4K master as parallel GitHub Actions jobs (free, 4 vCPU / 16 GB each, 20 at once) and join the parts cleanly. Use for every full render; the session authors and checks, the runners render.
---

# Parallel render on GitHub Actions

Plan and facts: PLAYBOOK §14. Never render a full film inside the session, and never use parallel cloud sessions to
render: they share one usage limit and one IP.

1. **Lock inputs on `main`:** script, VO, `vo/timing.json`, compositions, encode settings. Workflow files must be on
   `main` before they can be triggered.
2. **Split** the film into parts of about 60–90 s. Each part carries only the media seconds it uses; seams go inside a
   shot, never on a cut; part lengths are whole frames.
3. **Media to Drive:** pack each part's media and `rclone mkdir` the Drive folder before starting jobs.
4. **Check before triggering:** `tsc --noEmit` and stills at the key frames (Remotion), or `hyperframes check` on every
   part (older HyperFrames films). A check failure on a runner wastes the whole job.
5. **Trigger** the render workflow per part (GitHub MCP `actions_run_trigger`), 720p for review cuts, 4K (`--scale=2`)
   only for the approved master. Then end the turn; the runners need no watching.
6. **Join:** pull the parts, `ffmpeg -f concat -c copy`, then the mix over the full length (never per part). Check:
   each part's frame count, a strip of 3 frames each side of every seam, freeze and flash scans, loudness, picture and
   audio lengths within 0.15 s. Then `/review-cut`.
