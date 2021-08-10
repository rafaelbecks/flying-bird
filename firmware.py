#!/usr/bin/env python
# -*- coding: utf-8 -*-

import skywriter
import signal

from pathlib import Path
from PIL import ImageFont

from screen_device import get_device
from luma.core.render import canvas
import time

import mido


codes = [
    "\ue900", "\ue901", "\ue902", "\ue903", "\ue904", "\ue905"
]

def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)


def splash_screen(screen):
    icon = make_font("icomoon.ttf", 80)
    title = make_font('bandeins.ttf', 11)

    with canvas(screen) as draw:
        draw.text((23, 11), text="\ue902", font=icon, fill="white")
        draw.text((5, 100), text="gesture midi controller   ", font=title, fill="white")
        draw.text((55, 112), text="v0.1   ", font=title, fill="white")
    time.sleep(2)

def midi_device_selection(screen, **kwargs): 
    kwargs["selected"] = 0
    kwargs['device-selected'] = False
    selected = 0   
    icon = make_font("icomoon.ttf", 64)
    selection = make_font('bandeins.ttf', 11)
    real_midi_outputs = filter(lambda x: 'Midi Through:' not in x,mido.get_output_names())
    midi_devices = list(set(real_midi_outputs))
    
    @skywriter.touch(2)
    def touch(position):
        if(kwargs["selected"]  != len(midi_devices) -1):
            kwargs["selected"]  += 1
        else:
            kwargs["selected"] = 0

    @skywriter.flick()
    def select(start,finnish):
        if(finnish == 'east'):
            kwargs['device-selected'] = True
  
    while kwargs['device-selected'] == False:
        with canvas(screen) as draw:
            draw.text((32, 3), text="\ue900", font=icon, fill="white")
            draw.rectangle((0,80 + (16 * kwargs["selected"]),128,65 + (16 * kwargs["selected"])), fill='white',width=128)
            
                    
            for index, item in enumerate(midi_devices):
                if(index == kwargs["selected"]):
                    color = 'black'
                else:
                    color = 'white'

                draw.text((10, 66 + (16 * index)), text=item[:item.index(':')] + '  ', font=selection, fill=color, stroke_fill='red')
                
                
def main_menu(screen, **kwargs):
    kwargs["selected"] = 0
    icon = make_font("icomoon.ttf", 45)
    random_icon = make_font("icomoon.ttf", 58)
    menu_item = make_font('bandeins.ttf', 12)
    kwargs['screen-active'] = True
    options = ['chords', 'arp', 'random']
    
    position = {
        'chords': (12,55,53,65),
        'arp': (86,55,107,66),
        'random': (44,119,87,128)
    }

    @skywriter.touch(2)
    def touch(position):
        if(kwargs["selected"]  != 2):
            kwargs["selected"]  += 1
        else:
            kwargs["selected"] = 0
    
    def color_selection(selection):
        if(kwargs['selected'] == selection):
            return 'black'
        else:   
            return 'white'
                      
    while kwargs['screen-active']:
        with canvas(screen) as draw:
            draw.rectangle(position[options[kwargs['selected']]], fill='white')
            draw.text((11, 5), text="\ue903", font=icon, fill='white' )
            draw.text((13, 53), text="chords  ", font=menu_item, fill=color_selection(0))
            draw.text((75, 5), text="\ue905", font=icon, fill="white")
            draw.text((87, 53), text="arp  ", font=menu_item, fill=color_selection(1))
            draw.text((36, 62), text="\ue904", font=random_icon, fill="white")
            draw.text((44, 116), text="random  ", font=menu_item, fill=color_selection(2))


if __name__ == "__main__":
    try:
        screen = get_device()
        splash_screen(screen)
        midi_device_selection(screen)
        main_menu(screen)
    except KeyboardInterrupt:
        pass

signal.pause()