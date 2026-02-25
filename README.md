# 🌱 Natural Selection & Evolution Simulator

A Python-based, real-time 2D simulation of Darwinian evolution, genetic inheritance, and population dynamics. Watch as a population of "creatures" fights for survival, mutates, and adapts to their environment!

Inspired by ecosystem and evolution simulations, this project uses `tkinter` for the visual simulation and `pandas`/`seaborn` for tracking and graphing the ecological data.

## ✨ Features

* **🧬 Mendelian Genetics:** Creatures possess distinct traits (Speed and Vision) determined by dominant and recessive alleles (e.g., `SS`, `Ss`, `ss`). 
* **❤️ Reproduction & Mutation:** Well-fed creatures can mate when they collide, passing down a mix of genes using Punnett square logic, with a 5% chance of genetic mutation.
* **⚡ Metabolism System:** Every movement burns energy. Fast creatures have an evolutionary advantage in reaching food, but risk starving to death faster if they can't sustain their high metabolism.
* **🧠 Biased Movement (Sight):** Creatures calculate vectors and normalize their movement to actively hunt down food within their visual radius.
* **📊 Data Tracking:** The simulation actively logs the population sizes of every genotype and exports it to a CSV to be graphed.

## 📸 Emergent Gameplay Discovered
During testing, we discovered real-world biological concepts emerging organically from the code:
1. **Carrying Capacity:** The environment naturally hit a logistic growth curve, stabilizing at around ~105 creatures based on the regrowth rate of the food supply.
2. **The Swarm Trap:** In highly food-dense environments, "Eagle-Eyed" creatures wasted energy pathfinding to distant food, while "Blind" creatures stumbled into nearby food by pure chance. The blind creatures naturally selected themselves as the dominant species!

## 🛠️ Installation & Requirements

Make sure you have Python 3.x installed. You will also need to install the following libraries for data tracking and visualization:

```bash
pip install pandas matplotlib seaborn

```

*(Note: `tkinter` is used for the simulation engine, which comes pre-installed with most Python distributions).*

## 🚀 How to Run

**1. Start the Simulation**
Run the main Python file to launch the `tkinter` window and start the simulation.

```bash
python simul.py

```

*Watch the console! It will print real-time statistics about the surviving genotypes.*

**2. Graph the Data**
Once the simulation has run for a sufficient number of ticks, close the window. The data will be saved to `natural_selection_data.csv`. Run the graphing script to visualize your ecosystem's history:

```bash
python simuldata.py

```

## ⚙️ Modding the Environment

You can easily tweak the ecosystem balance by changing a few variables at the top of `simul.py`:

* `bushes`: Change the starting loop (e.g., `range(20)`) to increase or decrease the food supply.
* `regenTime`: Change how fast the bushes grow back their berries.
* `dominant_speed` / `recessive_speed`: Tweak the movement speeds of the genetic traits.

## 🤝 Contributing

Feel free to fork this project and add your own evolutionary mechanics! Some ideas for future updates:

* Add attractive gene for mating chance
* Add Gender
* Trees dying out from overeating
* Tree regeneration
* Add a "Size" gene that determines who wins in a fight over food.
* Add a Carnivore / Predator species.
* Add an aging system so creatures eventually die of old age.
