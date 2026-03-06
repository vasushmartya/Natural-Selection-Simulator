from entities.entity import Entity
import random

class Creature(Entity):
    def __init__(self, world, x, y):
        super().__init__(x, y)
        self.world = world
        self.energy = 100

        # Genotype initialization for all 4 traits
        self.genes = {
            "speed": [random.choice(["S", "s"]), random.choice(["S", "s"])],
            "vision": [random.choice(["V", "v"]), random.choice(["V", "v"])],
            "attractiveness": [random.choice(["A", "a"]), random.choice(["A", "a"])],
            "violence": [random.choice(["K", "k"]), random.choice(["K", "k"])]
        }

    def phenotype(self, trait_name):
        trait = self.world.traits[trait_name]
        return trait.express(self.genes[trait_name])