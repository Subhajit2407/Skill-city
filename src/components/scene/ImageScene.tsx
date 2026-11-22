'use client';
import {useEffect,useRef,useState} from 'react';
type Agent={id:string;title:string;category:string};
type Props={district:string|null;skillId:string|null;view?:'exterior'|'interior';agents:Agent[];onDistrict:(id:string)=>void;onAgent:(id:string)=>void;onEnter:()=>void};
// Coordinates are measured against the artwork, never the viewport.
const buildings=[['video','Video Studio',15,27],['design','Design',38,25],['marketing','Marketing',55,25],['dev','Development',72,25],['research','Research',90,25],['data','Data',14,59],['sales','Sales',39,57],['docs','Documents',63,58],['startup','Startup HQ',86,66]] as const;
export default function ImageScene({district,skillId,view,agents,onDistrict,onAgent,onEnter}:Props){
 const host=useRef<HTMLDivElement>(null);const [size,setSize]=useState({width:0,height:0});
 useEffect(()=>{const el=host.current;if(!el)return;const observer=new ResizeObserver(([entry])=>{const {width,height}=entry.contentRect;const w=Math.min(width,height*1672/941);setSize({width:w,height:w*941/1672})});observer.observe(el);return()=>observer.disconnect()},[]);
 const stage=skillId?'workspace':district?view==='interior'?'interior':'exterior':'home';
 const src=(district?`/images/districts/${district}/${stage}.png`:'/images/city.png')+'?v=city-20261123';
 const name=buildings.find(b=>b[0]===district)?.[1]||'Skill City';
 return <div ref={host} className={'image-scene image-scene-'+stage} data-district={district||'city'} data-stage={stage} aria-label={`${name} ${stage}`}><div className="artboard" style={{width:size.width||'100%',height:size.height||'100%'}}><img key={src} src={src} alt={`${name}: ${stage==='home'?'nine distinct skill buildings connected by bridges':stage==='exterior'?'domain-specific building with working Claude agents':stage==='interior'?'open floors with Claude agents in domain-specific outfits and tools':'Claude working at a profession-specific desk'}`} draggable={false} fetchPriority="high"/>
 {!district&&<div className="image-hotspots" role="group" aria-label="City buildings">{buildings.map(([id,label,x,y])=><button key={id} className="image-hit claude-target city-building-hit" style={{left:x+'%',top:y+'%'}} onClick={()=>onDistrict(id)} aria-label={'Explore '+label}><span>{label}</span></button>)}</div>}
 {district&&!skillId&&stage==='exterior'&&<button className="image-hit claude-target enter-building-hit" style={{left:'37%',top:'30%'}} onClick={onEnter} aria-label={'Enter '+name+' building'}><span>Enter {name} →</span></button>}
 {district&&!skillId&&stage==='interior'&&<div className="image-hotspots" role="group" aria-label="Agents in the building">{agents.slice(0,12).map((s,i)=><button key={s.id} className="image-hit claude-target agent-hit" style={{left:[28,45,62][i%3]+'%',top:[31,51,70,88][Math.floor(i/3)]+'%'}} onClick={()=>onAgent(s.id)} aria-label={'Open '+s.title+' workspace'}><span>{s.title}</span></button>)}</div>}
 {skillId&&<button className="image-hit claude-target room-agent" style={{left:'38%',top:'65%'}} onClick={()=>onAgent(skillId)} aria-label="Ask Claude: show example prompts"><span>Ask Claude</span></button>}
 </div></div>
}
