import {NextRequest,NextResponse} from 'next/server';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
export const runtime='nodejs';
export async function POST(request:NextRequest){
 const host=request.headers.get('host'),origin=request.headers.get('origin');
 if(origin&&new URL(origin).host!==host)return NextResponse.json({error:'Origin mismatch'},{status:403});
 try{await promisify(execFile)('python3',[path.join(process.cwd(),'scripts/build_catalog.py')],{timeout:20000});const data=JSON.parse(await readFile(path.join(process.cwd(),'src/data/catalog.json'),'utf8'));return NextResponse.json(data)}catch{return NextResponse.json({error:'Catalog refresh unavailable'},{status:500})}
}
