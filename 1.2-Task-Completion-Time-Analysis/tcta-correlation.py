import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from google.colab import files

 
# Upload BEFORE Enhancement Dataset
print("Upload BEFORE Enhancement CSV")
uploaded_before = files.upload()

before_file = next(iter(uploaded_before))
before = pd.read_csv(before_file)

print("\nBEFORE ENHANCEMENT DATASET")
print(before)

 
# Upload AFTER Enhancement Dataset
print("\nUpload AFTER Enhancement CSV")
uploaded_after = files.upload()

after_file = next(iter(uploaded_after))
after = pd.read_csv(after_file)

print("\nAFTER ENHANCEMENT DATASET")
print(after)

 
# Validate Dataset Length
if len(before) != len(after):
    raise ValueError(
        "Both datasets must contain the same number of participants for a Paired T-Test."
    )

 
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

before_mean, before_std = descriptive_stats(
    before["completion_time"],
    "BEFORE ENHANCEMENT ANALYSIS"
)

after_mean, after_std = descriptive_stats(
    after["completion_time"],
    "AFTER ENHANCEMENT ANALYSIS"
)

 
# Correlation Analysis
 

r, p_corr = stats.pearsonr(
    before["completion_time"],
    after["completion_time"]
)

print("\nCORRELATION ANALYSIS")
print("-" * 40)
print(f"Pearson Correlation (r): {r:.4f}")
print(f"p-value: {p_corr:.4f}")

if abs(r) >= 0.90:
    strength = "Very Strong"
elif abs(r) >= 0.70:
    strength = "Strong"
elif abs(r) >= 0.50:
    strength = "Moderate"
elif abs(r) >= 0.30:
    strength = "Weak"
else:
    strength = "Very Weak"

print(f"Relationship Strength: {strength}")

 
# Paired T-Test
t_stat, p_value = stats.ttest_rel(
    before["completion_time"],
    after["completion_time"]
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

 
# Cohen's d Effect Size
difference = (
    before["completion_time"]
    - after["completion_time"]
)

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
    [
        before["completion_time"],
        after["completion_time"]
    ],
    labels=["Before", "After"]
)
plt.title("Task Completion Time Comparison")
plt.ylabel("Time (Seconds)")
plt.show()

# Mean Comparison
print("\n")
plt.figure(figsize=(6,5))
plt.bar(
    ["Before", "After"],
    [before_mean, after_mean]
)
plt.title("Average Completion Time")
plt.ylabel("Seconds")
plt.show()

# Scatter Plot
print("\n")
plt.figure(figsize=(6,5))
plt.scatter(
    before["completion_time"],
    after["completion_time"]
)
print("\n")
plt.xlabel("Before Enhancement")
print("\n")
plt.ylabel("After Enhancement")
print("\n")
plt.title("Correlation Analysis")
print("\n")
plt.grid(True)
plt.show()

 
# Final Summary
print("\nFINAL INTERPRETATION")
print("-" * 40)

print(
    f"The average completion time changed from "
    f"{before_mean:.2f} sec to "
    f"{after_mean:.2f} sec."
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