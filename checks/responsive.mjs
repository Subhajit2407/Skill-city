import {chromium} from 'playwright-core';
import assert from 'node:assert/strict';
const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const p=await b.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
await p.goto('http://127.0.0.1:4173');await p.getByRole('button',{name:'Dismiss introduction'}).click();assert.equal(await p.locator('.welcome').count(),0);await p.reload();assert.equal(await p.locator('.welcome').count(),0);
for(const [w,h] of [[320,568],[390,844],[768,1024],[1024,768],[1366,768],[1440,900],[1920,1080],[1280,600]]){
 await p.setViewportSize({width:w,height:h});
 for(const hash of ['#explore','#explore?category=design','#explore?category=research&view=interior','#explore?skill=shark-panel&room=examples']){
  await p.goto('http://127.0.0.1:4173/'+hash);await p.locator('.artboard img').waitFor();await p.waitForTimeout(100);
  const info=await p.evaluate(()=>{const box=s=>document.querySelector(s)?.getBoundingClientRect();const a=box('.artboard'),i=box('.inspector');const img=document.querySelector('.artboard img');return{overflow:document.documentElement.scrollWidth>innerWidth,ratio:a.width/a.height,img:img.complete&&img.naturalWidth>0,overlap:i&&a.right>i.left+1&&a.bottom>i.top+1&&a.top<i.bottom}});
  assert(!info.overflow,`${w} overflow ${hash}`);assert(info.img);assert(Math.abs(info.ratio-1672/941)<.02);assert(!info.overlap,`${w} artwork / inspector overlap ${hash}`);
 }
 await p.goto('http://127.0.0.1:4173/#explore');await p.waitForTimeout(100);
 const targets=await p.locator('.city-building-hit').evaluateAll(els=>els.map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom}}));
 for(let i=0;i<targets.length;i++)for(let j=i+1;j<targets.length;j++){const a=targets[i],c=targets[j];assert(!(a.x<c.right&&a.right>c.x&&a.y<c.bottom&&a.bottom>c.y),`overlapping Claude targets at ${w}: ${i},${j}`)}
 if(w===390||w===1366){await p.screenshot({path:`checks/responsive-city-${w}.png`,fullPage:true});await p.goto('http://127.0.0.1:4173/#explore?category=design');await p.waitForTimeout(100);await p.screenshot({path:`checks/responsive-design-${w}.png`,fullPage:true})}
 console.log(w,h,'fitted artwork, separate inspector, no overflow or overlapping targets');
}
await p.setViewportSize({width:1366,height:768});await p.goto('http://127.0.0.1:4173/#explore');await p.getByRole('button',{name:'Explore Research',exact:true}).hover();assert.equal(await p.getByRole('button',{name:'Explore Research',exact:true}).evaluate(e=>getComputedStyle(e).boxShadow),'none');await p.getByRole('button',{name:'Explore Research',exact:true}).click();await p.getByRole('heading',{name:'Research',exact:true}).waitFor();
await p.evaluate(()=>localStorage.removeItem('skill-city-intro-seen'));await p.reload();await p.goto('http://127.0.0.1:4173/#explore');await p.locator('.welcome').waitFor();await p.locator('.welcome').waitFor({state:'hidden',timeout:12000});assert.equal(await p.evaluate(()=>localStorage.getItem('skill-city-intro-seen')),'1');
assert.deepEqual(errors,[]);await b.close();console.log('Welcome dismissal, reload persistence, auto-dismiss and Research hover/click verified.');
