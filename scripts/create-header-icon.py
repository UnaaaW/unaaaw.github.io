"""Render the hand-drawn header icon and its drawing animation."""
from PIL import Image, ImageDraw
import math
import random
from pathlib import Path

random.seed(27)
size = 550
ink = (27, 40, 69)
paper = (250, 251, 249)

def arc(cx, cy, rx, ry, start, end, count=100):
    return [(cx + rx*math.cos(t), cy + ry*math.sin(t)) for t in
            [start+(end-start)*i/(count-1) for i in range(count)]]

paths = [
    arc(99, 130, 36, 29, 0, math.pi*2, 65),
    [(135,128),(143,124),(153,128)],
    arc(190, 130, 36, 29, 0, math.pi*2, 65),
    [(62,122),(43,114)], [(226,122),(244,114)],
    arc(102,132,3,5,0,math.pi*2,16),
    arc(187,132,3,5,0,math.pi*2,16),
    [(144,143),(139,161),(150,163)],
    arc(145,164,48,35,.25,math.pi-.25,60),
]
# Handwritten letter strokes, drawn after the face: U, n, a, period.
paths += [
    [(290,102),(288,150),(292,177),(300,190),(316,194),(331,188),(338,176),(342,103)],
    [(365,191),(368,143),(370,173),(380,146),(394,138),(406,143),(411,157),(409,191)],
    arc(450,166,20,27,0,math.pi*2,65),
    [(470,142),(468,190),(481,191)],
    arc(504,188,3,3,0,math.pi*2,16),
]
# Subdivide straight strokes so letters appear written rather than popping in.
dense_paths=[]
for path in paths:
    dense=[]
    for a,b in zip(path,path[1:]):
        steps=max(1,int(math.dist(a,b)/2))
        dense.extend([(a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps) for i in range(steps)])
    dense.append(path[-1])
    dense_paths.append(dense)
paths=dense_paths
# Fixed irregularities keep the texture stable while strokes are revealed.
segments=[]
for path in paths:
    points=[(x+random.uniform(-1.3,1.3),y+random.uniform(-1.3,1.3)) for x,y in path]
    for a,b in zip(points,points[1:]):
        segments.append((a,b,random.randint(9,12)))
canvas=Image.new('RGB',(size,size),paper)
frames=[]
for frame in range(60):
    draw=ImageDraw.Draw(canvas)
    start=int(len(segments)*frame/60)
    end=int(len(segments)*(frame+1)/60)
    for a,b,width in segments[start:end]:
        draw.line([a,b],fill=ink,width=width)
        # Fine paper-colored flecks imitate a dry crayon stroke.
        for _ in range(3):
            t=random.random()
            x=a[0]+(b[0]-a[0])*t+random.uniform(-2,2)
            y=a[1]+(b[1]-a[1])*t+random.uniform(-2,2)
            draw.point((int(x),int(y)),fill=paper)
    frames.append(canvas.crop((30, 80, 530, 220)).resize((314, 88),Image.Resampling.LANCZOS))
out=Path(__file__).resolve().parents[1]/'img'
frames[-1].save(out/'una-home.png')
frames[0].save(out/'una-home.gif',save_all=True,append_images=frames[1:],duration=[50]*59+[2200],optimize=True)
