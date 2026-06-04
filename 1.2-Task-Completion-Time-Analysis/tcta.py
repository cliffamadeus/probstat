import pandas as pd
from google.colab import files

# Upload CSV
uploaded = files.upload()

filename = next(iter(uploaded))

df = pd.read_csv(filename)

print("TASK COMPLETION DATASET")
print(df)

# Descriptive Statistics
mean_time = df["completion_time"].mean()
median_time = df["completion_time"].median()
std_time = df["completion_time"].std()
var_time = df["completion_time"].var()
cv_time = (std_time / mean_time) * 100

print("\nTASK COMPLETION ANALYSIS")
print(f"Mean Time: {mean_time:.2f} sec")
print(f"Median Time: {median_time:.2f} sec")
print(f"Variance: {var_time:.2f}")
print(f"Standard Deviation: {std_time:.2f}")
print(f"Coefficient of Variation: {cv_time:.2f}%")

# Interpretation
if cv_time < 10:
    consistency = "Highly Consistent"
elif cv_time < 20:
    consistency = "Consistent"
elif cv_time < 30:
    consistency = "Moderately Consistent"
else:
    consistency = "Inconsistent"

print(f"Consistency Interpretation: {consistency}")