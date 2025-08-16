import numpy as np, matplotlib.pyplot as plt, pandas as pd
from lifelines import KaplanMeierFitter
from reliability.Fitters import Fit_Weibull_2P

def km_by_group(df: pd.DataFrame, out: str):
    palette = {"HTOL":"#d62728","THB":"#1f77b4","TC":"#2ca02c"}
    linestyles = {-40:(0,(1,1)),85:"--",125:"-",150:":"}
    km = KaplanMeierFitter()
    plt.figure(figsize=(9,6), dpi=150)
    for (tt,T), g in df.groupby(["Test_Type","Stress_Temperature_C"]):
        km.fit(durations=g["Failure_Time_Hours"], event_observed=1-g["Censored"], label=f"{tt}-{T}°C")
        km.plot(ci_show=False, color=palette.get(tt,"black"), ls=linestyles.get(T,"-"), lw=2)
    plt.title("Kaplan–Meier Survival by Test Type & Temperature")
    plt.xlabel("Hours"); plt.ylabel("Survival S(t)"); plt.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(out, dpi=300); plt.close()

def weibull_probability(df: pd.DataFrame, tt="HTOL", temp=150, volt=5.0, out=""):
    sel = df.query("Test_Type==@tt & Stress_Temperature_C==@temp & Stress_Voltage_V==@volt")
    fail = sel.loc[sel["Censored"]==0,"Failure_Time_Hours"].values
    cen  = sel.loc[sel["Censored"]==1,"Failure_Time_Hours"].values
    fit = Fit_Weibull_2P(failures=fail, right_censored=cen if len(cen) else None,
                         show_probability_plot=True, print_results=False)
    plt.suptitle(f"Weibull Probability Plot — {tt} {temp}°C @ {volt}V", y=1.02)
    plt.tight_layout(); plt.savefig(out, dpi=300, bbox_inches="tight"); plt.close()

def params_vs_temp(fits: pd.DataFrame, out: str):
    colors = {"HTOL":"#d62728","THB":"#1f77b4","TC":"#2ca02c"}
    markers = {0.0:"s",3.3:"^",4.5:"o",5.0:"D"}
    fig, ax = plt.subplots(1,2, figsize=(10,4), dpi=150)
    for tt, g in fits.groupby("Test_Type"):
        for v, gg in g.groupby("Volt_V"):
            ax[0].plot(gg["Temp_C"], gg["beta_shape"], marker=markers.get(v,"o"),
                       color=colors.get(tt,"black"), lw=1.5, label=f"{tt}@{v}V")
            ax[1].plot(gg["Temp_C"], gg["eta_scale_hours"], marker=markers.get(v,"o"),
                       color=colors.get(tt,"black"), lw=1.5, label=f"{tt}@{v}V")
    ax[0].set_title("Weibull β (shape) vs Temperature"); ax[0].set_xlabel("°C"); ax[0].set_ylabel("β"); ax[0].grid(alpha=0.3)
    ax[1].set_title("Weibull η (scale) vs Temperature"); ax[1].set_xlabel("°C"); ax[1].set_ylabel("η (hours)"); ax[1].grid(alpha=0.3)
    h,l = ax[1].get_legend_handles_labels(); uniq = dict(zip(l,h))
    fig.legend(uniq.values(), uniq.keys(), loc="lower center", ncol=4, frameon=True)
    plt.tight_layout(rect=(0,0.12,1,1)); plt.savefig(out, dpi=300); plt.close()

def arrhenius_lneta_vs_invT(fits: pd.DataFrame, out_png: str, out_csv: str):
    htol = fits[fits["Test_Type"]=="HTOL"].copy()
    htol["Temp_K"] = htol["Temp_C"] + 273.15
    x = 1.0 / htol["Temp_K"].values
    y = np.log(htol["eta_scale_hours"].values)
    A = np.vstack([np.ones_like(x), x]).T
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]
    xg = np.linspace(x.min()*0.98, x.max()*1.02, 100)
    yg = a + b*xg
    plt.figure(figsize=(6,4), dpi=150)
    plt.scatter(x, y, label="HTOL groups", color="#d62728")
    plt.plot(xg, yg, color="black", lw=1.5, label=f"fit: ln(η)={a:.2f}+{b:.2e}·(1/T)")
    plt.xlabel("1 / Temperature (1/K)"); plt.ylabel("ln(η)")
    plt.title("Arrhenius Check — HTOL"); plt.grid(alpha=0.3); plt.legend()
    plt.tight_layout(); plt.savefig(out_png, dpi=300); plt.close()
    pd.DataFrame([{"intercept_a":a, "slope_b":b}]).to_csv(out_csv, index=False)
