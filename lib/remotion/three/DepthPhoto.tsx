import {useThree} from '@react-three/fiber';
import {ThreeCanvas} from '@remotion/three';
import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import {grades, Grade} from '../Photo';
import {ease} from '../motion';

/**
 * An archive photo with a real camera move through it (PLAYBOOK §8.2): the photo on a finely subdivided plane,
 * displaced toward the camera by its depth map (scripts/depth_map.py → <name>_depth.png, white = near), filmed by a
 * perspective camera that dollies, pans and drifts. Near things (people, a cart, a lamp post) slide past far things
 * (the street, the sky) the way they would for a real lens: the "2.5D" look, with true occlusion stretch instead of
 * cut-out cards.
 *
 * Keys are local frames; every move is eased (ease.camera). `dolly` 0 = framed to cover, 0.2 = 20% closer.
 * `x`/`y` pan in frame widths (0.05 = 5% of the frame). `depth` is the relief (0.15–0.35 reads as real; more tears).
 * Rendered with --gl=swangle in the cloud (PLAYBOOK §16).
 */
export type DepthKey = {f: number; dolly?: number; x?: number; y?: number; roll?: number};

const val = (keys: DepthKey[], frame: number, p: keyof Omit<DepthKey, 'f'>): number => {
	const ks = keys.filter((k) => k[p] !== undefined);
	if (ks.length === 0) return 0;
	if (ks.length === 1) return ks[0][p] as number;
	return interpolate(frame, ks.map((k) => k.f), ks.map((k) => k[p] as number), {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: ease.camera,
	});
};

/**
 * The hold is released only once the canvas exists and has drawn (`ready`, from onCreated), never when the textures
 * arrive: between `setTex` and the ThreeCanvas mounting there is a tick with no hold, and a render tab that starts
 * mid-shot captured that tick as a black frame (v8 720p: 28 one-frame black flashes, 2026-10-31).
 */
const useTextures = (file: string, depthFile: string): [[THREE.Texture, THREE.Texture, number] | null, () => void] => {
	const [handle] = useState(() => delayRender(`DepthPhoto ${file}`));
	const [tex, setTex] = useState<[THREE.Texture, THREE.Texture, number] | null>(null);
	const ready = useMemo(() => {
		let done = false;
		return () => {
			if (done) return;
			done = true;
			// two animation frames: R3F renders the scene on the frame after onCreated
			requestAnimationFrame(() => requestAnimationFrame(() => continueRender(handle)));
		};
	}, [handle]);
	useEffect(() => {
		const loader = new THREE.TextureLoader();
		const url = (f: string) => (f.startsWith('http') ? f : staticFile(f));
		Promise.all([loader.loadAsync(url(file)), loader.loadAsync(url(depthFile))])
			.then(([img, dep]) => {
				img.colorSpace = THREE.SRGBColorSpace;
				img.anisotropy = 8;
				img.minFilter = THREE.LinearMipmapLinearFilter;
				const im = img.image as HTMLImageElement;
				setTex([img, dep, im.width / im.height]);
			})
			.catch((e) => {
				throw new Error(`DepthPhoto: could not load ${file}: ${e}`);
			});
	}, [file, depthFile, handle]);
	return [tex, ready];
};

const FOV = 30;

const Plate: React.FC<{img: THREE.Texture; dep: THREE.Texture; aspect: number; depth: number; viewAspect: number}> = ({
	img,
	dep,
	aspect,
	depth,
	viewAspect,
}) => {
	// Size the plate to cover the view at distance 1 with overscan for pans and the relief.
	const h = 2 * Math.tan(((FOV / 2) * Math.PI) / 180);
	const w = h * viewAspect;
	const over = 1.18;
	const [pw, ph] = aspect > viewAspect ? [h * aspect * over, h * over] : [w * over, (w / aspect) * over];
	const geo = useMemo(() => new THREE.PlaneGeometry(pw, ph, 320, Math.round(320 / aspect)), [pw, ph, aspect]);
	const mat = useMemo(
		() =>
			new THREE.MeshStandardMaterial({
				color: '#000000',
				emissive: '#ffffff',
				emissiveMap: img,
				displacementMap: dep,
				displacementScale: depth,
				displacementBias: -depth * 0.5,
				toneMapped: false,
			}),
		[img, dep, depth],
	);
	return <mesh geometry={geo} material={mat} />;
};

export const DepthPhoto: React.FC<{
	file: string;
	depthFile?: string;
	keys: DepthKey[];
	depth?: number;
	grade?: Grade;
	/** seeded handheld drift, in frame widths */
	drift?: number;
}> = ({file, depthFile, keys, depth = 0.22, grade = 'archive', drift = 0.004}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const [tex, ready] = useTextures(file, depthFile ?? file.replace(/\.(jpe?g|png)$/i, '_depth.png'));
	const viewAspect = width / height;
	const h = 2 * Math.tan(((FOV / 2) * Math.PI) / 180);
	const dolly = val(keys, frame, 'dolly');
	const x = val(keys, frame, 'x') * h * viewAspect + drift * Math.sin(frame / 97) * h * viewAspect;
	const y = val(keys, frame, 'y') * h + drift * Math.cos(frame / 113) * h;
	const roll = (val(keys, frame, 'roll') * Math.PI) / 180;
	const g = grades[grade];
	return (
		<AbsoluteFill style={{background: '#0b0b0c'}}>
			<AbsoluteFill style={{filter: g.filter}}>
				{tex ? (
					<ThreeCanvas
						width={width}
						height={height}
						gl={{antialias: true, preserveDrawingBuffer: true}}
						camera={{fov: FOV, position: [0, 0, 1], near: 0.01, far: 10}}
						onCreated={({gl}) => {
							gl.outputColorSpace = THREE.SRGBColorSpace;
							ready();
						}}
					>
						<CameraRig z={1 - dolly} x={x} y={y} roll={roll} />
						<Plate img={tex[0]} dep={tex[1]} aspect={tex[2]} depth={depth} viewAspect={viewAspect} />
					</ThreeCanvas>
				) : null}
			</AbsoluteFill>
			<AbsoluteFill style={{background: g.tint, mixBlendMode: 'overlay'}} />
		</AbsoluteFill>
	);
};

const CameraRig: React.FC<{z: number; x: number; y: number; roll: number}> = ({z, x, y, roll}) => {
	// Drive R3F's default camera directly: every frame re-renders this, so the camera is a pure function of the frame.
	const camera = useThree((st) => st.camera);
	camera.position.set(x, y, z);
	camera.lookAt(x * 0.85, y * 0.85, 0);
	camera.rotateZ(roll);
	camera.updateProjectionMatrix();
	return null;
};
