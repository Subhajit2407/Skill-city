import {chromium} from 'playwright-core';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const catalog=JSON.parse(fs.readFileSync('src/data/catalog.json'));
const manifest=JSON.parse(fs.readFileSync('docs/design/district-artwork.json'));
assert.equal(manifest.length,28);
assert.equal(new Set(manifest.map(r=>crypto.createHash('sha256').update(fs.readFileSync(r.asset)).digest('hex'))).size,28);
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const page=await browser.newPage({viewport:{width:1536,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto(process.env.CITY_URL||'http://127.0.0.1:4173');
async function scene(id,stage){await page.waitForFunction(({id,stage})=>{const el=document.querySelector('.image-scene');const img=el?.querySelector('img');return el?.getAttribute('data-district')===id&&el?.getAttribute('data-stage')===stage&&img?.complete&&img.naturalWidth>0},{id,stage});assert.equal(await page.locator('footer nav[aria-label="Districts"]').count(),1);assert.equal(await page.locator('canvas').count(),0);}
await scene('city','home');
for(const d of catalog.districts){
 await page.getByRole('navigation',{name:'Districts',exact:true}).getByRole('button',{name:d.short,exact:true}).click();
 await scene(d.id,'exterior');assert((await page.locator('.artboard>img').getAttribute('src')).includes(`/districts/${d.id}/exterior`));
 await page.locator('.building-actions button').click();await scene(d.id,'interior');
 assert.equal(await page.locator('.agent-hit').count(),Math.min(12,d.count));
 await page.locator('.agent-row').first().click();await scene(d.id,'workspace');
 assert(await page.getByRole('tab',{name:'Examples',exact:true}).getAttribute('aria-selected')==='true');
 assert(await page.locator('.prompt-card').count()>0);
 await page.screenshot({path:`checks/${d.id}-workspace.png`});
 console.log(d.id, d.count,'skills; exterior / interior / workspace OK');
}
for(const id of ['linkedin-roast-panel','shark-panel','marketing-council','local-client-finder']){
 const s=catalog.skills.find(x=>x.id===id);assert(s);await page.goto(`http://127.0.0.1:4173/#explore?skill=${id}&room=examples`);await scene(s.category,'workspace');assert.equal(await page.locator('.inspector h2').textContent(),s.title);
}
await page.setViewportSize({width:390,height:844});
for(const hash of ['#explore','#explore?category=research','#explore?category=docs&view=interior','#explore?skill=shark-panel']){await page.goto('http://127.0.0.1:4173/'+hash);await page.waitForTimeout(150);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow at ${hash}`);}
assert.deepEqual(errors,[]);await browser.close();console.log('28 unique assets and all nine three-stage district flows verified.');
