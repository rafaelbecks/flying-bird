#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import ImageFont
from pathlib import Path
import time
from luma.core.render import canvas

icons = {
    'bird': "\ue902",
    'device': "\ue900",
    'chords': "\ue903",
    'arp': "\ue905",
    "random": "\ue904"

}


def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)


menu_position = {
    'chords': (12, 55, 49, 65),
    'arp': (78, 55, 120, 66),
    'random': (43, 119, 88, 128)
}


def color_selection(selection, selected):
    if(selected == selection):
        return 'black'
    else:
        return 'white'


def splash_screen(screen):
    icon = make_font("icomoon.ttf", 80)
    title = make_font('bandeins.ttf', 11)

    with canvas(screen) as draw:
        draw.text((23, 11), text=icons['bird'], font=icon, fill="white")
        draw.text((5, 100), text="gesture midi controller   ",
                  font=title, fill="white")
        draw.text((55, 112), text="v0.1   ", font=title, fill="white")
    time.sleep(2)
    
    
def center_text_x(text):
    return (128 - len(text)) / 2