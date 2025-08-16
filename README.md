# Semiconductor Reliability Lifetime Analysis

Modern Semiconductors must operate reliably for years powering everything from cars to smartphones, but testing engineers can’t wait years to validate reliability. Instead, they run **accelerated stress tests** such as:  

- **HTOL** (High-Temperature Operating Life)  
- **THB** (Temperature Humidity Bias)  
- **TC** (Temperature Cycling)  

These tests simulate years of aging in weeks or months. The challenge is to extract **meaningful reliability insights** from limited, noisy, and often censored lifetime data.  

This project demonstrates such an analysis pipeline using **synthetic accelerated life test data**, combining survival statistics, Weibull reliability modeling, and Arrhenius temperature acceleration.  

---

## Workflow Glance 

- Generate realistic **synthetic semiconductor reliability data** with multiple stress conditions (HTOL, THB, TC) and censoring. 
- Apply **Kaplan–Meier survival analysis** (with censoring).  
- Perform **Weibull-2P modeling** per stress condition.  
- Use **Arrhenius acceleration modeling** to relate temperature and lifetime for HTOL.  
- Showcasing-quality visualizations **publication-style plots** and reproducible CSV summaries. 

---

## Dataset Overview  

**File:** `data/reliability_synthetic.csv`  
560 synthetic devices tested under multiple stress conditions.  

| Column | Description |
|--------|-------------|
| `Device_ID` | Unique identifier for each device |
| `Test_Type` | HTOL, THB, or TC |
| `Stress_Temperature_C` | Applied stress temperature (°C) |
| `Stress_Voltage_V` | Operating voltage under stress |
| `Failure_Time_Hours` | Time-to-failure or censoring point (hours) |
| `Censored` | 0 = failure observed, 1 = still alive at test end |
| `Batch_ID` | Manufacturing lot ID (captures lot-to-lot variation) |

**Note:** Censoring is common in real semiconductor tests, not all parts fail within the test window. For further analysis, we could think of more features such as, Measurement_No, Parameter_Value, Test_Date and so on.   

---

## Derived Results 

**Median Survival Times**

File: `results/km_medians_by_group.csv` 
- Median device lifetimes per stress group (Test_Type × Temperature).
- Derived from Kaplan–Meier survival curves.
- Useful for quick comparison across conditions.

**Weibull Fit Parameters**

File: `results/weibull_group_fits.csv` 
- Fitted Weibull-2P parameters for each group.
- β (shape): indicates failure mode (β>1 → wear-out).
- η (scale): characteristic life (hours).
- Includes MTTF (mean time to failure) and hazard interpretation.

**Arrhenius Regression Coefficients (HTOL only)**

File: `results/arrhenius_fit_coeffs_HTOL.csv` 
- Linear regression of ln(η) vs 1/T.
- Provides activation energy for temperature-driven aging.
- Used to extrapolate field lifetimes from high-temperature stress tests.

---

## Key Analyses  

### Kaplan–Meier Survival by Stress Group  
- HTOL @ 150 °C fails fastest (median ≈ 270 h).  
- HTOL @ 125 °C lasts longer (median ≈ 704 h).  
- THB (85 °C) and TC (-40 °C, 125 °C) show little degradation.  

![Kaplan–Meier Survival](results/km_by_group_publication.png)  

This was expected since HTOL at higher temperature quickly accelerates wear-out mechanisms like **electromigration** and **oxide breakdown**, while humidity and thermal cycling take much longer to manifest failures.  

---

### Failure Time Density by Test Type  
- HTOL has a broad failure distribution due to combined **temperature + voltage** acceleration.  
- TC and THB failures cluster tightly, with failures clustered around specific stress points.  

![Failure Density](results/density_by_testtype.png)  

The wider HTOL distribution reflects device-to-device variation in how quickly transistors degrade. In contrast, TC and THB failures are more uniform since they’re driven by physical stress thresholds like **package cracking** or **moisture ingress**.  

---

### Weibull Parameters vs Temperature  
- **β > 1** → wear-out dominated failures.  
- **η decreases with temperature** (HTOL), confirming stress acceleration.  
- TC/THB have higher η (longer lifetimes).  

![Weibull Parameters](results/weibull_group_params_vs_temp.png) 

The rising β with temperature means the devices don’t fail randomly, instead they fail progressively faster as stress accumulates. Lower η at 150 °C confirms **temperature-activated aging** is dominant.  

---

### Weibull Probability Plots (Fit Quality Checks)  
- Empirical points align closely with the Weibull fitted CDF.  
- Confidence intervals are narrow, this is stable estimates.  

![Weibull Probability Plot — HTOL 125 °C @ 4.5 V](results/weibull_probability_plot_HTOL_125C_4.5V.png)  
![Weibull Probability Plot — HTOL 150 °C @ 5.0 V](results/weibull_probability_plot_HTOL_150C_5.0V.png)  

Both HTOL groups fit cleanly to a Weibull distribution. This confirms **wear-out is the dominant mode** and that no unexpected early-life (“infant mortality”) failures are present in this sample dataset.  

---

### Arrhenius Temperature Acceleration (HTOL)  
- Positive slope in ln(η) vs 1/T, shorter lifetimes at higher T supports Arrhenius acceleration.  
- Extracted slope corresponds to realistic **activation energy**.   

![Arrhenius HTOL](results/arrhenius_lneta_vs_invT_HTOL.png)

The slope suggests an activation energy in the range expected for **diffusion-driven degradation mechanisms** (~0.6–0.8 eV). This is in line with published semiconductor reliability models, making our synthetic data look quite realistic.  

---

## Key Outputs
| File | Description |
|------|-------------|
| `data/reliability_synthetic.csv` | Synthetic dataset with Test_Type, Temp, Voltage, Failures, and Censoring |
| `results/km_medians_by_group.csv` | Median survival times by stress group |
| `results/weibull_group_fits.csv` | Weibull fit parameters per group |
| `results/arrhenius_fit_coeffs_HTOL.csv` | Arrhenius regression coefficients for HTOL |
| `notebooks/reliability_analysis.ipynb` | Full analysis workflow |

---

## Repository Structure 

```text
reliability_demo/    # Python package (data, Weibull fits, plotting, CLI)  
notebooks/           # Clean showcase notebook  
data/                # Synthetic dataset  
results/             # Output plots + CSV summaries  
requirements.txt     # Dependencies  
README.md            # Project overview  
``` 
---

### How to Run
```bash
# better to have venv & install deps
python3 -m venv venv
source venv/bin/activate  # for Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run pipeline
python -m reliability_demo.cli --seed 2025

# explore notebook
jupyter notebook notebooks/reliability_pipeline.ipynb
```
---

## Limitations  
- Here Dataset is **synthetic**; real semiconductor data would show mixed failure modes and noisier censoring.  
- Only **temperature acceleration (Arrhenius)** was modeled; real devices require multi-stress models (Eyring).  
- Did not include **degradation parameters** (e.g., leakage, ΔVth).  

## Future Work  
- Extend to **multi-stress acceleration models** (temperature + voltage + humidity).  
- Incorporate **degradation measurements** alongside failure times.  
- Apply **Bayesian or hierarchical models** for lot-to-lot variation.  
- Project **field lifetime estimates** under normal operating conditions.
- Apply *Machine Learning models** training and predict.