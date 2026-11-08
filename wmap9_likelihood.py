"""
Official WMAP9 9-year likelihood (v5) for Cobaya.

Same ctypes wrapper as Notebook 04, Cell 2. It lives in this file (not in the
notebook) because Cobaya saves a copy of every likelihood next to its chains,
which works for a class imported from a file but not for one defined inside a
notebook.

Author: Cherian Parangot Ittyipe
"""
import os
import ctypes

import numpy as np
from cobaya.likelihood import Likelihood

DATA_DIR = os.path.expanduser('~/Desktop/Cosmology/data')
LIKE_DIR = DATA_DIR + '/wmap9/wmap_likelihood_v5'
SO_PATH  = DATA_DIR + '/wmap9/libwmap9.so'

INIT_SYM    = '__wmap_likelihood_9yr_MOD_wmap_likelihood_init'
COMPUTE_SYM = '__wmap_likelihood_9yr_MOD_wmap_likelihood_compute'

NUM_WMAP   = 8
COMP_NAMES = [
    'TT high-l MASTER', 'TT low-l Gibbs', 'TT low-l det', 'Beam+ptsrc',
    'TE high-l chi2',   'TE high-l det',  'lowl TT/TE/EE/BB chi2', 'lowl TT/TE/EE/BB det',
]

DPA = ctypes.POINTER(ctypes.c_double)
_fn_compute = None


def load_library():
    """Load and initialise libwmap9.so once (exact setup from Notebook 04)."""
    global _fn_compute
    if _fn_compute is not None:
        return
    lib = ctypes.CDLL(SO_PATH)
    fn_init = getattr(lib, INIT_SYM)
    fn_init.restype  = None
    fn_init.argtypes = []
    fn_compute = getattr(lib, COMPUTE_SYM)
    fn_compute.restype  = None
    fn_compute.argtypes = [DPA, DPA, DPA, DPA, DPA]
    orig_dir = os.getcwd()
    os.chdir(LIKE_DIR)
    fn_init()
    os.chdir(orig_dir)
    _fn_compute = fn_compute


def wmap_like(cltt, clte, clee, clbb):
    """
    Official WMAP9 likelihood.
    Inputs : Dl arrays shape (1199,), ell=2..1200, muK^2.
    Returns: (total -2lnL, component vector shape (8,))
    """
    load_library()
    def a(x): return np.ascontiguousarray(x, dtype=np.float64)
    lk = np.zeros(NUM_WMAP, dtype=np.float64)
    _fn_compute(
        a(cltt).ctypes.data_as(DPA), a(clte).ctypes.data_as(DPA),
        a(clee).ctypes.data_as(DPA), a(clbb).ctypes.data_as(DPA),
        lk.ctypes.data_as(DPA)
    )
    return 2.0 * lk.sum(), 2.0 * lk


class WMAP9(Likelihood):
    """Cobaya likelihood: lensed D_ell from Cobaya's CAMB -> wmap_like."""

    def initialize(self):
        load_library()

    def get_requirements(self):
        return {'Cl': {'tt': 1200, 'te': 1200, 'ee': 1200, 'bb': 1200}}

    def logp(self, **params_values):
        cl = self.provider.get_Cl(ell_factor=True, units='muK2')   # D_ell, index = ell
        sl = slice(2, 1201)                                       # ell = 2..1200
        neg2, _ = wmap_like(cl['tt'][sl], cl['te'][sl], cl['ee'][sl], cl['bb'][sl])
        return -0.5 * neg2 if np.isfinite(neg2) else -np.inf
