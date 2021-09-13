import mido
import sys

from musthe import *

chromatic = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    
major = ['C','D','E','F','G','A','B','C']

available_scales = [
    'major',           
    'natural_minor',   
    'harmonic_minor',  
    'melodic_minor',   
    'major_pentatonic',
    'minor_pentatonic',
    # greek modes:
    'ionian',
    'dorian',
    'phrygian',
    'lydian',
    'mixolydian',
    'aeolian',
    'locrian',
    ]




base_notes = {    
'C': 24,
'C#': 25,
'Db': 25,
'C##': 26,
'D': 26,
'D#': 27,
'Eb': 27,
'D##': 28,
'E': 28,
'E#': 29,
'E##': 30,
'F': 29,
'F#': 30,
'Gb': 30,
'F##': 31,
'G': 31,
'G#': 32,
'Ab': 32,
'G##': 33,
'A': 33,
'A#': 34,
'Bb': 34,
'A##': 35,
'B': 35,
'B#': 36,
'B##': 37
}

def note(note,velocity = 64):
    return mido.Message('note_on',note=note,velocity = velocity, time=1)

def note_off(note,velocity = 64, time=2):
    return mido.Message('note_off',note=note,velocity = velocity, time=1)

def majorChord(root, velocity, outport):
    outport.send(note(root, velocity))
    outport.send(note(root+4, velocity))
    outport.send(note(root+7,velocity))
    outport.send(note_off(root, velocity))
    outport.send(note_off(root+4, velocity))
    outport.send(note_off(root+7, velocity))

def majorChord(root, velocity, outport):
    outport.send(note(root, velocity))
    outport.send(note(root+3, velocity))
    outport.send(note(root+7,velocity))
    outport.send(note_off(root, velocity))
    outport.send(note_off(root+3, velocity))
    outport.send(note_off(root+7, velocity))
    
def send_note(root, octave, velocity, outport):
    note_to_play = get_note(root, octave)
    outport.send(note(note_to_play, velocity))
    outport.send(note_off(note_to_play, velocity))

def get_note(tonic, octave):
    return base_notes[tonic] + (octave * 12)
    
def get_scale(tonic, mode):
    scale = Scale(Note(tonic), mode)
    return [str(scale[i]) for i in range(len(scale))]
 