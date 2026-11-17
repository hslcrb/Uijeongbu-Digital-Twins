import * as THREE from 'three';
import {SnowWeather} from './snow-weather.js';
import {Walking} from './walking.js';
import {CityStream} from './city-stream.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';
const status=document.querySelector('#status'),poster=document.querySelector('#poster');
const modes={day:{sky:0xb5d0db,fog:0xb5d0db,sun:0xfff1d4,intensity:3.4,ambient:2.1,exposure:1},sunset:{sky:0x9d8383,fog:0xb69688,sun:0xffb16b,intensity:2.2,ambient:1.5,exposure:1},night:{sky:0x152434,fog:0x203247,sun:0x9cb8dc,intensity:.5,ambient:.9,exposure:1.25}};
let renderer,scene,camera,controls,model,box,center,size,hemi,sun,raf=0,auto=false,high=false,dirty=true,last=0,nightLights=[],roomGlows=[],streetGlows=[],city,walking,snow;
function schedule(){dirty=true;if(!raf&&!document.hidden)raf=requestAnimationFrame(draw)}
function updateClipPlanes(){if(!camera||!box)return;const distance=camera.position.distanceTo(center),radius=size.length()*.5;const near=walking?.active ? .05 : Math.max(.08,Math.min(2,distance/500));const far=Math.max(200,distance+radius*1.5,city?24000:0);if(Math.abs(camera.near-near)>.01||Math.abs(camera.far-far)>1){camera.near=near;camera.far=far;camera.updateProjectionMatrix()}}
function draw(t){raf=0;if(t-last<33&&(auto||walking?.active||snow?.enabled)){schedule();return}const delta=last?Math.min(.05,Math.max(0,(t-last)/1000)):0;last=t;if(walking?.active)walking.update(delta);else controls?.update();snow?.update(delta,renderer?.domElement.height||innerHeight);city?.update();if(city)window.__cityStream=city.metrics;updateClipPlanes();if(renderer&&scene&&camera)renderer.render(scene,camera);dirty=false;if(auto||walking?.active||snow?.enabled)schedule()}
function resize(){if(!renderer)return;renderer.setPixelRatio(Math.min(devicePixelRatio,high?2:1.25));renderer.setSize(innerWidth,innerHeight);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();schedule()}
function preset(close=false){walking?.stop();if(!camera||!center)return;controls.target.copy(center);const d=Math.max(size.x,size.z)*(close?.35:.7);camera.position.set(center.x+d*.7,center.y+d*.85,center.z+d*.85);controls.minDistance=.3;controls.maxDistance=24000;camera.near=.05;camera.far=Math.max(size.x,size.z)*6;camera.updateProjectionMatrix();controls.update();schedule()}
function mode(key){const m=modes[key];if(!scene||!size)return;scene.background=new THREE.Color(m.sky);scene.fog=new THREE.Fog(m.fog,2000,22000);sun.color.setHex(m.sun);sun.intensity=m.intensity;hemi.intensity=m.ambient;renderer.toneMappingExposure=m.exposure;for(const l of nightLights)l.visible=key==='night';for(const m of roomGlows)m.emissiveIntensity=key==='night'?1.8:key==='sunset'?.63:0;for(const m of streetGlows)m.emissiveIntensity=key==='night'?5:key==='sunset'?1.5:.05;document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===key));schedule()}
try{
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,reversedDepthBuffer:true,logarithmicDepthBuffer:true,powerPreference:'high-performance'});renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.shadowMap.enabled=false;document.querySelector('#canvas').append(renderer.domElement);
 scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(45,innerWidth/innerHeight,.5,5000);controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=false;controls.maxPolarAngle=Math.PI;controls.autoRotateSpeed=.4;controls.addEventListener('change',schedule);
 hemi=new THREE.HemisphereLight(0xe4f0ff,0x696552,2.1);scene.add(hemi);sun=new THREE.DirectionalLight(0xfff1d4,3.4);sun.position.set(-400,800,300);scene.add(sun);
 snow=new SnowWeather({scene,camera,target:()=>controls.target,model:()=>model});
 const draco=new DRACOLoader();draco.setDecoderPath('/vendor/addons/libs/draco/gltf/');draco.setWorkerLimit(2);const loader=new GLTFLoader();loader.setDRACOLoader(draco);
 loader.load('/assets/station.glb',gltf=>{model=gltf.scene;model.traverse(o=>{if(o.isLight){o.intensity=Math.min(o.intensity,5);nightLights.push(o);o.visible=false}if(o.isMesh){o.frustumCulled=true;o.castShadow=false;o.receiveShadow=false;
for(const mat of (Array.isArray(o.material)?o.material:[o.material])){
 if(mat?.name==='Street lamp'){mat.emissive.setRGB(1,.72,.43);if(!streetGlows.includes(mat))streetGlows.push(mat);}
 const match=mat?.name?.match(/^Room glow ([0-3])/);
 if(match){const i=Number(match[1]);if(i<3){mat.emissive.setRGB(...[[1,.65,.32],[.65,.8,1],[1,.92,.78]][i]);if(!roomGlows.includes(mat))roomGlows.push(mat)}mat.emissiveIntensity=0;}
}}});scene.add(model);box=new THREE.Box3().setFromObject(model);center=box.getCenter(new THREE.Vector3());size=box.getSize(new THREE.Vector3());preset();resize();mode('day');walking=new Walking({model,camera,canvas:renderer.domElement,controls,onChange:schedule});poster.hidden=true;status.textContent='3D · 의정부역 주변';window.__twinReady={meshes:0,bounds:size.toArray(),depthMode:renderer.capabilities.reversedDepthBuffer?'reversed':'logarithmic'};model.traverse(o=>{if(o.isMesh)window.__twinReady.meshes++});city=new CityStream({scene,loader,camera,target:()=>controls.target,onChange:schedule,maxResident:devicePixelRatio>1?32:48});city.init().then(()=>schedule()).catch(e=>console.warn(e));},e=>{status.textContent=e.total?`3D 불러오는 중 ${Math.round(e.loaded/e.total*100)}%`:'3D 불러오는 중…'},err=>{console.error(err);status.textContent='3D를 불러오지 못했습니다. 렌더 사진을 표시합니다.';document.body.classList.add('fallback');});
 resize();schedule();
}catch(err){console.error(err);status.textContent='이 브라우저는 3D를 지원하지 않습니다. 렌더 사진을 표시합니다.';document.body.classList.add('fallback')}
document.querySelector('#home').onclick=()=>preset();document.querySelector('#city').onclick=()=>{walking?.stop();if(!controls||!camera)return;controls.target.set(700,0,-3500);camera.position.set(8500,14000,10500);controls.update();city?.update(true);schedule()};document.querySelector('#station').onclick=()=>preset(true);
document.querySelector('#rotate').onclick=e=>{auto=!auto;if(controls)controls.autoRotate=auto;e.currentTarget.setAttribute('aria-pressed',auto);schedule()};document.querySelector('#quality').onclick=e=>{high=!high;snow?.set(document.querySelector('#weather').value,high);e.currentTarget.setAttribute('aria-pressed',high);resize()};document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>mode(b.dataset.mode));
const about=document.querySelector('#about');document.querySelector('#info').onclick=()=>about.showModal();document.querySelector('#close').onclick=()=>about.close();addEventListener('resize',resize);document.addEventListener('visibilitychange',()=>{if(document.hidden&&raf){cancelAnimationFrame(raf);raf=0}else schedule()});

// Translate camera and orbit target together: interior/exterior remain one space.
addEventListener('keydown',e=>{
 if(walking?.active||walking?.selecting||!camera||!controls||document.querySelector('dialog[open]')||e.ctrlKey||e.metaKey||e.altKey)return;
 const k=e.key.toLowerCase();if(!['w','a','s','d','q','e','arrowup','arrowdown','arrowleft','arrowright'].includes(k))return;
 e.preventDefault();const forward=new THREE.Vector3();camera.getWorldDirection(forward);forward.y=0;forward.normalize();
 const right=new THREE.Vector3().crossVectors(forward,new THREE.Vector3(0,1,0)).normalize(),delta=new THREE.Vector3();
 if(k==='w'||k==='arrowup')delta.add(forward);if(k==='s'||k==='arrowdown')delta.sub(forward);
 if(k==='d'||k==='arrowright')delta.add(right);if(k==='a'||k==='arrowleft')delta.sub(right);
 if(k==='q')delta.y-=1;if(k==='e')delta.y+=1;delta.multiplyScalar(e.shiftKey?8:1.5);
 camera.position.add(delta);controls.target.add(delta);controls.update();schedule();
});

document.querySelector('#weather').addEventListener('change',e=>{snow?.set(e.target.value,high);schedule()});
