class EnergySystem:
    def update(self, world):
        world.entities = [
            e for e in world.entities
            if not hasattr(e, "energy") or e.energy > 0
        ]