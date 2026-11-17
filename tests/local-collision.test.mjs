import {test} from 'node:test';import assert from 'node:assert/strict';import * as THREE from 'three';
let LocalCollisionWorld;try{({LocalCollisionWorld}=await import('../web/local-collision.js'))}catch{}
test('local collision excludes distant geometry but preserves large ground triangles',()=>{assert.ok(LocalCollisionWorld);const group=new THREE.Group();for(let i=0;i<100;i++){const mesh=new THREE.Mesh(new THREE.BoxGeometry(2,4,2));mesh.position.set(i*10,2,0);group.add(mesh)}const ground=new THREE.Mesh(new THREE.BoxGeometry(4000,1,4000));ground.position.y=-.5;group.add(ground);const world=new LocalCollisionWorld(group);world.ensure(new THREE.Vector3(0,0,0));assert.ok(world.triangleCount<150);assert.ok(world.rayIntersect(new THREE.Ray(new THREE.Vector3(5,5,0),new THREE.Vector3(0,-1,0))));world.ensure(new THREE.Vector3(100,0,0));assert.equal(world.center.x,100)});


test('collision budgets reject dense locations instead of building an unbounded tree',()=>{
 const model=new THREE.Group();model.add(new THREE.Mesh(new THREE.BoxGeometry(2,2,2),new THREE.MeshBasicMaterial()));
 const world=new LocalCollisionWorld(model,{maxTriangles:1});
 assert.throws(()=>world.ensure(new THREE.Vector3()),/충돌 면/);
 const scanned=new LocalCollisionWorld(model,{maxScanned:1});
 assert.throws(()=>scanned.ensure(new THREE.Vector3()),/충돌 계산/);
});
