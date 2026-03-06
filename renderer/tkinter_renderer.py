import tkinter as tk


class TkinterRenderer:
    def __init__(self, world):
        self.world = world

        self.root = tk.Tk()
        self.root.title("Natural Selection Simulation")

        self.canvas = tk.Canvas(
            self.root,
            width=world.config.screen_width,
            height=world.config.screen_height,
            bg="white"
        )
        self.canvas.pack()

    def draw(self):
        self.canvas.delete("all")

        # Draw bushes first
        for bush in self.world.bushes:
            r = bush.radius
            x1, y1 = bush.x - r, bush.y - r
            x2, y2 = bush.x + r, bush.y + r
            
            if bush.is_dead:
                self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill="saddlebrown", outline="brown")
                continue # Stop drawing here so we don't draw green leaves!

            self.canvas.create_oval(x1, y1, x2, y2, fill="lawn green", outline="black")
            
            if bush.is_full:
                x11 = bush.x - 5
                y11 = bush.y - 5
                x21 = bush.x + 5
                y21 = bush.y + 5
                self.canvas.create_oval(x11, y11, x21, y21, fill="red")

        # Draw creatures
        for creature in self.world.creatures:
            r = 5
            x1 = creature.x - r
            y1 = creature.y - r
            x2 = creature.x + r
            y2 = creature.y + r
            
            speed = "".join(sorted(creature.genes["speed"]))
            if speed == "SS":
                color = "purple"
            elif speed == "Ss":
                color = "blue"
            else: # "ss"
                color = "cyan"
                
            if 'K' in creature.genes["violence"]:
                border_color = "red"
            elif 'v' in creature.genes["vision"] and 'V' not in creature.genes["vision"]:
                border_color = "gold"
            else:
                border_color = "black"

            dash_style = True if 'a' in creature.genes["attractiveness"] else None

            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=border_color, width=2, dash=dash_style)

        self.root.update()