#!/bin/bash
# One-off folder setup:  bash setup_cosmology.sh
#
#   ~/Desktop/Cosmology/
#     data/                                  <- ALL data, one place, one subfolder per source
#       wmap9/wmap_likelihood_v5/            official WMAP9 likelihood (copied from WMAP+DESI)
#       wmap9/libwmap9.so                    your compiled library (copied)
#       cobaya_packages/data/bao_data/       DESI DR1 + DR2 BAO (official, Cobaya installer)
#       cobaya_packages/data/sn_data/        Pantheon+ (official release files)
#     analyses/
#       wmap9_desi_dr2_pantheon_w0wa/        <- this extension only
#         05_wmap9_desi_dr2_pantheon_w0wa.ipynb
#         wmap9_likelihood.py                (Notebook 04 WMAP9 wrapper, as a Cobaya likelihood)
#         chains/  figures/  results/  reference_chains/
#
# Nothing is moved or deleted: existing files are only copied.

ROOT="$HOME/Desktop/Cosmology"
DATA="$ROOT/data"
ANA="$ROOT/analyses/wmap9_desi_dr2_pantheon_w0wa"
OLD="$HOME/Desktop/WMAP+DESI"

mkdir -p "$DATA/wmap9" "$DATA/cobaya_packages"
mkdir -p "$ANA/chains" "$ANA/figures" "$ANA/results" "$ANA/reference_chains"

echo "== WMAP9 likelihood (copy)"
cp -Rn "$OLD/wmap_likelihood_v5" "$DATA/wmap9/"
cp -n  "$OLD/Python files/libwmap9.so" "$DATA/wmap9/"

echo "== DESI DR1, DESI DR2 and Pantheon+ (official, via cobaya-install)"
cobaya-install bao.desi_2024_bao_all bao.desi_dr2.desi_bao_all sn.pantheonplus -p "$DATA/cobaya_packages"

echo "== Reference chains from the WMAP9 + DESI DR1 LCDM analysis (copy)"
for f in wmap9_lcdm_flat_samples_20260614_235110.npy \
         wmap9_desi_joint_corrected_flat_20261024_212301.npy; do
  cp -n "$OLD/Python files/chains/$f" "$ANA/reference_chains/" && echo "  $f"
done

echo "== Notebook and WMAP9 likelihood file (run this script from the folder you downloaded them to)"
for f in 05_wmap9_desi_dr2_pantheon_w0wa.ipynb wmap9_likelihood.py; do
  [ -f "$f" ] && cp -n "$f" "$ANA/" && echo "  $f"
done

cat > "$ROOT/README.txt" <<'EOF'
data/       all datasets, one subfolder per source (shared by every analysis, never edited)
analyses/   one folder per analysis; each keeps its own notebook, chains, figures, results
EOF

echo
echo "Done:"
find "$ROOT" -maxdepth 3 -not -path "*/wmap_likelihood_v5/*" -not -path "*/cobaya_packages/*/*" | sort
