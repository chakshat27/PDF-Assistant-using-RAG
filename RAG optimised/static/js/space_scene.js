
import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

const canvas = document.querySelector('#bg-canvas');
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
camera.position.z = 40;
camera.position.y = 20;
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: false,
    antialias: true
});

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

// --- Circular Texture Generation ---
function createCircleTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');

    const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
    gradient.addColorStop(0.3, 'rgba(255, 255, 255, 0.4)');
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(canvas);
}

const circleTexture = createCircleTexture();

// --- Milky Way Linear Band Parameters ---
const params = {
    count: 150000,   // High density
    size: 0.1,
    length: 120,    // Longer band
    thickness: 15,  // Thickness of the band
    depth: 6,       // Depth of the band
    coreColor: '#ffdca2',
    midColor: '#ff8a3d',
    outerColor: '#4422ff',
    dustColor: '#1a0d00' // Dark brown/black for dust lanes
};

const galaxyGeometry = new THREE.BufferGeometry();
const galaxyPositions = new Float32Array(params.count * 3);
const galaxyColors = new Float32Array(params.count * 3);

const colorCore = new THREE.Color(params.coreColor);
const colorMid = new THREE.Color(params.midColor);
const colorOuter = new THREE.Color(params.outerColor);
const colorDust = new THREE.Color(params.dustColor);

for (let i = 0; i < params.count; i++) {
    const i3 = i * 3;

    // Linear distribution along a diagonal axis
    const t = (Math.random() - 0.5) * params.length;
    const r = Math.pow(Math.random(), 2) * params.thickness; // Concentrated in middle
    const angle = Math.random() * Math.PI * 2;

    // Diagonal tilt math (Milky Way across the sky)
    const x = t;
    const y = Math.cos(angle) * r;
    const z = Math.sin(angle) * r * 0.4; // Squashed

    // Apply a 45-degree rotation to make it diagonal
    const angleTilt = Math.PI / 4;
    galaxyPositions[i3] = x * Math.cos(angleTilt) - y * Math.sin(angleTilt);
    galaxyPositions[i3 + 1] = x * Math.sin(angleTilt) + y * Math.cos(angleTilt);
    galaxyPositions[i3 + 2] = z;

    // Color Logic: Central band is bright, edges are dark
    const distFromCenter = Math.abs(t) / (params.length / 2);
    const distFromAxis = r / params.thickness;

    let mixedColor;

    // Simulate Dust Lanes (Randomly make some particles very dark)
    const isDust = Math.random() < 0.2 && distFromAxis < 0.3 && Math.abs(t) < 40;

    if (isDust) {
        mixedColor = colorDust.clone().lerp(new THREE.Color('#000000'), Math.random());
    } else {
        mixedColor = colorCore.clone();
        if (distFromCenter < 0.4) {
            mixedColor.lerp(colorMid, distFromCenter * 2);
        } else {
            mixedColor.lerp(colorOuter, distFromCenter);
        }

        // Glow effect for the very center
        if (distFromCenter < 0.1 && distFromAxis < 0.2) {
            mixedColor.add(new THREE.Color('#ffffff').multiplyScalar(0.4));
        }
    }

    galaxyColors[i3] = mixedColor.r;
    galaxyColors[i3 + 1] = mixedColor.g;
    galaxyColors[i3 + 2] = mixedColor.b;
}

galaxyGeometry.setAttribute('position', new THREE.BufferAttribute(galaxyPositions, 3));
galaxyGeometry.setAttribute('color', new THREE.BufferAttribute(galaxyColors, 3));

const galaxyMaterial = new THREE.PointsMaterial({
    size: params.size,
    sizeAttenuation: true,
    depthWrite: false,
    map: circleTexture,
    blending: THREE.AdditiveBlending,
    vertexColors: true,
    transparent: true,
    opacity: 0.85
});

const galaxy = new THREE.Points(galaxyGeometry, galaxyMaterial);
scene.add(galaxy);

// --- Dense Background Starfield ---
const starCount = 8000;
const starGeometry = new THREE.BufferGeometry();
const starPositions = new Float32Array(starCount * 3);
for (let i = 0; i < starCount * 3; i++) {
    starPositions[i] = (Math.random() - 0.5) * 600;
}
starGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
const starMaterial = new THREE.PointsMaterial({
    size: 0.08, // Very small sharp stars
    color: 0xffffff,
    map: circleTexture,
    transparent: true,
    opacity: 0.5,
    sizeAttenuation: true,
    depthWrite: false
});
const starField = new THREE.Points(starGeometry, starMaterial);
scene.add(starField);

// --- Hazy Glow Layer (The "Nebula" part, kept subtle) ---
const fogCount = 600;
const fogGeometry = new THREE.BufferGeometry();
const fogPositions = new Float32Array(fogCount * 3);
const fogColors = new Float32Array(fogCount * 3);

for (let i = 0; i < fogCount; i++) {
    const i3 = i * 3;
    const t = (Math.random() - 0.5) * (params.length * 0.8);
    const r = Math.random() * 15;
    const angle = Math.random() * Math.PI * 2;

    const x = t;
    const y = Math.cos(angle) * r;
    const z = Math.sin(angle) * r;

    const angleTilt = Math.PI / 4;
    fogPositions[i3] = x * Math.cos(angleTilt) - y * Math.sin(angleTilt);
    fogPositions[i3 + 1] = x * Math.sin(angleTilt) + y * Math.cos(angleTilt);
    fogPositions[i3 + 2] = z;

    const fColor = new THREE.Color(params.midColor).lerp(new THREE.Color('#220011'), Math.random());
    fogColors[i3] = fColor.r;
    fogColors[i3 + 1] = fColor.g;
    fogColors[i3 + 2] = fColor.b;
}

fogGeometry.setAttribute('position', new THREE.BufferAttribute(fogPositions, 3));
fogGeometry.setAttribute('color', new THREE.BufferAttribute(fogColors, 3));

const fogMaterial = new THREE.PointsMaterial({
    size: 10,
    map: circleTexture,
    transparent: true,
    opacity: 0.03, // Very subtle haze
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    vertexColors: true
});
const fogLayer = new THREE.Points(fogGeometry, fogMaterial);
scene.add(fogLayer);

// --- Animation ---
let mouseX = 0, mouseY = 0;
let targetX = 0, targetY = 0;
const windowHalfX = window.innerWidth / 2;
const windowHalfY = window.innerHeight / 2;

document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX - windowHalfX);
    mouseY = (e.clientY - windowHalfY);
});

const clock = new THREE.Clock();

const animate = () => {
    const elapsedTime = clock.getElapsedTime();

    targetX = mouseX * 0.0002; // Slower mouse response for scale
    targetY = mouseY * 0.0002;

    // Movement: Slow drift along the galaxy axis
    galaxy.rotation.y = elapsedTime * 0.005;
    fogLayer.rotation.y = elapsedTime * 0.006;
    starField.rotation.y = elapsedTime * 0.002;

    // Movement tilt
    galaxy.rotation.x += 0.02 * (targetY - galaxy.rotation.x);
    galaxy.rotation.z += 0.02 * (targetX - galaxy.rotation.z);

    fogLayer.rotation.x = galaxy.rotation.x;
    fogLayer.rotation.z = galaxy.rotation.z;

    renderer.render(scene, camera);
    window.requestAnimationFrame(animate);
};

animate();

window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
