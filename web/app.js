import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';
const status=document.querySelector('#status'),poster=document.querySelector('#poster');
const modes={day:{sky:0xb5d0db,fog:0xb5d0db,sun:0xfff1d4,intensity:3.4,ambient:2.1,exposure:1},sunset:{sky:0x9d8383,fog:0xb69688,sun:0xffb16b,intensity:2.2,ambient:1.5,exposure:1},night:{sky:0x152434,fog:0x203247,sun:0x9cb8dc,intensity:.5,ambient:.9,exposure:1.25}};
let renderer,scene,camera,controls,model,box,center,size,hemi,sun,raf=0,auto=false,high=false,dirty=true,last=0,nightLights=[];
function schedule(){dirty=true;if(!raf&&!document.hidden)raf=requestAnimationFrame(draw)}
function draw(t){raf=0;if(t-last<33&&auto){schedule();return}last=t;controls?.update();if(renderer&&scene&&camera)renderer.render(scene,camera);dirty=false;if(auto)schedule()}
function resize(){if(!renderer)return;renderer.setPixelRatio(Math.min(devicePixelRatio,high?2:1.25));renderer.setSize(innerWidth,innerHeight);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();schedule()}
function preset(close=false){if(!camera||!center)return;controls.target.copy(center);const d=Math.max(size.x,size.z)*(close?.35:.7);camera.position.set(center.x+d*.7,center.y+d*.85,center.z+d*.85);controls.minDistance=.3;controls.maxDistance=Math.max(size.x,size.z)*2.3;camera.near=.05;camera.far=Math.max(size.x,size.z)*6;camera.updateProjectionMatrix();controls.update();schedule()}
function mode(key){const m=modes[key];if(!scene)return;scene.background=new THREE.Color(m.sky);scene.fog=new THREE.Fog(m.fog,Math.max(size.x,size.z)*.9,Math.max(size.x,size.z)*3.5);sun.color.setHex(m.sun);sun.intensity=m.intensity;hemi.intensity=m.ambient;renderer.toneMappingExposure=m.exposure;for(const l of nightLights)l.visible=key==='night';document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===key));schedule()}
try{
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:'high-performance'});renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.shadowMap.enabled=false;document.querySelector('#canvas').append(renderer.domElement);
 scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(45,innerWidth/innerHeight,.5,5000);controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=false;controls.maxPolarAngle=Math.PI*.49;controls.autoRotateSpeed=.4;controls.addEventListener('change',schedule);
 hemi=new THREE.HemisphereLight(0xe4f0ff,0x696552,2.1);scene.add(hemi);sun=new THREE.DirectionalLight(0xfff1d4,3.4);sun.position.set(-400,800,300);scene.add(sun);
 const draco=new DRACOLoader();draco.setDecoderPath('/vendor/addons/libs/draco/gltf/');draco.setWorkerLimit(2);const loader=new GLTFLoader();loader.setDRACOLoader(draco);
 loader.load('/assets/station.glb',gltf=>{model=gltf.scene;model.traverse(o=>{if(o.isLight){o.intensity=Math.min(o.intensity,5);nightLights.push(o);o.visible=false}if(o.isMesh){o.frustumCulled=true;o.castShadow=false;o.receiveShadow=false;}});scene.add(model);box=new THREE.Box3().setFromObject(model);center=box.getCenter(new THREE.Vector3());size=box.getSize(new THREE.Vector3());preset();resize();mode('day');poster.hidden=true;status.textContent='3D · 의정부역 주변';window.__twinReady={meshes:0,bounds:size.toArray()};model.traverse(o=>{if(o.isMesh)window.__twinReady.meshes++});draco.dispose();},e=>{status.textContent=e.total?`3D 불러오는 중 ${Math.round(e.loaded/e.total*100)}%`:'3D 불러오는 중…'},err=>{console.error(err);status.textContent='3D를 불러오지 못했습니다. 렌더 사진을 표시합니다.';document.body.classList.add('fallback');});
 resize();schedule();
}catch(err){console.error(err);status.textContent='이 브라우저는 3D를 지원하지 않습니다. 렌더 사진을 표시합니다.';document.body.classList.add('fallback')}
document.querySelector('#home').onclick=()=>preset();document.querySelector('#station').onclick=()=>preset(true);
document.querySelector('#rotate').onclick=e=>{auto=!auto;if(controls)controls.autoRotate=auto;e.currentTarget.setAttribute('aria-pressed',auto);schedule()};document.querySelector('#quality').onclick=e=>{high=!high;e.currentTarget.setAttribute('aria-pressed',high);resize()};document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>mode(b.dataset.mode));
const about=document.querySelector('#about');document.querySelector('#info').onclick=()=>about.showModal();document.querySelector('#close').onclick=()=>about.close();addEventListener('resize',resize);document.addEventListener('visibilitychange',()=>{if(document.hidden&&raf){cancelAnimationFrame(raf);raf=0}else schedule()});

// Translate camera and orbit target together: interior/exterior remain one space.
addEventListener('keydown',e=>{
 if(!camera||!controls||document.querySelector('dialog[open]')||e.ctrlKey||e.metaKey||e.altKey)return;
 const k=e.key.toLowerCase();if(!['w','a','s','d','q','e','arrowup','arrowdown','arrowleft','arrowright'].includes(k))return;
 e.preventDefault();const forward=new THREE.Vector3();camera.getWorldDirection(forward);forward.y=0;forward.normalize();
 const right=new THREE.Vector3().crossVectors(forward,new THREE.Vector3(0,1,0)).normalize(),delta=new THREE.Vector3();
 if(k==='w'||k==='arrowup')delta.add(forward);if(k==='s'||k==='arrowdown')delta.sub(forward);
 if(k==='d'||k==='arrowright')delta.add(right);if(k==='a'||k==='arrowleft')delta.sub(right);
 if(k==='q')delta.y-=1;if(k==='e')delta.y+=1;delta.multiplyScalar(e.shiftKey?8:1.5);
 camera.position.add(delta);controls.target.add(delta);controls.update();schedule();
});
