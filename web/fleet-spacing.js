import {consistsConflict} from './fleet-capsules.js';
// Conservative game spacing, NOT a railway signalling or braking model.
import {fleetState} from './fleet-control.js';
import {consistPose} from './rail-simulation.js';
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[2]-b[2]);
export function sweptSeparation(a0,a1,b0,b1){const x=a0[0]-b0[0],z=a0[2]-b0[2],vx=a1[0]-a0[0]-b1[0]+b0[0],vz=a1[2]-a0[2]-b1[2]+b0[2],n=vx*vx+vz*vz,t=n?Math.max(0,Math.min(1,-(x*vx+z*vz)/n)):0;return Math.hypot(x+vx*t,z+vz*t);}
function center(layer,t,d){const p=consistPose(layer.route,d,t.userData.carCount,t.userData.carSpacing,t.userData.bogieSpan).anchor;return [p[0],layer.group.position.y,p[2]];}
export function advanceFleet(layers,time,delta,realDelta){const entries=[];
 for(const layer of layers)for(const [i,t] of layer.trains.entries()){
  const m=t.userData.manualState,previous=fleetState(layer,t,i,time-delta),d0=previous.d;
  if(m)m.update(realDelta);
  const next=fleetState(layer,t,i,time),length=(t.userData.carCount-1)*t.userData.carSpacing+(t.userData.carSpacing||20);
  entries.push({layer,t,i,m,d0,previous,next,p0:center(layer,t,d0),p1:center(layer,t,next.d),radius:length/2+6,held:false,hidden:false});
 }
 // A player-occupied train receives priority over initially overlapping automatic spawns.
 entries.sort((a,b)=>Number(!!b.m)-Number(!!a.m));
 for(let pass=0;pass<entries.length;pass++){let changes=0;
 for(let i=0;i<entries.length;i++)for(let j=0;j<i;j++){
  const a=entries[i],b=entries[j];if(a.hidden||b.hidden||Math.abs(a.p0[1]-b.p0[1])>4)continue;
  const gap=a.radius+b.radius,old=distance(a.p0,b.p0),next=distance(a.p1,b.p1);
  if(old<gap-.01&&consistsConflict({...a,held:true},{...b,held:true})){
   // Suppress a conflicting auto spawn instead of displaying interpenetrating trains.
   if(!a.m){a.hidden=true;a.held=true;a.p1=a.p0;changes++;continue;}
   if(next>old+.001)continue; // permit escape from a pre-existing occupied overlap
  }
  if(sweptSeparation(a.p0,a.p1,b.p0,b.p1)<gap&&consistsConflict(a,b)){if(!a.m){a.hidden=true;a.held=true;a.p1=a.p0;changes++;continue;}if(!a.held||!b.held)changes++;a.held=true;b.held=true;a.p1=a.p0;b.p1=b.p0;}
 }
 if(!changes)break;
 }
 for(const e of entries){const {t,m}=e;t.userData.safetyHeld=e.held;t.userData.safetyHidden=e.hidden;t.visible=!e.hidden;
  if(e.held){if(m){m.d=e.d0;m.v=0;m.power=0;}else t.userData.timeOffset=(t.userData.timeOffset||0)-delta;}
 }
 return entries;
}
