import test from 'node:test';import assert from 'node:assert/strict';
import {project,prepareRoute,trainState,arrivals} from '../web/rail-simulation.js';
test('projection matches station origin',()=>assert.deepEqual(project([127.046,37.738]),[0,0,0]));
const raw={id:'t',points:[[127.046,37.738],[127.047,37.738],[127.048,37.738]],stations:[{name:'A',lon:127.046,lat:37.738},{name:'B',lon:127.047,lat:37.738},{name:'C',lon:127.048,lat:37.738}]};
test('train stops at each station and turns without teleport',()=>{let r=prepareRoute(raw,{speed:10,dwell:20});assert.equal(trainState(r,5).station,'A');assert.equal(trainState(r,30).station,'B');assert.equal(trainState(r,r.oneWay+5).station,'C');assert.equal(trainState(r,r.period+5).station,'A');});
test('arrival board returns sorted nonnegative times',()=>{let r=prepareRoute(raw,{speed:10,dwell:20});let a=arrivals(r,1,12,30);assert.ok(a.length);assert.ok(a.every(x=>x.seconds>=0));assert.ok(a.every((x,i)=>i===0||a[i-1].seconds<=x.seconds));});
import fs from 'node:fs';
test('all sourced routes have valid endpoints, monotonic stops and finite simulation',()=>{const data=JSON.parse(fs.readFileSync(new URL('../web/rail/network.json',import.meta.url)));assert.equal(data.routes.length,6);for(const raw of data.routes){const r=prepareRoute(raw);assert.ok(r.stations.every(s=>s.snapError<50));assert.ok(r.period>0);for(let t=0;t<r.period;t+=73){const x=trainState(r,t);assert.ok(x.position.every(Number.isFinite));assert.ok(Number.isFinite(x.heading));}assert.ok(Math.abs(r.stations[0].d)<100);assert.ok(r.stations.at(-1).d<=r.dist.at(-1))}});
