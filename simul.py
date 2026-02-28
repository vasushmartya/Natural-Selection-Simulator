import tkinter as tk
import random
import csv

#tasks:
# - more modular
# - energy conservation
# - add disease

#considerations:
# - energy conservation (bushes can add energy to environment, movement produces unusable energy)
# - frequency-dependent selection (the fitness of a trait depends on how common it is in the population)
# - trade offs
# - Density dependence
# - predator - prey dynamics
# - 

#world settings

SEED = 234
USE_SEED = True
if USE_SEED:
    random.seed(SEED)
    print(f"Random seed set to {SEED}") 
else:
    print("Random seed not used.")

screen_width = 800
screen_height = 600

run_after_time = 50
tick_count = 0

MAX_HEALTH = 100
FUNKY_HEALTH = 50

high_speed = 8
low_speed = 4
dominant_speed_gene = 'S'

high_vision = 60
low_vision = 150
dominant_vision_gene = 'V'

dominant_attractive_chance = 0.5
recessive_attractive_chance = 0.9
dominant_attractive_gene = 'a'

# 4. Violence Trait (K/k)
more_violent = 0.10     # 25% chance to attempt kill when touching
less_violent = 0.02     # 2% chance
dominant_violent_gene = 'K'

# Violence tuning parameters
violence_gain_ratio = 0.5  # % of victim energy gained (0.5 = 50%)
violence_energy_cost = 15   # flat energy cost per attack

violence_hunger_threshold = 90   # attack only if energy below this

alpha_death = 100 # after how many cycles does the age increment
beta_death = 3000 # proportionality factor for death probability : p(death) = age/beta_death

n_initial_creatures = 150
n_initial_bushes = 25

killcnt = 0

with open("natural_selection_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Tick", "Total Creatures", "Speed_SS", "Speed_Ss", "Speed_ss", "Vision_VV", "Vision_Vv", "Vision_vv", "Beauty_AA", "Beauty_Aa", "Beauty_aa",
                     "Violence_KK", "Violence_Kk", "Violence_kk"])

class Bush:
    def __init__(self, radius=15, is_full=True, regenTime=3*1.5):
        self.radius = radius
        self.is_full = is_full
        self.x = random.randint(self.radius, screen_width - self.radius)
        self.y = random.randint(self.radius, screen_height - self.radius)
        self.regenTime = regenTime
        self.timer = 0
        self.times_eaten = 0
        self.max_eaten = random.randint(3,10)
        self.is_dead = False
        
class Creature:
    def __init__(self, x, y, speed_genes, sight_genes, attractive_genes, violent_genes):
        self.x = x
        self.y = y
        self.speed_genes = speed_genes
        self.sight_genes = sight_genes
        self.attractive_genes = attractive_genes
        self.violent_genes = violent_genes
        self.energy = 150
        self.timer = 0
        self.age = 0
        
        # 1. Speed Trait (S/s)
        self.speed = high_speed if dominant_speed_gene in speed_genes else low_speed
        
        # 2. Vision Trait (V/v)
        self.sight_radius = high_vision if dominant_vision_gene in sight_genes else low_vision

        # 3. Attractiveness Trait (A/a)
        self.mating_chance = dominant_attractive_chance if dominant_attractive_gene in attractive_genes else recessive_attractive_chance

        self.violent_chance = more_violent if dominant_violent_gene in violent_genes else less_violent

    def move(self, bushes):
        target_bush = None
        closest_dist = self.sight_radius # Start by only looking within their sight limit

        # 1. Look for the closest food!
        for bush in bushes:
            if bush.is_full:
                dist = ((self.x - bush.x)**2 + (self.y - bush.y)**2) ** 0.5
                if dist < closest_dist:
                    closest_dist = dist
                    target_bush = bush

        # 2. Biased Movement (If they see food)
        if target_bush is not None:
            # Find the direction to the bush
            dx = target_bush.x - self.x
            dy = target_bush.y - self.y
            
            # Normalize the vector (make it a length of 1) and multiply by speed
            length = (dx**2 + dy**2) ** 0.5
            
            # Prevent ZeroDivisionError!
            if length > 0:
                dx = (dx / length) * self.speed
                dy = (dy / length) * self.speed
            
        # 3. Random Walk (If they don't see food)
        else:
            dx = random.choice([-self.speed, self.speed])
            dy = random.choice([-self.speed, self.speed])

        # Apply the movement
        self.x += dx
        self.y += dy

        # Boundary checks
        if self.x < 5: self.x = 5
        elif self.x > 795: self.x = 795
        if self.y < 5: self.y = 5
        elif self.y > 595: self.y = 595
        
        # Energy drain (Option 1: Flat drain to balance the game!)
        self.energy -= 0.05*((dx**2 + dy**2)**0.5) 

    def reproduce(self, partner):

        if self.mating_chance < random.random():
            return None
        # Punnett Squares for BOTH traits!
        baby_speed = [random.choice(self.speed_genes), random.choice(partner.speed_genes)]
        baby_sight = [random.choice(self.sight_genes), random.choice(partner.sight_genes)]
        baby_attractive = [random.choice(self.attractive_genes), random.choice(partner.attractive_genes)]
        baby_violent = [random.choice(self.violent_genes), random.choice(partner.violent_genes)]

        # 5% chance of mutation for Speed
        if random.random() < 0.05:
            baby_speed[0] = 'S' if baby_speed[0] == 's' else 's'
            
        # 5% chance of mutation for Sight
        if random.random() < 0.05:
            baby_sight[0] = 'V' if baby_sight[0] == 'v' else 'v'
        
        # 5% chance of mutation for Attractiveness
        if random.random() < 0.05:
            baby_attractive[0] = 'A' if baby_attractive[0] == 'a' else 'a'

        # 5% mutation of mutation for violence
        if random.random() < 0.05:
            baby_violent[0] = 'K' if baby_violent[0] == 'k' else 'k'
            
        return Creature(self.x, self.y,
                baby_speed,
                baby_sight,
                baby_attractive,
                baby_violent)

creatures = []
for _ in range(n_initial_creatures):
    s_genes = [random.choice(['S', 's']), random.choice(['S', 's'])]
    v_genes = [random.choice(['V', 'v']), random.choice(['V', 'v'])]
    a_genes = [random.choice(['A', 'a']), random.choice(['A', 'a'])]
    k_genes = ['K' if random.random() < 0.2 else 'k', 'K' if random.random() < 0.2 else 'k'] # more probability for initial population to be peacefull
    
    creatures.append(Creature(random.randint(300, 500), random.randint(200,400), s_genes, v_genes, a_genes, k_genes))

bushes = []
for _ in range(n_initial_bushes):
    bushes.append(Bush(radius=random.randint(15,30)))

def draw_creature(canvas, creature):
    # Determine Color from SPEED Genotype
    speed = "".join(sorted(creature.speed_genes)) 
    
    if speed == "SS":
        color = "purple"
    elif speed == "Ss":
        color = "blue"
    else: # "ss"
        color = "cyan"

        
    r = 5 
    x1 = creature.x - r
    y1 = creature.y - r
    x2 = creature.x + r
    y2 = creature.y + r
    
    # Determine border color priority:
    if 'K' in creature.violent_genes:
        border_color = "red"
    elif 'v' in creature.sight_genes and 'V' not in creature.sight_genes:
        border_color = "gold"
    else:
        border_color = "black"

    # We use dashed line if they are attractive
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=border_color, width=2, dash=True if 'a' in creature.attractive_genes else None)

def draw_bush(canvas, bush):
    x1 = bush.x - bush.radius
    y1 = bush.y - bush.radius
    x2 = bush.x + bush.radius
    y2 = bush.y + bush.radius
    
    if bush.is_dead:
        # Draw a smaller brown circle to represent a dead stump
        canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill="saddlebrown", outline="brown")
        return # Stop drawing here so we don't draw green leaves!

    # Red berry coordinates
    x11 = bush.x - 5
    y11 = bush.y - 5
    x21 = bush.x + 5
    y21 = bush.y + 5

    canvas.create_oval(x1, y1, x2, y2, fill="lawn green", outline="black")
    if bush.is_full:
        canvas.create_oval(x11, y11, x21, y21, fill="red")

def update_simulation():
    global tick_count
    tick_count += 1

    global killcnt

    # Clear the Board
    canvas.delete("all") 

    # Draw Bushes
    for bush in bushes:
        if not bush.is_full:
            bush.timer += 1 # Count up by 1 every frame
            if bush.timer >= bush.regenTime:
                bush.is_full = True # The berries are back!
                bush.timer = 0 # Reset the timer for next time

                if bush.is_dead:
                    # Teleport to a completely new random location
                    bush.x = random.randint(bush.radius, screen_width - bush.radius)
                    bush.y = random.randint(bush.radius, screen_height - bush.radius)
                    bush.is_dead = False
                    bush.times_eaten = 0 # Reset health for the new tree

        draw_bush(canvas, bush)

    # Update and draw creatures
    for creature in creatures[:]: 
        creature.timer += 1
        creature.age = creature.timer // alpha_death
        
        # Check for death by no food
        if creature.energy <= 0:
            if creature in creatures:
                creatures.remove(creature)
            continue
        
        # Check for death by age
        if creature.age/beta_death > random.random():
            creatures.remove(creature)
            continue

        creature.move(bushes)

        # Eating Logic
        creature_radius = 5
        
        for bush in bushes:
            if bush.is_full:
                dx = abs(creature.x - bush.x)
                dy = abs(creature.y - bush.y)
                radii_sum = creature_radius + bush.radius
                
                if dx > radii_sum or dy > radii_sum: continue 
                
                if (dx * dx) + (dy * dy) < (radii_sum * radii_sum):
                    # Peaceful creatures are specialized herbivores
                    if 'K' not in creature.violent_genes:
                        creature.energy += 50
                    # Violent creatures are omnivores (poor plant digestion)
                    else:
                        creature.energy += 10 

                    # Cap energy at 150
                    if creature.energy > 150:
                        creature.energy = 150

                    bush.is_full = False

                    # Check Overeating
                    bush.times_eaten += 1
                    if bush.times_eaten >= bush.max_eaten:
                        bush.is_dead = True
                    
                    break

        # Violence Logic
        victim_to_remove = None

        # Only attack if hungry
        if creature.energy < violence_hunger_threshold:

            for other in creatures:
                if other is creature:
                    continue

                dx = creature.x - other.x
                dy = creature.y - other.y

                if (dx * dx) + (dy * dy) < 100:  # touching
                    
                    if random.random() < creature.violent_chance:
                        victim_to_remove = other
                        break

        # Apply outcome AFTER loop
        if victim_to_remove is not None:
            # 1. Gain the energy
            energy_gained = victim_to_remove.energy * violence_gain_ratio
            creature.energy += energy_gained
            creature.energy -= violence_energy_cost

            if creature.energy > 200:
                creature.energy = 200

            # 2. Safely kill the victim
            victim_to_remove.energy = -999  # Ensure they act dead if their turn is next
            
            # 3. Safely remove them from the master list to prevent ValueError
            if victim_to_remove in creatures:
                creatures.remove(victim_to_remove)
                killcnt += 1

        # Mating Logic
        # Only try to mate if they are well-fed (energy 120 or higher)
        if creature.energy >= 120:
            for partner in creatures:
                # Don't mate with yourself, and make sure the partner is also well-fed!
                if partner != creature and partner.energy >= 120:
                    
                    # Broad Phase + Narrow Phase Collision (Are they touching?)
                    dx = abs(creature.x - partner.x)
                    dy = abs(creature.y - partner.y)
                    
                    # Combined radii for two creatures is 5 + 5 = 10
                    if dx > 10 or dy > 10: continue
                    
                    if (dx * dx) + (dy * dy) < 100: # 10 squared is 100
                        baby = creature.reproduce(partner)

                        # Checking if they can reproduce or not
                        if baby is not None:
                            creatures.append(baby)
                            
                            # Subtract the massive energy cost of reproduction
                            creature.energy -= 60
                            partner.energy -= 60
                            
                            # Stop looking for partners this frame
                            break
                        
        draw_creature(canvas, creature)
    
    # Print console stats once per second
    if tick_count % 20 == 0:
        display_console()

    root.after(run_after_time, update_simulation) 

def display_console():
    speed_SS, speed_Ss, speed_ss = 0, 0, 0
    vision_VV, vision_Vv, vision_vv = 0, 0, 0
    beauty_AA, beauty_Aa, beauty_aa = 0, 0, 0
    violent_KK, violent_Kk, violent_kk = 0, 0, 0
    
    for c in creatures:
        # Track Speed
        s_genes = "".join(sorted(c.speed_genes))
        if s_genes == "SS": speed_SS += 1
        elif s_genes == "Ss": speed_Ss += 1
        else: speed_ss += 1
            
        # Track Vision
        v_genes = "".join(sorted(c.sight_genes))
        if v_genes == "VV": vision_VV += 1
        elif v_genes == "Vv": vision_Vv += 1
        else: vision_vv += 1

        # Track Beauty
        a_genes = "".join(sorted(c.attractive_genes))
        if a_genes == "AA": beauty_AA += 1
        elif a_genes == "Aa": beauty_Aa += 1
        else: beauty_aa += 1

        # Track Violence
        k_genes = "".join(sorted(c.violent_genes))
        if k_genes == "KK":
            violent_KK += 1
        elif k_genes == "Kk":
            violent_Kk += 1
        else:
            violent_kk += 1
        
    print(f"Total creatures: {len(creatures)}")
    print(f"SPEED | Fast (SS): {speed_SS} | Fast (Ss): {speed_Ss} | Slow (ss): {speed_ss}")
    print(f"SIGHT | Blind (VV): {vision_VV} | Blind (Vv): {vision_Vv} | Eagle-Eyed (vv): {vision_vv}")
    print(f"Attractivness | Hot (AA): {beauty_AA} | Ugly (Aa): {beauty_Aa} | Ugly (aa): {beauty_aa}")
    print(f"Violence | Strong (KK): {violent_KK} | Hybrid (Kk): {violent_Kk} | Peaceful (kk): {violent_kk}")
    print(f"kill count = {killcnt}")
    print("-" * 40)

    with open("natural_selection_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            tick_count,
            len(creatures),
            speed_SS, speed_Ss, speed_ss,
            vision_VV, vision_Vv, vision_vv,
            beauty_AA, beauty_Aa, beauty_aa,
            violent_KK, violent_Kk, violent_kk
        ])

# --- Setup the Window ---
root = tk.Tk()
root.title("Natural Selection Simulation")
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
canvas.pack()

update_simulation() 

root.mainloop()
