import fs from 'node:fs';
import crypto from 'node:crypto';
import {gunzipSync} from 'node:zlib';
fs.rmSync('web-dist',{recursive:true,force:true});fs.mkdirSync('web-dist',{recursive:true});
fs.cpSync('web','web-dist',{recursive:true});fs.mkdirSync('web-dist/vendor',{recursive:true});
fs.cpSync('node_modules/three/build','web-dist/vendor/three',{recursive:true});fs.cpSync('node_modules/three/examples/jsm','web-dist/vendor/addons',{recursive:true});
fs.cpSync('renders','web-dist/renders',{recursive:true,filter:p=>!p.endsWith('.png')});
fs.writeFileSync('web-dist/build.json',JSON.stringify({commit:process.env.CF_PAGES_COMMIT_SHA||process.env.WORKERS_CI_COMMIT_SHA||process.env.COMMIT_HASH||'local',built:new Date().toISOString()}));

// The compressed source avoids the connector request-size limit without losing bytes.
if(fs.existsSync('web/assets/station.glb.gz')) {
 const restored=gunzipSync(fs.readFileSync('web/assets/station.glb.gz'));
 if(restored.toString('ascii',0,4)!=='glTF'||restored.readUInt32LE(8)!==restored.length) throw new Error('Invalid restored GLB');
 fs.writeFileSync('web-dist/assets/station.glb',restored);
 fs.rmSync('web-dist/assets/station.glb.gz',{force:true});
}

// Content-addressed GLB URLs prevent an older scene surviving a newer deployment.
const model=fs.readFileSync('web-dist/assets/station.glb');
const hash=crypto.createHash('sha256').update(model).digest('hex').slice(0,16);
const modelUrl='/assets/station.'+hash+'.glb';
fs.writeFileSync('web-dist'+modelUrl,model);
const app=fs.readFileSync('web-dist/app.js','utf8').replace("'/assets/station.glb'",JSON.stringify(modelUrl));
fs.writeFileSync('web-dist/app.js',app);

// Preserve 104 independent streaming URLs while uploading one source archive.
if(fs.existsSync('web/city/city-tiles.tar.gz')) {
 const tar=gunzipSync(fs.readFileSync('web/city/city-tiles.tar.gz'));
 fs.rmSync('web-dist/city/tiles',{recursive:true,force:true});const paths=new Set();
 let count=0;
 for(let offset=0;offset+512<=tar.length;){
  const h=tar.subarray(offset,offset+512);if(h.every(v=>v===0))break;
  const str=(a,b)=>h.toString('utf8',a,b).split('\0')[0];
  let name=str(0,100),prefix=str(345,500);if(prefix)name=prefix+'/'+name;
  name=name.replace(/^\.\//,'');const length=parseInt(str(124,136).trim()||'0',8);const type=h[156];
  if(!Number.isSafeInteger(length)||length<0||offset+512+length>tar.length)throw Error('Invalid city archive length');
  if(type===0||type===48){
   if(!/^tiles\/[-0-9_]+\.glb$/.test(name))throw Error('Unexpected city archive path: '+name);
   if(paths.has(name))throw Error('Duplicate city tile '+name);paths.add(name);
   const data=tar.subarray(offset+512,offset+512+length);
   if(data.toString('ascii',0,4)!=='glTF'||data.readUInt32LE(8)!==length)throw Error('Invalid city GLB '+name);
   fs.mkdirSync('web-dist/city/tiles',{recursive:true});fs.writeFileSync('web-dist/city/'+name,data);count++;
  }else if(type!==53)throw Error('Unsupported city tar entry type '+type);
  offset+=512+Math.ceil(length/512)*512;
 }
 const manifest=JSON.parse(fs.readFileSync('web-dist/city/city-stream.json','utf8'));
 if(count!==manifest.tiles.length)throw Error('City tile count mismatch');
 for(const t of manifest.tiles){const data=fs.readFileSync('web-dist/city/'+t.url);if(data.length!==t.bytes)throw Error('Tile length mismatch '+t.id);if(t.sha256&&crypto.createHash('sha256').update(data).digest('hex')!==t.sha256)throw Error('Tile hash mismatch '+t.id);}
 fs.rmSync('web-dist/city/city-tiles.tar.gz',{force:true});
 console.log('Restored city tiles:',count);
}

// Bake and render geometry must be from the exact same final model bytes.
const fullModelHash=crypto.createHash('sha256').update(model).digest('hex');
const versionPath='web-dist/collision-version.js';
if(fs.existsSync(versionPath))fs.writeFileSync(versionPath,fs.readFileSync(versionPath,'utf8').replace('__STATION_COLLISION_HASH__',fullModelHash));
const {buildCollisionAssets}=await import('./scripts/build-collision-assets.mjs');
console.log('Static collision:',buildCollisionAssets('web/collision','web-dist/collision',fullModelHash));
