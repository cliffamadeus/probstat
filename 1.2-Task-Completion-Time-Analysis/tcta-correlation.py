import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from google.colab import files

# Upload Dataset
print("Upload CSV file")
uploaded = files.upload()

filename = next(iter(uploaded))
df = pd.read_csv(filename)

print("\nDATASET")
print(df)

# Validate Required Columns

required_columns = ["user", "before", "after"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Descriptive Statistics Function

def descriptive_stats(series, label):

    mean = series.mean()
    median = series.median()
    std = series.std()
    var = series.var()
    cv = (std / mean) * 100

    print(f"\n{label}")
    print("-" * 40)
    print(f"Mean: {mean:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Variance: {var:.2f}")
    print(f"Standard Deviation: {std:.2f}")
    print(f"Coefficient of Variation: {cv:.2f}%")

    if cv < 10:
        consistency = "Highly Consistent"
    elif cv < 20:
        consistency = "Consistent"
    elif cv < 30:
        consistency = "Moderately Consistent"
    else:
        consistency = "Inconsistent"

    print(f"Consistency Interpretation: {consistency}")

    return mean, std

# Descriptive Statistics

before_mean, before_std = descriptive_stats(
    df["before"],
    "BEFORE ENHANCEMENT ANALYSIS"
)

after_mean, after_std = descriptive_stats(
    df["after"],
    "AFTER ENHANCEMENT ANALYSIS"
)

# Normality Test

difference = df["before"] - df["after"]

shapiro_stat, shapiro_p = stats.shapiro(difference)

print("\nNORMALITY TEST (Shapiro-Wilk)")
print("-" * 40)
print(f"Statistic: {shapiro_stat:.4f}")
print(f"P-value: {shapiro_p:.4f}")

if shapiro_p > 0.05:
    print("Result: Differences are approximately normally distributed.")
else:
    print("Result: Differences may not be normally distributed.")

# Paired T-Test

t_stat, p_value = stats.ttest_rel(
    df["before"],
    df["after"]
)

print("\nPAIRED T-TEST ANALYSIS")
print("-" * 40)
print(f"T Statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

alpha = 0.05

if p_value < alpha:
    print("Decision: Reject H₀")
    print("Interpretation: Significant improvement detected.")
else:
    print("Decision: Fail to Reject H₀")
    print("Interpretation: No significant improvement detected.")

# Effect Size (Cohen's d)

cohens_d = difference.mean() / difference.std()

print("\nEFFECT SIZE ANALYSIS")
print("-" * 40)
print(f"Cohen's d: {cohens_d:.4f}")

if abs(cohens_d) < 0.20:
    effect = "Negligible"
elif abs(cohens_d) < 0.50:
    effect = "Small"
elif abs(cohens_d) < 0.80:
    effect = "Medium"
else:
    effect = "Large"

print(f"Effect Size Interpretation: {effect}")

# Improvement Percentage

improvement = (
    (before_mean - after_mean)
    / before_mean
) * 100

print("\nIMPROVEMENT ANALYSIS")
print("-" * 40)
print(f"Average Improvement: {improvement:.2f}%")

# Charts

# Boxplot

plt.figure(figsize=(8,5))
plt.boxplot(
    [df["before"], df["after"]],
    labels=["Before", "After"]
)
plt.title("Task Completion Time Comparison")
plt.ylabel("Time (Seconds)")
plt.show()

# Mean Comparison

plt.figure(figsize=(6,5))
plt.bar(
    ["Before", "After"],
    [before_mean, after_mean]
)
plt.title("Average Completion Time")
plt.ylabel("Seconds")
plt.show()

# Participant Comparison

plt.figure(figsize=(10,5))
plt.plot(df["user"], df["before"], marker='o', label="Before")
plt.plot(df["user"], df["after"], marker='o', label="After")
plt.title("Participant Completion Times")
plt.xlabel("Participant")
plt.ylabel("Time (Seconds)")
plt.legend()
plt.grid(True)
plt.show()

# Final Summary
print("\nFINAL INTERPRETATION")
print("-" * 40)

print(
    f"The average completion time decreased from "
    f"{before_mean:.2f} seconds to "
    f"{after_mean:.2f} seconds."
)

print(
    f"This represents an improvement of "
    f"{improvement:.2f}%."
)

if p_value < 0.05:
    print(
        "The paired t-test indicates that the improvement "
        "is statistically significant at α = 0.05."
    )
else:
    print(
        "The paired t-test indicates that the improvement "
        "is not statistically significant at α = 0.05."
    )

print(
    f"The effect size was {effect.lower()} "
    f"(Cohen's d = {cohens_d:.2f})."
)