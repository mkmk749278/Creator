import {ThreeCanvas} from '@remotion/three';
import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';
import {noise2D} from '@remotion/noise';

// A Kalvari (Scorpène) type hull drawn from the class's published shape (ILLUSTRATION): a 67.5 m body of
// revolution, 6.2 m beam, the fin forward of amidships with its masts, cruciform stern planes, a seven-blade screw.
// Units are metres; the bow points to +x. Used under water (T1) and, with `ghost`, for the "invisible" beat.

export const HULL_LEN = 67.5;
const R = 3.1;

const radius = (x: number): number => {
	// x from 0 (stern tip) to HULL_LEN (bow tip)
	const bowLen = 9;
	const sternLen = 20;
	if (x > HULL_LEN - bowLen) {
		const u = (HULL_LEN - x) / bowLen; // 0 at the tip
		return R * Math.sqrt(Math.max(0, 1 - (1 - u) * (1 - u)));
	}
	if (x < sternLen) {
		const u = x / sternLen; // 0 at the tail
		return 0.35 + (R - 0.35) * Math.pow(Math.sin((u * Math.PI) / 2), 1.35);
	}
	return R;
};

const hullGeometry = (): THREE.BufferGeometry => {
	const pts: THREE.Vector2[] = [];
	const N = 120;
	for (let i = 0; i <= N; i++) {
		const x = (i / N) * HULL_LEN;
		pts.push(new THREE.Vector2(Math.max(0.001, radius(x)), x));
	}
	const g = new THREE.LatheGeometry(pts, 72);
	g.rotateZ(-Math.PI / 2); // axis along +x
	g.translate(-HULL_LEN / 2, 0, 0);
	return g;
};

const finGeometry = (): THREE.BufferGeometry => {
	// side profile of the fin (x along the hull, y up), extruded across the beam
	const s = new THREE.Shape();
	const L = 9.5;
	const Hh = 4.6;
	s.moveTo(0, 0);
	s.lineTo(L, 0);
	s.lineTo(L - 0.6, Hh - 0.6);
	s.quadraticCurveTo(L - 1.2, Hh, L - 2.2, Hh);
	s.lineTo(1.2, Hh);
	s.quadraticCurveTo(0.2, Hh, 0.1, Hh - 1.4);
	s.lineTo(0, 0);
	const g = new THREE.ExtrudeGeometry(s, {depth: 1.3, bevelEnabled: true, bevelSize: 0.35, bevelThickness: 0.35, bevelSegments: 4, curveSegments: 12});
	g.translate(0, 0, -0.65);
	return g;
};

type Props = {
	/** 0 = masts housed, 1 = snorkel fully raised */
	mast?: number;
	/** 0 = solid, 1 = gone (the "ghost maker" beat) */
	ghost?: number;
	/** glow of the AIP plug section (0..1), amber */
	plug?: number;
	/** camera: [x, y, z] and look-at target */
	cam: [number, number, number];
	look?: [number, number, number];
	fov?: number;
	/** boat's own position along x over the shot, metres */
	x?: number;
	depthTint?: number;
};

const Boat: React.FC<Omit<Props, 'cam' | 'look' | 'fov'>> = ({mast = 0, ghost = 0, plug = 0, x = 0}) => {
	const frame = useCurrentFrame();
	const hull = useMemo(hullGeometry, []);
	const fin = useMemo(finGeometry, []);
	const plugGeo = useMemo(() => {
		const g = new THREE.CylinderGeometry(R * 1.004, R * 1.004, 10, 72, 1, true);
		g.rotateZ(Math.PI / 2);
		return g;
	}, []);
	const op = 1 - ghost;
	const mat = (
		<meshStandardMaterial color="#2c343d" roughness={0.55} metalness={0.35} transparent={ghost > 0} opacity={op} />
	);
	const finX = HULL_LEN / 2 - 26; // fin's aft edge, metres from the middle
	const sternX = -HULL_LEN / 2 + 3.2;
	const prop = frame * 0.06;
	const bob = 0.05 * noise2D('bob', frame / 120, 0);
	return (
		<group position={[x, bob, 0]}>
			<mesh geometry={hull}>{mat}</mesh>
			<mesh geometry={fin} position={[finX, R - 0.5, 0]}>
				{mat}
			</mesh>
			{/* masts on the fin: the snorkel rises with `mast` */}
			<mesh position={[finX + 5.2, R + 4.2 + mast * 5.5, 0]}>
				<cylinderGeometry args={[0.22, 0.26, 3 + mast * 2, 16]} />
				{mat}
			</mesh>
			<mesh position={[finX + 3.4, R + 4.2 + mast * 3.2, 0]}>
				<cylinderGeometry args={[0.16, 0.18, 2.5, 16]} />
				{mat}
			</mesh>
			{/* fin planes */}
			<mesh position={[finX + 6.2, R + 2.6, 0]}>
				<boxGeometry args={[2.2, 0.16, 7]} />
				{mat}
			</mesh>
			{/* cruciform stern planes */}
			{[0, 1, 2, 3].map((i) => (
				<mesh key={i} position={[sternX + 2.2, 0, 0]} rotation={[(i * Math.PI) / 2, 0, 0]}>
					<mesh position={[0, 2.2, 0]}>
						<boxGeometry args={[3.2, 3.4, 0.18]} />
						{mat}
					</mesh>
				</mesh>
			))}
			{/* the screw */}
			<group position={[sternX - 0.6, 0, 0]} rotation={[prop, 0, 0]}>
				{Array.from({length: 7}).map((_, i) => (
					<mesh key={i} rotation={[(i * 2 * Math.PI) / 7, 0, 0]} position={[0, 0, 0]}>
						<mesh position={[0, 1.1, 0]} rotation={[0, 0.5, 0]}>
							<boxGeometry args={[0.5, 2.0, 0.08]} />
							<meshStandardMaterial color="#3a3226" roughness={0.4} metalness={0.8} transparent={ghost > 0} opacity={op} />
						</mesh>
					</mesh>
				))}
			</group>
			{plug > 0 ? (
				<mesh geometry={plugGeo} position={[-2, 0, 0]}>
					<meshBasicMaterial color="#f2a93b" transparent opacity={0.7 * plug * op} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} />
				</mesh>
			) : null}
		</group>
	);
};

/** The boat under water: blue fog, light from the surface, drifting particles. */
export const SubUnderwater: React.FC<Props> = ({cam, look = [0, 0, 0], fov = 32, depthTint = 0, ...boat}) => {
	const {width, height} = useVideoConfig();
	const frame = useCurrentFrame();
	const motes = useMemo(() => {
		const a: [number, number, number][] = [];
		for (let i = 0; i < 260; i++) {
			const r = (k: number) => {
				const v = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453;
				return v - Math.floor(v);
			};
			a.push([(r(1) - 0.5) * 140, (r(2) - 0.5) * 50, (r(3) - 0.5) * 90]);
		}
		return a;
	}, []);
	const fogColor = new THREE.Color().lerpColors(new THREE.Color('#0b3a55'), new THREE.Color('#020a12'), depthTint);
	return (
		<ThreeCanvas width={width} height={height} style={{backgroundColor: '#' + fogColor.getHexString()}}>
			<color attach="background" args={['#' + fogColor.getHexString()]} />
			<fog attach="fog" args={['#' + fogColor.getHexString(), 60, 260 - depthTint * 80]} />
			<PerspCam pos={cam} look={look} fov={fov} />
			<hemisphereLight args={['#7fc8ff', '#02060a', 1.1 - depthTint * 0.6]} />
			<directionalLight position={[10, 60, 30]} intensity={3.2 - depthTint * 1.6} color="#cfeaff" />
			<directionalLight position={[-40, 20, -60]} intensity={1.6} color="#5fb4e8" />
			<directionalLight position={[-30, -10, -20]} intensity={0.3} color="#1e5f8a" />
			<Boat {...boat} />
			{motes.map((m, i) => (
				<mesh key={i} position={[m[0] + ((frame * 0.03 + i) % 7) - 3.5, m[1] + Math.sin(frame / 90 + i) * 0.4, m[2]]}>
					<sphereGeometry args={[0.06, 6, 6]} />
					<meshBasicMaterial color="#9fd8ff" transparent opacity={0.35} />
				</mesh>
			))}
		</ThreeCanvas>
	);
};

const PerspCam: React.FC<{pos: [number, number, number]; look: [number, number, number]; fov: number}> = ({pos, look, fov}) => {
	const camera = useThree((st) => st.camera) as THREE.PerspectiveCamera;
	camera.fov = fov;
	camera.near = 0.5;
	camera.far = 600;
	camera.position.set(...pos);
	camera.lookAt(...look);
	camera.updateProjectionMatrix();
	camera.updateMatrixWorld();
	return null;
};
