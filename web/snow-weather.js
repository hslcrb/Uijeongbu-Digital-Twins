import * as THREE from 'three';
import {snowSettings,snowVolume} from './snow-state.js';

/** One reusable GPU particle pool. No per-frame geometry or texture allocation. */
export class SnowWeather {
 constructor({scene,camera,target,model}) {
  this.camera=camera;this.target=target;this.model=model;this.enabled=false;this.elapsed=0;this.roofClock=0;this.sheltered=false;
  this.ray=new THREE.Raycaster();this.up=new THREE.Vector3(0,1,0);this.hits=[];
  const seeds=new Float32Array(6000*3);
  for(let i=0;i<seeds.length;i++)seeds[i]=Math.random();
  this.geometry=new THREE.BufferGeometry();this.geometry.setAttribute('position',new THREE.BufferAttribute(seeds,3));
  this.material=new THREE.ShaderMaterial({transparent:true,depthWrite:false,depthTest:true,
   uniforms:{time:{value:0},eye:{value:new THREE.Vector3()},radius:{value:26},height:{value:32},flakeSize:{value:.13},pixelHeight:{value:800}},
   vertexShader:`uniform float time,radius,height,flakeSize,pixelHeight;uniform vec3 eye;varying float opacity;
    #include <common>
    #include <logdepthbuf_pars_vertex>
    void main(){vec3 p=position;float speed=.65+p.z*.75;
     vec3 world=eye+vec3((fract(p.x+time*.009)-.5)*radius*2.,(fract(p.y-time*speed/height)-.35)*height,(p.z-.5)*radius*2.);
     world.x+=sin(time*.8+p.y*80.)*.4;world.z+=cos(time*.65+p.x*70.)*.3;
     vec4 mvPosition=modelViewMatrix*vec4(world,1.);gl_Position=projectionMatrix*mvPosition;
     gl_PointSize=clamp(flakeSize*pixelHeight/max(1.,-mvPosition.z),1.3,9.);
     opacity=(1.-smoothstep(radius*.2,radius*1.4,length(world-eye)))*.8;
     #include <logdepthbuf_vertex>
    }`,
   fragmentShader:`varying float opacity;
    #include <logdepthbuf_pars_fragment>
    void main(){
     #include <logdepthbuf_fragment>
     float d=length(gl_PointCoord-.5);if(d>.5)discard;
     gl_FragColor=vec4(.92,.96,1.,opacity*(1.-smoothstep(.12,.5,d)));
    }`
  });
  this.points=new THREE.Points(this.geometry,this.material);this.points.frustumCulled=false;this.points.visible=false;this.points.name='Weather snowfall';scene.add(this.points);
 }
 set(mode,high=false){this.enabled=mode==='snow';this.geometry.setDrawRange(0,snowSettings(mode,high).count);this.points.visible=this.enabled&&!this.sheltered;this.roofClock=1;}
 update(dt,pixelHeight){
  if(!this.enabled)return;
  const step=Math.max(0,Math.min(.05,dt));this.elapsed+=step;this.roofClock+=step;
  const distance=this.camera.position.distanceTo(this.target());const v=snowVolume(distance);
  const u=this.material.uniforms;u.time.value=this.elapsed;u.eye.value.copy(this.camera.position);u.radius.value=v.radius;u.height.value=v.height;u.flakeSize.value=v.size;u.pixelHeight.value=pixelHeight;
  // Hide the local snow field beneath a roof. Depth testing occludes exterior flakes.
  // This is a visual weather effect, not a snow-accumulation simulation.
  if(this.roofClock>=.5){this.roofClock=0;this.hits.length=0;const root=this.model();
   this.sheltered=false;
   if(root){this.ray.set(this.camera.position,this.up);this.ray.far=80;this.ray.intersectObject(root,true,this.hits);
    this.sheltered=this.hits.some(h=>h.distance>.2&&!/tree|leaf|foliage|light|lamp/i.test(h.object.name));}
  }
  this.points.visible=!this.sheltered;
 }
 dispose(){this.points.removeFromParent();this.geometry.dispose();this.material.dispose();}
}
