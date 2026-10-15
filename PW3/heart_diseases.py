import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

# Part 1
df = pd.read_csv("heart.csv")

print(df.shape)
print(df.head())

age = df["age"]
chol = df["chol"]
trestbps = df["trestbps"]
thalach = df["thalach"]


# Part 2
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

axes[0,0].hist(age, color="yellow", edgecolor="black")
axes[0,1].hist(chol, color="red", edgecolor="black")
axes[1,0].hist(trestbps, color="blue", edgecolor="black")
axes[1,1].hist(thalach, color="green", edgecolor="black")

axes[0,0].set_title("Age")
axes[0,1].set_title("Cholesterol level")
axes[1,0].set_title("Resting blood pressure")
axes[1,1].set_title("Maximum heart rate")

plt.tight_layout()
plt.savefig("Health_graphs.png")


# Part 3
cols = ["age", "chol", "trestbps", "thalach"]

for c in cols:
    print(f"{c} skewness: {st.skew(df[c])}")

fig2, axes2 = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

st.probplot(age, dist="norm", plot=axes2[0, 0])
st.probplot(chol, dist="norm", plot=axes2[0, 1])
st.probplot(trestbps, dist="norm", plot=axes2[1, 0])
st.probplot(thalach, dist="norm", plot=axes2[1, 1])

axes2[0,0].set_title("Age")
axes2[0,1].set_title("Cholesterol level")
axes2[1,0].set_title("Resting blood pressure")
axes2[1,1].set_title("Maximum heart rate")

plt.tight_layout()
plt.savefig("Distribution.png")


# Part 4
thalach_healthy = list()
thalach_ill = list()

for i, t in enumerate(df["target"]):
    if t == 0:
        thalach_healthy.append(df["thalach"].iloc[i])
    else:
        thalach_ill.append(df["thalach"].iloc[i])

result = st.mannwhitneyu(thalach_healthy, thalach_ill)

if result.pvalue < 0.05:
    print("The groups have significantly different distributions.")
else:
    print("There is no significant difference between the groups.")

healthy_mean = np.mean(thalach_healthy)
ill_mean = np.mean(thalach_ill)

healthy_err = st.sem(thalach_healthy)
ill_err = st.sem(thalach_ill)

print("Healthy mean:", healthy_mean)
print("Healthy standard error:", healthy_err)

print("Ill mean:", ill_mean)
print("Ill standard error:", ill_err)

fig3, ax3 = plt.subplots(figsize=(6, 6))

ax3.bar(
    ["Healthy", "Ill"],
    [healthy_mean, ill_mean],
    yerr=[healthy_err, ill_err],
    color=["yellow", "green"],
    edgecolor="black",
    capsize=5
)

ax3.set_ylabel("Maximum heart rate")
ax3.set_title("Mean maximum heart rate")

plt.tight_layout()
plt.savefig("Heart_rate_comparison.png")


# Part 5
correlation, p = st.pearsonr(age, thalach)

print("Age and heart rate correlation:", correlation)
if correlation < 0:
    print("Age and maximum heart rate have a negative relationship.")
elif correlation > 0:
    print("Age and maximum heart rate have a positive relationship.")
else:
    print("There is no linear relationship.")

fig4, ax4 = plt.subplots(figsize=(6, 6))
ax4.scatter(age, thalach, color="blue", edgecolor="black")
ax4.set_xlabel("Age")
ax4.set_ylabel("Maximum heart rate")
ax4.set_title("Age vs maximum heart rate")

plt.tight_layout()
plt.savefig("Age_Heart_rate.png")


# Part 6
df2 = pd.read_csv("chemicals_cancer.csv")

print(df2.shape)
print(df2.head())

benzene = df2["benzene"]
cadmium = df2["cadmium"]
malignancy = df2["malignancy"]

correlation_benzene, p_benzene = st.pearsonr(benzene, malignancy)
correlation_cadmium, p_cadmium = st.pearsonr(cadmium, malignancy)

print("Benzene correlation:", correlation_benzene)
print("Cadmium correlation:", correlation_cadmium)

if abs(correlation_benzene) > abs(correlation_cadmium):
    print("Naive analysis: benzene appears more strongly associated with malignancy.")
else:
    print("Naive analysis: cadmium appears more strongly associated with malignancy.")


# Part 7
df_filtered = df2[(df2["pollution_index"] > 40) &(df2["pollution_index"] < 60)]

benzene_filtered = df_filtered["benzene"]
cadmium_filtered = df_filtered["cadmium"]
malignancy_filtered = df_filtered["malignancy"]

correlation_benzene_filtered, p_benzene_filtered = st.pearsonr(benzene_filtered, malignancy_filtered)
correlation_cadmium_filtered, p_cadmium_filtered = st.pearsonr(cadmium_filtered, malignancy_filtered)

print("Number of patients after filtering:", len(df_filtered))
print("Benzene correlation after filtering:", correlation_benzene_filtered)
print("Cadmium correlation after filtering:", correlation_cadmium_filtered)