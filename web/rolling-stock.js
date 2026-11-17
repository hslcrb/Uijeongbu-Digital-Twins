import * as THREE from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
// Original procedural approximation, not a scanned manufacturer's model.
export function createRollingStock(route={}){
 const light=route.line==='uline',count=light?2:10,w=light?2.08:3.12,l=light?13.7:19.5,gap=light?.6:.6;
 const colors={body:0xc6cdd2,glass:0x132c3a,blue:light?0x28883e:0x164b8b,red:light?0xda3e36:0xd44848,dark:0x343b40,roof:0xe0e4e5,white:0xfff2cc};
 const buckets=Object.fromEntries(Object.keys(colors).map(k=>[k,[]])),parts={windows:0,doors:0,wheels:0};let pantographs=0;
 function box(k,x,y,z,sx,sy,sz,rx=0,ry=0,rz=0){let g=new THREE.BoxGeometry(sx,sy,sz);g.rotateX(rx);g.rotateY(ry);g.rotateZ(rz);g.translate(x,y,z);buckets[k].push(g)}
 function wheel(x,y,z){let g=new THREE.CylinderGeometry(light?.28:.43,light?.28:.43,.18,10);g.rotateZ(Math.PI/2);g.translate(x,y,z);buckets.dark.push(g);parts.wheels++}
 for(let c=0;c<count;c++){
  const z=-c*(l+gap),bodyY=light?1.95:2.35,h=light?2.45:2.8,top=bodyY+h/2;
  box('body',0,bodyY,z,w,h,l);box(light?'red':'roof',0,top+.12,z,w*.96,.24,l-.4);box('dark',0,light?.6:.8,z,w*.8,.55,l-2);
  for(let side of [-1,1]){
   box('blue',side*(w/2+.015),bodyY-.65,z,.035,.34,l-.3);
   const doors=light?3:4;for(let d=0;d<doors;d++){
    const dz=z-l*.36+d*(l*.72/(doors-1));box('roof',side*(w/2+.03),bodyY-.1,dz,.04,h-.2,1.3);box('dark',side*(w/2+.055),bodyY-.1,dz,.025,h-.2,.025);
    for(let s of [-1,1])box('glass',side*(w/2+.06),bodyY+.35,dz+s*.32,.025,.85,.47);parts.doors++;parts.windows+=2;
   }
   for(let j=0;j<doors-1;j++){const dz=z-l*.36+(j+.5)*(l*.72/(doors-1));box('glass',side*(w/2+.035),bodyY+.4,dz,.04,.95,light?1.5:2.1);parts.windows++;}
  }
  for(let bz of [-l*.31,l*.31]){box('dark',0,.7,z+bz,w*.78,.35,2);for(let axle of [-.68,.68])for(let side of [-1,1])wheel(side*w*.36,.63,z+bz+axle);}
  box('roof',0,top+.3,z-l*.2,w*.66,.36,light?1.8:3.1);box('roof',0,top+.3,z+l*.2,w*.66,.36,light?1.8:3.1);
  if(!light&&[1,4,7].includes(c)){pantographs++;box('dark',0,top+.38,z,.95,.12,1.6);for(let s of [-1,1]){box('dark',0,top+.77,z+s*.35,.055,.85,.055,s*.6);box('dark',0,top+1.1,z+s*.35,.055,.65,.055,-s*.65)}box('dark',0,top+1.35,z,1.45,.065,.15);}
  if(c<count-1)box('dark',0,bodyY,z-l/2-gap/2,w*.65,h*.78,gap);
  for(let end of c===0?[1]:c===count-1?[-1]:[]){let ez=z+end*(l/2+.035);
   box('blue',0,bodyY,ez,w*.94,h,.09);box('glass',0,bodyY+(light?.2:.52),ez+end*.06,w*.83,light?1.85:1.02,.05);box('red',0,bodyY-.48,ez+end*.06,w*.9,.38,.05);
   box('dark',0,top-.18,ez+end*.08,w*.58,.23,.05);box('white',0,top-.18,ez+end*.11,w*.3,.07,.025);
   for(let s of [-1,1]){box('white',s*w*.32,bodyY-.83,ez+end*.09,.26,.17,.04);box('dark',s*w*.19,bodyY+.26,ez+end*.1,.035,.57,.035,0,0,s*.3)}
   box('dark',0,.7,ez+end*.3,.35,.22,.5);
  }
 }
 let train=new THREE.Group();for(let [k,geometries] of Object.entries(buckets)){if(!geometries.length)continue;let geometry=mergeGeometries(geometries);for(let g of geometries)g.dispose();train.add(new THREE.Mesh(geometry,new THREE.MeshLambertMaterial({color:colors[k]})));}
 train.userData={carCount:count,pantographs,parts,modelLabel:light?'VAL208 참고 2량 근사 모델':'코레일 통근형 참고 10량 근사 모델'};return train;
}
