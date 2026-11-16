import fs from 'node:fs';
fs.rmSync('web-dist',{recursive:true,force:true});fs.mkdirSync('web-dist',{recursive:true});
fs.cpSync('web','web-dist',{recursive:true});fs.mkdirSync('web-dist/vendor',{recursive:true});
fs.cpSync('node_modules/three/build','web-dist/vendor/three',{recursive:true});fs.cpSync('node_modules/three/examples/jsm','web-dist/vendor/addons',{recursive:true});
fs.cpSync('renders','web-dist/renders',{recursive:true,filter:p=>!p.endsWith('.png')});
fs.writeFileSync('web-dist/build.json',JSON.stringify({commit:process.env.CF_PAGES_COMMIT_SHA||process.env.WORKERS_CI_COMMIT_SHA||process.env.COMMIT_HASH||'local',built:new Date().toISOString()}));
