import * as THREE from 'three';
// Same loop, fleet size and simulation clock as the visible trains. No live API.
export function boardRows(layers,time,direction){
 const rows=[];
 for(const {route:r,count} of layers){
  if(!r||!count)continue;
  const index=r.stations.findIndex(s=>s.name==='의정부');if(index<0)continue;
  const spacing=r.period/count;
  for(let train=0;train<count;train++){
   const phase=((time+train*spacing)%r.period+r.period)%r.period;
   for(const l of r.legs){
    if(l.i!==index||Math.sign(r.stations[l.j].d-r.stations[l.i].d)!==direction)continue;
    const stopped=phase+1e-9>=l.start&&phase<l.depart-1e-9;
    rows.push({train,route:r.id||r.name,destination:r.stations[direction>0?r.stations.length-1:0].name,seconds:stopped?0:(l.start-phase+r.period)%r.period,status:stopped?'정차 중':'도착 예정'});
   }
  }
 }
 return rows.sort((a,b)=>a.seconds-b.seconds).slice(0,2);
}
export class StationBoards{
 constructor({scene,canvasFactory=()=>document.createElement('canvas')}){
  this.scene=scene;this.lastSecond=null;this.lastLayers=null;this.screens=[];this.canvases=[];
  // build_interior.py ±6,2.8,3.55 + append_interior offset 2,57,11.
  // Front faces point towards concourse entry (+Z in glTF Y-up coordinates).
  for(const x of [-4,8]){
   const canvas=canvasFactory();canvas.width=1024;canvas.height=432;
   const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;
   const mesh=new THREE.Mesh(new THREE.PlaneGeometry(2.4,1),new THREE.MeshBasicMaterial({map:texture,toneMapped:false}));
   mesh.name='Live simulated concourse departure board';mesh.position.set(x,14.55,-59.62);
   scene.add(mesh);this.screens.push(mesh);this.canvases.push(canvas);
  }
 }
 update(time,layers=[]){
  const second=Math.floor(time),signature=layers.map(l=>`${l.route?.id||l.route?.name}:${l.count}`).join('|');if(second===this.lastSecond&&signature===this.lastLayers)return;
  this.lastSecond=second;this.lastLayers=signature;
  for(let i=0;i<2;i++){
   const ctx=this.canvases[i].getContext('2d'),rows=boardRows(layers,time,i===0?-1:1);
   ctx.fillStyle='#061119';ctx.fillRect(0,0,1024,432);
   ctx.textAlign='left';ctx.fillStyle='#c4e9ff';ctx.font='bold 45px sans-serif';ctx.fillText('의정부 · 열차 도착 안내',32,65);
   ctx.fillStyle='#ffc35c';ctx.font='30px sans-serif';ctx.fillText('가상 운행 · 실제 도착정보 아님',32,112);
   ctx.font='bold 42px sans-serif';
   if(!rows.length){ctx.fillStyle='#e6edf0';ctx.fillText('운행 자료를 기다리는 중',32,215)}
   rows.forEach((r,j)=>{ctx.fillStyle='#e6edf0';ctx.fillText(`${r.destination}행`,32,207+j*80);ctx.fillStyle='#72f2b4';ctx.textAlign='right';ctx.fillText(r.status==='정차 중'?'정차 중':`${Math.floor(r.seconds/60)}분 ${Math.floor(r.seconds%60)}초`,985,207+j*80);ctx.textAlign='left'});
   ctx.fillStyle='#8eb2c7';ctx.font='28px monospace';ctx.fillText(`SIM ${Math.floor(time/3600).toString().padStart(2,'0')}:${Math.floor(time/60%60).toString().padStart(2,'0')}:${(second%60).toString().padStart(2,'0')}`,32,395);
   this.screens[i].material.map.needsUpdate=true;
  }
 }
 dispose(){for(const mesh of this.screens){this.scene.remove(mesh);mesh.geometry.dispose();mesh.material.map.dispose();mesh.material.dispose()}this.screens=[];}
}
