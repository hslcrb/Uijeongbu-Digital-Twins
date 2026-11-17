import {Vector3,Ray} from 'three';
import {CapsuleMotor} from './walking-physics.js';
// Derived from append_interior.py: local eye (1,-12,1.75) + (2,57,11), Z-up -> Y-up.
// This is a photo-study alignment, not a surveyed station coordinate.
export const CONCOURSE_ENTRY={feet:[3,11.05,-45],target:[2,12.65,-61]};
export function resolveWalkEntry(world,desired){world.ensure(desired);const hit=world.rayIntersect(new Ray(desired.clone().add(new Vector3(0,.6,0)),new Vector3(0,-1,0)));if(!hit||hit.distance>1.3||hit.triangle.getNormal(new Vector3()).y<.65)throw new Error('입장 지점의 바닥을 확인할 수 없습니다. 다른 바닥을 선택하세요.');const feet=hit.position.clone().add(new Vector3(0,.025,0));const motor=new CapsuleMotor(world,feet);const ceiling=world.rayIntersect(new Ray(feet.clone().add(new Vector3(0,.02,0)),new Vector3(0,1,0)));if(ceiling&&ceiling.distance<motor.height-.02)throw new Error('입장 지점에 충분한 보행 공간이 없습니다.');const blocked=world.capsuleIntersect(motor.capsule);if(blocked&&blocked.depth>.04)throw new Error('입장 지점에 충분한 보행 공간이 없습니다.');return motor}
