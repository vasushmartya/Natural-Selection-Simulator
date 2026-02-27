import tkinter as tk
import random
import csv

screen_width = 800
screen_height = 600

run_after_time = 50
tick_count = 0

dominant_speed = 10
recessive_speed = 5

dominant_vision = 50
recessive_vision = 200

dominant_attractive_chance = 0.4
recessive_attractive_chance = 0.8

n_initial_creatures = 50
n_initial_bushes = 20

with open("natural_selection_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Tick", "Total Creatures", "Speed_SS", "Speed_Ss", "Speed_ss", "Vision_VV", "Vision_Vv", "Vision_vv", "Beauty_AA", "Beauty_Aa", "Beauty_aa"])

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
    def __init__(self, x, y, speed_genes, sight_genes, attractive_genes):
        self.x = x
        self.y = y
        self.speed_genes = speed_genes
        self.sight_genes = sight_genes
        self.attractive_genes = attractive_genes
        self.energy = 100
        
        # 1. Speed Trait (S/s)
        self.speed = dominant_speed if 'S' in speed_genes else recessive_speed
        
        # 2. Vision Trait (V/v)
        self.sight_radius = dominant_vision if 'v' in sight_genes else recessive_vision

        # 3. Attractiveness Trait (A/a)
        self.mating_chance = dominant_attractive_chance if 'a' in attractive_genes else recessive_attractive_chance

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
        
        # 5% chance of mutation for Speed
        if random.random() < 0.05:
            baby_speed[0] = 'S' if baby_speed[0] == 's' else 's'
            
        # 5% chance of mutation for Sight
        if random.random() < 0.05:
            baby_sight[0] = 'V' if baby_sight[0] == 'v' else 'v'
        
        # 5% chance of mutation for Attractiveness
        if random.random() < 0.05:
            baby_attractive[0] = 'A' if baby_attractive[0] == 'a' else 'a'
            
        return Creature(self.x, self.y, baby_speed, baby_sight, baby_attractive)

creatures = []
# Create 50 creatures
for _ in range(n_initial_creatures):
    s_genes = [random.choice(['S', 's']), random.choice(['S', 's'])]
    v_genes = [random.choice(['V', 'v']), random.choice(['V', 'v'])]
    a_genes = [random.choice(['A', 'a']), random.choice(['A', 'a'])]
    creatures.append(Creature(400, 300, s_genes, v_genes, a_genes))

bushes = []
for _ in range(n_initial_bushes):
    bushes.append(Bush())

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
    
    # We can use the outline color to show their VISION trait
    # Gold border if they have mutant good sight (vv), black border if bad sight (V)
    border_color = "gold" if 'v' in creature.sight_genes and 'V' not in creature.sight_genes else "black"
    
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

    # Clear the board
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

    # Update and draw Creatures
    for creature in creatures[:]: 
        
        # Check for death
        if creature.energy <= 0:
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
                    # Give them +50 energy, cap at 150.
                    creature.energy += 50
                    if creature.energy > 150:
                        creature.energy = 150
                    
                    bush.is_full = False

                    # Check Overeating
                    bush.times_eaten += 1
                    if bush.times_eaten >= bush.max_eaten:
                        bush.is_dead = True

                    break 

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
        
    print(f"Total creatures: {len(creatures)}")
    print(f"SPEED | Fast (SS): {speed_SS} | Fast (Ss): {speed_Ss} | Slow (ss): {speed_ss}")
    print(f"SIGHT | Blind (VV): {vision_VV} | Blind (Vv): {vision_Vv} | Eagle-Eyed (vv): {vision_vv}")
    print(f"Attractivness | Hot (AA): {beauty_AA} | Ugly (Aa): {beauty_Aa} | Ugly (aa): {beauty_aa}")
    print("-" * 40)

    with open("natural_selection_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([tick_count, len(creatures), speed_SS, speed_Ss, speed_ss, vision_VV, vision_Vv, vision_vv, beauty_AA, beauty_Aa, beauty_aa])

# --- Setup the Window ---
root = tk.Tk()
root.title("Natural Selection Simulation")
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
canvas.pack()

update_simulation() 

root.mainloop()
