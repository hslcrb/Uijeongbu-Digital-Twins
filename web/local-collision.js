import {Box3,Vector3,Triangle} from 'three';
import {Octree} from 'three/addons/math/Octree.js';
// Keep the full-detail city render out of a monolithic physics octree.
// Only triangles in a 12m neighborhood are indexed; rebuild before its edge.
export class LocalCollisionWorld {
 constructor(model,{maxTriangles=20000,maxScanned=1000000}={}){this.maxTriangles=maxTriangles;this.maxScanned=maxScanned;this.meshes=[];model.updateWorldMatrix(true,true);model.traverse(mesh=>{if(mesh.isMesh&&mesh.geometry.attributes.position){mesh.geometry.computeBoundingBox();this.meshes.push({mesh,box:mesh.geometry.boundingBox.clone().applyMatrix4(mesh.matrixWorld)})}});this.center=new Vector3(Infinity,Infinity,Infinity);this.tree=null;this.triangleCount=0}
 ensure(position){if(this.tree&&Math.abs(position.x-this.center.x)<2.5&&Math.abs(position.z-this.center.z)<2.5&&Math.abs(position.y-this.center.y)<1.5)return;const region=new Box3(position.clone().add(new Vector3(-6,-4,-6)),position.clone().add(new Vector3(6,4,6)));const tree=new Octree();tree.maxLevel=7;tree.trianglesPerLeaf=24;const triangle=new Triangle(),triBox=new Box3();let count=0,scanned=0;
 for(const {mesh,box} of this.meshes){if(!region.intersectsBox(box))continue;const positions=mesh.geometry.attributes.position,indices=mesh.geometry.index,n=indices?indices.count:positions.count;for(let i=0;i<n;i+=3){if(++scanned>this.maxScanned)throw new Error('충돌 계산이 복잡한 위치입니다. 더 넓고 단순한 바닥에서 시작하세요.');triangle.a.fromBufferAttribute(positions,indices?indices.getX(i):i).applyMatrix4(mesh.matrixWorld);triangle.b.fromBufferAttribute(positions,indices?indices.getX(i+1):i+1).applyMatrix4(mesh.matrixWorld);triangle.c.fromBufferAttribute(positions,indices?indices.getX(i+2):i+2).applyMatrix4(mesh.matrixWorld);triBox.makeEmpty().expandByPoint(triangle.a).expandByPoint(triangle.b).expandByPoint(triangle.c);if(region.intersectsBox(triBox)&&region.intersectsTriangle(triangle)){if(++count>this.maxTriangles)throw new Error('이 위치의 충돌 면이 너무 많습니다. 다른 바닥을 선택하세요.');tree.addTriangle(triangle.clone())}}}
 // Keep the partition bounded even for a kilometer-wide floor triangle.
 tree.bounds.copy(region);tree.build();this.tree=tree;this.center.copy(position);this.triangleCount=count;
 }
 capsuleIntersect(capsule){return this.tree?.capsuleIntersect(capsule)||false}
 rayIntersect(ray){return this.tree?.rayIntersect(ray)||false}
}
