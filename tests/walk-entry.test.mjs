import {test} from 'node:test';import assert from 'node:assert/strict';import * as THREE from 'three';import {LocalCollisionWorld} from '../web/local-collision.js';
let resolveWalkEntry;try{({resolveWalkEntry}=await import('../web/walk-entry.js'))}catch{}
function fixture(ceiling=false){const g=new THREE.Group();const floor=new THREE.Mesh(new THREE.BoxGeometry(20,1,20));floor.position.y=10.5;g.add(floor);if(ceiling){const m=new THREE.Mesh(new THREE.BoxGeometry(20,1,20));m.position.y=12.2;g.add(m)}return new LocalCollisionWorld(g)}
test('landmark entry finds actual nearby floor and sets capsule height',()=>{assert.ok(resolveWalkEntry);const m=resolveWalkEntry(fixture(),new THREE.Vector3(0,11.05,0));assert.ok(Math.abs(m.feet.y-11.025)<.001);assert.ok(m.eye.y>12.6)});
test('landmark refuses missing floor rather than creating an invisible platform',()=>{assert.ok(resolveWalkEntry);assert.throws(()=>resolveWalkEntry(fixture(),new THREE.Vector3(50,11,50)),/바닥/)});
test('landmark refuses low ceiling',()=>{assert.ok(resolveWalkEntry);assert.throws(()=>resolveWalkEntry(fixture(true),new THREE.Vector3(0,11,0)),/공간/)});
