# Importing from Panda3d and System
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import sys
import os
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.showbase import OnScreenDebug
from panda3d.core import Loader as PandaLoader
from direct.showbase import Loader

base = ShowBase()

# Text input
text = TextNode('text')
text.setText("Lomin!")
text.setAlign(TextNode.ACenter)

# Font load
font = loader.loadFont('arial.ttf')
font.setPixelsPerUnit(60)
font.setRenderMode(TextFont.RMSolid)
text.setFont(font)

# Text rendering
textNode = render.attachNewNode(text)
textNode.setScale(3)
textNode.setSy(0.3)
textNode.setPos(0,0,0)

# Text texture
tex = loader.loadTexture('maps/envir-ground.jpg')
tex_stage = TextureStage.get_default()
textNode.set_tex_gen(tex_stage, TexGenAttrib.M_world_position)
textNode.set_tex_hpr(tex_stage, 0., -90., 0.)
textNode.set_texture(tex)

#Light source
light = render.attachNewNode(Spotlight("Spot"))
light.node().setScene(render)
light.node().setShadowCaster(True)
light.node().showFrustum()
light.node().getLens().setFov(40)
light.node().getLens().setNearFar(-100, 100)
render.setLight(light)
light.setPos(0, -40, 25)
light.lookAt(0, 0, 0)
light.node().setColor(LVector4(1, 1, 1, 1))

render.setShaderAuto()

# Camera
base.cam.reparentTo(render)
base.cam.setPos(7, -23, 12)
base.cam.lookAt(0, 0, 0)


base.run()
base.win.save_screenshot("scrshot_test.png")