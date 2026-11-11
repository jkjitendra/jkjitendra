#!/usr/bin/env python3
"""Build self-contained GitHub-compatible SVG illustrations. No external assets."""
from __future__ import annotations
import base64
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
NAVY = '#070D17'
PANEL = '#0B1423'
WHITE = '#EEF6FF'
MUTED = '#92A4B9'
CYAN = '#50D9F5'
GOLD = '#FFCF61'
GREEN = '#51D9A7'
BLUE = '#5CA9FF'

# Use the actual blue-and-gold JK logo supplied by the owner. Do not generate a substitute.
logo_path = ASSETS / 'jk-logo.png'
if not logo_path.is_file():
    raise FileNotFoundError('Place your uploaded JK logo at assets/jk-logo.png before rebuilding')
logo_b64 = base64.b64encode((ASSETS / 'jk-logo.png').read_bytes()).decode()

def svg(title, w, h, content, extra_style=''):
    # Main typography is intentionally system-font based: no remote font loading.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#08101A"/><stop offset=".57" stop-color="#0A131C"/><stop offset="1" stop-color="#0A0F19"/></linearGradient>
 <radialGradient id="glow"><stop stop-color="#48DDF8" stop-opacity=".18"/><stop offset="1" stop-color="#48DDF8" stop-opacity="0"/></radialGradient>
 <filter id="softGlow" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="7"/></filter>
 <style><![CDATA[
 .sans{{font-family:Inter,Segoe UI,Arial,sans-serif;}}
 .mono{{font-family:ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace;}}
 .secondary{{fill:{MUTED};}}
 .twinkle{{animation:twinkle 3.8s ease-in-out infinite;}}
 @keyframes twinkle{{0%,100%{{opacity:.25}}50%{{opacity:.82}}}}
 @keyframes blink{{0%,45%{{opacity:1}}50%,100%{{opacity:0}}}}
 .cursor{{animation:blink 1.1s step-end infinite;}}
 @media (prefers-reduced-motion: reduce){{.twinkle,.cursor{{animation:none}}.request-bubble,.pulse-ring{{display:none}}}}
 {extra_style}
 ]]></style>
</defs>
{content}
</svg>'''

def stars(w,h,n,seed=79,top=0):
    import random
    rng=random.Random(seed)
    return ''.join(f'<circle cx="{rng.randrange(8,w-8)}" cy="{rng.randrange(top+8,h-8)}" r="{rng.choice([.7,.9,1.25])}" fill="{rng.choice(["#8AA4C2","#F7FDFF","#2F6C99"])}" opacity="{rng.choice([.17,.25,.32,.44])}"/>' for _ in range(n))

def txt(x,y,s,size=18,color=WHITE,weight=500,cls='sans',anchor=None,spacing=None):
    attrs=f'x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" class="{cls}"'
    if anchor: attrs+=f' text-anchor="{anchor}"'
    if spacing: attrs+=f' letter-spacing="{spacing}"'
    return f'<text {attrs}>{escape(s)}</text>'

def pill(x,y,label,color=CYAN,width=None):
    width=width or max(74,int(len(label)*8.2+25))
    return f'<rect x="{x}" y="{y}" width="{width}" height="26" rx="13" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".28"/>'+txt(x+width/2,y+18,label,12,color,650,anchor='middle')

# 1. Animated map: cards are separately rendered to keep labels clear even on narrower screens.
W,H=1200,630
map_items = [
    ('Arkil','IDENTITY & SECURITY', 292,205,'#55C5FF',-1),
    ('CodeBundle','DEVELOPER TOOLS',524,139,'#FFCA66',-1),
    ('Transfer Aggregator','MICROSERVICES',839,187,'#FF995D',1),
    ('EduKitBox','OFFLINE-FIRST PWA',956,414,'#4FD5A4',1),
    ('Recomart Pipeline','ML / RECOMMENDATIONS',737,540,'#A891FF',1),
    ('Heart Disease MLOps','ML ENGINEERING',407,537,'#63A8FF',-1),
    ('MazeSolver','ALGORITHMS',230,394,'#FFC86B',-1),
    ('DrostScope','IN DEVELOPMENT',1010,286,'#F17A9D',-1),
]
cx,cy=600,335
parts=[f'<rect width="{W}" height="{H}" rx="26" fill="url(#bg)"/>',
       f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="25" fill="none" stroke="#233449"/>',
       f'<circle cx="{cx}" cy="{cy}" r="225" fill="url(#glow)"/>',
       stars(W,H,105,91,65),
       '<rect x="36" y="34" width="6" height="17" rx="2" fill="#53E0B0"/>',
       txt(56,49,'PROJECT CONSTELLATION',14,GREEN,750,spacing='2.3'),
       txt(40,92,'Everything I build, connected.',32,WHITE,800),
       txt(42,122,'A living map of projects, systems, and ideas in motion.',16,MUTED,400),
       pill(992,40,'8 SIGNAL NODES',BLUE,160),
       '<path d="M38 153 H1162" stroke="#314155" stroke-opacity=".65"/>',
       ]
# Implicit connections between related work, intentionally subtle and away from text.
for a,b in [(0,1),(0,6),(1,2),(1,7),(2,3),(2,7),(3,4),(4,5),(5,6)]:
    _,_,ax,ay,_,_=map_items[a]
    _,_,bx,by,_,_=map_items[b]
    parts.append(f'<path d="M{ax} {ay} L{bx} {by}" fill="none" stroke="#385878" stroke-width="1" opacity=".25" stroke-dasharray="3 9"/>')
for i,(name,sub,x,y,color,side) in enumerate(map_items):
    # Curved inward transport path; 'animateMotion' is SVG-native, requires no JS.
    midx=(x+cx)/2 + (cy-y)*.10
    midy=(y+cy)/2 - (cx-x)*.08
    path=f'M {x} {y} Q {midx:.1f} {midy:.1f} {cx} {cy}'
    parts += [f'<path d="{path}" fill="none" stroke="{color}" opacity=".37" stroke-width="1.5"/>',
              f'<path d="{path}" fill="none" stroke="#FFFFFF" stroke-opacity=".09" stroke-width=".6" stroke-dasharray="3 7"/>',
              f'<circle class="request-bubble" r="5" fill="{color}" opacity=".92"><animateMotion dur="{3.9+i*.25:.2f}s" begin="{-(i*.53):.2f}s" repeatCount="indefinite" path="{path}"/><animate attributeName="opacity" values="0;.95;.95;0" dur="{3.9+i*.25:.2f}s" begin="{-(i*.53):.2f}s" repeatCount="indefinite"/></circle>']
# Node dots with label positioning; keep well away from core pulse (r <= 80).
for i,(name,sub,x,y,color,side) in enumerate(map_items):
    label_x=x+22 if side==1 else x-22
    anchor='start' if side==1 else 'end'
    # Glow then crisp circle
    parts += [f'<circle cx="{x}" cy="{y}" r="18" fill="{color}" opacity=".13"/>',
              f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" stroke="#0C1521" stroke-width="3"/>',
              txt(label_x,y-1,name,16,WHITE,750,anchor=anchor),
              txt(label_x,y+18,sub,10,MUTED,650,cls='mono',anchor=anchor,spacing='.4'),
              f'<circle class="twinkle" cx="{x+14}" cy="{y-14}" r="2.2" fill="{color}" style="animation-delay:{i*.31}s"/>']
# Core pulse circles r=47..80; project labels stay beyond x=200px from center.
for i in range(3):
    parts += [f'<circle class="pulse-ring" cx="{cx}" cy="{cy}" r="62" stroke="{CYAN}" stroke-width="2.2" fill="none" opacity="0"><animate attributeName="r" values="62;98;98" dur="4.5s" begin="{i*1.5}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".78;.22;0" dur="4.5s" begin="{i*1.5}s" repeatCount="indefinite"/></circle>']
parts += [f'<circle cx="{cx}" cy="{cy}" r="68" fill="#83DFFF" opacity=".20" filter="url(#softGlow)"/>',
          f'<circle cx="{cx}" cy="{cy}" r="60" fill="#F5F1E8" stroke="#C6A767" stroke-opacity=".90" stroke-width="2"/>',
          f'<image x="{cx-51}" y="{cy-51}" width="102" height="102" href="data:image/png;base64,{logo_b64}"/>',
          txt(cx,cy+76,'JK • ENGINEERING HUB',13,CYAN,700,cls='mono',anchor='middle',spacing='1.4'),
          '<path d="M38 580 H1162" stroke="#314155" stroke-opacity=".58"/>',
          txt(42,607,'SIGNAL / PROJECT  →  HUB',12,GOLD,650,cls='mono'),
          txt(1157,607,'SVG MOTION • NO JAVASCRIPT',11,MUTED,550,cls='mono',anchor='end')]
(ASSETS/'network.svg').write_text(svg('Animated project constellation with radiating JK logo and inward request bubbles',W,H,'\n'.join(parts)),encoding='utf8')

# 2. Dark technical stack inspired by screenshot 3 but sourced from the provided resume.
W,H=1200,675
cats=[
    ('BACKEND & LANGUAGES',[("Java","#E97428"),("Spring Boot","#6BB64C"),("Spring Ecosystem","#5A9A3E"),("Go","#0AABC7"),("Scala","#D95954"),("Node.js","#4B9A42"),("REST APIs","#117DAB")]),
    ('FRONTEND',[("React","#2985AA"),("Next.js","#374151"),("TypeScript","#3178C6"),("JavaScript","#DDBF20"),("Redux","#7A51B5"),("Tailwind CSS","#0FA9A9")]),
    ('DATABASE & CACHING',[("PostgreSQL","#3565A1"),("MySQL","#296C95"),("MongoDB","#387D4A"),("Cassandra","#3F85A4"),("Redis","#B84740")]),
    ('MESSAGING & CLOUD',[("Apache Kafka","#444855"),("AWS","#CD8E33"),("S3","#4B965B"),("Lambda","#B87932"),("Protobuf","#536995")]),
    ('DEVOPS & DELIVERY',[("Docker","#177BB2"),("Jenkins","#7B4E4E"),("CircleCI","#374151"),("Git","#C55139"),("Maven","#7550AA"),("Nomad","#528F74"),("Consul","#A64C80")]),
    ('QUALITY, SECURITY & OBSERVABILITY',[("SonarQube","#417FAB"),("OAuth2 / JWT","#535A77"),("Grafana","#A45F24"),("Prometheus","#D95E3F"),("Postman","#ED774A"),("ESLint","#5E5DAD")])]
parts=[f'<rect width="{W}" height="{H}" rx="26" fill="url(#bg)"/>',f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="25" stroke="#26364B" fill="none"/>',stars(W,H,38,122,0),
       txt(42,57,'TOOLS OF THE TRADE',13,GOLD,700,cls='mono',spacing='2'),
       txt(42,102,'Tech Stack',34,WHITE,800),
       txt(42,132,'Selected technologies from my engineering experience and personal projects',15,MUTED),
       '<path d="M42 156 H1158" stroke="#34465A" stroke-opacity=".85"/>']
ys=[188,270,352,434,516,598]
for (header, chips),y in zip(cats,ys):
    parts += [f'<circle cx="48" cy="{y-2}" r="3" fill="{CYAN}"/>',txt(65,y+4,header,14,WHITE,750,spacing='.6')]
    x=66
    for label,fill in chips:
        cw=round(max(66, len(label)*8.4+28))
        # Row starts underneath its heading, y+17 .. y+48; <= final height.
        parts.append(f'<rect x="{x}" y="{y+15}" width="{cw}" height="33" rx="6" fill="{fill}" fill-opacity=".90"/>')
        parts.append(txt(x+cw/2,y+37,label,14,'#FFFFFF',650,anchor='middle'))
        x+=cw+8
        if x>1150:
            raise RuntimeError(f'Row overflow for {header}: {x}')
(ASSETS/'stack.svg').write_text(svg('Technology stack organized into six resume-based categories',W,H,'\n'.join(parts)),encoding='utf8')

# 3. Screenshot-1 inspired moon cards. Names and descriptions verified from resume.
W,H=1200,590
moons=[
    ('MOON 01','arkil','Multi-tenant IAM kernel with OAuth2/OIDC,','MFA, secure JWT rotation, and Redis.','JAVA / SPRING BOOT','#F5AB36'),
    ('MOON 02','codebundle','Local-first desktop utility for bundling','code into structured, AI-ready exports.','TYPESCRIPT / ELECTRON','#5EABEC'),
    ('MOON 03','recomart-pipeline','Recommendation pipeline built around','Python, MLflow and model workflows.','PYTHON / MLOPS','#76C6FF'),
    ('MOON 04','transfer-aggregator-service','Airport supplier aggregator providing','Search, Book and Cancel APIs.','JAVA / MICROSERVICES','#F0A338'),
]
parts=[f'<rect width="{W}" height="{H}" rx="25" fill="{NAVY}"/>',txt(29,47,'FEATURED REPOSITORIES',14,GOLD,780,cls='mono',spacing='1.8'),txt(29,82,'Four worlds, one engineering mindset.',26,WHITE,740)]
for i,(moon,name,desc1,desc2,lang,accent) in enumerate(moons):
    x=20+(i%2)*590; y=110+(i//2)*232; cw=570; ch=216
    parts += [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="19" fill="#0A1220" stroke="#1D283C"/>',stars(cw,ch,19,seed=198+i*9,top=4).replace('cx="','cx="',1)]
    # Star field must be translated into card's coordinate system. Remove global stars injected above and replace in group.
    parts.pop()
    parts += [f'<g transform="translate({x},{y})">{stars(cw,ch,18,seed=198+i*9,top=4)}</g>',
              txt(x+28,y+34,moon,14,GOLD,800,cls='mono',spacing='2'),
              f'<circle cx="{x+518}" cy="{y+35}" r="13" fill="{accent}" fill-opacity=".82"/>',
              f'<ellipse cx="{x+518}" cy="{y+35}" rx="21" ry="5.5" stroke="#92BDE1" stroke-opacity=".74" fill="none" transform="rotate(-10 {x+518} {y+35})"/>',
              txt(x+28,y+83,name,26,WHITE,760,cls='mono'),
              txt(x+28,y+115,desc1,16,'#D2E0EE',440),
              txt(x+28,y+139,desc2,16,'#D2E0EE',440),
              '<path d="M'+str(x+28)+' '+str(y+156)+' H'+str(x+540)+'" stroke="#24344B"/>',
              f'<circle cx="{x+34}" cy="{y+184}" r="4.2" fill="{accent}"/>',
              txt(x+47,y+189,lang,13,MUTED,700,cls='mono')]
(ASSETS/'moons.svg').write_text(svg('Four featured repositories on celestial dark moon cards',W,H,'\n'.join(parts)),encoding='utf8')

# 4. Terminal-style profile from screenshot 2; values from resume, no fake live GitHub statistics.
W,H=1200,575
parts=[f'<rect width="{W}" height="{H}" rx="18" fill="#090F18" stroke="#1B728D" stroke-width="2"/>',
       f'<rect x="1" y="1" width="{W-2}" height="51" rx="18" fill="#0E1621"/>',
       '<path d="M1 52 H1199" stroke="#2C445B"/>',
       '<circle cx="22" cy="27" r="5" fill="#FF5F57"/><circle cx="40" cy="27" r="5" fill="#FEBB2E"/><circle cx="58" cy="27" r="5" fill="#28C840"/>',
       txt(600,31,'jkjitendra@dev-os: ~/profile.sh --live',15,'#7189A4',550,cls='mono',anchor='middle'),
       f'<circle cx="1111" cy="27" r="4" fill="{CYAN}"/>',txt(1123,31,'ONLINE',12,CYAN,650,cls='mono'),
       '<rect x="24" y="74" width="448" height="428" rx="14" fill="#07121D" stroke="#1E5B75"/>',
       '<rect x="490" y="74" width="687" height="428" rx="14" fill="#07121D" stroke="#1E5B75"/>',
       txt(45,105,'VISUAL.IDENTITY',12,'#6F99B5',700,cls='mono',spacing='1.2'),
       txt(512,105,'SYSTEM.INFO',12,'#6F99B5',700,cls='mono',spacing='1.2'),
       f'<path d="M490 352 H1177" stroke="#17506A" opacity=".55"/>']
# Display the same uploaded JK emblem used in the header and constellation.
# A pale medallion maintains contrast for the deep-blue and gold strokes.
parts += [
    '<circle cx="248" cy="292" r="145" fill="#49CFF0" fill-opacity=".10" filter="url(#softGlow)"/>',
    '<circle cx="248" cy="292" r="139" fill="#F5F1E8" stroke="#C8AE76" stroke-width="2.5"/>',
    f'<image x="123" y="167" width="250" height="250" href="data:image/png;base64,{logo_b64}"/>',
]
parts += [txt(248,477,'ENGINEER / BUILDER / LEADER',14,CYAN,680,cls='mono',anchor='middle'),
          txt(513,143,'IDENTITY',14,GREEN,760,cls='mono',spacing='2')]
identity=[('Name','Jitendra Kumar Tiwari'),('Role','Team Lead / Full Stack Engineer'),('Location','India'),('Focus','Real-time APIs • distributed systems'),('Stack','Java • Spring Boot • React • TypeScript')]
for i,(k,v) in enumerate(identity):
    y=184+i*33
    parts+=[txt(514,y,k,14,CYAN,650,cls='mono'),txt(683,y,v,14,WHITE,540,cls='mono')]
parts.append(txt(513,385,'ENGINEERING SIGNAL',14,GREEN,760,cls='mono',spacing='2'))
signals=[('Experience','5+ years'),('Scale','~2.3k requests / second'),('API latency','~95ms P95 at peak'),('GitHub','@jkjitendra')]
for i,(k,v) in enumerate(signals):
    y=415+i*25
    parts+=[txt(514,y,k,13,CYAN,650,cls='mono'),txt(683,y,v,13,WHITE,540,cls='mono')]
parts += [txt(39,545,'$ building performant systems since 2020',14,MUTED,550,cls='mono'),
          f'<rect class="cursor" x="446" y="530" width="9" height="17" fill="{CYAN}"/>',
          txt(1154,544,'jkjitendra.in',13,'#7793AA',600,cls='mono',anchor='end')]
(ASSETS/'terminal.svg').write_text(svg('Terminal developer profile with an animated cursor and resume-based engineering metrics',W,H,'\n'.join(parts)),encoding='utf8')

# Short matching title banner.
W,H=1200,180
parts=[f'<rect width="{W}" height="{H}" rx="19" fill="url(#bg)"/>',stars(W,H,53,46),
       f'<rect x="34" y="35" width="6" height="98" rx="3" fill="{CYAN}"/>',
       txt(61,71,'HELLO, WORLD. I AM',16,GOLD,700,cls='mono',spacing='2'),
       txt(61,120,'JITENDRA KUMAR TIWARI',38,WHITE,820),
       txt(63,149,'Full Stack Engineer  /  Team Lead  /  System Builder',15,MUTED,550,cls='mono'),
       f'<circle cx="1067" cy="89" r="60" fill="#F5F1E8" stroke="#C6A767" stroke-width="2"/>',
       f'<image x="1021" y="43" width="92" height="92" href="data:image/png;base64,{logo_b64}"/>',
       f'<circle cx="1067" cy="89" r="67" fill="none" stroke="{CYAN}" opacity=".38"><animate attributeName="opacity" values=".12;.60;.12" dur="4s" repeatCount="indefinite"/></circle>']
(ASSETS/'header.svg').write_text(svg('Jitendra Kumar Tiwari GitHub developer introduction',W,H,'\n'.join(parts)),encoding='utf8')
print('Generated',*(str(p) for p in sorted(ASSETS.glob('*.svg'))),sep='\n - ')
