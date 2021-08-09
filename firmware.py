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
    time.sleep(3)

def midi_device_selection(screen, **kwargs): 
    kwargs["selected"] = 0
    kwargs['device-selected'] = False
    selected = 0   
    icon = make_font("icomoon.ttf", 64)
    selection = make_font('bandeins.ttf', 11)
    real_midi_outputs = filter(lambda x: 'Midi Through:' not in x,mido.get_output_names())
    midi_devices = list(set(real_midi_outputs))
    
    @skywriter.touch(selected)
    def touch(position):
        print(kwargs["selected"] )
        if(kwargs["selected"]  != len(midi_devices) -1):
            kwargs["selected"]  += 1
        else:
            kwargs["selected"] = 0

    @skywriter.double_tap()
    def doubletap(position):
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
    icon = make_font("icomoon.ttf", 45)
    random_icon = make_font("icomoon.ttf", 58)
    while True:
        with canvas(screen) as draw:
            draw.text((11, 9), text="\ue903", font=icon, fill="white")
            draw.text((75, 9), text="\ue905", font=icon, fill="white")
            draw.text((36, 65), text="\ue904", font=random_icon, fill="white")


if __name__ == "__main__":
    try:
        screen = get_device()
        splash_screen(screen)
        midi_device_selection(screen)
        main_menu(screen)
    except KeyboardInterrupt:
        pass

signal.pause()