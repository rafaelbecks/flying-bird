#!/usr/bin/env python
import skywriter
import signal
import mido
import math

# port = mido.open_output('JU-06A:JU-06A MIDI 1 24:0')

some_value = 5000

c_scale = [55 ,57, 60, 64, 65, 67, 69, 71]

cmajor7 = [60, 64, 67, 71 ]

eminor = [64,67,71, 72]

fmaj = [64, 67, 71, 74]

@skywriter.move()
def move(x, y, z):
  #  y = math.floor( y * 2)
  #  x = math.floor( x * 2)

   note_to_send = math.floor((y * 45) + 45)

  #  port.send(mido.Message('note_on', channel=0, note=note_to_send, velocity=5, time=0.5))
  #  port.send(mido.Message('note_off', channel=0, note=note_to_send, velocity=5, time=0.5))

   if(y == 0 and x == 0):
  #    #cmaj
     print('cmaj' )
  #    port.send(mido.Message('note_on', channel=0, note=60, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=64, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=67, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=71, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=60, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=64, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=67, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=71, velocity=5, time=0.5))
  #  if( x == 1 and y == 0):
  #    #fmaj
  #    print('fmaj' )
  #    port.send(mido.Message('note_on', channel=0, note=65, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=69, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=72, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=76, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=65, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=69, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=72, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=76, velocity=5, time=0.5))
  #  if( x== 0):
  #    #emin
  #    print('cmaj' )
  #    port.send(mido.Message('note_on', channel=0, note=60, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=64, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=67, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=71, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=60, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=64, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=67, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=71, velocity=5, time=0.5))

  #  if(y == 1 and x== 1):
  #    print('emin' )
  #    port.send(mido.Message('note_on', channel=0, note=64, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=67, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=71, velocity=5, time=0.5))
  #    port.send(mido.Message('note_on', channel=0, note=74, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=64, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=67, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=71, velocity=5, time=0.5))
  #    port.send(mido.Message('note_off', channel=0, note=74, velocity=5, time=0.5))

@skywriter.flick()
def flick(start,finish):
  print('Got a flick!', start, finish)

@skywriter.airwheel()
def spinny(delta):
  global some_value
  some_value += delta
  if some_value < 0:
  	some_value = 0
  if some_value > 10000:
    some_value = 10000
  print(some_value/100)

@skywriter.double_tap()
def doubletap(position):
  print('Double tap!', position)

@skywriter.tap()
def tap(position):
  print('Tap!', position)
  # port.send(mido.Message('note_on', channel=0, note=74, velocity=2, time=0.5))
  # port.send(mido.Message('note_off', channel=0, note=74, velocity=2, time=0.5))
  


@skywriter.touch()
def touch(position):
  print('Touch!', position)

signal.pause()
