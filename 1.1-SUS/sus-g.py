import pandas as pd
from google.colab import files

# Upload CSV
uploaded = files.upload()

filename = next(iter(uploaded))

df = pd.read_csv(filename)

print("SUS DATASET")
print(df)

# SUS Question Columns
sus_columns = [f"Q{i}" for i in range(1, 11)]

# Calculate SUS Score
def calculate_sus(row):
    score = 0

    for i, col in enumerate(sus_columns, start=1):
        response = row[col]

        # Odd-numbered items
        if i % 2 == 1:
            score += response - 1

        # Even-numbered items
        else:
            score += 5 - response

    return score * 2.5

# Compute SUS Scores
df["sus_score"] = df.apply(calculate_sus, axis=1)

print("\nINDIVIDUAL SUS SCORES")
if "user" in df.columns:
    print(df[["user", "sus_score"]])
else:
    print(df[["sus_score"]])

# Descriptive Statistics
mean_sus = df["sus_score"].mean()
median_sus = df["sus_score"].median()
std_sus = df["sus_score"].std()
var_sus = df["sus_score"].var()
cv_sus = (std_sus / mean_sus) * 100

print("\nSUS ANALYSIS")
print(f"Mean SUS Score: {mean_sus:.2f}")
print(f"Median SUS Score: {median_sus:.2f}")
print(f"Variance: {var_sus:.2f}")
print(f"Standard Deviation: {std_sus:.2f}")
print(f"Coefficient of Variation: {cv_sus:.2f}%")

# SUS Interpretation
if mean_sus >= 80.3:
    usability = "Excellent"
elif mean_sus >= 68:
    usability = "Good"
elif mean_sus >= 51:
    usability = "Below Average"
else:
    usability = "Poor"

print(f"Usability Interpretation: {usability}")

# Consistency Interpretation
if cv_sus < 10:
    consistency = "Highly Consistent"
elif cv_sus < 20:
    consistency = "Consistent"
elif cv_sus < 30:
    consistency = "Moderately Consistent"
else:
    consistency = "Inconsistent"

print(f"Consistency Interpretation: {consistency}")