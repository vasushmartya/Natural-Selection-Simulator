import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the new data
df = pd.read_csv("natural_selection_data.csv")
sns.set_theme(style="darkgrid")

# Create a massive dashboard with 4 subplots (2 rows, 2 columns)
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# We will plot "Total Creatures" faintly in the background of each graph for context!

# 1. Speed Evolution
sns.lineplot(ax=axes[0, 0], data=df, x="Tick", y="Total Creatures", color="red", alpha=0.2)
sns.lineplot(ax=axes[0, 0], data=df, x="Tick", y="Speed_SS", label="Fast (SS)", color="darkgoldenrod")
sns.lineplot(ax=axes[0, 0], data=df, x="Tick", y="Speed_Ss", label="Fast (Ss)", color="olivedrab")
sns.lineplot(ax=axes[0, 0], data=df, x="Tick", y="Speed_ss", label="Slow (ss)", color="lightseagreen")
axes[0, 0].set_title("Evolution of Speed")
axes[0, 0].set_ylabel("Population")

# 2. Vision Evolution
sns.lineplot(ax=axes[0, 1], data=df, x="Tick", y="Total Creatures", color="red", alpha=0.2)
sns.lineplot(ax=axes[0, 1], data=df, x="Tick", y="Vision_VV", label="Blind (VV)", color="darkgoldenrod")
sns.lineplot(ax=axes[0, 1], data=df, x="Tick", y="Vision_Vv", label="Blind (Vv)", color="olivedrab")
sns.lineplot(ax=axes[0, 1], data=df, x="Tick", y="Vision_vv", label="Eagle-Eyed (vv)", color="lightseagreen")
axes[0, 1].set_title("Evolution of Vision")
axes[0, 1].set_ylabel("Population")

# 3. Beauty Evolution
sns.lineplot(ax=axes[1, 0], data=df, x="Tick", y="Total Creatures", color="red", alpha=0.2)
sns.lineplot(ax=axes[1, 0], data=df, x="Tick", y="Beauty_AA", label="Hot (AA)", color="darkgoldenrod")
sns.lineplot(ax=axes[1, 0], data=df, x="Tick", y="Beauty_Aa", label="Ugly (Aa)", color="olivedrab")
sns.lineplot(ax=axes[1, 0], data=df, x="Tick", y="Beauty_aa", label="Ugly (aa)", color="lightseagreen")
axes[1, 0].set_title("Evolution of Attractiveness")
axes[1, 0].set_ylabel("Population")

# 4. Violence Evolution
sns.lineplot(ax=axes[1, 1], data=df, x="Tick", y="Total Creatures", color="red", alpha=0.2)
sns.lineplot(ax=axes[1, 1], data=df, x="Tick", y="Violence_KK", label="Strong (KK)", color="firebrick")
sns.lineplot(ax=axes[1, 1], data=df, x="Tick", y="Violence_Kk", label="Strong (Kk)", color="coral")
sns.lineplot(ax=axes[1, 1], data=df, x="Tick", y="Violence_kk", label="Peaceful (kk)", color="mediumseagreen")
axes[1, 1].set_title("Evolution of Violence (Predator vs Prey)")
axes[1, 1].set_ylabel("Population")

plt.tight_layout()
plt.savefig("Figure_1.png")
plt.show()