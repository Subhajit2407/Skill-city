import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {readRoute,routeHash,readSaved,searchSkills,type Catalog} from '../src/lib/catalog.ts';
const catalog:Catalog=JSON.parse(readFileSync(new URL('../src/data/catalog.json',import.meta.url),'utf8'));
assert.equal(catalog.skills.length,catalog.total);assert.equal(new Set(catalog.skills.map(s=>s.id)).size,catalog.total);
for(const d of catalog.districts)assert.equal(d.count,catalog.skills.filter(s=>s.category===d.id).length);
assert.equal(catalog.skills.find(s=>s.id==='shark-panel')?.category,'startup');assert(searchSkills(catalog.skills,'linkedin roast').some(s=>s.id==='linkedin-roast-panel'));
assert.deepEqual(readSaved('not json',catalog.skills),[]);assert.deepEqual(readSaved('["missing",4,"shark-panel"]',catalog.skills),['shark-panel']);
for(const s of catalog.skills){const r=readRoute('#district/'+s.category+'?tab=commands&skill='+s.id,catalog.skills);assert.equal(r.skill,s.id);assert.equal(r.tab,'examples');assert.deepEqual(readRoute(routeHash(r),catalog.skills),r)}
assert.equal(readRoute('#explore?category=__proto__&skill=missing',catalog.skills).district,null);console.log(`Catalog and route checks passed for ${catalog.total} skills and ${catalog.districts.length} districts.`);
