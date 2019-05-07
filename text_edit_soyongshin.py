# Importing from Panda3d and System
from panda3d.core import *
import sys
import os
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.showbase import OnScreenDebug
from panda3d.core import Loader as PandaLoader
from direct.showbase import Loader


# Instruction
def addInstruction(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.07,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))


# Class define
class World(DirectObject):

    # Initialization
    def __init__(self):

        # Initialization of instruction key, camera, setting
        self.inst_l = addInstruction(0.06, 'L : move light source')
        self.inst_x = addInstruction(0.12, 'Left/Right Arrow : switch camera angles')
        base.setBackgroundColor(0, 0, 0, 1)
        base.camLens.setNearFar(1, 10000)
        base.camLens.setFov(75)
        base.disableMouse()

        # Floor generation
        floorTex = loader.loadTexture('maps/envir-ground.jpg')
        cm = CardMaker('')
        cm.setFrame(-2, 2, -2, 2)
        floor = render.attachNewNode(PandaNode ("floor"))
        for y in range(12):
            for x in range(12):
                nn = floor.attachNewNode(cm.generate())
                nn.setP(-90)
                nn.setPos((x-6)*4, (y-6)*4, 0)
        
        # Text generation
        text1 = TextNode('text1')               
        text1.setText("Lomin!")              # Text string
        text1.setAlign(TextNode.ACenter)            # Center alignment
        font = loader.loadFont('arial.ttf')         # Font name
        font.setPixelsPerUnit(60)                   # Font quality
        font.setRenderMode(TextFont.RMSolid)        # Font model to 3D
        text1.setFont(font)                         
        self.textNode = render.attachNewNode(text1)      # 3D rendering
        self.textNode.setScale(3)                        # Size of the text
        self.textNode.setSy(0.3)                         # Y-direction scale
        self.textNode.setPos(0,0,0)                      # Position of the text

        # Texture generation
        tex = loader.loadTexture('maps/envir-ground.jpg')               # Texture load
        tex_stage = TextureStage.get_default()                          # 
        self.textNode.set_tex_gen(tex_stage, TexGenAttrib.M_world_position)  # 
        self.textNode.set_tex_hpr(tex_stage, 0., -90., 0.)                   # Texture orientation
        self.textNode.set_texture(tex)                                       

        # Light source
        self.light = render.attachNewNode(Spotlight("Spot"))            # Light rendering for Spotlight
        self.light.node().setScene(render)                              # Light rendering
        self.light.node().setShadowCaster(True)                         # Shadow setting
        self.light.node().showFrustum()                                 
        self.light.node().getLens().setFov(40)
        self.light.node().getLens().setNearFar(10, 100)
        render.setLight(self.light)

        self.alight = render.attachNewNode(AmbientLight("Ambient"))     # Ambient light
        self.alight.node().setColor(LVector4(0, 0, 0, 1))               # Ambient light color
        render.setLight(self.alight)

        # Important! Enable the shader generator.
        render.setShaderAuto()

        # Default values
        self.cameraSelection = 0
        self.lightSelection = 0

        self.incrementCameraPosition(0)
        self.incrementLightPosition(0)

        self.accept('escape', sys.exit)
        self.accept("arrow_left", self.incrementCameraPosition, [-1])
        self.accept("arrow_right", self.incrementCameraPosition, [1])
        self.accept("l", self.incrementLightPosition, [1])
        base.accept("enter", lambda: base.win.save_screenshot("screenshot.png"))

    def toggleUpdateShadowMap(self):
        buffer = self.light.node().getShadowBuffer(base.win.gsg)
        buffer.active = not buffer.active

    # Camera increment setting
    def incrementCameraPosition(self, n):
        self.cameraSelection = (self.cameraSelection + n) % 6
        if (self.cameraSelection == 0):
            base.cam.reparentTo(render)
            base.cam.setPos(30, -45, 26)
            base.cam.lookAt(0, 0, 0)
        if (self.cameraSelection == 1):
            base.cam.reparentTo(render)
            base.cam.setPos(7, -23, 12)
            base.cam.lookAt(0, 0, 0)
        if (self.cameraSelection == 2):
            base.cam.reparentTo(render)
            base.cam.setPos(3.5, -11.5, 6)
            base.cam.lookAt(0, 0, 0)
        if (self.cameraSelection == 3):
            base.cam.reparentTo(render)
            base.cam.setPos(1.5, -5, 2)
            base.cam.lookAt(0, 0, 0)
        if (self.cameraSelection == 4):
            base.cam.reparentTo(render)
            base.cam.setPos(0, 10, 10)
            base.cam.lookAt(0, 0, 0)
        if (self.cameraSelection == 5):
            base.cam.reparentTo(render)
            base.cam.setPos(-7, -23, 26)
            base.cam.lookAt(0, 0, 0)

    # Light increment setting
    def incrementLightPosition(self, n):
        self.lightSelection = (self.lightSelection + n) % 4
        if (self.lightSelection == 0):
            self.light.setPos(0, -40, 25)
            self.light.lookAt(0, 0, 0)
            self.light.node().getLens().setNearFar(10,10000)
            self.light.node().setColor(LVector4(1,1,1,1))
        if (self.lightSelection == 1):
            self.light.setPos(0, -40, 25)
            self.light.lookAt(0, 0, 0)
            self.light.node().getLens().setNearFar(10, 10000)
            self.light.node().setColor(LVector4(1,0,0,1))
        if (self.lightSelection == 2):
            self.light.setPos(12, -12, 12)
            self.light.lookAt(0, 0, 0)
            self.light.node().getLens().setNearFar(10, 10000)
            self.light.node().setColor(LVector4(1,1,1,1))
        if (self.lightSelection == 3):
            self.light.setPos(12, -12, 12)
            self.light.lookAt(0, 0, 0)
            self.light.node().setColor(LVector4(1,0.2,0.2,1))
    def shadeSupported(self):
        return base.win.getGsg().getSupportsBasicShaders() and \
               base.win.getGsg().getSupportsDepthTexture() and \
               base.win.getGsg().getSupportsShadowFilter()

if __name__ == '__main__':
    base = ShowBase()
    w = World()
    base.run()
    base.win.save_screenshot("limbee.png")