"""Registry of all MOI methods."""
from tools.mosd.moi_methods.snf import run_snf
from tools.mosd.moi_methods.spectrum import run_spectrum
from tools.mosd.moi_methods.consensus_clustering import run_consensus_clustering
from tools.mosd.moi_methods.coca import run_coca
from tools.mosd.moi_methods.lracluster import run_lracluster
from tools.mosd.moi_methods.mofa import run_mofa
from tools.mosd.moi_methods.pinsplus import run_pinsplus
from tools.mosd.moi_methods.nemo import run_nemo
from tools.mosd.moi_methods.intnmf import run_intnmf
from tools.mosd.moi_methods.iclusterplus import run_iclusterplus

METHODS = {
    'SNF': run_snf, 'Spectrum': run_spectrum, 'CC': run_consensus_clustering,
    'COCA': run_coca, 'LRAcluster': run_lracluster, 'MOFA': run_mofa,
    'PINSPlus': run_pinsplus, 'NEMO': run_nemo, 'IntNMF': run_intnmf,
    'iClusterPlus': run_iclusterplus,
}
