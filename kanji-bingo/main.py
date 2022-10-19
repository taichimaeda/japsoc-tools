# brew install imagemagick
# pip install beautifulsoup4
# pip install Pillow

import requests
import random
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

URL = 'https://mojinavi.com/d/list-kanji-kanken-08'
SELECTOR = '.itiran tr td ruby a'
FONT = ImageFont.truetype('/System/Library/Fonts/ヒラギノ明朝 ProN.ttc', 300)
NUM_CARDS = 10
PAGE_HEIGHT = 3508 // 2
PAGE_WIDTH = 2480
BOX_COLS = 3
BOX_ROWS = 3
BOX_SIZE = PAGE_HEIGHT - 400
BOX_CENTER_X = PAGE_WIDTH / 2
BOX_CENTER_Y = PAGE_HEIGHT / 2
BOX_X_START = BOX_CENTER_X - BOX_SIZE / 2
BOX_X_END = BOX_CENTER_X + BOX_SIZE / 2
BOX_Y_START = BOX_CENTER_Y - BOX_SIZE / 2
BOX_Y_END = BOX_CENTER_Y + BOX_SIZE / 2

req = requests.get(URL)
req.encoding = req.apparent_encoding
bs_obj = BeautifulSoup(req.text, 'html.parser')
chars = [elem.text for elem in bs_obj.select(SELECTOR)]

def draw_line(draw, coords):
    draw.line(coords, fill='black', width=2)

def draw_char(draw, coord, char):
    draw.text(coord, char, fill='black', font=FONT, anchor='mm')

def draw_box(draw):
    for r in range(BOX_ROWS + 1):
        draw_line(draw, [
            (BOX_X_START, BOX_Y_START + BOX_SIZE / 3 * r),
            (BOX_X_END, BOX_Y_START + BOX_SIZE / 3 * r)
        ])
    for c in range(BOX_COLS + 1):
        draw_line(draw, [
            (BOX_X_START + BOX_SIZE / 3 * c, BOX_Y_START),
            (BOX_X_START + BOX_SIZE / 3 * c, BOX_Y_END),
        ])

def get_card_at(i):
    image = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), color='white')
    draw = ImageDraw.Draw(image)
    draw_box(draw)
    for r in range(BOX_ROWS):
        for c in range(BOX_COLS):
            draw_char(draw, (
                BOX_X_START + BOX_SIZE / BOX_COLS * (c + 0.5),
                BOX_Y_START + BOX_SIZE / BOX_ROWS * (r + 0.5),
            ), chars[3 * r + c])
    return image

for i in range(NUM_CARDS // 2):
    random.shuffle(chars)
    card1 = get_card_at(i)
    card2 = get_card_at(i + 1)
    dest = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT * 2), color='white')
    dest.paste(card1, (0, 0))
    dest.paste(card2, (0, PAGE_HEIGHT))
    draw_line(ImageDraw.Draw(dest), [(0, PAGE_HEIGHT), (PAGE_WIDTH, PAGE_HEIGHT)])
    dest.save(f'./img/page{i + 1}.jpg', quality=95)
