import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
 
os.makedirs("results", exist_ok=True)
os.makedirs("figures", exist_ok=True)
 
wine = load_wine(as_frame=True)
X = wine.data
cultivar = wine.target
print(wine.DESCR)
print(X.describe().round(3))
 
pca_raw = PCA()
pca_raw.fit(X)
print("Raw PC1 explained variance ratio:", pca_raw.explained_variance_ratio_[0].round(4))
raw_loadings = pd.Series(pca_raw.components_[0], index=X.columns)
print(raw_loadings.sort_values(key=abs, ascending=False).round(4))
 
scaler = StandardScaler()
Z = scaler.fit_transform(X)
print("Mean of Z:", Z.mean(axis=0).round(3))
print("Std of Z:", Z.std(axis=0).round(3))
 
pca = PCA()
scores = pca.fit_transform(Z)
evr = pca.explained_variance_ratio_
cum = np.cumsum(evr)
pca_table = pd.DataFrame({
    "component": ["PC" + str(i + 1) for i in range(len(evr))],
    "explained": evr, "cumulative": cum}).round(3)
print(pca_table)
pca_table.to_csv("results/B3_variance.csv", index=False)
print("Components for 90%:", np.argmax(cum >= 0.9) + 1)
print("PC1-PC2 keep:", cum[1].round(3))
 
plt.figure()
plt.bar(range(1, len(evr) + 1), evr, label="explained")
plt.plot(range(1, len(evr) + 1), cum, "o-", color="k", label="cumulative")
plt.axhline(0.9, color="r", ls="--", label="0.9")
plt.xlabel("Principal component")
plt.ylabel("Explained variance ratio")
plt.title("Scree plot (scaled data)")
plt.legend()
plt.savefig("figures/B3_scree.png", dpi=150)
plt.close()
 
loadings = pd.DataFrame(pca.components_[:2].T, index=X.columns,
                        columns=["PC1", "PC2"]).round(3)
print(loadings.sort_values("PC1"))
print(loadings.sort_values("PC2"))
loadings.to_csv("results/B3_loadings.csv")
 
plt.figure()
plt.scatter(scores[:, 0], scores[:, 1])
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Wines on PC1-PC2")
plt.savefig("figures/B3_pc1_pc2.png", dpi=150)
plt.close()
 
seed_rows = []
for rs in range(8):
    k1 = KMeans(n_clusters=3, init="k-means++", n_init=1, random_state=rs).fit(Z)
    seed_rows.append({"random_state": rs, "inertia": k1.inertia_})
seed_df = pd.DataFrame(seed_rows).round(3)
print(seed_df)
seed_df.to_csv("results/B4_seeds.csv", index=False)
 
ks = list(range(1, 11))
inertias = []
for k in ks:
    kk = KMeans(n_clusters=k, init="k-means++", n_init=10, max_iter=300,
                random_state=0).fit(Z)
    inertias.append(kk.inertia_)
elbow_df = pd.DataFrame({"k": ks, "inertia": inertias}).round(3)
print(elbow_df)
elbow_df.to_csv("results/B4_elbow.csv", index=False)
 
plt.figure()
plt.plot(ks, inertias, "o-")
plt.xlabel("k")
plt.ylabel("Inertia")
plt.title("Elbow curve")
plt.savefig("figures/B4_elbow.png", dpi=150)
plt.close()
 
k_best = 3
km = KMeans(n_clusters=k_best, init="k-means++", n_init=10, max_iter=300,
            random_state=0).fit(Z)
print("Cluster sizes:", np.bincount(km.labels_))
centres = pd.DataFrame(scaler.inverse_transform(km.cluster_centers_),
                       columns=X.columns).round(2)
print(centres.T)
centres.to_csv("results/B5_centres.csv")
 
plt.figure()
plt.scatter(scores[:, 0], scores[:, 1], c=km.labels_)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("K-Means clusters on PC1-PC2")
plt.savefig("figures/B5_clusters.png", dpi=150)
plt.close()
 
def agreement(labels):
    table = pd.crosstab(cultivar, labels)
    return table, table.max(axis=0).sum() / len(cultivar)
 
table_s, agr_s = agreement(km.labels_)
km_raw = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
table_r, agr_r = agreement(km_raw.labels_)
km_pc = KMeans(n_clusters=3, n_init=10, random_state=0).fit(scores[:, :2])
table_p, agr_p = agreement(km_pc.labels_)
print(table_s)
print(table_r)
print(table_p)
 
B_agreement = pd.DataFrame({
    "version": ["scaled", "raw", "PC1-PC2"],
    "agreement": [agr_s, agr_r, agr_p]}).round(3)
print(B_agreement)
B_agreement.to_csv("results/B_agreement.csv", index=False)
 
Xtr, Xte, ytr, yte = train_test_split(X, cultivar, test_size=0.25,
                                      random_state=42, stratify=cultivar)
full = make_pipeline(StandardScaler(), KNeighborsClassifier(5)).fit(Xtr, ytr)
two = make_pipeline(StandardScaler(), PCA(n_components=2),
                    KNeighborsClassifier(5)).fit(Xtr, ytr)
print("KNN, 13 features:", round(full.score(Xte, yte), 3))
print("PCA(2) + KNN:", round(two.score(Xte, yte), 3))
