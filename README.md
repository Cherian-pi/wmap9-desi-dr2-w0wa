# WMAP9 + DESI DR2 + Pantheon+ : w₀wₐCDM

Constraints on evolving dark energy, w(a) = w₀ + wₐ(1 − a), from the full WMAP9 likelihood combined with DESI DR2 BAO and Pantheon+ supernovae, sampled with Cobaya.

This extends my earlier ΛCDM analysis, [wmap9-desi-joint](https://github.com/Cherian-pi/wmap9-desi-joint) (WMAP9 + DESI DR1), to the w₀wₐ (CPL) model.

## Data and likelihoods

| Probe | Likelihood |
| --- | --- |
| CMB | Official WMAP9 v5 likelihood (TT, TE, EE, BB; ℓ = 2–1200), called through a ctypes wrapper (`wmap9_likelihood.py`) |
| BAO | `bao.desi_dr2.desi_bao_all` (Cobaya, 13 measurements) |
| SNe Ia | `sn.pantheonplus` (Cobaya, 1590 SNe with z > 0.01, M marginalised) |

Theory: CAMB with the PPF dark-energy module, one massive neutrino (Σmν = 0.06 eV), flat geometry.

Priors: w₀ ∈ [−3, 1], wₐ ∈ [−3, 2], H₀ ∈ [50, 90], w₀ + wₐ < 0.

## Results

Metropolis–Hastings MCMC, converged at R − 1 = 0.0096 (means) and 0.063 (95% bounds); 16,640 accepted samples, 30% burn-in removed.

| Parameter | Mean ± 68% |
| --- | --- |
| Ωb h² | 0.02255 ± 0.00043 |
| Ωc h² | 0.1153 ± 0.0024 |
| H₀ [km/s/Mpc] | 67.33 ± 0.70 |
| nₛ | 0.972 ± 0.010 |
| ln(10¹⁰ Aₛ) | 3.096 ± 0.029 |
| τ | 0.087 (+0.012 / −0.014) |
| w₀ | −0.886 ± 0.059 |
| wₐ | −0.25 (+0.28 / −0.24) |
| Ωm | 0.3056 ± 0.0063 |
| r_d [Mpc] | 148.15 ± 0.87 |
| w_p (z_p = 0.247) | −0.936 ± 0.028 |

Best-fit χ²:

| Model | WMAP9 | DESI DR2 | Pantheon+ | Total |
| --- | --- | --- | --- | --- |
| ΛCDM | 7558.09 | 10.56 | 1406.80 | 8975.45 |
| w₀wₐCDM | 7558.23 | 8.69 | 1402.61 | 8969.52 |

Δχ² = 5.93 for two extra parameters, a 1.95σ preference for w₀wₐCDM. ΛCDM lies 2.0σ from the posterior mean in the w₀–wₐ plane.

## Repository layout

```
05_wmap9_desi_dr2_pantheon_w0wa.ipynb   analysis notebook (validation, MAP, MCMC, plots)
wmap9_likelihood.py                     WMAP9 ctypes wrapper + Cobaya likelihood class
setup_cosmology.sh                      folder setup and likelihood installation
chains/                                 Cobaya MCMC chain and minimizer output
figures/                                trace, corner, w0-wa, H0-Ωm figures
results/                                summary tables
```

## Reproducing

1. Build the official WMAP9 v5 likelihood from [LAMBDA](https://lambda.gsfc.nasa.gov/product/wmap/dr5/likelihood_get.html) as a shared library (`libwmap9.so`). The likelihood data and library are not included here.
2. Run `setup_cosmology.sh`. It creates the folders and installs the DESI DR2 and Pantheon+ likelihoods with `cobaya-install`.
3. Edit the paths in Cell 1 of the notebook (default `~/Desktop/Cosmology`) and run it top to bottom. The MCMC resumes from existing chains if present.

Tested with Python 3.11, CAMB 1.5.5, Cobaya 3.5.7, GetDist.

## Author

Cherian Parangot Ittyipe
