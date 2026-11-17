import {Vector3,Ray} from 'three';
import {Capsule} from 'three/addons/math/Capsule.js';

// Meter-scale kinematic character, not free-flight camera translation.
// Fixed 120 Hz steps bound collision travel even when a browser frame stalls.
export class CapsuleMotor {
 constructor(world,feet){this.world=world;this.radius=.32;this.height=1.78;this.eyeHeight=1.65;this.velocity=new Vector3();this.capsule=new Capsule(new Vector3(),new Vector3(),this.radius);this.grounded=false;this.accumulator=0;this.reset(feet)}
 get feet(){return this.capsule.start.clone().add(new Vector3(0,-this.radius,0))}
 get eye(){return this.feet.add(new Vector3(0,this.eyeHeight,0))}
 reset(feet){this.capsule.start.copy(feet).y+=this.radius;this.capsule.end.copy(feet).y+=this.height-this.radius;this.velocity.set(0,0,0);this.accumulator=0;this.grounded=false}
 jump(){if(!this.grounded)return false;this.velocity.y=6;this.grounded=false;return true}
 update(delta,direction,sprint=false){this.accumulator+=Math.max(0,Math.min(.1,Number.isFinite(delta)?delta:0));const dt=1/120;while(this.accumulator>=dt){this.step(dt,direction,sprint);this.accumulator-=dt}}
 stepUp(direction){if(!this.grounded||direction.lengthSq()<.01)return;const foot=this.feet, ahead=direction.clone().normalize().multiplyScalar(this.radius+.06);const ray=new Ray(foot.clone().add(ahead).add(new Vector3(0,.34,0)),new Vector3(0,-1,0));const hit=this.world.rayIntersect(ray);if(!hit||hit.distance>.34)return;const rise=hit.position.y-foot.y;if(rise<.04||rise>.32)return;const normal=hit.triangle.getNormal(new Vector3());if(normal.y<.65)return;const trial=this.capsule.clone();trial.translate(new Vector3(0,rise+.015,0));const blocked=this.world.capsuleIntersect(trial);if(!blocked||blocked.depth<.01){this.capsule.copy(trial);this.velocity.y=0}}
 step(dt,direction,sprint){this.stepUp(direction);const desired=direction.clone();desired.y=0;if(desired.lengthSq()>1)desired.normalize();desired.multiplyScalar(sprint?5:2.8);const blend=1-Math.exp(-(this.grounded?18:5)*dt);this.velocity.x+=(desired.x-this.velocity.x)*blend;this.velocity.z+=(desired.z-this.velocity.z)*blend;this.velocity.y=Math.max(-40,this.velocity.y-22*dt);this.capsule.translate(this.velocity.clone().multiplyScalar(dt));this.grounded=false;
  // Resolve corners in several passes rather than accepting one combined normal.
  for(let i=0;i<5;i++){const hit=this.world.capsuleIntersect(this.capsule);if(!hit)break;if(hit.normal.y>.55&&this.velocity.y<=0)this.grounded=true;const inward=this.velocity.dot(hit.normal);if(inward<0)this.velocity.addScaledVector(hit.normal,-inward);this.capsule.translate(hit.normal.multiplyScalar(hit.depth+1e-5))}
 }
}
