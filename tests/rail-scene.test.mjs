import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import * as THREE from 'three';import {RailNetwork} from '../web/rail-network.js';
// Minimal DOM fixture; geometry and simulator run through actual Three.js.
class Element{constructor(){this.children=[];this.nodes={};this.value='0'}append(x){this.children.push(x)}querySelector(id){return this.nodes[id]??=(new Element())}add(x){this.children.push(x)}replaceChildren(){this.children=[]}setAttribute(){}getContext(){return {fillRect(){},fillText(){}}}}
globalThis.document={createElement:()=>new Element(),body:new Element(),querySelector:()=>new Element()};globalThis.Option=class{constructor(text,value){Object.assign(this,{text,value})}};
globalThis.fetch=async()=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(new URL('../web/rail/network.json',import.meta.url)))});
test('all actual route scenes build, switch, animate and dispose',async()=>{const camera=new THREE.PerspectiveCamera(),controls={target:new THREE.Vector3(),update(){}};let r=new RailNetwork({camera,controls,schedule(){},stopWalking(){}});await r.init();r.set(true);for(let i=0;i<r.routes.length;i++){r.choose(i);r.update(1);assert.ok(r.group.children.length>r.route.stations.length);assert.ok(r.trains.length<=64);assert.ok(r.trains.every(t=>t.position.toArray().every(Number.isFinite)));r.stationView();assert.ok(camera.position.toArray().every(Number.isFinite));}r.set(false);assert.equal(r.panel.hidden,true);r.clear();assert.equal(r.group.children.length,0)});

import {positionAt} from '../web/rail-simulation.js';
test('platforms remain eight meters perpendicular to each station track',async()=>{
 const camera=new THREE.PerspectiveCamera(),controls={target:new THREE.Vector3(),update(){}};
 const r=new RailNetwork({camera,controls,schedule(){},stopWalking(){}});await r.init();
 for(let route=0;route<r.routes.length;route++){
  r.choose(route);const platforms=r.group.children.filter(o=>o.geometry?.parameters?.width===8);
  assert.equal(platforms.length,r.route.stations.length);
  platforms.forEach((platform,i)=>{const p=positionAt(r.route,r.route.stations[i].d),dx=platform.position.x-p.position[0],dz=platform.position.z-p.position[2];assert.ok(Math.abs(Math.hypot(dx,dz)-8)<1e-6);assert.ok(Math.abs(dx*Math.sin(p.heading)+dz*Math.cos(p.heading))<1e-6,'platform offset must be perpendicular, not along track');});
 }
 r.clear();
});
