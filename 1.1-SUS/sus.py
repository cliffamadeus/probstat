import pandas as pd
from google.colab import files

# Upload CSV
uploaded = files.upload()

filename = next(iter(uploaded))

df = pd.read_csv(filename)

print("SUS DATASET")
print(df)

# Descriptive Statistics
mean_sus = df["sus"].mean()
median_sus = df["sus"].median()
std_sus = df["sus"].std()
var_sus = df["sus"].var()
cv_sus = (std_sus / mean_sus) * 100

print("\nSUS ANALYSIS")
print(f"Mean SUS: {mean_sus:.2f}")
print(f"Median SUS: {median_sus:.2f}")
print(f"Variance: {var_sus:.2f}")
print(f"Standard Deviation: {std_sus:.2f}")
print(f"Coefficient of Variation: {cv_sus:.2f}%")

# SUS Interpretation
if mean_sus >= 80:
    interpretation = "Excellent"
elif mean_sus >= 68:
    interpretation = "Good"
else:
    interpretation = "Needs Improvement"

print(f"Usability Interpretation: {interpretation}")