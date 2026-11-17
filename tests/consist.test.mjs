import test from 'node:test';import assert from 'node:assert/strict';import * as THREE from 'three';import * as sim from '../web/rail-simulation.js';import {createRollingStock} from '../web/rolling-stock.js';
const route={points:[[0,0,0],[0,0,100],[100,0,100]],dist:[0,100,200]};
test('each car samples the route and curves independently',()=>{assert.equal(typeof sim.consistPose,'function');let p=sim.consistPose(route,100,3,20,12);assert.equal(p.cars.length,3);assert.ok(p.cars[0].heading>1);assert.ok(p.cars[2].heading<.1);assert.equal(p.cars[1].d,100);});
test('endpoint centers keep formation on route without bunching',()=>{let a=sim.consistPose(route,0,3,20,12),b=sim.consistPose(route,200,3,20,12);assert.deepEqual(a.cars.map(x=>x.d),[46,26,6]);assert.deepEqual(b.cars.map(x=>x.d),[194,174,154]);assert.deepEqual(sim.consistPose(route,0,3,20,12),a);});
test('stock is articulated with finite skin weights and bounded draws',()=>{let s=createRollingStock({line:'uline'});let meshes=s.children.filter(x=>x.isSkinnedMesh);assert.equal(meshes.length,7);for(let m of meshes){assert.equal(m.skeleton.bones.length,2);assert.ok(m.geometry.attributes.skinWeight);let a=m.geometry.attributes.skinWeight;for(let i=0;i<a.count;i++)assert.equal(a.getX(i)+a.getY(i)+a.getZ(i)+a.getW(i),1);}});
import {clone as cloneSkeleton} from 'three/addons/utils/SkeletonUtils.js';
test('cloned consists deform independently using their own car bones',()=>{
 const base=createRollingStock({line:'uline'}),a=cloneSkeleton(base),b=cloneSkeleton(base);let am=a.children.find(o=>o.isSkinnedMesh),bm=b.children.find(o=>o.isSkinnedMesh);
 assert.notEqual(am.skeleton.bones[0],bm.skeleton.bones[0]);
 const before=new THREE.Vector3();am.getVertexPosition(0,before);am.skeleton.bones[0].position.x+=17;a.updateMatrixWorld(true);am.skeleton.update();let after=new THREE.Vector3();am.getVertexPosition(0,after);let unchanged=new THREE.Vector3();bm.getVertexPosition(0,unchanged);assert.ok(Math.abs(after.x-before.x-17)<1e-6);assert.ok(Math.abs(unchanged.x-before.x)<1e-6);
});
