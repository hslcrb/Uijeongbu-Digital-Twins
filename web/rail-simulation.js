// Deterministic illustrative operations, never a real railway signalling system.
export function project([lon,lat]){return [(lon-127.046)*111320*Math.cos(37.738*Math.PI/180),0,((37.738-lat)*111320)||0]}
export function prepareRoute(raw,{speed=18,dwell=25}={}){
 const points=raw.points.map(project),dist=[0];for(let i=1;i<points.length;i++)dist.push(dist[i-1]+Math.hypot(points[i][0]-points[i-1][0],points[i][2]-points[i-1][2]));
 if(points.length<2||dist.at(-1)<=0)throw Error('Empty rail geometry');
 const stations=raw.stations.map(s=>{let p=project([s.lon,s.lat]),best=Infinity,d=0;for(let i=1;i<points.length;i++){let a=points[i-1],b=points[i],dx=b[0]-a[0],dz=b[2]-a[2],den=dx*dx+dz*dz,t=den?Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[2]-a[2])*dz)/den)):0,e=Math.hypot(p[0]-a[0]-dx*t,p[2]-a[2]-dz*t);if(e<best){best=e;d=dist[i-1]+(dist[i]-dist[i-1])*t}}return {...s,d,snapError:best}}).sort((a,b)=>a.d-b.d);
 if(stations.length<2)throw Error('Route needs two sourced stations');
 const order=[...stations.keys(),...Array.from({length:stations.length-2},(_,i)=>stations.length-2-i)],legs=[];let time=0,oneWay=0;
 for(let k=0;k<order.length;k++){let i=order[k],j=order[(k+1)%order.length];if(i===stations.length-1)oneWay=time;let travel=Math.abs(stations[j].d-stations[i].d)/speed;legs.push({i,j,start:time,depart:time+dwell,end:time+dwell+travel});time+=dwell+travel}
 return {...raw,points,dist,stations,legs,period:time,oneWay,speed,dwell};
}
export function positionAt(r,d){let lo=1,hi=r.dist.length-1;while(lo<hi){let m=(lo+hi)>>1;if(r.dist[m]<d)lo=m+1;else hi=m}let i=lo,a=r.points[i-1],b=r.points[i],u=Math.max(0,Math.min(1,(d-r.dist[i-1])/(r.dist[i]-r.dist[i-1]||1)));return {position:a.map((v,j)=>v+(b[j]-v)*u),heading:Math.atan2(b[0]-a[0],b[2]-a[2])};}
export function trainState(r,time){let t=((time%r.period)+r.period)%r.period,l=r.legs.find(x=>t<x.end)||r.legs.at(-1),stop=t<l.depart,f=stop?0:(t-l.depart)/(l.end-l.depart),a=r.stations[l.i],b=r.stations[l.j],d=a.d+(b.d-a.d)*f;return {...positionAt(r,d),heading:positionAt(r,d).heading+(b.d<a.d?Math.PI:0),station:stop?a.name:null,next:b.name,index:l.i,direction:b.d>a.d?1:-1,d};}
export function arrivals(r,index,time,headway=180,fleet=[]){const count=Math.max(1,Math.min(64,Math.ceil(r.period/headway))),spacing=r.period/count,result=[];for(let train=0;train<count;train++)for(const l of r.legs.filter(l=>l.i===index)){if(fleet[train]?.userData?.manualState||fleet[train]?.userData?.safetyHeld||fleet[train]?.userData?.safetyHidden)continue;let seconds=((l.start-time-train*spacing-(fleet[train]?.userData?.timeOffset||0))%r.period+r.period)%r.period;result.push({train,seconds,destination:r.stations[l.j>l.i?r.stations.length-1:0].name})}return result.sort((a,b)=>a.seconds-b.seconds).slice(0,3)}

// Distances refer to the consist centre, not a cab. Reversal changes travel
// direction without rotating/swapping physical cars at a terminus.
export function consistPose(r,d,count,spacing,bogieSpan){
 const half=(count-1)*spacing/2,margin=half+bogieSpan/2,total=r.dist.at(-1);
 const center=total>=margin*2?Math.max(margin,Math.min(total-margin,d)):total/2;
 const anchor=positionAt(r,center).position;
 const cars=Array.from({length:count},(_,i)=>{let cd=center+half-i*spacing;
  const front=positionAt(r,cd+bogieSpan/2).position,rear=positionAt(r,cd-bogieSpan/2).position;
  const position=front.map((v,k)=>(v+rear[k])/2);
  return {d:cd,position,heading:Math.atan2(front[0]-rear[0],front[2]-rear[2])};
 });return {anchor,cars};
}
