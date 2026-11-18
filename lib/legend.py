import os
import hashlib
import xbmcvfs

from pathlib import Path

from . import config
from . import utils
from . import conv

# Map legends
#
# Drawn once per layer / unit / language and cached, then exposed as Map.N.Legend.
# The image is a horizontal strip (2x the 1400x60 slot skins typically reserve).

VERSION = 1
HEIGHT  = 120
PAD     = 22
BAR     = (16, 54)
LABELY  = 62
PANEL   = (255, 255, 255, 215)
TEXT    = (34, 34, 34, 255)
BORDER  = (120, 120, 120, 255)
LAND    = (242, 239, 233)

# weather.gc.ca GDPS_15km_AirTemp_2m (°C), sampled from its WMS GetLegendGraphic
TEMP = [ (-40.0, '00007f'), (-37.5, '000096'), (-35.0, '0000b4'), (-32.5, '0000ce'), (-30.0, '0000ec'), (-27.5, '001af4'), (-25.0, '003cfc'), (-22.5, '0065fd'), (-20.0, '008ffd'), (-17.5, '00b5fd'), (-15.0, '00dffd'), (-12.5, '15efcc'), (-10.0, '2ffa90'), (-7.5, '4ffc86'), (-5.0, '74fc86'), (-2.5, '93fc6a'), (0.0, 'b7fd46'), (2.5, 'd6fd27'), (5.0, 'fbfe03'), (7.5, 'fedf00'), (10.0, 'fdbd00'), (12.5, 'fd9b00'), (15.0, 'fd7900'), (17.5, 'fd5700'), (20.0, 'fd3500'), (22.5, 'f71d00'), (25.0, 'ef0200'), (27.5, 'd70000'), (30.0, 'b90000'), (32.5, '9d0000'), (35.0, '810000'), (37.5, '6b0000'), (40.0, '560000') ]

# weather.gc.ca GDPS_15km_WindSpeed_10m (kt), sampled from its WMS GetLegendGraphic
WIND = [ (0.0, '00007f'), (2.5, '0000a4'), (5.0, '0000ca'), (7.5, '0017e8'), (10.0, '0036fd'), (12.5, '0074fd'), (15.0, '03affa'), (17.5, '0ae8f3'), (20.0, '28fcd5'), (22.5, '5efc9f'), (25.0, '90fc6d'), (27.5, 'c2fd3b'), (30.0, 'e2eb1b'), (32.5, 'fdd400'), (35.0, 'fd9f00'), (37.5, 'fd7100'), (40.0, 'fd3b00'), (42.5, 'f01800'), (45.0, 'd50700'), (47.5, 'b10000'), (50.0, '850000'), (52.5, '6d0000'), (55.0, '550000') ]

# rainviewer.com "Universal Blue" (dBZ, RGBA), the only scheme the public API serves
RAIN = [ (0, '827b6949'), (5, '92887164'), (10, 'cec08796'), (14, 'ded097be'), (15, '88ddeeff'), (20, '00a3e0ff'), (25, '0077aaff'), (30, '005588ff'), (34, '004768ff'), (35, 'ffee00ff'), (40, 'ffaa00ff'), (44, 'ff8100ff'), (45, 'ff4400ff'), (50, 'c10000ff'), (54, '5d0000ff'), (55, 'ffaaffff'), (60, 'ff77ffff') ]
SNOW = [ (0, 'c7ffff7f'), (5, 'c3ffffbf'), (10, 'bfffffff'), (15, '9fdfffff'), (20, '7fbfffff'), (25, '5f9fffff'), (30, '4f8fffff'), (35, '3f7fffff'), (40, '2f6fffff'), (45, '1f5fffff'), (50, '0f4fffff') ]

# Beaufort scale lower limits (km/h), see conv.beaufort()
BEAUFORT = [ 1.0, 5.6, 12.0, 20.0, 29.0, 39.0, 50.0, 62.0, 75.0, 89.0, 103.0, 118.0 ]

KT = 1.852


def get(layer):
	try:
		spec = _spec(layer)

		if not spec:
			return ''

		key  = hashlib.md5(repr((VERSION, layer, spec)).encode('utf-8')).hexdigest()[:10]
		dir  = Path(config.addon_cache)
		file = dir / f'legend_{layer}_{key}.png'

		if not file.is_file():
			os.makedirs(dir, exist_ok=True)

			for old in dir.glob(f'legend_{layer}_*.png'):
				old.unlink()

			_draw(spec, file)
			utils.log(f'Legend created: {file.name}', 3)

		return str(file)

	except Exception as e:
		utils.log(f'Legend {layer}: {e}', 2)
		return ''


### SPECS
def _spec(layer):

	if layer == 'gctemp':
		unit = conv.temp()
		f    = lambda c: conv.tempraw(c, unit)
		return ( 1500, [ ( unit, _stops(TEMP), -40.0, 40.0, _ticks(f, -40.0, 40.0) ) ] )

	elif layer == 'gcwind':
		unit = conv.speed()
		lo   = 0.0
		hi   = 55.0 * KT

		if unit.lower() == 'beaufort':
			ticks = [ ((v - lo) / (hi - lo), str(i + 1)) for i, v in enumerate(BEAUFORT) if v <= hi ]
			title = utils.locaddon(32369)
		else:
			ticks = _ticks(lambda k: conv.speedraw(k, unit), lo, hi)
			title = unit

		return ( 1500, [ ( title, [ (v * KT, c) for v, c in _stops(WIND) ], lo, hi, ticks ) ] )

	elif layer == 'rvradar':
		light    = utils.locaddon(32402)
		moderate = utils.locaddon(32403)
		heavy    = utils.locaddon(32404)
		extreme  = utils.locaddon(32405)

		rain = ( utils.locaddon(32212), _stops(RAIN), 0, 60,
		         [ (0.08, utils.locaddon(32207)), (0.33, light), (0.55, moderate), (0.75, heavy), (0.95, extreme) ] )
		snow = ( utils.locaddon(32217), _stops(SNOW), 0, 50,
		         [ (0.1, light), (0.5, moderate), (0.9, heavy) ] )

		return ( 2200, [ rain, snow ] )

	return None


def _stops(table):
	return tuple( (float(v), tuple(int(c[i:i + 2], 16) for i in range(0, len(c), 2))) for v, c in table )


def _ticks(f, lo, hi, target=8):
	a, b  = f(lo), f(hi)
	vmin  = min(a, b)
	vmax  = max(a, b)
	span  = vmax - vmin
	step  = 1.0

	for mag in [ 10 ** e for e in range(-1, 7) ]:
		for m in ( 1, 2, 2.5, 5 ):
			step = m * mag
			if span / step <= target:
				break
		else:
			continue
		break

	ticks = []
	value = -(-vmin // step) * step

	while value <= vmax + 1e-9:
		label = f'{value:g}' if step >= 1 else f'{value:.1f}'
		ticks.append( (round((value - a) / (b - a), 4), label) )
		value += step

	return sorted(ticks)


### DRAW
def _draw(spec, file):
	from PIL import Image, ImageDraw, ImageFont

	width, bars = spec

	try:
		FONT  = xbmcvfs.translatePath('special://xbmc/media/Fonts/arial.ttf')
		font  = ImageFont.truetype(FONT, 38)
		title = ImageFont.truetype(FONT, 44)
	except Exception:
		font  = title = ImageFont.load_default()

	image = Image.new('RGBA', (width, HEIGHT), (0, 0, 0, 0))
	draw  = ImageDraw.Draw(image)

	try:
		draw.rounded_rectangle([0, 0, width - 1, HEIGHT - 1], radius=18, fill=PANEL)
	except AttributeError:
		draw.rectangle([0, 0, width - 1, HEIGHT - 1], fill=PANEL)

	part = (width - PAD * 2) / len(bars)

	for idx, bar in enumerate(bars):
		x0 = PAD + idx * part + (20 if idx else 0)
		x1 = PAD + (idx + 1) * part - (20 if idx < len(bars) - 1 else 0)
		_bar(draw, int(x0), int(x1), bar, font, title)

	image.save(file)


def _bar(draw, x0, x1, bar, font, titlefont):
	name, stops, lo, hi, ticks = bar

	draw.text((x0, (HEIGHT - 44) // 2 - 6), name, font=titlefont, fill=TEXT)
	bx0 = x0 + _width(draw, name, titlefont) + 20
	bx1 = x1

	for x in range(bx0, bx1):
		value = lo + (x - bx0) / max(1, bx1 - bx0 - 1) * (hi - lo)
		draw.line([(x, BAR[0]), (x, BAR[1])], fill=_colour(stops, value))

	draw.rectangle([bx0, BAR[0], bx1 - 1, BAR[1]], outline=BORDER, width=2)

	for pos, label in ticks:
		if pos < -0.001 or pos > 1.001:
			continue

		x = bx0 + pos * (bx1 - bx0 - 1)
		w = _width(draw, label, font)
		draw.line([(x, BAR[1]), (x, BAR[1] + 6)], fill=TEXT, width=2)
		draw.text((min(max(x - w / 2, bx0 - 4), bx1 - w + 4), LABELY), label, font=font, fill=TEXT)


def _colour(stops, value):
	if value <= stops[0][0]:
		c = stops[0][1]
	elif value >= stops[-1][0]:
		c = stops[-1][1]
	else:
		for (v0, c0), (v1, c1) in zip(stops, stops[1:]):
			if v0 <= value <= v1:
				k = (value - v0) / (v1 - v0)
				c = tuple(round(a + (b - a) * k) for a, b in zip(c0, c1))
				break

	# Translucent colours (radar) are shown over a light map background
	if len(c) == 4:
		k = c[3] / 255.0
		c = tuple(round(LAND[i] * (1 - k) + c[i] * k) for i in range(3))

	return tuple(c[:3]) + (255,)


def _width(draw, text, font):
	try:
		return draw.textbbox((0, 0), text, font=font)[2]
	except AttributeError:
		return draw.textsize(text, font=font)[0]
