from traits.trait_registry import TRAITS
from systems.movement import MovementSystem
from systems.feeding import FeedingSystem
from systems.combat import CombatSystem
from systems.reproduction import ReproductionSystem
from logging.data_logger import DataLogger
# from systems.energy import EnergySystem # Replaced by Movement logic

import random

class World:
    def __init__(self, config):
        self.config = config
        self.creatures = []
        self.bushes = []
        self.tick = 0
        self.kill_count = 0
        self.traits = TRAITS

        self.systems = [
            FeedingSystem(),
            CombatSystem(),
            MovementSystem(),
            ReproductionSystem(),
            DataLogger()
        ]
    
    def update(self):
        self.tick += 1

        for system in self.systems:
            system.update(self)

        # Cleanup dead creatures
        self.creatures = [c for c in self.creatures if c.energy > 0]
        
        # Update bushes
        for bush in self.bushes:
            bush.update()