#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
os.environ["PYSDL2_DLL_PATH"] = "\\resources\\"
from ctypes import py_object, pointer, cast, c_void_p, POINTER

import sdl2.ext as sdl2ext
from sdl2 import (pixels, render, events as sdlevents, surface, error,
                  timer)
from sdl2.sdlttf import (TTF_OpenFont,
                         TTF_RenderText_Shaded,
                         TTF_GetError,
                         TTF_Init,
                         TTF_Quit
                         )


class TextSprite(sdl2ext.TextureSprite):
    def __init__(self, renderer, font=None, text="", fontSize=16,
                 textColor=pixels.SDL_Color(255, 255, 255),
                 backgroundColor=pixels.SDL_Color(0, 0, 0)):
        if isinstance(renderer, sdl2ext.RenderContext):
            self.renderer = renderer.renderer
        elif isinstance(renderer, render.SDL_Renderer):
            self.renderer = renderer
        else:
            raise TypeError("unsupported renderer type")

        if font is None:
            font = os.path.join(os.environ["windir"], "Fonts", "Arial.ttf")
        elif not os.path.isfile(font):
            if os.path.isfile(os.path.join(os.environ["windir"], "Fonts", font + ".ttf")):
                font = os.path.join(os.environ["windir"], "Fonts", font + ".ttf")
            else:
                raise IOError("Cannot find %s" % font)

        self.font = TTF_OpenFont(font, fontSize)
        if self.font is None:
            raise TTF_GetError()
        self._text = text
        self.fontSize = fontSize
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        texture = self._createTexture()

        super(TextSprite, self).__init__(texture)

    def _createTexture(self):
        textSurface = TTF_RenderText_Shaded(self.font, self._text, self.textColor, self.backgroundColor)
        if textSurface is None:
            raise TTF_GetError()
        texture = render.SDL_CreateTextureFromSurface(self.renderer, textSurface)
        if texture is None:
            raise sdl2ext.SDLError()
        surface.SDL_FreeSurface(textSurface)
        return texture

    def _updateTexture(self):
        textureToDelete = self.texture

        texture = self._createTexture()
        super(TextSprite, self).__init__(texture)

        render.SDL_DestroyTexture(textureToDelete)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value
        self._updateTexture()


class FPS(object):
    def __init__(self, sprite):
        super(FPS, self).__init__()
        self.counter = 0
        self.text = sprite


class FPSCounter(sdl2ext.Entity):
    def __init__(self, world, *args, **kwargs):
        if "renderer" not in kwargs:
            raise ValueError("you have to provide a renderer= argument")
        renderer = kwargs['renderer']
        super(FPSCounter, self).__init__(world, *args, **kwargs)
        textSprite = TextSprite(renderer, "Comic", "FPS: -")
        self.fps = FPS(textSprite)
        self.textSprite = textSprite
        object.__setattr__(self, 'callback', self.getCallBackFunc())
        object.__setattr__(self, 'timerId', timer.SDL_AddTimer(1000, self.callback, None))

    def getCallBackFunc(self):
        def oneSecondElapsed(time, userdata):
            event = sdlevents.SDL_Event()
            user_event = sdlevents.SDL_UserEvent()

            user_event.type = sdlevents.SDL_USEREVENT
            user_event.code = 0
            user_event.data1 = cast(pointer(py_object(self)), c_void_p)
            user_event.data2 = 0

            event.type = sdlevents.SDL_USEREVENT
            event.user = user_event

            sdlevents.SDL_PushEvent(event)

            return time

        return timer.SDL_TimerCallback(oneSecondElapsed)


class FPSController(sdl2ext.System):
    def __init__(self):
        """Creates a new Frame per Second counter."""
        super(FPSController, self).__init__()
        self.componenttypes = (FPS,)

    def process(self, world, components):
        for fps in components:
            fps.counter += 1


def main():
    sdl2ext.init()
    TTF_Init()

    window = sdl2ext.Window("Text display", size=(800, 600))
    window.show()

    renderer = sdl2ext.RenderContext(window)
    factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
    world = sdl2ext.World()

    fps = FPSCounter(world, renderer=renderer)

    spriteRenderer = factory.create_sprite_renderer()
    fpsController = FPSController()

    world.add_system(fpsController)
    world.add_system(spriteRenderer)

    running = True

    while running:
        for event in sdl2ext.get_events():
            if event.type == sdlevents.SDL_QUIT:
                running = False
                break
            elif event.type == sdlevents.SDL_USEREVENT:
                entity = cast(event.user.data1, POINTER(py_object)).contents.value
                entity.textsprite.text = "FPS: " + str(entity.fps.counter)
                entity.fps.counter = 0
        renderer.clear()
        world.process()

    TTF_Quit()
    sdl2ext.quit()
    return 0


if __name__ == '__main__':
    main()
