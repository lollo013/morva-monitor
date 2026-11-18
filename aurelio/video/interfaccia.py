"""Sovrappone un'interfaccia generica tipo TikTok (senza marchi) per controllare l'area sicura."""
import sys
from PIL import Image, ImageDraw, ImageFont
F = '/usr/share/fonts/opentype/inter/'
def ui(im):
    im = im.convert('RGBA'); W, H = im.size
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((0, 0, W, 200), fill=(0, 0, 0, 70))
    f = ImageFont.truetype(F + 'Inter-SemiBold.otf', 44)
    d.text((300, 90), 'Seguiti', font=f, fill=(255, 255, 255, 170)); d.text((560, 90), 'Per te', font=f, fill=(255, 255, 255, 255))
    d.line((575, 150, 690, 150), fill=(255, 255, 255, 255), width=5)
    for i, y in enumerate((980, 1150, 1310, 1470, 1630)):
        d.ellipse((960, y, 1060, y + 100), fill=(30, 30, 30, 150), outline=(255, 255, 255, 230), width=4)
        if i: d.text((978, y + 108), ['', '1,2 M', '8.402', '3.511', '9.870'][i], font=ImageFont.truetype(F + 'Inter-SemiBold.otf', 26), fill=(255, 255, 255, 255))
    d.rectangle((0, 1540, W, 1920), fill=(0, 0, 0, 90))
    g = ImageFont.truetype(F + 'Inter-SemiBold.otf', 40); h = ImageFont.truetype(F + 'Inter-Medium.otf', 34)
    d.text((40, 1580), '@professoreaurelio', font=g, fill=(255, 255, 255, 255))
    d.text((40, 1640), 'Il token pirata spiegato facile #scuola #curiosità', font=h, fill=(255, 255, 255, 235))
    d.text((40, 1690), '♫ suono originale', font=h, fill=(255, 255, 255, 210))
    d.rectangle((0, 1800, W, 1920), fill=(0, 0, 0, 210))
    d.rectangle((SX := 60, 230, 900, 1480), outline=(0, 255, 140, 200), width=4)
    return Image.alpha_composite(im, lay).convert('RGB')
if __name__ == '__main__':
    S = sys.argv[1]; ts = sys.argv[2].split(',')
    ims = [ui(Image.open(f'{S}/quadro-{t}.png')).resize((270, 480)) for t in ts]
    m = Image.new('RGB', (len(ims) * 275, 485), (80, 80, 80))
    for i, x in enumerate(ims): m.paste(x, (i * 275, 0))
    m.save(f'{S}/area-sicura.png')
