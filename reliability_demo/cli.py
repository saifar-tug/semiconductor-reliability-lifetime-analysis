import argparse
import os
import pandas as pd

from reliability_demo.data import synthesize
from reliability_demo.weibull import fit_groups
from reliability_demo.plots import (
    km_by_group,
    weibull_probability,
    params_vs_temp,
    arrhenius_lneta_vs_invT,
)

def _ensure_dirs(out_data: str, out_dir: str) -> None:
    os.makedirs(os.path.dirname(out_data) or ".", exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

def run_pipeline(
    seed: int = 2025,
    out_data: str = "data/reliability_synthetic.csv",
    out_dir: str = "results",
    probplot_test: str = "HTOL",
    probplot_temp_c: int = 150,
    probplot_volt_v: float = 5.0,
    make_probplot: bool = True,
):
    """Core pipeline logic: generate data, fit Weibull, make plots."""
    _ensure_dirs(out_data, out_dir)

    df = synthesize(seed=seed)
    df.to_csv(out_data, index=False)

    fits = fit_groups(df)
    fits.to_csv(f"{out_dir}/weibull_group_fits.csv", index=False)

    km_by_group(df, f"{out_dir}/km_by_group_publication.png")

    if make_probplot:
        weibull_probability(
            df,
            probplot_test,
            probplot_temp_c,
            float(probplot_volt_v),
            f"{out_dir}/weibull_probability_plot_{probplot_test}_{probplot_temp_c}C_{probplot_volt_v}V.png",
        )

    params_vs_temp(fits, f"{out_dir}/weibull_group_params_vs_temp.png")
    arrhenius_lneta_vs_invT(
        fits,
        f"{out_dir}/arrhenius_lneta_vs_invT_{probplot_test}.png",
        f"{out_dir}/arrhenius_fit_coeffs_{probplot_test}.csv",
    )
    return df, fits

def main():
    p = argparse.ArgumentParser(description="Semiconductor-style reliability pipeline")
    p.add_argument("--seed", type=int, default=2025)
    p.add_argument("--out-data", default="data/reliability_synthetic.csv")
    p.add_argument("--out-dir", default="results")
    # tiny, useful knobs (optional)
    p.add_argument("--probplot-test", default="HTOL", choices=["HTOL", "THB", "TC"])
    p.add_argument("--probplot-temp-c", type=int, default=150)
    p.add_argument("--probplot-volt-v", type=float, default=5.0)
    p.add_argument("--no-probplot", action="store_true")
    args = p.parse_args()

    run_pipeline(
        seed=args.seed,
        out_data=args.out_data,
        out_dir=args.out_dir,
        probplot_test=args.probplot_test,
        probplot_temp_c=args.probplot_temp_c,
        probplot_volt_v=args.probplot_volt_v,
        make_probplot=not args.no_probfplot if hasattr(args, "no_probfplot") else not args.no_probplot,
    )

def main_notebook(seed=2025, out_data="data/reliability_synthetic.csv", out_dir="results"):
    """
    Notebook entrypoint: returns (df, fits) and writes CSVs/PNGs.
    """
    _ensure_dirs(out_data, out_dir)
    return run_pipeline(seed=seed, out_data=out_data, out_dir=out_dir)

if __name__ == "__main__":
    main()
