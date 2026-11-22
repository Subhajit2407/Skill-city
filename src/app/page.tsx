import {readFile} from 'node:fs/promises';
import path from 'node:path';
import SkillCity from '@/components/ui/SkillCity';
import type {Catalog} from '@/lib/catalog';
export const dynamic='force-dynamic';
export default async function Page(){const catalog:Catalog=JSON.parse(await readFile(path.join(process.cwd(),'src/data/catalog.json'),'utf8'));return <SkillCity catalog={catalog}/>}
