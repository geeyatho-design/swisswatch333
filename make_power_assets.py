"""Build minute-based hands and theme masks from the original Rail Dial artwork."""
from pathlib import Path
from math import sin, cos, pi
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
APP = ROOT / 'app/src/main/res/drawable-nodpi'
AOD = ROOT / 'aod/src/main/res/drawable-nodpi'
SIZE, CENTER, SCALE = 450, 225, 4


def cropped_hand(source, name, x, y, white=False):
    image = Image.open(APP / (source + '.png')).convert('RGBA')
    if white:
        mask = image.getchannel('A')
        image = Image.new('RGBA', image.size, 'white')
        image.putalpha(mask)
    left, top, right, bottom = image.getchannel('A').getbbox()
    image = image.crop((left, top, right, bottom))
    image.save(APP / (name + '.png'))
    if not white:
        image.save(AOD / (name + '.png'))
    x, y = x + left, y + top
    return dict(resource=name, x=x, y=y, width=image.width, height=image.height,
                pivotX=(CENTER-x)/image.width, pivotY=(CENTER-y)/image.height)


def part(hand, expression, tint=None, ambient=None):
    attrs = ' '.join(f'{k}="{v:.9g}"' if isinstance(v, float) else f'{k}="{v}"'
                     for k, v in hand.items() if k != 'resource')
    if tint:
        attrs += f' tintColor="{tint}"'
    if ambient is True:
        attrs += ' alpha="0"'
    lines = [f'    <PartImage {attrs}>']
    if ambient is not None:
        lines.append(f'      <Variant mode="AMBIENT" target="alpha" value="{255 if ambient else 0}" />')
    lines += [f'      <Transform target="angle" value="{expression}" />',
              f'      <Image resource="{hand["resource"]}" />', '    </PartImage>']
    return '\n'.join(lines)


mask = Image.new('RGBA', (SIZE*SCALE, SIZE*SCALE))
draw = ImageDraw.Draw(mask)
draw.ellipse(tuple(v*SCALE for v in (5, 5, 445, 445)), outline='white', width=5*SCALE)
for index in range(60):
    angle = 2*pi*index/60-pi/2
    inner, outer = (169 if index % 5 == 0 else 184), 208
    width = 12 if index % 5 == 0 else 3
    points = [(round((CENTER+r*cos(angle))*SCALE), round((CENTER+r*sin(angle))*SCALE))
              for r in (inner, outer)]
    draw.line(points, fill='white', width=width*SCALE)
mask.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(APP/'dial_mask.png')

hour = cropped_hand('hour', 'hour_mask', 212, 105, white=True)
minute = cropped_hand('minute', 'minute_mask', 215, 55, white=True)
hour_aod = cropped_hand('hour_ambient', 'hour_ambient_compact', 212, 105)
minute_aod = cropped_hand('minute_ambient', 'minute_ambient_compact', 215, 55)
hour_expression = '[HOUR_0_11] * 30 + [MINUTE] * 0.5'
minute_expression = '[MINUTE] * 6'
classic = '''<WatchFace width="450" height="450">
  <Metadata key="CLOCK_TYPE" value="ANALOG" />
  <UserConfigurations>
    <ColorConfiguration id="theme" displayName="theme_label" defaultValue="dark">
      <ColorOption id="dark" displayName="dark_label" colors="#000000 #c8c8c8 #dedede" />
      <ColorOption id="light" displayName="light_label" colors="#f7f7f4 #121212 #111111" />
    </ColorConfiguration>
    <BooleanConfiguration id="seconds" displayName="seconds_label" defaultValue="FALSE" />
  </UserConfigurations>
  <Scene backgroundColor="[CONFIGURATION.theme.0]">
    <Variant mode="AMBIENT" target="backgroundColor" value="#000000" />
    <!-- Static backgrounds precede moving hands, allowing layer reuse. -->
    <PartImage x="0" y="0" width="450" height="450" tintColor="[CONFIGURATION.theme.1]">
      <Variant mode="AMBIENT" target="alpha" value="0" />
      <Image resource="dial_mask" />
    </PartImage>
    <PartImage x="0" y="0" width="450" height="450" alpha="0">
      <Variant mode="AMBIENT" target="alpha" value="255" />
      <Image resource="dial_ambient" />
    </PartImage>
    <!-- Integer minute/hour sources intentionally avoid sub-minute work. -->
'''
classic += part(hour, hour_expression, '[CONFIGURATION.theme.2]', False) + '\n'
classic += part(minute, minute_expression, '[CONFIGURATION.theme.2]', False) + '\n'
classic += part(hour_aod, hour_expression, ambient=True) + '\n'
classic += part(minute_aod, minute_expression, ambient=True) + '\n'
classic += '''    <!-- The second dependency exists only in the opted-in branch. -->
    <BooleanConfiguration id="seconds">
      <BooleanOption id="TRUE">
        <PartImage x="207" y="30" width="36" height="240" pivotX="0.5" pivotY="0.8125">
          <Variant mode="AMBIENT" target="alpha" value="0" />
          <Transform target="angle" value="[SECOND] * 6" />
          <Image resource="second" />
        </PartImage>
      </BooleanOption>
    </BooleanConfiguration>
  </Scene>
</WatchFace>
'''
(ROOT/'app/src/main/res/raw/watchface.xml').write_text(classic)

ambient = '''<WatchFace width="450" height="450">
  <Metadata key="CLOCK_TYPE" value="ANALOG" />
  <Scene backgroundColor="#000000">
    <PartImage x="0" y="0" width="450" height="450"><Image resource="dial_ambient" /></PartImage>
    <!-- No seconds, animation, or sensor sources in either display mode. -->
'''
ambient += part(hour_aod, hour_expression) + '\n'
ambient += part(minute_aod, minute_expression) + '\n'
ambient += '  </Scene>\n</WatchFace>\n'
(ROOT/'aod/src/main/res/raw/watchface.xml').write_text(ambient)
print('Generated theme masks, cropped hands, and minute-based watch face definitions.')
