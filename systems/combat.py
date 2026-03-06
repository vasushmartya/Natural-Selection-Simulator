import random

class CombatSystem:
    def update(self, world):

        for creature in world.creatures[:]:

            if creature.energy >= world.config.violence_hunger_threshold:
                continue

            for other in world.creatures:
                if other is creature:
                    continue

                dx = creature.x - other.x
                dy = creature.y - other.y

                if (dx * dx) + (dy * dy) < 100:

                    violent_chance = creature.phenotype("violence")
                    if random.random() < violent_chance:

                        energy_gained = other.energy * world.config.violence_gain_ratio

                        creature.energy += energy_gained
                        creature.energy -= world.config.violence_energy_cost
                        creature.energy = min(creature.energy, 200)

                        world.creatures.remove(other)
                        world.kill_count += 1
                        break