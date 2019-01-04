import sys
import sdl2
import sdl2.ext

RESOURCES = sdl2.ext.Resources(__file__, "resources")

print(RESOURCES)

class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Hello World!", size=(400, 240))

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sprite = factory.from_image(RESOURCES.get_path("hello.bmp"))

    spriterenderer = factory.create_sprite_render_system(window)
    spriterenderer.render(sprite)

    world = sdl2.ext.World()

    world.add_system(spriterenderer)
    color = sdl2.ext.Color(255, 255, 255)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_paddle1 = factory.from_color(color, size=(20, 100))
    sp_paddle2 = factory.from_color(color, size=(20, 100))

    player1 = Player(world, sp_paddle1, 0, 250)
    player2 = Player(world, sp_paddle2, 780, 250)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        world.process()

    window.show()
    return 0


if __name__ == "__main__":
    sys.exit(run())
