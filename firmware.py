#!/usr/bin/env python
# -*- coding: utf-8 -*-

import skywriter
import signal
from luma.core.render import canvas

from screen_device import get_device
from ui import icons, make_font, menu_position, color_selection, splash_screen, center_text_x
from midi import send_note, get_scale, available_scales, chromatic

import math

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
    print(midi_devices)

    @skywriter.touch(2)
    def touch(position):
        
        if(len(midi_devices) == 0):
            return
        
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
            
            if(len(midi_devices) == 0):
                draw.text((10, 66), text='No MIDI devices', font=selection, fill='black', stroke_fill='red')

            for index, item in enumerate(midi_devices):
                if(index == kwargs["selected"]):
                    color = 'black'
                else:
                    color = 'white'

                draw.text((10, 66 + (16 * index))   , text=item[:item.index(
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
            draw.text((12, 5), text=icons['chords'],
                      font=menu_icon, fill='white')
            draw.text((15, 53), text="notes  ",
                      font=menu_item, fill=color_selection(0, kwargs['selected']))
            draw.text((75, 5), text=icons['arp'], font=menu_icon, fill="white")
            draw.text((80, 53), text="chords  ", font=menu_item,
                      fill=color_selection(1, kwargs['selected']))
            draw.text((36, 62), text=icons['random'],
                      font=random_icon, fill="white")
            draw.text((44, 116), text="random  ",
                      font=menu_item, fill=color_selection(2, kwargs['selected']))

    return kwargs['selected']
  

def chord(screen, midi_device, **kwargs):
    icon = make_font("icomoon.ttf", 70)
    menu_item = make_font('bandeins.ttf', 16)
    kwargs['screen_active'] = True
    kwargs['is_playing'] = False
    kwargs["current_scale"] = 0
    kwargs["current_note"] = 0
    kwargs["note_index"] = 0
    kwargs['octave'] = 1
    
    port = mido.open_output(midi_device)
    kwargs['midi_on'] = False
    
    @skywriter.flick()
    def select(start, finnish):
        if(kwargs['is_playing']):
            return 

        if(finnish == 'west'):
          kwargs['screen_active'] = False


    @skywriter.touch(11)
    def touch(position):
        
        
        if(position == 'south'):
            kwargs['midi_on'] = not(kwargs['midi_on'])
            return
            
        if(kwargs["current_scale"] != 11):
            kwargs["current_scale"] += 1
        else:
            kwargs["current_scale"] = 0
            
    kwargs["delta"] = 0
    
    @skywriter.airwheel()
    def spinny(delta):
        kwargs["delta"] += delta
        if kwargs["delta"] < 0:
            kwargs["delta"] = 0
        if kwargs["delta"] > 10000:
            kwargs["delta"] = 10000
            
        calibrated_value = math.floor(kwargs["delta"]/600)
        if(calibrated_value == 13):
           kwargs["delta"] = 0

        kwargs["current_note"] = calibrated_value     
        
            
    @skywriter.move()
    def move(x, y, z):
        if(kwargs['midi_on']):
            scale = get_scale(chromatic[kwargs["current_note"]], available_scales[kwargs["current_scale"]])
            kwargs['is_playing'] = True
            kwargs['note_index'] = math.floor( x * len(scale))
            velocity = 100 - math.floor( z * 100)
            kwargs['octave'] = math.floor( y * 4)
            send_note(scale[kwargs['note_index']],kwargs['octave'] + 1, velocity, port)
            print('note:' + scale[kwargs['note_index']],' octave:' + str(kwargs['octave']),' velocity:' + str(round(velocity,2)))
    
    
    while kwargs['screen_active']:
      with canvas(screen) as draw:
          scale = available_scales[kwargs["current_scale"]]
          current_scale = get_scale(chromatic[kwargs["current_note"]], scale) 
          
          if(kwargs['note_index'] < len(current_scale)):
            draw.text((center_text_x(chromatic[kwargs["current_note"]] + ':', 16) - 3, 8), text=chromatic[kwargs["current_note"]] + ':'+current_scale[kwargs['note_index']]+ str(kwargs['octave']),font=menu_item, fill='white')
            draw.text((center_text_x(scale,16), 108), text=scale,font=menu_item, fill='white')
            if(kwargs['midi_on']):
                draw.text((29, 32), text=icons['chords'], font=icon, fill="white")

modules = {
  0: chord,
}

def boot(**kwargs):
    screen = get_device()
    splash_screen(screen)


    midi_device = midi_device_selection(screen)

    while True:
      selection = main_menu(screen, midi_device)
      if(selection >= 0):
        modules[selection](screen, midi_device)   
      selection == -1
    

if __name__ == "__main__":
    try:
        boot()
    except KeyboardInterrupt:
        pass

signal.pause()
