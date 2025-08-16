import numpy as np, pandas as pd
from scipy.special import gamma
from reliability.Fitters import Fit_Weibull_2P

def fit_groups(df: pd.DataFrame, min_fails: int = 5) -> pd.DataFrame:
    rows, skipped = [], []
    for (tt, T, V), g in df.groupby(["Test_Type","Stress_Temperature_C","Stress_Voltage_V"]):
        failures = g.loc[g["Censored"]==0,"Failure_Time_Hours"].values
        censored = g.loc[g["Censored"]==1,"Failure_Time_Hours"].values
        if len(failures) < min_fails:
            skipped.append((tt,T,V))
            continue
        fit = Fit_Weibull_2P(failures=failures, right_censored=censored if len(censored) else None,
                             show_probability_plot=False, print_results=False)
        res = fit.results.set_index("Parameter")  # version returns Alpha, Beta
        eta  = float(res.loc["Alpha","Point Estimate"])
        beta = float(res.loc["Beta","Point Estimate"])
        mttf = eta * gamma(1.0 + 1.0/beta)
        hz = "Decreasing" if beta < 0.9 else ("~Constant" if beta <= 1.1 else "Increasing")
        rows.append({
            "Test_Type": tt, "Temp_C": int(T), "Volt_V": float(V),
            "n_total": int(len(g)), "n_fail": int(len(failures)), "n_censored": int(len(censored)),
            "beta_shape": beta, "eta_scale_hours": eta, "MTTF_hours": mttf,
            "hazard_interpretation": f"{hz} hazard"
        })
    return pd.DataFrame(rows).sort_values(["Test_Type","Temp_C","Volt_V"]).reset_index(drop=True)
