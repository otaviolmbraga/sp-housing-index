"""
NON-DESTRUCTIVE verification of the Case-Shiller index estimation.

Reproduces the published index from repeated_sales.pkl and recomputes it under
three variants to quantify whether a methodological change moves the headline
numbers. WRITES NOTHING to the analysis folder -- only prints a comparison.

    C:/Users/otavi/anaconda3/python.exe _build/verify_index_methods.py

Variants:
  (A) PUBLISHED : GLS weight = 1/sigma_hat     + MA12  (current code)
  (B) CS-CORRECT: GLS weight = 1/sigma_hat^2   + MA12  (textbook Case-Shiller)
  (C) RAW       : GLS weight = 1/sigma_hat^2, NO MA12  (pre-smoothing series)
"""
import numpy as np
import pandas as pd

CLEAN = r"C:/Users/otavi/Dropbox/sp_housing/data/clean_data/"

# --- load repeat-sales pairs, same preprocessing as build_csindex_RB.py ------
df = pd.read_pickle(CLEAN + "repeated_sales.pkl")
for c in ("date1", "date2"):
    df[c] = pd.to_datetime(df[c])
df = df[(df["date2"] - df["date1"]).dt.days >= 1095]          # 3-year filter
df["date1"] = df["date1"].dt.to_period("M").dt.to_timestamp()
df["date2"] = df["date2"].dt.to_period("M").dt.to_timestamp()

months = pd.date_range(df["date1"].min(), df["date2"].max(), freq="MS")
m2i = {m: i for i, m in enumerate(months)}
N, T = len(df), len(months)

xxx = np.zeros((N, T))
hhh = np.ones((N, 2))
d1 = df["date1"].values
d2 = df["date2"].values
hp = (df["date2"] - df["date1"]).dt.days.values / 30.44
for i in range(N):
    hhh[i, 1] = hp[i]
    xxx[i, m2i[df["date1"].iloc[i]]] = -1
    xxx[i, m2i[df["date2"].iloc[i]]] = 1

x = xxx[:, 1:]
r = df["log_return"].values.reshape(-1, 1)

# --- stage 1 OLS + stage 2 variance model (shared) --------------------------
beta_ols = np.linalg.inv(x.T @ x) @ (x.T @ r)
resid_sq = (r - x @ beta_ols) ** 2
proj_resid = np.linalg.inv(hhh.T @ hhh) @ (hhh.T @ resid_sq)
var_hat = (hhh @ proj_resid).ravel()                          # sigma_hat^2
n_neg = int((var_hat <= 0).sum())
print(f"N pairs = {N:,} | T months = {T} | fitted variances <= 0: {n_neg}")

# clip non-positive fitted variances so weights stay finite
var_clip = np.where(var_hat > 0, var_hat, np.nan)
var_clip = np.where(np.isnan(var_clip), np.nanmedian(var_clip), var_clip)


def gls(weight_vec):
    w = weight_vec.reshape(-1, 1)
    xw = x * w
    return np.linalg.inv(xw.T @ x) @ (xw.T @ r)


beta_A = gls(1.0 / np.sqrt(var_clip))        # 1/sigma_hat   (published)
beta_B = gls(1.0 / var_clip)                 # 1/sigma_hat^2 (corrected)

lvl_A = np.insert(np.exp(beta_A), 0, 1.0)
lvl_B = np.insert(np.exp(beta_B), 0, 1.0)

ma12 = lambda a: pd.Series(a).rolling(12, min_periods=1).mean().values
A = ma12(lvl_A)   # published
B = ma12(lvl_B)   # corrected + MA12
C = lvl_B         # corrected, raw (no MA12)

out = pd.DataFrame({"date": months, "A_pub": A, "B_corr": B, "C_raw": C})
for col in ("A_pub", "B_corr", "C_raw"):
    base = out.loc[out["date"] == "2010-01-01", col].iloc[0]
    out[col] = out[col] / base
out = out[(out["date"] >= "2010-01-01") & (out["date"] <= "2025-12-01")].reset_index(drop=True)

# --- cross-check A against the published csv --------------------------------
pub = pd.read_csv(CLEAN + "cs_index_final.csv")
pub["date"] = pd.to_datetime(pub["date"])
merged = out.merge(pub[["date", "cs_sp"]], on="date", how="left")
max_dev = (merged["A_pub"] - merged["cs_sp"]).abs().max()
print(f"max |A_pub - published cs_sp| = {max_dev:.6f}  (should be ~0)")

# --- headline comparison ----------------------------------------------------
def at(col, ym):
    return out.loc[out["date"] == ym, col].iloc[0]

print("\nIndex level (Jan-2010 = 1.000)")
print(f"{'date':>9} {'A_pub':>9} {'B_corr':>9} {'C_raw':>9}")
for ym in ("2010-01-01", "2013-01-01", "2015-01-01", "2018-01-01",
           "2020-01-01", "2022-01-01", "2025-12-01"):
    print(f"{ym[:7]:>9} {at('A_pub',ym):>9.4f} {at('B_corr',ym):>9.4f} {at('C_raw',ym):>9.4f}")

end = "2025-12-01"
print("\nCumulative nominal return 2010-01 -> 2025-12")
for col, lab in (("A_pub", "A published (1/s)  +MA12"),
                 ("B_corr", "B corrected (1/s^2)+MA12"),
                 ("C_raw", "C corrected raw    noMA12")):
    print(f"  {lab}: {(at(col,end)-1)*100:+.1f}%")

print("\nDifferences vs published (A):")
for col, lab in (("B_corr", "B 1/s^2 +MA12"), ("C_raw", "C raw")):
    d = (merged if False else out)
    dev = (out[col] - out["A_pub"]).abs()
    print(f"  {lab}: mean |dev| = {dev.mean():.4f}, max |dev| = {dev.max():.4f}, "
          f"end-level dev = {at(col,end)-at('A_pub',end):+.4f}")
