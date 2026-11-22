import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                            confusion_matrix, accuracy_score, precision_score,
                            recall_score, f1_score)
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.inspection import permutation_importance
 
os.makedirs("results", exist_ok=True)
os.makedirs("figures", exist_ok=True)
 
df = pd.read_csv("data/concrete.csv")
print("Duplicate rows:", df.duplicate
.sum())
print("Missing values:")
print(df.isna().sum())
 
df = df.drop_duplicates().reset_index(drop=True)
X = df.drop("strength", axis=1)
y = df["strength"]
print(df.describe())
 
plt.figure()
plt.scatter(df["cement"], df["strength"])
plt.xlabel("Cement (kg/m3)")
plt.ylabel("Strength (MPa)")
plt.title("Strength vs Cement")
plt.savefig("figures/A2_cement.png", dpi=150)
plt.close()
 
plt.figure()
plt.scatter(df["age"], df["strength"])
plt.xlabel("Age (days)")
plt.ylabel("Strength (MPa)")
plt.title("Strength vs Age")
plt.savefig("figures/A2_age.png", dpi=150)
plt.close()
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("Training data size:", len(X_train))
print("Testing data size:", len(X_test))
 
model = LinearRegression()
model.fit(X_train, y_train)
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)
 
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)
n = len(X_train)
p = X_train.shape[1]
train_adjusted_r2 = 1 - (1 - train_r2) * (n - 1) / (n - p - 1)
 
A4_table = pd.DataFrame([{
    "train_rmse": train_rmse, "test_rmse": test_rmse, "test_mae": test_mae,
    "train_r2": train_r2, "train_adj_r2": train_adjusted_r2, "test_r2": test_r2,
}]).round(3)
print(A4_table)
A4_table.to_csv("results/A4_linear.csv", index=False)
 
print("Intercept:", model.intercept_)
for name, coef in zip(X.columns, model.coef_):
    print(name, ":", coef)
 
residuals = y_test - y_test_pred
plt.figure()
plt.scatter(X_test["age"], residuals)
plt.axhline(0, color="k", lw=0.8)
plt.xlabel("Age (days)")
plt.ylabel("Residuals (MPa)")
plt.title("Residuals vs Age")
plt.xscale("log")
plt.savefig("figures/A4_residuals.png", dpi=150)
plt.close()
 
rows = []
for degree in [1, 2, 3, 4]:
    poly = make_pipeline(
        PolynomialFeatures(degree=degree, include_bias=False),
        StandardScaler(),
        LinearRegression()
    )
    poly.fit(X_train, y_train)
    ytr = poly.predict(X_train)
    yte = poly.predict(X_test)
 
    p_poly = poly[0].n_output_features_
    tr_r2 = r2_score(y_train, ytr)
    rows.append({
        "degree": degree,
        "p": p_poly,
        "train_rmse": np.sqrt(mean_squared_error(y_train, ytr)),
        "test_rmse": np.sqrt(mean_squared_error(y_test, yte)),
        "train_r2": tr_r2,
        "train_adj_r2": 1 - (1 - tr_r2) * (n - 1) / (n - p_poly - 1),
        "test_r2": r2_score(y_test, yte),
    })
A5_table = pd.DataFrame(rows).round(3)
print(A5_table)
A5_table.to_csv("results/A5_poly.csv", index=False)
 
y_class = (df["strength"] >= 40).astype(int)
print(y_class.value_counts(normalize=True))
Xc_train, Xc_test, c_train, c_test = train_test_split(
    X, y_class, test_size=0.2, random_state=42, stratify=y_class)
 
Ks = [1, 3, 5, 7, 15, 25, 51, 101]
knn_rows = []
for K in Ks:
    knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K))
    knn.fit(Xc_train, c_train)
    knn_rows.append({"K": K,
                     "train_acc": knn.score(Xc_train, c_train),
                     "test_acc": knn.score(Xc_test, c_test)})
knn_df = pd.DataFrame(knn_rows).round(3)
print(knn_df)
knn_df.to_csv("results/A6_knn.csv", index=False)
 
plt.figure()
plt.plot(knn_df["K"], knn_df["train_acc"], "o-", label="train")
plt.plot(knn_df["K"], knn_df["test_acc"], "s-", label="test")
plt.xscale("log")
plt.xlabel("K")
plt.ylabel("accuracy")
plt.legend()
plt.savefig("figures/A6_knn.png", dpi=150)
plt.close()
 
K_best = 7 
 
knn_s = make_pipeline(StandardScaler(),
                      KNeighborsClassifier(n_neighbors=K_best)).fit(Xc_train, c_train)
knn_raw = KNeighborsClassifier(n_neighbors=K_best).fit(Xc_train, c_train)
print("with scaler:", knn_s.score(Xc_test, c_test),
      " without:", knn_raw.score(Xc_test, c_test))
 
accs = []
for rs in range(5):
    a, b, c, d = train_test_split(X, y_class, test_size=0.2,
                                  random_state=rs, stratify=y_class)
    m = make_pipeline(StandardScaler(),
                      KNeighborsClassifier(n_neighbors=K_best)).fit(a, c)
    accs.append(m.score(b, d))
print("5 splits:", np.round(accs, 3), "mean", np.mean(accs), "std", np.std(accs))
 
depths = [1, 2, 3, 4, 5, 6, 8, None]
tree_rows = []
for dpt in depths:
    t = DecisionTreeClassifier(criterion="entropy", max_depth=dpt,
                               random_state=0).fit(Xc_train, c_train)
    tree_rows.append({"max_depth": str(dpt),
                      "leaves": t.get_n_leaves(),
                      "train_acc": t.score(Xc_train, c_train),
                      "test_acc": t.score(Xc_test, c_test)})
tree_df = pd.DataFrame(tree_rows).round(3)
print(tree_df)
tree_df.to_csv("results/A6_tree.csv", index=False)
 
plt.figure()
xs = range(len(depths))
plt.plot(xs, tree_df["train_acc"], "o-", label="train")
plt.plot(xs, tree_df["test_acc"], "s-", label="test")
plt.xticks(xs, tree_df["max_depth"])
plt.xlabel("max_depth")
plt.ylabel("accuracy")
plt.legend()
plt.savefig("figures/A6_tree.png", dpi=150)
plt.close()
 
depth_best = 4 
tree = DecisionTreeClassifier(criterion="entropy", max_depth=depth_best,
                              random_state=0).fit(Xc_train, c_train)
print(export_text(tree, feature_names=list(X.columns), max_depth=2))
 
def metrics_row(name, y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {"model": name, "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0)}
 
A_metrics = pd.DataFrame([
    metrics_row("KNN", c_test, knn_s.predict(Xc_test)),
    metrics_row("Tree", c_test, tree.predict(Xc_test)),
]).round(3)
print(A_metrics)
A_metrics.to_csv("results/A_metrics.csv", index=False)  # used by B7
 
proba = knn_s.predict_proba(Xc_test)[:, 1]
th_rows = []
for t in [0.3, 0.5, 0.7, 0.9]:
    pred = (proba >= t).astype(int)
    th_rows.append(metrics_row(f"KNN t={t}", c_test, pred))
th_df = pd.DataFrame(th_rows).round(3)
print(th_df)
th_df.to_csv("results/A7_thresholds.csv", index=False)
 
pipe = make_pipeline(StandardScaler(), LinearRegression()).fit(X_train, y_train)
imp = pd.DataFrame({
    "raw_coef": model.coef_,
    "std_coef": pipe[-1].coef_,
    "tree_imp": tree.feature_importances_,
}, index=X.columns)
 
pi_knn = permutation_importance(knn_s, Xc_test, c_test, scoring="f1",
                                n_repeats=20, random_state=0)
pi_tree = permutation_importance(tree, Xc_test, c_test, scoring="f1",
                                 n_repeats=20, random_state=0)
imp["perm_knn"] = pi_knn.importances_mean
imp["perm_tree"] = pi_tree.importances_mean
print(imp.round(3))
imp.round(4).to_csv("results/A8_importance.csv")
 
imp[["std_coef", "tree_imp", "perm_knn"]].plot.bar(figsize=(9, 4))
plt.tight_layout()
plt.savefig("figures/A8_importance.png", dpi=150)
plt.close()
