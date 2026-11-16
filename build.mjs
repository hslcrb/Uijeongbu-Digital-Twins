import fs from 'node:fs';
import crypto from 'node:crypto';
fs.rmSync('web-dist',{recursive:true,force:true});fs.mkdirSync('web-dist',{recursive:true});
fs.cpSync('web','web-dist',{recursive:true});fs.mkdirSync('web-dist/vendor',{recursive:true});
fs.cpSync('node_modules/three/build','web-dist/vendor/three',{recursive:true});fs.cpSync('node_modules/three/examples/jsm','web-dist/vendor/addons',{recursive:true});
fs.cpSync('renders','web-dist/renders',{recursive:true,filter:p=>!p.endsWith('.png')});
fs.writeFileSync('web-dist/build.json',JSON.stringify({commit:process.env.CF_PAGES_COMMIT_SHA||process.env.WORKERS_CI_COMMIT_SHA||process.env.COMMIT_HASH||'local',built:new Date().toISOString()}));

// Content-addressed GLB URLs prevent an older scene surviving a newer deployment.
const model=fs.readFileSync('web-dist/assets/station.glb');
const hash=crypto.createHash('sha256').update(model).digest('hex').slice(0,16);
const modelUrl='/assets/station.'+hash+'.glb';
fs.writeFileSync('web-dist'+modelUrl,model);
const app=fs.readFileSync('web-dist/app.js','utf8').replace("'/assets/station.glb'",JSON.stringify(modelUrl));
fs.writeFileSync('web-dist/app.js',app);
