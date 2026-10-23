// tejasModel.js: the real Tejas airframe for the walk-around (TurboSquid "HAL Tejas Fighter Navy", product 1458138, free,
// TurboSquid Royalty Free License, treated as editorial use: documentary only, never in the thumbnail; the model file is not
// redistributed and stays out of git, see media_manifest.csv). The file is the twin-seat naval variant; we repaint it in Air Force
// grey and hide its navy decals (their images are not in the FBX), missiles and nav lights, so it reads as a new, unmarked airframe
// on the line. Output: nose = +Z, up = +Y, wheels on y = 0, metres (length 13.2 m).
import { THREE } from "./jebA.js";
import { FBXLoader } from "three/addons/loaders/FBXLoader.js";

export const TEJAS = { length: 13.2 };
const HIDE = /navy|3002|tricolor|airforce logo|kisspng|rescue|tejas written|danger|free pilot|oxygen|jetdanger|canopy handle|emgergency|missile|emisson/i;

/** load once; returns { model, bay } where model is a Group to clone and bay = nozzle exit (local, metres) */
export async function loadTejas(url, { paint = 0x5d646b, radome = 0x4c5055, atlas = null } = {}) {
  const fbx = await new FBXLoader().loadAsync(url);
  // matte low-sheen air-superiority grey (a roughness map or clearcoat made it read as chrome under the hangar HDRI)
  const skin = new THREE.MeshStandardMaterial({ color: paint, roughness: 0.7, metalness: 0.05, envMapIntensity: 0.6,
    bumpMap: atlas, bumpScale: atlas ? 0.9 : 0 });
  const skinDark = skin.clone(); skinDark.color = new THREE.Color(paint).multiplyScalar(0.82);
  const nose = skin.clone(); nose.color = new THREE.Color(radome); nose.roughness = 0.5;
  const glass = new THREE.MeshStandardMaterial({ color: 0x10161e, roughness: 0.08, metalness: 0.0, transparent: true, opacity: 0.42, depthWrite: false });
  const steel = new THREE.MeshStandardMaterial({ color: 0x9aa0a8, roughness: 0.32, metalness: 0.9 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x15171a, roughness: 0.7, metalness: 0.35 });
  const display = new THREE.MeshStandardMaterial({ color: 0x050807, emissive: new THREE.Color(0x2a6a52), emissiveIntensity: 0.35, roughness: 0.3 });
  const tyre = new THREE.MeshStandardMaterial({ color: 0x0c0c0d, roughness: 0.92 });
  const nozzle = new THREE.MeshStandardMaterial({ color: 0x3e3f43, roughness: 0.58, metalness: 0.85, side: THREE.DoubleSide });
  const pick = (m) => {
    const n = m.name || "";
    if (HIDE.test(n)) return null;
    if (/^body fuselage dark/i.test(n)) return skinDark;
    if (/^body fuselage/i.test(n)) return skin;
    if (/^nose/i.test(n)) return nose;
    if (/glass|windshield|mirror/i.test(n)) return glass;
    if (/display|hud|button/i.test(n)) return display;
    if (/tire/i.test(n)) return tyre;
    if (/engine plates/i.test(n)) return nozzle;
    if (/steel|pipe/i.test(n)) return steel;
    return dark;   // seats, cables, cockpit cabin, metallic grey parts, __DEFAULT
  };
  const hidden = new THREE.MeshBasicMaterial({ visible: false });
  // the FBX carries the author's Blender studio lights and cameras: drop them (cloned per jet they blew out the hangar)
  const extras = []; fbx.traverse((o) => { if (o.isLight || o.isCamera) extras.push(o); });
  extras.forEach((o) => o.parent.remove(o));
  fbx.userData.droppedExtras = extras.length;
  fbx.traverse((o) => {
    if (!o.isMesh) return;
    o.castShadow = o.receiveShadow = false;
    if (Array.isArray(o.material)) o.material = o.material.map((m) => pick(m) || hidden);
    else o.material = pick(o.material) || hidden;
  });
  // normalise: longest axis = length; nose towards +Z; wheels on the floor
  const box = new THREE.Box3().setFromObject(fbx); const size = box.getSize(new THREE.Vector3());
  const s = TEJAS.length / Math.max(size.x, size.z);
  const g = new THREE.Group(); const inner = new THREE.Group(); inner.add(fbx); g.add(inner);
  inner.scale.setScalar(s);
  if (size.x > size.z) inner.rotation.y = -Math.PI / 2;   // length along x -> along z
  inner.updateMatrixWorld(true);
  // find the nose: the radome material's vertices sit at one end
  let noseZ = 0, nN = 0; const v = new THREE.Vector3();
  fbx.traverse((o) => { if (!o.isMesh) return; const pos = o.geometry.attributes.position; const groups = o.geometry.groups.length ? o.geometry.groups : [{ start: 0, count: o.geometry.index ? o.geometry.index.count : pos.count, materialIndex: 0 }];
    const mats = Array.isArray(o.material) ? o.material : [o.material]; const idx = o.geometry.index;
    for (const gr of groups) { if (mats[gr.materialIndex] !== nose) continue; for (let i = gr.start; i < gr.start + gr.count; i += 9) { v.fromBufferAttribute(pos, idx ? idx.getX(i) : i).applyMatrix4(o.matrixWorld); noseZ += v.z; nN++; } } });
  if (nN && noseZ / nN < 0) inner.rotation.y += Math.PI;
  inner.updateMatrixWorld(true);
  const b2 = new THREE.Box3().setFromObject(inner); const c2 = b2.getCenter(new THREE.Vector3());
  inner.position.set(-c2.x, -b2.min.y, -c2.z);
  g.updateMatrixWorld(true);
  const b3 = new THREE.Box3().setFromObject(g);
  // the nozzle's bounds (material "Engine plates"), so cameras can aim down the exhaust
  const nb = new THREE.Box3();
  fbx.traverse((o) => { if (!o.isMesh) return; const pos = o.geometry.attributes.position; const idx = o.geometry.index; const mats = Array.isArray(o.material) ? o.material : [o.material];
    const groups = o.geometry.groups.length ? o.geometry.groups : [{ start: 0, count: idx ? idx.count : pos.count, materialIndex: 0 }];
    for (const gr of groups) { if (mats[gr.materialIndex] !== nozzle) continue; for (let i = gr.start; i < gr.start + gr.count; i += 3) nb.expandByPoint(v.fromBufferAttribute(pos, idx ? idx.getX(i) : i).applyMatrix4(o.matrixWorld)); } });
  // the exhaust exit: nozzle-material vertices in the last metre of the tail -> centre and radius
  const tb = new THREE.Box3();
  fbx.traverse((o) => { if (!o.isMesh) return; const pos = o.geometry.attributes.position; const idx = o.geometry.index; const mats = Array.isArray(o.material) ? o.material : [o.material];
    const groups = o.geometry.groups.length ? o.geometry.groups : [{ start: 0, count: idx ? idx.count : pos.count, materialIndex: 0 }];
    for (const gr of groups) { if (mats[gr.materialIndex] !== nozzle) continue; for (let i = gr.start; i < gr.start + gr.count; i++) { v.fromBufferAttribute(pos, idx ? idx.getX(i) : i).applyMatrix4(o.matrixWorld); if (v.z < b3.min.z + 1.0) tb.expandByPoint(v); } } });
  const exhaust = tb.isEmpty() ? null : { center: tb.getCenter(new THREE.Vector3()), radius: Math.min(tb.max.x - tb.min.x, tb.max.y - tb.min.y) / 2, zExit: tb.min.z };
  return { model: g, box: b3, nozzleBox: nb, exhaust, dropped: extras.length, materials: { skin, skinDark, nose, glass, nozzle } };
}
