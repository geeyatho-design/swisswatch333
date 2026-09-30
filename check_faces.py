"""Offline structural checks and previews of the actual WFF image/transform nodes.

This is not a Wear OS emulator or a battery measurement.
"""
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'review'
OUT.mkdir(exist_ok=True)


def render(module, theme='dark', seconds=False, ambient=False, hour=10, minute=10, second=32):
    res = ROOT/module/'src/main/res'
    root = ET.parse(res/'raw/watchface.xml').getroot()
    palette = ['#000000', '#c8c8c8', '#dedede']
    config = root.find('UserConfigurations')
    if config is not None:
        options = config.find('ColorConfiguration')
        palette = next(o.get('colors').split() for o in options if o.get('id') == theme)

    def color(value):
        if value.startswith('[CONFIGURATION.theme.'):
            return palette[int(value.split('.')[-1][:-1])]
        return value

    def attrs(node):
        a = dict(node.attrib)
        if ambient:
            for v in node.findall('Variant'):
                a[v.get('target')] = v.get('value')
        return a

    scene = root.find('Scene')
    canvas = Image.new('RGBA', (450, 450), color(attrs(scene).get('backgroundColor', '#000000')))
    visible_sources = set()
    pivots = []

    def visit(node):
        if node.tag in ('Variant', 'Transform', 'Image'):
            return
        if node.tag == 'BooleanConfiguration':
            option = node.find(f"BooleanOption[@id='{'TRUE' if seconds else 'FALSE'}']")
            if option is not None:
                for child in option:
                    visit(child)
            return
        if node.tag != 'PartImage':
            raise AssertionError('Unsupported renderer node: '+node.tag)
        a = attrs(node)
        if int(a.get('alpha', 255)) == 0:
            return
        p = res/'drawable-nodpi'/(node.find('Image').get('resource')+'.png')
        image = Image.open(p).convert('RGBA')
        w, h = int(a['width']), int(a['height'])
        assert image.size == (w, h), (p, image.size, (w, h))
        if 'tintColor' in a:
            tinted = Image.new('RGBA', image.size, color(a['tintColor']))
            tinted.putalpha(image.getchannel('A'))
            image = tinted
        x, y = int(a['x']), int(a['y'])
        transform = node.find('Transform')
        angle = 0
        if transform is not None:
            expr = transform.get('value')
            visible_sources.update(re.findall(r'\[([^]]+)\]', expr))
            expr = expr.replace('[HOUR_0_11]', str(hour%12)).replace('[MINUTE]', str(minute)).replace('[SECOND]', str(second))
            assert re.fullmatch(r'[0-9.+* ()-]+', expr)
            angle = eval(expr, {'__builtins__': {}}, {})
            cx = x+float(a['pivotX'])*w
            cy = y+float(a['pivotY'])*h
            assert abs(cx-225)<0.0001 and abs(cy-225)<0.0001, (cx, cy)
            pivots.append((node.find('Image').get('resource'), angle))
        layer = Image.new('RGBA', (450, 450))
        layer.alpha_composite(image, (x, y))
        canvas.alpha_composite(layer.rotate(-angle, Image.Resampling.BICUBIC, center=(225, 225)))
    for node in scene:
        visit(node)
    return canvas.convert('RGB'), visible_sources, pivots


states = [('Dark / seconds off', 'app', 'dark', False, False),
          ('Light / seconds off', 'app', 'light', False, False),
          ('Dark / seconds on', 'app', 'dark', True, False),
          ('Always-on display', 'app', 'light', True, True),
          ('Rail Dial AOD 1.0.1', 'aod', 'dark', False, False)]
images = []
for label, module, theme, seconds, ambient in states:
    image, sources, _ = render(module, theme, seconds, ambient)
    assert ('SECOND' in sources) == (module == 'app' and seconds and not ambient)
    if ambient or module == 'aod':
        lit = sum(max(pixel) > 0 for pixel in image.getdata())
        coverage = lit / (3.141592653589793 * 225 * 225)
        assert coverage < 0.15, coverage
        print(f'{label}: lit-pixel coverage {coverage:.2%}')
    images.append((label, image))
    image.save(OUT/(module+'-'+theme+('-ambient' if ambient else '-active')+('-seconds' if seconds else '')+'.jpg'), quality=95)
    if module == 'app' and theme == 'dark' and not seconds and not ambient:
        image.save(ROOT/'app/src/main/res/drawable-nodpi/preview.png')
    if module == 'aod':
        image.save(ROOT/'aod/src/main/res/drawable-nodpi/preview.png')

for module in ('app', 'aod'):
    a, _, _ = render(module, second=0)
    b, _, _ = render(module, second=59)
    assert ImageChops.difference(a, b).getbbox() is None
    c, _, angles = render(module, hour=3, minute=30)
    assert [angle for _, angle in angles] == [105, 180], angles
    assert ImageChops.difference(a, c).getbbox() is not None
for theme in ('light', 'dark'):
    a, _, _ = render('app', theme, False, True)
    b, _, _ = render('app', theme, True, True)
    c, _, _ = render('aod')
    assert ImageChops.difference(a, b).getbbox() is None
    assert ImageChops.difference(a, c).getbbox() is None

sheet = Image.new('RGB', (450*3, 490*2), '#252525')
draw = ImageDraw.Draw(sheet)
for i, (label, image) in enumerate(images):
    x, y = (i%3)*450, (i//3)*490
    sheet.paste(image, (x, y+32))
    draw.text((x+12, y+10), label, fill='white')
sheet.save(OUT/'rail-dial-1.1.0-review.jpg', quality=95)
print('PASS: configuration branches, ambient invariance, clock pivots, minute-only default updates.')
