# systems/movement.py

import random
from entities.creature import Creature
from entities.bush import Bush


class MovementSystem:
    def update(self, world):
        for entity in world.creatures:
            if not isinstance(entity, Creature):
                continue

            creature = entity

            # Get phenotype values
            speed = creature.phenotype("speed")
            sight_radius = creature.phenotype("vision")

            target_bush = None
            closest_dist = sight_radius

            # Find bushes in world
            bushes = world.bushes

            # 1. Look for closest food
            for bush in bushes:
                if bush.is_full:
                    dx = creature.x - bush.x
                    dy = creature.y - bush.y
                    dist = (dx**2 + dy**2) ** 0.5

                    if dist < closest_dist:
                        closest_dist = dist
                        target_bush = bush

            # 2. Biased movement
            if target_bush:
                dx = target_bush.x - creature.x
                dy = target_bush.y - creature.y

                length = (dx**2 + dy**2) ** 0.5

                if length > 0:
                    dx = (dx / length) * speed
                    dy = (dy / length) * speed
                else:
                    dx, dy = 0, 0
            else:
                dx = random.choice([-speed, speed])
                dy = random.choice([-speed, speed])

            # Apply movement
            creature.x += dx
            creature.y += dy

            # Boundary constraints from config
            creature.x = max(5, min(world.config.screen_width - 5, creature.x))
            creature.y = max(5, min(world.config.screen_height - 5, creature.y))

            # Energy drain proportional to movement
            movement_cost = 0.05 * ((dx**2 + dy**2) ** 0.5)
            creature.energy -= movement_cost