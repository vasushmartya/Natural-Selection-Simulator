import random
from entities.creature import Creature

class ReproductionSystem:
    def update(self, world):
        # We need a new list of babies so we don't iterate over them in the same tick
        new_babies = []

        for creature in world.creatures:
            if creature.energy >= 120:
                for partner in world.creatures:
                    if partner != creature and partner.energy >= 120:
                        
                        dx = abs(creature.x - partner.x)
                        dy = abs(creature.y - partner.y)
                        
                        if dx > 10 or dy > 10: continue
                        
                        if (dx * dx) + (dy * dy) < 100:
                            
                            # Check mating chance
                            mating_chance = creature.phenotype("attractiveness")
                            if random.random() > mating_chance:
                                continue

                            # Reproduce
                            baby = self.reproduce(world, creature, partner)
                            
                            if baby:
                                new_babies.append(baby)
                                creature.energy -= 60
                                partner.energy -= 60
                                break # Stop looking for partners this tick

        world.creatures.extend(new_babies)

    def reproduce(self, world, parent1, parent2):
        baby = Creature(world, parent1.x, parent1.y)

        for trait_name in parent1.genes.keys():
            # Punnett square choice
            allele1 = random.choice(parent1.genes[trait_name])
            allele2 = random.choice(parent2.genes[trait_name])
            
            # Mutation check
            trait = world.traits[trait_name]
            allele1 = trait.mutate(allele1)
            # original didn't mutate the 2nd allele explicitly in the same way, but let's apply mutation rate properly
            # Actually, simul.py mutated the first allele of the baby pair.
            
            baby.genes[trait_name] = [allele1, allele2]

        return baby