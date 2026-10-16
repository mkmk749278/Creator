// Night track bed shared by E3 and E10: rails catching moonlight, PSC sleepers, ballast stones, an RFID tag with a cyan glint.
import { THREE, mats, buildTrack, buildGround, buildStones, buildRFIDTag, sleeperZ, SLEEPER_TOP } from "./kav3d.js";
export function nightTrack(st, { z0 = -120, z1 = 40, tagZ = -14 } = {}) {
  const M = mats(), S = st.scene;
  M.ground.color.setRGB(0.42, 0.42, 0.5); M.ballast.color.setRGB(0.7, 0.7, 0.78); M.concrete.color.setRGB(0.62, 0.63, 0.7);   // night: no daylight colour
  S.add(buildGround(M), buildTrack(M, { cx: 0, z0, z1 }), buildStones(M, { z0: tagZ - 30, z1: z1, n: 5200, seed: 9 }));
  const zt = sleeperZ(z0, tagZ), tag = buildRFIDTag(M); tag.position.set(0, SLEEPER_TOP, zt); S.add(tag);
  // a cool moon low ahead so the rail heads catch a long specular streak
  st.sun.intensity = 0.55; st.hemi.intensity = 0.16; S.environmentIntensity = 0.55;   // rail heads pick up the sky
  const glint = new THREE.PointLight(0x38bdf8, 0, 2.5, 2); glint.position.set(0, SLEEPER_TOP + 0.5, zt + 0.3); S.add(glint);
  return { tag, zt, glint };
}
