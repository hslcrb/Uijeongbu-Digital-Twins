import assert from 'node:assert/strict';
import {CityStream} from '../web/city-stream.js';
let callbacks=[],active=0,peak=0,disposed=0;
const scene={add(){},remove(){}};
const loader={load(url,ok){
 active++;peak=Math.max(peak,active);
 callbacks.push(()=>{
  active--;
  const node={name:'',traverse(fn){fn({isMesh:true,geometry:{dispose(){disposed++}},material:{dispose(){}}});}};
  ok({scene:node});
 });
}};
let target={x:0,y:0,z:0};const camera={position:{x:0,y:50,z:0}};
const s=new CityStream({scene,loader,camera,target:()=>target,onChange(){},maxResident:4});s.base=new URL('https://example.test/city/');s.tiles=Array.from({length:20},(_,i)=>({id:String(i),url:`tiles/${i}.glb`,center:[i*1000,0,0]}));
s.update(true);while(callbacks.length)callbacks.shift()();assert(peak<=2);assert(s.loaded.size<=4);const before=[...s.loaded.keys()];target={x:15000,y:0,z:0};s.update(true);while(callbacks.length)callbacks.shift()();assert(s.loaded.size<=4);assert(disposed>0);assert(!s.loaded.has(before[0]));camera.position.y=14000;target={x:9500,y:0,z:0};s.update(true);while(callbacks.length)callbacks.shift()();assert.equal(s.loaded.size,20);assert(peak<=2);console.log(JSON.stringify({pass:true,peakConcurrent:peak,nearResidentMax:4,wideResident:s.loaded.size,disposed}));
// Real tile extent, rather than a fixed grid margin, participates in selection.
const s2=new CityStream({scene,loader,camera:{position:{x:0,y:0,z:0}},target:()=>({x:0,y:0,z:0}),onChange(){},maxResident:4});s2.base=s.base;s2.tiles=[{id:'long',url:'tiles/long.glb',center:[3900,0,0],radius:2000}];s2.update(true);while(callbacks.length)callbacks.shift()();assert(s2.loaded.has('long'));console.log('Actual-bounds radius selection PASS');
