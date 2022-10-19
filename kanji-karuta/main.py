# brew install imagemagick
# pip install beautifulsoup4
# pip install Pillow
# pip install qrcode

import requests
import random
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageOps
import qrcode

URL = 'https:/mojinavi.com/d/list-kanji-kanken-04'
SELECTOR = '.itiran tr td ruby a'
FONT = ImageFont.truetype('/System/Library/Fonts/ヒラギノ明朝 ProN.ttc', 500)
PAGE_HEIGHT = 2480
PAGE_WIDTH = 3508
GRID_SPLIT = 8
GRID_COORDS = [
    (PAGE_WIDTH / 8 * 1, PAGE_HEIGHT / 4),
    (PAGE_WIDTH / 8 * 3, PAGE_HEIGHT / 4),
    (PAGE_WIDTH / 8 * 5, PAGE_HEIGHT / 4),
    (PAGE_WIDTH / 8 * 7, PAGE_HEIGHT / 4),
    (PAGE_WIDTH / 8 * 1, PAGE_HEIGHT / 4 * 3),
    (PAGE_WIDTH / 8 * 3, PAGE_HEIGHT / 4 * 3),
    (PAGE_WIDTH / 8 * 5, PAGE_HEIGHT / 4 * 3),
    (PAGE_WIDTH / 8 * 7, PAGE_HEIGHT / 4 * 3),
]

req = requests.get(URL)
req.encoding = req.apparent_encoding
bs_obj = BeautifulSoup(req.text, 'html.parser')

items = [(elem.text, elem['href']) for elem in bs_obj.select(SELECTOR)]
random.shuffle(items)
items += [('', '') for _ in range((len(items) * -1) % GRID_SPLIT)]
chars = [char for (char, _) in items]
links = [urlparse(URL).netloc + path for (_, path) in items]

def draw_line(draw, coords):
    draw.line(coords, fill='black', width=2)

def draw_char(draw, coord, char):
    draw.text(coord, char, fill='black', font=FONT, anchor='mm')

def draw_grid(draw, image):
    draw_line(draw, [(0, PAGE_HEIGHT / 2), (PAGE_WIDTH, PAGE_HEIGHT / 2)])
    draw_line(draw, [(PAGE_WIDTH / 4, 0), (PAGE_WIDTH / 4, PAGE_HEIGHT)])
    draw_line(draw, [(PAGE_WIDTH / 4 * 2, 0), (PAGE_WIDTH / 4 * 2, PAGE_HEIGHT)])
    draw_line(draw, [(PAGE_WIDTH / 4 * 3, 0), (PAGE_WIDTH / 4 * 3, PAGE_HEIGHT)])
    image = ImageOps.expand(image, border=2, fill='black')

def get_char_page_at(i):
    image = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), color='white')
    draw = ImageDraw.Draw(image)
    draw_grid(draw, image)
    for j in range(GRID_SPLIT):
        draw_char(draw, GRID_COORDS[j], chars[i * GRID_SPLIT + j])
    return image

def get_qr_image(data):
    qr = qrcode.QRCode(version=4, border=4, box_size=15)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color='black', back_color='white')

def get_qr_page_at(i):
    offset = get_qr_image('').size[0] / 2
    image = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), color='white')
    draw = ImageDraw.Draw(image)
    draw_grid(draw, image)
    for j in range(GRID_SPLIT):
        (x, y) = GRID_COORDS[j]
        image.paste(get_qr_image(links[GRID_SPLIT * i + j]), (x - offset, y - offset))
    return image

for i in range(len(items) // GRID_SPLIT):
    char_page = get_char_page_at(i)
    qr_page = get_qr_page_at(i)
    qr_page = qr_page.transpose(Image.FLIP_TOP_BOTTOM)
    char_page.save(f'./img/page{i + 1}-1.jpg', quality=95)
    qr_page.save(f'./img/page{i + 1}-2.jpg', quality=95)
