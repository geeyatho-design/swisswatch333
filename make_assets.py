"""Deterministic watch artwork, including a low-power ambient dial."""
from pathlib import Path
from math import sin, cos, pi
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'app/src/main/res/drawable-nodpi'
OUT.mkdir(parents=True, exist_ok=True)
SCALE = 4
SIZE = 450
CENTER = 225

def save_scaled(image, name, size):
    image.resize(size, Image.Resampling.LANCZOS).save(OUT / (name + '.png'))

def dial(name, ambient=False):
    image = Image.new('RGBA', (SIZE*SCALE, SIZE*SCALE), '#000000' if ambient else '#f7f7f4')
    draw = ImageDraw.Draw(image)
    if not ambient:
        draw.ellipse(tuple(v*SCALE for v in (5,5,445,445)), outline='#151515', width=5*SCALE)
    for index in range(60):
        if ambient and index % 5:
            continue
        angle = 2*pi*index/60-pi/2
        inner = 182 if ambient else (169 if index%5 == 0 else 184)
        outer = 208
        width = 4 if ambient else (12 if index%5 == 0 else 3)
        points = [(CENTER+radius*cos(angle), CENTER+radius*sin(angle)) for radius in (inner,outer)]
        draw.line([(round(x*SCALE),round(y*SCALE)) for x,y in points], fill='#a0a0a0' if ambient else '#121212',width=width*SCALE)
    save_scaled(image, name, (SIZE,SIZE))

def hand(name,width,top,bottom,body,color,disc=None):
    height=bottom-top
    image=Image.new('RGBA',(width*SCALE,height*SCALE))
    draw=ImageDraw.Draw(image)
    left=(width-body)/2
    draw.rectangle((int(left*SCALE),0,int((left+body)*SCALE)-1,height*SCALE-1),fill=color)
    if disc:
        radius,y=disc
        box=((width/2-radius)*SCALE,(y-top-radius)*SCALE,(width/2+radius)*SCALE,(y-top+radius)*SCALE)
        draw.ellipse(box,fill=color)
    save_scaled(image,name,(width,height))

dial('dial')
dial('dial_ambient',True)
hand('hour',26,105,238,24,'#111111')
hand('minute',20,55,242,18,'#111111')
# The disc fits entirely inside the image; earlier artwork clipped its top.
hand('second',36,30,270,5,'#d3232c',(16,48))
hand('hour_ambient',26,105,238,5,'#b0b0b0')
hand('minute_ambient',20,55,242,4,'#b0b0b0')
for ambient in (False,True):
    canvas=Image.open(OUT/('dial_ambient.png' if ambient else 'dial.png')).convert('RGBA')
    layers=[('hour',305.2666667,105,26),('minute',63.2,55,20)]
    if not ambient:
        layers.append(('second',192,30,36))
    for name,angle,top,width in layers:
        asset=Image.open(OUT/(name+('_ambient' if ambient else '')+'.png'))
        layer=Image.new('RGBA',(SIZE,SIZE))
        layer.alpha_composite(asset,(CENTER-width//2,top))
        canvas.alpha_composite(layer.rotate(-angle,resample=Image.Resampling.BICUBIC,center=(CENTER,CENTER)))
    canvas.save(OUT/('preview_ambient.png' if ambient else 'preview.png'))
    canvas.convert('RGB').save(ROOT/('preview_ambient.jpg' if ambient else 'preview.jpg'),quality=95)
