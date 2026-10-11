import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("heart.csv")
print(df.shape)
print(df.head())

age=df["age"]
chol=df["chol"]
trestbps=df["trestbps"]
thalach=df["thalach"]

fig, axes=plt.subplots(nrows=2, ncols=2, figsize=(8,8))
axes[0,0].hist(age,color="yellow",edgecolor="black")
axes[0,0].set_title("age")
axes[0,1].hist(chol,color="red",edgecolor="black")
axes[0,1].set_title("chol")
axes[1,0].hist(trestbps,color="blue",edgecolor="black")
axes[1,0].set_title("trestbps")
axes[1,1].hist(thalach,color="green",edgecolor="black")
axes[1,1].set_title("thalach")
plt.savefig("Health_graphs.png")

import scipy.stats as st
fig2, axes2=plt.subplots(nrows=2, ncols=2, figsize=(12,12))
st.probplot(age, dist="norm", plot=axes2[0,0])
axes2[0,0].set_title("age")

st.probplot(chol, dist="norm", plot=axes2[0,1])
axes2[0,1].set_title("chol")

st.probplot(trestbps, dist="norm", plot=axes2[1,0])
axes2[1,0].set_title("trestbps")

st.probplot(thalach, dist="norm", plot=axes2[1,1])
axes2[1,1].set_title("thalach")
plt.savefig("Distribution.png")
plt.show()