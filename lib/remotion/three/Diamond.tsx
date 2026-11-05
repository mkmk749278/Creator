import {ThreeCanvas} from '@remotion/three';
import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';

/**
 * A cut diamond, built in code (PLAYBOOK §8.6–8.7: our own reconstruction, labelled where it could pass as real).
 * Software GL (--gl=swangle) flattens glass transmission into a milky blob, so the gem is drawn the way jewellery
 * renders cheat: mirror-polished facets (flat-shaded, metal, zero roughness) reflecting a black studio with a few
 * bright softboxes, warm and cool for "fire", plus an inner mirrored shell turning the other way for internal sparkle.
 * Cushion-cut proportions: table, star, upper-girdle, girdle, lower-girdle and pavilion rings to a culet.
 */
const cushion = (n = 16, squash = 0.1): THREE.BufferGeometry => {
	const rings: Array<[number, number, number]> = [
		[0.55, 0.22, 0],
		[0.74, 0.18, 1],
		[0.91, 0.09, 0],
		[1.0, 0.014, 1],
		[1.0, -0.014, 1],
		[0.86, -0.2, 0],
		[0.48, -0.52, 1],
	];
	const culet = new THREE.Vector3(0, -0.88, 0);
	const top = new THREE.Vector3(0, 0.22, 0);
	const pt = (r: number, y: number, i: number, off: number): THREE.Vector3 => {
		const a = ((i + off * 0.5) / n) * Math.PI * 2;
		const c = 1 + squash * Math.cos(4 * a);
		return new THREE.Vector3(Math.cos(a) * r * c, y, Math.sin(a) * r * c);
	};
	const pos: number[] = [];
	const tri = (a: THREE.Vector3, b: THREE.Vector3, c: THREE.Vector3) => pos.push(a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z);
	for (let i = 0; i < n; i++) {
		const j = (i + 1) % n;
		const [r0, y0, o0] = rings[0];
		tri(top, pt(r0, y0, j, o0), pt(r0, y0, i, o0));
		for (let k = 0; k < rings.length - 1; k++) {
			const [ra, ya, oa] = rings[k];
			const [rb, yb, ob] = rings[k + 1];
			const a0 = pt(ra, ya, i, oa);
			const a1 = pt(ra, ya, j, oa);
			const b0 = pt(rb, yb, i, ob);
			const b1 = pt(rb, yb, j, ob);
			tri(a0, a1, b0);
			tri(a1, b1, b0);
		}
		const [rl, yl, ol] = rings[rings.length - 1];
		tri(pt(rl, yl, i, ol), pt(rl, yl, j, ol), culet);
	}
	const g = new THREE.BufferGeometry();
	g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
	g.computeVertexNormals();
	return g;
};

/**
 * Jewellery studio: a dim warm floor, one big overhead softbox, a ring of twelve vertical strip lights (alternating
 * white, amber and blue for "fire") and a few hot spots, so every facet catches a light at some angle as it turns.
 */
const studio = (): THREE.Scene => {
	const s = new THREE.Scene();
	s.background = new THREE.Color('#2a1c11');
	const add = (az: number, el: number, w: number, h: number, col: string, k: number, dist = 6) => {
		const m = new THREE.Mesh(
			new THREE.PlaneGeometry(w, h),
			new THREE.MeshBasicMaterial({color: new THREE.Color(col).multiplyScalar(k), side: THREE.DoubleSide, toneMapped: false}),
		);
		const a = (az * Math.PI) / 180;
		const e = (el * Math.PI) / 180;
		m.position.set(Math.cos(a) * Math.cos(e) * dist, Math.sin(e) * dist, Math.sin(a) * Math.cos(e) * dist);
		m.lookAt(0, 0, 0);
		s.add(m);
	};
	add(0, 88, 4, 4, '#fff4e6', 2.0);
	add(45, 70, 0.6, 4, '#000000', 0);
	add(90, 75, 1.2, 3.5, '#ffe2bd', 1.6);
	const ring = ['#ffffff', '#ffc98a', '#ffffff', '#a8c4ff', '#ffffff', '#ffb36b'];
	for (let i = 0; i < 12; i++) {
		add(i * 30 + 8, 18, 0.9, 5, ring[i % ring.length], i % 2 ? 2.2 : 4.5);
	}
	for (let i = 0; i < 14; i++) {
		// small hot spots scattered over the upper hemisphere: the glints
		const az = (i * 137.5) % 360;
		const el = 20 + ((i * 53) % 60);
		add(az, el, 0.35, 0.35, i % 4 === 0 ? '#ffd7a8' : '#ffffff', 14, 5);
	}
	const floor = new THREE.Mesh(
		new THREE.CircleGeometry(9, 48),
		new THREE.MeshBasicMaterial({color: new THREE.Color('#3a2414').multiplyScalar(1.4), side: THREE.DoubleSide, toneMapped: false}),
	);
	floor.rotation.x = -Math.PI / 2;
	floor.position.y = -3;
	s.add(floor);
	return s;
};

const Gem: React.FC<{spin: number; tilt: number; scale: number; glow: number}> = ({spin, tilt, scale, glow}) => {
	const geometry = useMemo(() => cushion(), []);
	const outer = useMemo(
		() =>
			new THREE.MeshPhysicalMaterial({
				color: '#f3f6ff',
				metalness: 1,
				roughness: 0.03,
				envMapIntensity: 2.4,
				clearcoat: 1,
				clearcoatRoughness: 0,
				flatShading: true,
				transparent: true,
				opacity: 0.92,
			}),
		[],
	);
	const inner = useMemo(
		() =>
			new THREE.MeshStandardMaterial({
				color: '#ffffff',
				metalness: 1,
				roughness: 0,
				envMapIntensity: 1.6,
				flatShading: true,
				side: THREE.BackSide,
				transparent: true,
				opacity: 0.75,
			}),
		[],
	);
	return (
		<group rotation={[tilt, 0, 0]} scale={scale}>
			<mesh geometry={geometry} material={inner} rotation={[0, -spin * 1.7 + 0.3, 0]} scale={0.94} />
			<mesh geometry={geometry} material={outer} rotation={[0, spin, 0]} />
			<pointLight position={[1.5, 2.5, 2.5]} intensity={8 * glow} color="#FFB36B" distance={10} />
		</group>
	);
};

export const Diamond: React.FC<{
	/** degrees of spin per second */
	spinRate?: number;
	/** tilt of the table towards the camera, radians */
	tilt?: number;
	scale?: number;
	glow?: number;
	cameraZ?: number;
	cameraY?: number;
	startSpin?: number;
	x?: number;
	y?: number;
}> = ({spinRate = 12, tilt = 0.35, scale = 0.62, glow = 1, cameraZ = 4.2, cameraY = 1.6, startSpin = 0, x = 0, y = 0}) => {
	const frame = useCurrentFrame();
	const {width, height, fps} = useVideoConfig();
	const spin = ((startSpin + (frame / fps) * spinRate) * Math.PI) / 180;
	return (
		<ThreeCanvas
			width={width}
			height={height}
			gl={{antialias: true, alpha: true, preserveDrawingBuffer: true}}
			camera={{fov: 30, position: [0, cameraY, cameraZ], near: 0.1, far: 50}}
			onCreated={({camera, gl, scene}) => {
				// The environment must exist before the first frame is drawn (an effect would run too late for a still).
				const pmrem = new THREE.PMREMGenerator(gl);
				scene.environment = pmrem.fromScene(studio(), 0).texture;
				pmrem.dispose();
				camera.lookAt(0, 0, 0);
				gl.toneMapping = THREE.AgXToneMapping;
				gl.toneMappingExposure = 1.2;
			}}
		>
			<group position={[x, y, 0]}>
				<Gem spin={spin} tilt={tilt} scale={scale} glow={glow} />
			</group>
		</ThreeCanvas>
	);
};
