class Config:
    def __init__(
        self,
        screen_width=800,
        screen_height=600,
        initial_creatures=50,
        initial_bushes=2,
        tick_delay=50,
        mutation_rate=0.05,
        bush_radius=15,
        bush_regen_time=150, # 3*1.5 tick equivalent scaled or keep 150 depending on original? org was 3*1.5 = 4.5. Let's use 4.5
        bush_min_life=3,
        bush_max_life=10,
        # Gene values
        high_speed=10,
        low_speed=5,
        high_vision=50,
        low_vision=20,
        dominant_attractive_chance=0.4,
        recessive_attractive_chance=0.8,
        more_violent=0.10,
        less_violent=0.02,
        # Violence parameters
        violence_gain_ratio=0.4,
        violence_energy_cost=8,
        violence_hunger_threshold=80
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.initial_creatures = initial_creatures
        self.initial_bushes = initial_bushes
        self.tick_delay = tick_delay
        self.mutation_rate = mutation_rate
        self.bush_radius = bush_radius
        self.bush_regen_time = bush_regen_time
        self.bush_min_life = bush_min_life
        self.bush_max_life = bush_max_life
        
        self.high_speed = high_speed
        self.low_speed = low_speed
        self.high_vision = high_vision
        self.low_vision = low_vision
        self.dominant_attractive_chance = dominant_attractive_chance
        self.recessive_attractive_chance = recessive_attractive_chance
        self.more_violent = more_violent
        self.less_violent = less_violent
        
        self.violence_gain_ratio = violence_gain_ratio
        self.violence_energy_cost = violence_energy_cost
        self.violence_hunger_threshold = violence_hunger_threshold