// Bounded budgets keep weather predictable on mobile and integrated graphics.
export function snowSettings(mode, high=false) {
 return {count:mode==='snow'?(high?6000:2400):0};
}
export function snowVolume(distance) {
 const radius=Math.max(26,Math.min(500,Number.isFinite(distance)?distance*.22:26));
 return {radius,height:Math.max(32,radius*1.2),size:Math.min(1.4,Math.max(.13,radius*.003))};
}
