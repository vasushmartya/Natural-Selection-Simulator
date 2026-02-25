import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("natural_selection_data.csv")

sns.set_palette("husl")
sns.lineplot(data=df, x="Tick", y="Total Creatures", label="Total Creatures")
sns.lineplot(data=df, x="Tick", y="Speed_SS", label="Speed_SS")
sns.lineplot(data=df, x="Tick", y="Speed_Ss", label="Speed_Ss")
sns.lineplot(data=df, x="Tick", y="Speed_ss", label="Speed_ss")
sns.lineplot(data=df, x="Tick", y="Vision_VV", label="Vision_VV")
sns.lineplot(data=df, x="Tick", y="Vision_Vv", label="Vision_Vv")
sns.lineplot(data=df, x="Tick", y="Vision_vv", label="Vision_vv")

plt.show()