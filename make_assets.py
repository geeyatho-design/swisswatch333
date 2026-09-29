from PIL import Image, ImageDraw
from pathlib import Path
from math import sin,cos,pi
p=Path(__file__).parent/'app/src/main/res/drawable-nodpi'; p.mkdir(parents=True,exist_ok=True)
S=450; C=225
im=Image.new('RGBA',(S,S),'#f7f7f4'); d=ImageDraw.Draw(im)
d.ellipse((5,5,445,445),outline='#151515',width=5)
for i in range(60):
 a=2*pi*i/60-pi/2
 r1=169 if i%5==0 else 184
 r2=208
 w=12 if i%5==0 else 3
 d.line((C+r1*cos(a),C+r1*sin(a),C+r2*cos(a),C+r2*sin(a)),fill='#121212',width=w)
im.save(p/'dial.png')
# Each PNG coordinates place pivot at y=225 in the 450-unit scene.
def hand(name,w,top,bottom,body,color,disc=None):
 h=bottom-top; im=Image.new('RGBA',(w,h)); d=ImageDraw.Draw(im)
 d.rectangle((w//2-body//2,0,w//2+(body-1)//2,h-1),fill=color)
 if disc:
  r,y=disc; d.ellipse((w//2-r,y-top-r,w//2+r,y-top+r),fill=color)
 im.save(p/(name+'.png'))
hand('hour',26,105,238,24,'#111111')
hand('minute',20,55,242,18,'#111111')
hand('second',34,34,270,5,'#d3232c',(16,48))
# A realistic static preview, 10:10:32.
from PIL import Image as I
out=I.open(p/'dial.png').convert('RGBA')
for name,ang,top,bottom,w in [('hour',305,105,238,26),('minute',60,55,242,20),('second',192,34,270,34)]:
 src=I.open(p/(name+'.png')); layer=I.new('RGBA',(450,450));layer.alpha_composite(src,(225-w//2,top));layer=layer.rotate(-ang,resample=I.Resampling.BICUBIC,center=(225,225));out.alpha_composite(layer)
out.save(p/'preview.png')
