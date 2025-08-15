## 📊 Project Overview
This project demonstrates **semiconductor-style reliability data analysis** using a synthetic accelerated life test dataset.  
The workflow includes:
- Generating realistic reliability data with multiple stress conditions (HTOL, THB, TC) and censoring.
- **Kaplan–Meier survival analysis** with right-censoring.
- **Weibull-2P modeling** per stress condition.
- **Arrhenius temperature acceleration analysis** for HTOL.
- Publication-quality visualizations and CSV outputs.

---

## 🔍 Kaplan–Meier Survival by Stress Group
**Purpose:** Visualize survival probability over time and compare stress conditions.  
**Key insight:** Higher temperature HTOL tests fail faster; low-stress TC and THB conditions show minimal degradation.

![Kaplan–Meier Survival](results/km_by_group_publication.png)

---

## 📈 Weibull Parameters vs Temperature
**Purpose:** Show how **shape (β)** and **scale (η)** parameters vary with stress level.  
**Key insight:** β > 1 for all groups → wear-out dominated failures; η decreases with increasing temperature/voltage for HTOL.

![Weibull β and η vs Temperature](results/weibull_group_params_vs_temp.png)

---

## 📊 Weibull Probability Plot (Example: HTOL 150 °C @ 5 V)
**Purpose:** Assess fit quality for a specific stress condition.  
**Key insight:** Fitted Weibull CDF aligns closely with empirical failure data; CI region is narrow, indicating high confidence.

![Weibull Probability Plot — HTOL 150C @ 5V](results/weibull_probability_plot_HTOL_150C_5V.png)

---

## 🌡 Arrhenius Temperature Acceleration (HTOL)
**Purpose:** Quantify acceleration of failures with temperature.  
**Key insight:** Positive slope in ln(η) vs 1/T indicates shorter lifetimes at higher temperatures; slope magnitude corresponds to a realistic activation energy for electronic degradation.

![Arrhenius HTOL](results/arrhenius_lneta_vs_invT_HTOL.png)

---

## 📂 Key Outputs
| File | Description |
|------|-------------|
| `data/reliability_synthetic.csv` | Synthetic dataset with Test_Type, Temp, Voltage, Failures, and Censoring |
| `results/km_medians_by_group.csv` | Median survival times by stress group |
| `results/weibull_group_fits.csv` | Weibull fit parameters per group |
| `results/arrhenius_fit_coeffs_HTOL.csv` | Arrhenius regression coefficients for HTOL |
| `notebooks/reliability_analysis.ipynb` | Full analysis workflow |

---

### 🛠️ How to Run
```bash
# Clone repo
git clone https://github.com/saifar-tug/semiconductor-reliability-lifetime-analysis.git
cd semiconductor-reliability-lifetime-analysis

# Create venv & install deps
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Launch notebook
jupyter notebook notebooks/reliability_analysis.ipynb
