# scripts/make_synthetic_reliability.py
# Synthetic semiconductor-style reliability dataset with multiple stress levels and censoring.
# Run: python scripts/make_synthetic_reliability.py

import os, math, random
import numpy as np
import pandas as pd

rng = np.random.default_rng(2025)

os.makedirs("data", exist_ok=True)

# -----------------------
# CONFIG (you can tweak)
# -----------------------
N_PER_GROUP = 80          # devices per stress group
BATCHES = ["B1","B2","B3","B4"]
TEST_TYPES = {
    "HTOL": { # High Temp Operating Life (elevated T & V)
        "temps_C":[125, 150],        # stress temperatures
        "voltages_V":[4.5, 5.0],     # stress voltages
        "test_end_hours": 2000,      # censor point if survives
        "beta_shape": 2.2            # wear-out dominated (β>1)
    },
    "THB": {  # Temp Humidity Bias (lower temp, bias + humidity)
        "temps_C":[85],              # lower temp
        "voltages_V":[3.3],          # bias
        "test_end_hours": 1500,
        "beta_shape": 1.6
    },
    "TC": {   # Temperature Cycling (cycles ≈ hours proxy here)
        "temps_C":[-40, 125],        # represent low/high extremes
        "voltages_V":[0.0],          # no bias
        "test_end_hours": 1200,
        "beta_shape": 1.8
    }
}

# Arrhenius‑style acceleration: eta(T) = eta_ref * exp( Ea/k * (1/T - 1/T_ref) )
K_B = 8.617333262145e-5   # eV/K (Boltzmann)
EA_eV = 0.6               # activation energy (typical order 0.3–0.8 eV)
T_REF_K = 398.15          # 125°C reference
ETA_REF = 1200.0          # hours at T_REF for baseline

# Voltage acceleration (simple multiplier): higher V -> lower eta
def voltage_factor(v):
    # 3.3V baseline; scale down lifetime as voltage increases
    return 1.0 / (1.0 + 0.15*(v - 3.3))  # ~15% faster wear per +1V

# Batch random effect (manufacturing variability)
BATCH_EFFECTS = {b: rng.normal(1.0, 0.08) for b in BATCHES}  # ~8% sigma

rows = []
device_counter = 1

for test_type, cfg in TEST_TYPES.items():
    beta = cfg["beta_shape"]
    test_end = cfg["test_end_hours"]
    for T_C in cfg["temps_C"]:
        for V in cfg["voltages_V"]:
            # target Weibull scale (eta) from Arrhenius + voltage + batch
            T_K = T_C + 273.15
            AF = math.exp((EA_eV/K_B) * (1.0/T_K - 1.0/T_REF_K))  # acceleration factor vs reference
            eta_base = ETA_REF * AF * voltage_factor(V)

            for _ in range(N_PER_GROUP):
                batch = rng.choice(BATCHES)
                eta = eta_base * BATCH_EFFECTS[batch] * rng.normal(1.0, 0.06)  # small device-to-device noise

                # Draw failure time from Weibull(β, η). Inverse CDF: t = η * (-ln(1-u))^(1/β)
                u = rng.random()
                t_fail = eta * (-np.log(1.0 - u))**(1.0/beta)

                # Right censoring at test end
                censored = int(t_fail >= test_end)
                observed_time = float(min(t_fail, test_end))

                rows.append({
                    "Device_ID": f"D{device_counter:04d}",
                    "Test_Type": test_type,
                    "Stress_Temperature_C": T_C,
                    "Stress_Voltage_V": V,
                    "Failure_Time_Hours": observed_time,
                    "Censored": censored,                 # 0 = failed during test, 1 = survived to end
                    "Batch_ID": batch
                })
                device_counter += 1

df = pd.DataFrame(rows)
df.to_csv("data/reliability_synthetic.csv", index=False)
print(f"Saved: data/reliability_synthetic.csv  shape={df.shape}")
print(df.head())
