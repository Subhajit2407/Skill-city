"""Read installed skill metadata, never execute skill instructions."""
import json, re, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
HOME = Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))/'skills'

DISTRICTS = [
 dict(id='startup',name='Startup HQ',short='Startup',color='#16dcd4',icon='briefcase',description='Pressure-test your next venture with the Shark Panel.',position=[65,65]),
 dict(id='video',name='Video Studio',short='Video',color='#e3833d',icon='film',description='From a first frame to the final story.',position=[18,46]),
 dict(id='design',name='Design Quarter',short='Design',color='#9b79bf',icon='palette',description='Interfaces with clarity, character and craft.',position=[42,45]),
 dict(id='marketing',name='Marketing Exchange',short='Marketing',color='#cf7770',icon='megaphone',description='Find your audience. Give them a reason to care.',position=[61,44]),
 dict(id='dev',name='Developer Campus',short='Development',color='#579b90',icon='code',description='Build, debug and improve the way you work.',position=[84,44]),
 dict(id='research',name='Research Library',short='Research',color='#709cc7',icon='book',description='Understand the context before the next move.',position=[18,78]),
 dict(id='data',name='Data Lab',short='Data',color='#579aab',icon='database',description='Turn evidence into something you can act on.',position=[42,79]),
 dict(id='sales',name='Sales Plaza',short='Sales',color='#c5a04c',icon='briefcase',description='Find the right people and start a conversation.',position=[64,79]),
 dict(id='docs',name='Document House',short='Documents',color='#9290bc',icon='file',description='Write, explain and share ideas with intention.',position=[85,79]),
]
GROUPS = {
'video':'lemo-opuscar reelmimic sketch-to-3d cinematic-film claude-animation-base video image imagegen',
'design':'animate animate-expo animation-performance animation-vocabulary apple-design apple-design-hig ask-sonner break-ui choreograph emil-design-eng find-animation-opportunities improve-animations mobile-native pick-ui-library prototype remove-animations review-animations ui-ux-pro-max anatomy impeccable unslop taste-skill ask-emil gestures learn-taste design-is',
'marketing':'ab-testing ad-creative ads ai-seo aso churn-prevention co-marketing community-marketing competitors content-strategy copy-editing copywriting directory-submissions emails events free-tools influencer-marketing launch lead-magnets link-building marketing-council marketing-ideas marketing-loops marketing-plan marketing-psychology offers onboarding paywalls popups pricing product-marketing programmatic-seo public-relations referrals schema seo-audit signup site-architecture sms social ig-audit ig-caption ig-carousel ig-comment ig-dm ig-human ig-plan ig-profile ig-reel ig-reply ig-repurpose ig-story ig-viral',
'research':'reverse-engineer-anything competitor-profiling customer-research investigate-first caveman-discover caveman-explore learn-codebase mem-search smart-explore what-the how-it-works pathfinder',
'data':'analytics attribution conversion-tracking agent-cost-report timeline-report caveman-stats',
'startup':'shark-panel',
'sales':'local-client-finder prospecting cold-email sales-enablement revops reverse-engineer-marketing',
'docs':'linkedin-roast-panel openai-docs standup weekly-digests handoff knowledge-agent wowerpoint owner-goals',
}
TASKS = {
'lemo-opuscar':'Make a 10-second 3D film of CLAUDE taking off in a toy plane. Use my character reference and include a surprised reaction followed by a happy wave.',
'reelmimic':'Analyze my reference video. Explain its framing, pacing, transitions and visual language, then propose an original storyboard for my topic.',
'sketch-to-3d':'Create a marker-sketch reveal of my supplied 3D model, ending on the full-color render. Show the stage stills first.',
'cinematic-film':'Create a 45-second narrated explainer about how QR codes work, using a continuous camera over a designed world of evidence cards.',
'claude-animation-base':'Create a character-led system-design explainer from my script and reference images. Keep the two characters consistent throughout.',
'video':'Help me choose a repeatable production approach for a 30-second product demo. Compare a screen recording, a generated scene and a code-built video.',
'image':'Plan visual assets for a product campaign. Suggest the right image-generation workflow and prompts for each placement.',
'imagegen':'Generate a polished 3D image of my orange CLAUDE mascot on a turquoise toy aeroplane, preserving its caret eyes, side nubs and four legs.',
'anatomy':'Build an interactive isometric illustration that explains how a cache works, using a physical cabinet metaphor and a live readout.',
'impeccable':'Review my homepage for hierarchy, spacing, typography, accessibility and responsive behavior, then improve the implementation.',
'ui-ux-pro-max':'Create a coherent design system for a desktop skill directory, including navigation, colors, typography and accessible interaction patterns.',
'unslop':'Review my existing interface for generic AI design patterns and give it a clearer visual direction with specific implementation improvements.',
'taste-skill':'Build a professional frontend for my company with clear copy, a consistent visual system and purposeful motion.',
'apple-design':'Improve the drawer and navigation interactions in my web app using spatial consistency, immediate feedback and interruptible motion.',
'apple-design-hig':'Review my app against Apple interface guidelines, prioritizing navigation, accessible controls and platform conventions.',
'animate':'Add purposeful animation to my existing interface. Inspect the project first and preserve reduced-motion support.',
'animate-expo':'Add polished, responsive animations to my existing Expo app, respecting the installed libraries and reduced-motion settings.',
'animation-performance':'Investigate the jank in my page animations and fix the expensive rendering or layout work.',
'animation-vocabulary':'Help me name the motion techniques in this reference and explain how each effect works.',
'ask-sonner':'Implement a clear toast-notification flow in my application using Sonner and the existing project conventions.',
'break-ui':'Try to break my interface with long text, empty states, small screens and keyboard interaction, then fix the issues you find.',
'choreograph':'Coordinate the entrance of the heading, cards and supporting content so the motion has a clear hierarchy.',
'emil-design-eng':'Refine the small interaction and visual details of my existing interface while keeping the product behavior intact.',
'ask-emil':'Help me make a frontend design decision for this interface using the supplied context and references.',
'find-animation-opportunities':'Inspect my interface and identify where motion would clarify a state change or improve feedback.',
'improve-animations':'Review the current animations and improve their timing, continuity and responsiveness.',
'mobile-native':'Make my mobile web app feel more native through better navigation, touch feedback and layout.',
'pick-ui-library':'Inspect my project and recommend a UI library that fits its stack, product requirements and accessibility needs.',
'prototype':'Create interactive interface prototypes for my proposed feature so I can compare the approaches.',
'remove-animations':'Remove unnecessary motion from my interface while preserving useful feedback and state changes.',
'review-animations':'Review my interface animations for clarity, timing, continuity and reduced-motion behavior.',
'gestures':'Improve the touch and drag interactions in my app, accounting for cancellation, velocity and gesture conflicts.',
'learn-taste':'Learn the visual preferences in my supplied references and capture a reusable design direction.',
'reverse-engineer-anything':'Analyze this existing product or interface and explain its structure and behavior before proposing a faithful implementation.',
'write-swift':'Implement this feature in my Swift project using modern language and platform conventions.',
'shark-panel':'Pressure-test my side-hustle idea with five investor perspectives. Ask for my pitch and numbers before giving verdicts.',
'local-client-finder':'Find independent cafes near my area that could use my reel-editing service. Verify the business and Instagram facts and draft pitches for me to review.',
'linkedin-roast-panel':'Review my LinkedIn profile for my target role. Give specific feedback and rewrite the headline, About and experience without inventing achievements.',
'openai-docs':'Help me implement this OpenAI feature using current official documentation and examples suited to my project.',
'skill-creator':'Help me turn my repeatable workflow into a clear, reusable Codex skill with the right instructions and supporting files.',
'skill-installer':'Find and install a requested Codex skill from its GitHub repository, preserving existing installations.',
'review-agent':'Review my proposed changes and report concrete issues with actionable evidence.',
'mem-search':'Find relevant prior project work in the connected Claude-Mem service, using a filtered search before retrieving full details.',
'task-observer':'Review friction in my recent skill-based workflow and propose reusable improvements without changing installed skills automatically.',
'find-skills':'Find an existing skill for my task and explain its fit before installing anything.',
}
MORE = {
'ab-testing':'Plan an A/B test for my landing-page headline with a clear hypothesis and success metric.',
'ad-creative':'Draft ad creative variants for my product using the audience and channel context I provide.',
'ads':'Plan a paid advertising campaign with audience, creative and measurement requirements.',
'ai-seo':'Improve how my site answers relevant questions for AI-assisted search discovery.',
'analytics':'Define meaningful marketing analytics for my product and show how to interpret them.',
'aso':'Review my app store listing and suggest improvements for discovery and conversion.',
'attribution':'Help me understand which marketing touchpoints contribute to conversions.',
'churn-prevention':'Identify why customers leave and design a retention experiment.',
'co-marketing':'Design a partnership campaign with a complementary business.',
'cold-email':'Write a concise outbound email sequence using verified prospect context.',
'community-marketing':'Plan a useful community program for my product audience.',
'competitor-profiling':'Build an evidence-based profile of a competitor from public sources.',
'competitors':'Plan a competitor-comparison page that accurately explains our differences.',
'content-strategy':'Build a content strategy around my audience, product and goals.',
'conversion-tracking':'Audit the events and conversion tracking for my website.',
'copy-editing':'Edit my existing marketing copy for clarity, specificity and consistency.',
'copywriting':'Write homepage copy based on my product, target audience and proof.',
'cro':'Review my page for conversion friction and prioritize practical improvements.',
'customer-research':'Plan customer interviews to test our assumptions about the problem.',
'directory-submissions':'Identify relevant directories for my business and prepare accurate submissions.',
'emails':'Create an email sequence for my customer lifecycle stage.',
'events':'Plan an event that serves my audience and supports a measurable goal.',
'free-tools':'Evaluate a useful free-tool idea for reaching our product audience.',
'influencer-marketing':'Plan an influencer collaboration with audience fit and a measurement approach.',
'launch':'Plan a product launch with clear channels, timing and responsibilities.',
'lead-magnets':'Design a useful lead magnet connected to our customer problem.',
'link-building':'Plan an ethical outreach approach for earning relevant links.',
'marketing-council':'Review my marketing challenge through multiple complementary perspectives.',
'marketing-ideas':'Suggest marketing experiments appropriate to my product and available resources.',
'marketing-loops':'Identify a repeatable acquisition or retention loop for my product.',
'marketing-plan':'Build a prioritized marketing plan from my goals, budget and audience.',
'marketing-psychology':'Improve my messaging using relevant behavioral principles without misleading users.',
'offers':'Refine my offer so the audience, outcome and terms are clear.',
'onboarding':'Improve my new-user onboarding so users reach a useful outcome sooner.',
'paywalls':'Review the upgrade experience and clarify the value of the paid plan.',
'popups':'Design a contextual popup that is useful and easy to dismiss.',
'pricing':'Help me evaluate a pricing structure from my costs, customer segments and value.',
'product-marketing':'Clarify positioning and messaging for my product.',
'programmatic-seo':'Evaluate a programmatic SEO opportunity without producing thin duplicate pages.',
'prospecting':'Research relevant prospective customers using verified public information.',
'public-relations':'Develop a newsworthy story and media outreach plan for my business.',
'referrals':'Design a referral program with clear incentives and measurable outcomes.',
'reverse-engineer-marketing':'Analyze a competitor marketing approach and derive experiments for my own business.',
'revops':'Map the handoffs and data flow between marketing and sales.',
'sales-enablement':'Create sales material that addresses real buyer questions.',
'schema':'Review and implement structured data appropriate to my actual page content.',
'seo-audit':'Audit my site for technical and content issues affecting organic discovery.',
'signup':'Review my signup flow and prioritize the friction that matters most.',
'site-architecture':'Organize my website so users and search engines can find the right pages.',
'sms':'Plan a concise SMS campaign with the right context and consent requirements.',
'social':'Plan social content suited to my audience and platform.',
'ig-audit':'Audit my Instagram profile and content using the available account information.',
'ig-caption':'Write Instagram captions for my supplied content and audience.',
'ig-carousel':'Plan an Instagram carousel with a clear hook and useful progression.',
'ig-comment':'Draft a relevant Instagram comment for me to review before sending.',
'ig-dm':'Draft a personal Instagram DM using the context I provide; do not send it.',
'ig-human':'Make my Instagram communication feel more natural and specific.',
'ig-plan':'Create an Instagram content plan for my niche and resources.',
'ig-profile':'Improve my Instagram profile so the audience and value are clear.',
'ig-reel':'Plan an Instagram reel with a hook, visual beats and a clear payoff.',
'ig-reply':'Draft a helpful Instagram reply for me to review.',
'ig-repurpose':'Adapt my existing content into platform-appropriate Instagram formats.',
'ig-story':'Plan an Instagram story sequence with a clear purpose.',
'ig-viral':'Analyze the shareability of my Instagram idea without promising reach.',
}
TASKS.update(MORE)
MEMORY = set('agent-cost-report babysit backup-setup build build-and-release ccs-align childhood cloud-sync design-is do handoff how-it-works knowledge-agent learn-codebase make-plan mem-search mode-creator oh-my-issues owner-goals pathfinder release request-progress screenpipe smart-explore standup timeline-report version-bump weekly-digests what-the wowerpoint'.split())
PRETTY={'lemo-opuscar':'Lemo-Opuscar','reelmimic':'ReelMimic','sketch-to-3d':'Sketch-to-3D','ui-ux-pro-max':'UI UX Pro Max','claude-animation-base':'Claude Animation Base','cinematic-film':'Cinematic Film','imagegen':'Image Generation','taste-skill':'Taste','openai-docs':'OpenAI Docs','apple-design-hig':'Apple Design HIG'}
def frontmatter(text):
 if not text.startswith('---'):return {}
 head=text.split('---',2)[1];out={};key=None
 for line in head.splitlines():
  m=re.match(r'^(name|description):\s*(.*)',line)
  if m:key=m[1];out[key]=m[2].strip().strip('"\'')
  elif key=='description' and line.startswith('  '):out[key]+=' '+line.strip()
  elif line and not line.startswith(' '):key=None
 for k in out:out[k]=re.sub(r'^[>|][-+]?\s*','',out[k]).replace('\\"','"').strip()
 return out
def plugin_skills():
 root=HOME.parent/'plugins/cache'
 seen=set()
 if not root.is_dir():return
 for market in sorted(root.iterdir(),key=lambda p:p.name!='openai-curated-remote'):
  if not market.is_dir():continue
  for plugin in sorted(market.iterdir()):
   if not plugin.is_dir() or plugin.name in seen:continue
   versions=[v for v in plugin.iterdir() if v.is_dir() and re.match(r'^\d',v.name)]
   if not versions:continue
   version=max(versions,key=lambda v:tuple(int(n) for n in re.findall(r'\d+',v.name)))
   paths=sorted((version/'skills').glob('*/SKILL.md'))+sorted((version/'.codex-plugin/migrated-command-skills').glob('*/SKILL.md'))
   if paths:seen.add(plugin.name)
   for path in paths:yield path,plugin.name

def plugin_category(folder,plugin):
 for category,names in GROUPS.items():
  if folder in names.split():return category
 text=(plugin+' '+folder).lower()
 if any(w in text for w in ['investor','startup','founder','shark']):return 'startup'
 if any(w in text for w in ['sales','prospect','cold-email','client-finder','lead-intelligence','revops']):return 'sales'
 if any(w in text for w in ['research','scientific','osint','literature','scholar','competitor']):return 'research'
 if any(w in text for w in ['video','remotion','heygen','hyperframes','cinematic','image','manim']):return 'video'
 if any(w in text for w in ['marketing','seo','social','content','copywriting','crosspost','brand-voice','brand-discovery','article-writing']):return 'marketing'
 if any(w in text for w in ['analytics','spreadsheet','cost','billing','finance','data-throughput','benchmark']):return 'data'
 if any(w in text for w in ['design','accessibility','motion','animation','a11y','ui-canvas','ui-demo','ui-to-vue','frontend-slides','taste']):return 'design'
 if any(w in text for w in ['documents','google-drive','pages','pdf','presentations','template','docs-governance','living-docs','code-tour','codebase-onboarding']):return 'docs'
 return 'dev'

def build():
 if not HOME.is_dir():raise FileNotFoundError('Installed skill directory not found; preserve the existing snapshot.')
 examples=ROOT/'src/data/task-examples.json'
 if examples.exists():TASKS.update(json.loads(examples.read_text()))
 records=[]
 paths=[(p,None) for p in sorted(HOME.glob('*/SKILL.md'))+sorted((HOME/'.system').glob('*/SKILL.md'))]+list(plugin_skills())
 for path,plugin in paths:
  folder=path.parent.name;raw=path.read_text(errors='replace');meta=frontmatter(raw)
  name=meta.get('name',folder);name=(name if ':' in name else plugin+':'+name) if plugin else name;record_id=plugin+':'+folder if plugin else folder;desc=meta.get('description','Read the skill guide for its supported workflow.')
  category=plugin_category(folder,plugin) if plugin else next((k for k,names in GROUPS.items() if folder in names.split()),'dev')
  title=PRETTY.get(folder,folder.replace('-',' ').title().replace('Ig ','Instagram '))
  task=TASKS.get(folder)
  if not task:
   first=re.split(r'(?<=[.!?])\s+',desc)[0]
   task=f'Help me with {title.lower()} for my project. My goal and project context: [describe your task]. Follow this skill’s workflow and ask for any required inputs.'
  intent=re.sub(r'^Use (?:this skill )?when\s*','',desc,flags=re.I)
  summary=re.split(r'(?<=[.!?])\s+',intent)[0]
  if len(summary)>190:summary=summary[:187].rsplit(' ',1)[0]+'…'
  summaries={'lemo-opuscar':'Build animated films with code and a consistent visual direction.','reelmimic':'Analyze a reference video and plan an original adaptation.','sketch-to-3d':'Reveal existing 3D models through animated marker sketches.','cinematic-film':'Create narrated cinematic stories with one continuous camera.','claude-animation-base':'Create hand-painted 2D character explainers.','video':'Choose a production approach and plan repeatable video content.','image':'Create and refine visual assets for marketing.','imagegen':'Generate or edit images using prompts and references.'}
  summary=summaries.get(folder,summary)
  usecases=[task]
  short_cases={
   'lemo-opuscar':['A short character animation with consistent models','A practical system-design reel','A product story with a moving camera'],
   'reelmimic':['Break down a reference video’s visual language','Develop an original storyboard from a reference'],
   'sketch-to-3d':['A marker-sketch reveal of a product model','A sketch-to-render effect for a website'],
   'cinematic-film':['A narrated product or founder story','A documentary-style explainer with evidence cards'],
   'claude-animation-base':['A hand-painted 2D educational short','A character-led explanation of a technical idea'],
   'video':['Choose a workflow for a product demo','Plan a repeatable marketing-video process'],
   'image':['Plan marketing images for a campaign','Refine visual assets for a landing page'],
   'imagegen':['Create a new image from a detailed prompt','Edit an existing image using supplied references']}
  usecases=short_cases.get(folder,usecases)
  note=''
  if folder in MEMORY:note='Bundled with Claude-Mem. Some workflows require its memory service, integrations or repository context; installing skill files does not configure those services.'
  elif folder.startswith('caveman') or folder in {'cavecrew','megacave','ultracave'}:note='Some Caveman workflows need its Cloud service, agent definitions or host usage hooks. Skill installation alone does not configure those integrations.'
  elif folder.startswith('ig-'):note='Account-specific research or actions may require a connected Instagram account. A copied prompt does not authorize sending or publishing.'
  elif folder=='review-agent':note='A built-in support skill. Availability and invocation can depend on the Codex host.'
  if plugin:note=(note+' ' if note else '')+'Plugin guide from '+plugin+'. Required tools, services or account connections must be configured separately.'
  records.append(dict(id=record_id,name=name,title=title,description=desc,summary=summary,category=category,command='$'+name,prompt='$'+name+'\n\n'+task,usecases=usecases,note=note,system='.system' in path.parts,guide=raw,source=str(path),plugin=plugin))
 DISTRICTS.sort(key=lambda d: d['id']=='startup')
 counts={d['id']:sum(s['category']==d['id'] for s in records) for d in DISTRICTS}
 catalog=dict(skills=records,districts=[dict(d,count=counts[d['id']]) for d in DISTRICTS],total=len(records),personal=sum(not s['system'] and not s.get('plugin') for s in records),plugins=sum(bool(s.get('plugin')) for s in records),system=sum(s['system'] for s in records),scope='Personal, built-in and latest cached plugin skill guides. Plugin availability depends on configured integrations.')
 (ROOT/'src/data').mkdir(exist_ok=True);(ROOT/'src/data/catalog.tmp').write_text(json.dumps(catalog,ensure_ascii=False,indent=2));(ROOT/'src/data/catalog.tmp').replace(ROOT/'src/data/catalog.json')
 print(f'Indexed {len(records)} skills: '+', '.join(f'{k} {v}' for k,v in counts.items()))
if __name__=='__main__':build()
