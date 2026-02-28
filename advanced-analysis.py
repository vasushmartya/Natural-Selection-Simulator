import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("natural_selection_data.csv")

# Feature Engineering: Group the populations
# Prey = Peaceful (kk)
df['Prey'] = df['Violence_kk']
# Predators = Strong (KK) + Hybrid (Kk)
df['Predators'] = df['Violence_KK'] + df['Violence_Kk']

# Smooth the data slightly to remove frame-by-frame noise (Rolling Average)
df['Prey_Smooth'] = df['Prey'].rolling(window=20).mean()
df['Predators_Smooth'] = df['Predators'].rolling(window=20).mean()

# Drop NaN values caused by the rolling window
df = df.dropna()

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# --- PLOT 1: THE PHASE PORTRAIT ---
# Plotting Predators vs Prey directly
sns.scatterplot(ax=axes[0], x=df['Prey_Smooth'], y=df['Predators_Smooth'], 
                hue=df['Tick'], palette="viridis", s=10, edgecolor=None)
axes[0].set_title("Phase Portrait: Predator vs. Prey Dynamics")
axes[0].set_xlabel("Prey Population (kk)")
axes[0].set_ylabel("Predator Population (KK + Kk)")

# --- PLOT 2: CROSS-CORRELATION (Finding the Lag) ---
# We must mean-center the data to use xcorr
prey_centered = df['Prey_Smooth'] - df['Prey_Smooth'].mean()
pred_centered = df['Predators_Smooth'] - df['Predators_Smooth'].mean()

# Plot the cross-correlation
axes[1].xcorr(prey_centered, pred_centered, maxlags=150, usevlines=True, 
              linewidth=2, color='coral')
axes[1].set_title("Cross-Correlation: Statistical Lag")
axes[1].set_xlabel("Lag (Ticks)")
axes[1].set_ylabel("Correlation Coefficient (r)")
axes[1].grid(True)

plt.tight_layout()
plt.show()

# --- FIND THE EXACT MATHEMATICAL LAG ---
# Numpy correlate calculates the sliding dot product
correlations = np.correlate(prey_centered, pred_centered, mode='full')
# Find the index of the highest correlation
best_lag_index = np.argmax(correlations)
# Convert index to actual lag (mode='full' makes the center 0)
actual_lag = best_lag_index - (len(prey_centered) - 1)

print("-" * 50)
print(f"DATA SCIENCE REPORT:")
print(f"Max correlation found at a lag of: {abs(actual_lag)} ticks.")
if actual_lag < 0:
    print("Conclusion: The Predator population statistically LAGS behind the Prey.")
print("-" * 50)