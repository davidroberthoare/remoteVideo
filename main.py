#!/usr/bin/env python

from __future__ import print_function

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import sys
import pyglet
#for transparency
from pyglet.gl import *
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


s1 = pyglet.media.load("media/test1.mp4")
fmt = s1.video_format
if not fmt:
    print('No video track in this s1.')
    sys.exit(1)

p1 = pyglet.media.Player()
p1.queue(s1)
p1.play()

s2 = pyglet.media.load("media/test2.mp4")
fmt = s2.video_format
if not fmt:
    print('No video track in this s2.')
    sys.exit(1)

p2 = pyglet.media.Player()
p2.queue(s2)
p2.play()

# window = pyglet.window.Window(width=fmt.width, height=fmt.height)
window = pyglet.window.Window()
window.config.alpha_size = 8


@window.event
def on_draw():
    window.clear()
    p1.texture.blit(0, 0)
    p2.texture.blit(100, 100)


pyglet.app.run()