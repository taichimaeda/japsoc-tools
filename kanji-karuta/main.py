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

URL = 'https://mojinavi.com/d/list-kanji-kanken-04'
SELCTOR = '.itiran tr td ruby a'
FONT = ImageFont.truetype('/System/Library/Fonts/ヒラギノ明朝 ProN.ttc', 500)
HEIGHT = 2480
WIDTH = 3508
SPLIT = 8
COORDS = [
    (WIDTH // 8, HEIGHT // 4),
    (WIDTH // 8 * 3, HEIGHT // 4),
    (WIDTH // 8 * 5, HEIGHT // 4),
    (WIDTH // 8 * 7, HEIGHT // 4),
    (WIDTH // 8, HEIGHT // 4 * 3),
    (WIDTH // 8 * 3, HEIGHT // 4 * 3),
    (WIDTH // 8 * 5, HEIGHT // 4 * 3),
    (WIDTH // 8 * 7, HEIGHT // 4 * 3),
]

req = requests.get(URL)
req.encoding = req.apparent_encoding
bs_obj = BeautifulSoup(req.text, 'html.parser')

items = [(elem.text, elem['href']) for elem in bs_obj.select(SELCTOR)]
random.shuffle(items)
items += [('', '') for _ in range((len(items) * -1) % SPLIT)]
chars = [char for (char, _) in items]
links = [urlparse(URL).netloc + path for (_, path) in items]

def draw_line(draw_obj, coords):
    draw_obj.line(coords, fill='black', width=2)

def draw_char(draw_obj, coord, char):
    draw_obj.text(coord, char, fill='black', font=FONT, anchor='mm')

def draw_grid(draw_obj, image_obj):
    draw_line(draw_obj, [(0, HEIGHT // 2), (WIDTH, HEIGHT // 2)])
    draw_line(draw_obj, [(WIDTH // 4, 0), (WIDTH // 4, HEIGHT)])
    draw_line(draw_obj, [(WIDTH // 4 * 2, 0), (WIDTH // 4 * 2, HEIGHT)])
    draw_line(draw_obj, [(WIDTH // 4 * 3, 0), (WIDTH // 4 * 3, HEIGHT)])
    image_obj = ImageOps.expand(image_obj, border=2, fill='black')

def add_offset(coord, offset):
    (x, y) = coord
    return (x - offset, y - offset)

def get_qr_image(data):
    qr_obj = qrcode.QRCode(version=4, border=4, box_size=15)
    qr_obj.add_data(data)
    qr_obj.make(fit=True)
    return qr_obj.make_image(fill_color='black', back_color='white')

def get_char_page_at(i):
    image_obj = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    draw_obj = ImageDraw.Draw(image_obj)
    draw_grid(draw_obj, image_obj)
    for j in range(SPLIT):
        draw_char(draw_obj, COORDS[j], chars[i * SPLIT + j])
    return image_obj

def get_qr_page_at(i):
    offset = get_qr_image('').size[0] // 2
    image_obj = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    draw_obj = ImageDraw.Draw(image_obj)
    draw_grid(draw_obj, image_obj)
    for j in range(SPLIT):
        image_obj.paste(get_qr_image(links[i * SPLIT + j]), add_offset(COORDS[j], offset))
    return image_obj

for i in range(len(items) // SPLIT):
    char_page = get_char_page_at(i)
    qr_page = get_qr_page_at(i)
    qr_page = qr_page.transpose(Image.FLIP_TOP_BOTTOM)
    char_page.save(f'./img/page{i + 1}-1.jpg', quality=95)
    qr_page.save(f'./img/page{i + 1}-2.jpg', quality=95)
