import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from google.colab import files


# Upload CSV
print("Upload a CSV file containing:")
print("user,sus,completion_time")

uploaded = files.upload()

filename = next(iter(uploaded))

df = pd.read_csv(filename)


# Display Dataset
print("\nDATASET")
print("=" * 50)
print(df)

# Descriptive Statistics

print("\nDESCRIPTIVE STATISTICS")
print("=" * 50)

print(f"Mean SUS: {df['sus'].mean():.2f}")
print(f"Mean Completion Time: {df['completion_time'].mean():.2f}")

print(f"\nSUS Standard Deviation: {df['sus'].std():.2f}")
print(f"Completion Time Standard Deviation: {df['completion_time'].std():.2f}")

# Pearson Correlation
r, p = pearsonr(
    df["sus"],
    df["completion_time"]
)

print("\nCORRELATION ANALYSIS")
print("=" * 50)

print(f"Pearson Correlation Coefficient (r): {r:.4f}")
print(f"P-value: {p:.10f}")

# Strength Interpretation
abs_r = abs(r)

if abs_r >= 0.90:
    strength = "Very Strong"
elif abs_r >= 0.70:
    strength = "Strong"
elif abs_r >= 0.50:
    strength = "Moderate"
elif abs_r >= 0.30:
    strength = "Weak"
else:
    strength = "Negligible"

direction = "Positive" if r > 0 else "Negative"

print(f"\nRelationship: {strength} {direction} Correlation")


# Statistical Significance
alpha = 0.05

if p < alpha:
    significance = "Significant"
else:
    significance = "Not Significant"

print(f"Statistical Significance: {significance}")


# Research Interpretation
print("\nINTERPRETATION")
print("=" * 50)

if r < 0:
    print(
        f"There is a {strength.lower()} negative relationship "
        f"between SUS scores and task completion time "
        f"(r = {r:.4f}, p = {p:.4f}). "
        f"Users who completed tasks faster tended to report "
        f"higher usability scores."
    )
else:
    print(
        f"There is a {strength.lower()} positive relationship "
        f"between SUS scores and task completion time "
        f"(r = {r:.4f}, p = {p:.4f})."
    )


# Scatter Plot
plt.figure(figsize=(8,5))

plt.scatter(
    df["completion_time"],
    df["sus"]
)

plt.title("SUS vs Task Completion Time")
plt.xlabel("Task Completion Time (seconds)")
plt.ylabel("SUS Score")

plt.grid(True)

plt.show()