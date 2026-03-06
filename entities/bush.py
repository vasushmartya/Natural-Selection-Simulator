import random
from entities.entity import Entity


class Bush(Entity):
    def __init__(self, world, x, y):
        super().__init__(x, y)

        self.config = world.config

        # Size
        self.radius = self.config.bush_radius

        # Food state
        self.is_full = True

        # Regeneration
        self.regen_time = self.config.bush_regen_time
        self.timer = 0

        # Overeating mechanics
        self.times_eaten = 0
        self.max_eaten = random.randint(
            self.config.bush_min_life,
            self.config.bush_max_life
        )

        self.is_dead = False

    def update(self):
        """
        Handles regrowth logic.
        This keeps bush behavior self-contained.
        """

        if not self.is_full:
            self.timer += 1

            if self.timer >= self.regen_time:
                self.is_full = True
                self.timer = 0

                if self.is_dead:
                    # Teleport to a completely new random location
                    self.x = random.randint(self.radius, self.config.screen_width - self.radius)
                    self.y = random.randint(self.radius, self.config.screen_height - self.radius)
                    self.is_dead = False
                    self.times_eaten = 0 # Reset health for the new tree

    def mark_eaten(self):
        """
        Called by FeedingSystem when a creature eats from this bush.
        """

        self.is_full = False
        self.times_eaten += 1

        if self.times_eaten >= self.max_eaten:
            self.is_dead = True