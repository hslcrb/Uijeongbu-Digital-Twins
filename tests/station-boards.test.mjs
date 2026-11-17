import test from 'node:test';
import assert from 'node:assert/strict';
import {prepareRoute} from '../web/rail-simulation.js';
import {boardRows,StationBoards} from '../web/station-boards.js';
import * as THREE from 'three';
const route=prepareRoute({name:'시험',points:[[127.046,37.74],[127.046,37.738],[127.046,37.736]],stations:[{name:'북쪽',lon:127.046,lat:37.74},{name:'의정부',lon:127.046,lat:37.738},{name:'남쪽',lon:127.046,lat:37.736}]});
test('both directional boards use exact shared fleet spacing and dwell state',()=>{let layers=[{route,count:2}],t=route.legs.find(l=>l.i===1&&l.j===2).start;let rows=boardRows(layers,t,1);assert.equal(rows[0].destination,'남쪽');assert.equal(rows[0].seconds,0);assert.equal(rows[0].status,'정차 중');assert.equal(boardRows(layers,t,-1)[0].destination,'북쪽');assert.notEqual(boardRows(layers,t+30,1)[0].seconds,rows[0].seconds)});
test('missing station data is explicitly unavailable, not invented',()=>{assert.deepEqual(boardRows([],0,1),[])});
test('two world screens throttle texture uploads and dispose',()=>{let draws=0;const ctx={fillRect(){},fillText(){draws++}};const canvasFactory=()=>({width:0,height:0,getContext:()=>ctx});const scene=new THREE.Scene();let b=new StationBoards({scene,canvasFactory});assert.equal(b.screens.length,2);b.update(0,[{route,count:2}]);let n=draws;b.update(.2,[{route,count:2}]);assert.equal(draws,n);b.update(1,[{route,count:2}]);assert.ok(draws>n);assert.equal(b.screens[0].position.z,-59.62);b.dispose();assert.equal(scene.children.length,0)});
