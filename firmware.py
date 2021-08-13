#!/usr/bin/env python
# -*- coding: utf-8 -*-

import skywriter
import signal


from screen_device import get_device
from ui import icons, make_font, menu_position, color_selection, splash_screen
from luma.core.render import canvas

import mido

def midi_device_selection(screen, **kwargs):
    kwargs["selected"] = 0
    kwargs['device-selected'] = False
    selected = 0
    icon = make_font("icomoon.ttf", 64)
    selection = make_font('bandeins.ttf', 11)
    real_midi_outputs = filter(
        lambda x: 'Midi Through:' not in x, mido.get_output_names())
    midi_devices = list(set(real_midi_outputs))

    @skywriter.touch(2)
    def touch(position):
        if(kwargs["selected"] != len(midi_devices) - 1):
            kwargs["selected"] += 1
        else:
            kwargs["selected"] = 0

    @skywriter.flick()
    def select(start, finnish):
        if(finnish == 'east'):
            kwargs['device-selected'] = True

    while kwargs['device-selected'] == False:
        with canvas(screen) as draw:
            draw.text((32, 3), text=icons['device'], font=icon, fill="white")
            draw.rectangle((0, 80 + (16 * kwargs["selected"]), 128, 65 + (
                16 * kwargs["selected"])), fill='white', width=128)

            for index, item in enumerate(midi_devices):
                if(index == kwargs["selected"]):
                    color = 'black'
                else:
                    color = 'white'

                draw.text((10, 66 + (16 * index)), text=item[:item.index(
                    ':')] + '  ', font=selection, fill=color, stroke_fill='red')

    return midi_devices[kwargs["selected"]]


def main_menu(screen, midi_device, **kwargs):
    menu_icon = make_font("icomoon.ttf", 45)
    random_icon = make_font("icomoon.ttf", 58)
    menu_item = make_font('bandeins.ttf', 12)
    options = ['chords', 'arp', 'random']
    kwargs["selected"] = 0
    kwargs['selection_made'] = False

    @skywriter.flick()
    def select(start, finnish):
        if(finnish == 'east'):
             kwargs['selection_made'] = True
              
    @skywriter.touch(2)
    def touch(position):
        if(kwargs["selected"] != 2):
            kwargs["selected"] += 1
        else:
            kwargs["selected"] = 0

    while  kwargs['selection_made'] != True:
        with canvas(screen) as draw:
            draw.rectangle(
                menu_position[options[kwargs['selected']]], fill='white')
            draw.text((11, 5), text=icons['chords'],
                      font=menu_icon, fill='white')
            draw.text((13, 53), text="chords  ",
                      font=menu_item, fill=color_selection(0, kwargs['selected']))
            draw.text((75, 5), text=icons['arp'], font=menu_icon, fill="white")
            draw.text((87, 53), text="arp  ", font=menu_item,
                      fill=color_selection(1, kwargs['selected']))
            draw.text((36, 62), text=icons['random'],
                      font=random_icon, fill="white")
            draw.text((44, 116), text="random  ",
                      font=menu_item, fill=color_selection(2, kwargs['selected']))

    return kwargs['selected']


def chord(screen, midi_device, **kwargs):
    icon = make_font("icomoon.ttf", 80)
    kwargs['screen_active'] = True
    print(midi_device)

    @skywriter.flick()
    def select(start, finnish):
        print(finnish)
        if(finnish == 'west'):
          kwargs['screen_active'] = False
            
    while kwargs['screen_active']:
      with canvas(screen) as draw:
          draw.text((23, 11), text=icons['chords'], font=icon, fill="white")


modules = {
  0: chord,
}

def boot(**kwargs):
    screen = get_device()
    splash_screen(screen)


    midi_device = midi_device_selection(screen)

    while True:
      selection = main_menu(screen, midi_device)
      print(selection)
      if(selection >= 0):
        modules[selection](screen, midi_device)   
      selection == -1
      print('end flow')     
    

if __name__ == "__main__":
    try:
        boot()
    except KeyboardInterrupt:
        pass

signal.pause()
