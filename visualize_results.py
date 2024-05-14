import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("tweet_data_with_returns.csv")

# Setting the aesthetic style for the plots
sns.set(style="whitegrid")

# Create a figure to hold the subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    "Histograms of Forward Returns at Different Intervals with Statistics", fontsize=16
)

# List of time intervals
time_intervals = ["1min", "5min", "15min", "60min"]
axes_list = [axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]]

for i, interval in enumerate(time_intervals):
    # Column name
    col_name = f"return_{interval}"

    # Histogram for each interval
    sns.histplot(df[col_name], kde=True, color=f"C{i}", ax=axes_list[i])
    axes_list[i].set_title(f"{interval} Forward Returns")
    axes_list[i].set_xlabel("Return")
    axes_list[i].set_ylabel("Frequency")

    # Calculate statistics
    mean_val = df[col_name].mean()
    var_val = df[col_name].var()

    # Display statistics on the histogram
    stats_text = f"Mean: {mean_val:.4f}\nVariance: {var_val:.4f}"
    axes_list[i].text(
        0.95,
        0.95,
        stats_text,
        transform=axes_list[i].transAxes,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(
            boxstyle="round,pad=0.3", edgecolor="black", facecolor="white", alpha=0.5
        ),
    )

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the plots
plt.show()

