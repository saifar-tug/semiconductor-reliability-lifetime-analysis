import math, numpy as np, pandas as pd

K_B = 8.617333262145e-5  # eV/K

def voltage_factor(v: float) -> float:
    return 1.0 / (1.0 + 0.15 * (v - 3.3))

def synthesize(n_per_group=80, ea_ev=0.6, t_ref_k=398.15, eta_ref=1200.0, seed=2025) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    batches = ["B1","B2","B3","B4"]
    batch_eff = {b: rng.normal(1.0, 0.08) for b in batches}
    tests = {
        "HTOL": {"temps":[125,150], "volts":[4.5,5.0], "end_h":2000, "beta":2.2},
        "THB":  {"temps":[85],      "volts":[3.3],    "end_h":1500, "beta":1.9},
        "TC":   {"temps":[-40,125], "volts":[0.0],    "end_h":1200, "beta":1.8},
    }
    rows, did = [], 1
    for tt,cfg in tests.items():
        beta = cfg["beta"]
        for t_c in cfg["temps"]:
            t_k = t_c + 273.15
            af_t = math.exp((ea_ev / K_B) * (1.0 / t_k - 1.0 / t_ref_k))
            for v in cfg["volts"]:
                eta_base = eta_ref * af_t * voltage_factor(v)
                for _ in range(n_per_group):
                    b = rng.choice(batches)
                    eta = eta_base * batch_eff[b] * rng.normal(1.0, 0.06)
                    u = rng.random()
                    t_fail = eta * (-np.log(1.0 - u)) ** (1.0 / beta)
                    t_end = cfg["end_h"]
                    cens = int(t_fail >= t_end)
                    rows.append({
                        "Device_ID": f"D{did:04d}",
                        "Test_Type": tt,
                        "Stress_Temperature_C": t_c,
                        "Stress_Voltage_V": float(v),
                        "Failure_Time_Hours": float(min(t_fail, t_end)),
                        "Censored": cens,
                        "Batch_ID": b,
                    })
                    did += 1
    return pd.DataFrame(rows)
