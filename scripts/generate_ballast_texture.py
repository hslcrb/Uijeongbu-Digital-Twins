# Original angular stone illustration; run with system Python/Pillow.
from PIL import Image,ImageDraw
from pathlib import Path
import random,math,sys
rng=random.Random(1105);im=Image.new('RGB',(512,512),(45,43,39));d=ImageDraw.Draw(im)
for k in range(1800):
 x,y=rng.uniform(-15,527),rng.uniform(-15,527);r=rng.uniform(3,11);a=rng.uniform(0,6.28);v=[(x+math.cos(a+j*math.tau/5)*r*rng.uniform(.7,1.3),y+math.sin(a+j*math.tau/5)*r*rng.uniform(.7,1.3)) for j in range(5)];c=rng.randint(58,135);d.polygon(v,fill=(c,int(c*.96),int(c*.90)));d.line(v[:3],fill=(min(180,c+22),min(180,c+19),min(180,c+15)),width=1)
im.save(sys.argv[1] if len(sys.argv)>1 else 'rail-ballast-procedural.png')
