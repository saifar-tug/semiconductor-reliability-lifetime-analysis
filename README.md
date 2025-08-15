## 📊 Project Overview
This project demonstrates **semiconductor-style reliability data analysis** using:
- Synthetic accelerated life test data
- **Kaplan–Meier survival analysis** with right-censoring
- **Weibull-2P model fitting** for each stress condition
- Parameter trends vs temperature and voltage
- Median survival time estimation

---

## 🔍 Kaplan–Meier Survival by Stress Group
![Kaplan–Meier Survival](results/km_by_group_publication.png)

---

## 📈 Weibull Parameters vs Temperature
![Weibull β and η vs Temperature](results/weibull_group_params_vs_temp.png)

---

## 📂 Key Outputs
| File | Description |
|------|-------------|
| `data/reliability_synthetic.csv` | Synthetic dataset with Test_Type, Temp, Voltage, Failures, and Censoring |
| `results/km_medians_by_group.csv` | Median survival times by stress group |
| `results/weibull_group_fits.csv` | Weibull fit parameters per group |
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
