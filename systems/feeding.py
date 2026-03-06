class FeedingSystem:
    def update(self, world):
        for creature in world.creatures:
            creature_radius = 5

            for bush in world.bushes:
                if not bush.is_full:
                    continue

                dx = abs(creature.x - bush.x)
                dy = abs(creature.y - bush.y)
                radii_sum = creature_radius + bush.radius

                if dx > radii_sum or dy > radii_sum:
                    continue

                if (dx * dx) + (dy * dy) < (radii_sum * radii_sum):

                    creature.energy += 50
                    creature.energy = min(creature.energy, 150)

                    bush.is_full = False
                    bush.times_eaten += 1

                    if bush.times_eaten >= bush.max_eaten:
                        bush.is_dead = True

                    break