from config import Config
from world import World
from entities.creature import Creature
from entities.bush import Bush
from renderer.tkinter_renderer import TkinterRenderer
import random


def main():
    config = Config()
    world = World(config)

    # Spawn creatures
    for _ in range(config.initial_creatures):
        x = random.randint(50, config.screen_width - 50)
        y = random.randint(50, config.screen_height - 50)
        world.creatures.append(Creature(world, x, y))

    # Spawn bushes
    for _ in range(config.initial_bushes):
        x = random.randint(50, config.screen_width - 50)
        y = random.randint(50, config.screen_height - 50)
        world.bushes.append(Bush(world, x, y))

    renderer = TkinterRenderer(world)

    def game_loop():
        world.update()
        renderer.draw()
        renderer.root.after(config.tick_delay, game_loop)

    game_loop()
    renderer.root.mainloop()


if __name__ == "__main__":
    main()