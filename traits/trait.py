import random

class Trait:
    def __init__(self, name, dominant, dominant_value, recessive_value, mutation_rate=0.05):
        self.name = name
        self.dominant = dominant
        self.dominant_value = dominant_value
        self.recessive_value = recessive_value
        self.mutation_rate = mutation_rate

    def express(self, alleles):
        if self.dominant in alleles:
            return self.dominant_value
        return self.recessive_value

    def mutate(self, allele):
        if random.random() < self.mutation_rate:
            return self.flip(allele)
        return allele

    def flip(self, allele):
        return self.dominant if allele != self.dominant else allele.lower()