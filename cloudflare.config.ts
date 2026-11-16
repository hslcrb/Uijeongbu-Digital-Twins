import { defineConfig } from 'cf/config';
export default defineConfig({worker:{name:'uijeongbu-digital-twins',compatibilityDate:'2026-11-16',workersDev:true,domains:['twin.uijeongbu.rhee.life'],assets:{htmlHandling:'auto-trailing-slash',notFoundHandling:'404-page'}}});
