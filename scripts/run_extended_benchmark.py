#!/usr/bin/env python3
"""
MutBench extended benchmark infrastructure.

Provides:
  - FASTA loading and per-position feature computation
  - 9 scoring formulas for mutation hotspot detection
  - 15 detector classes (Wavelet, KDE, SlidingWindow, etc.)
  - Evaluation metrics (MCC, F1, enrichment)

Used by run_multilayer_benchmark.py and other 9-pathogen analysis scripts.
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter
from math import log2, sqrt
import warnings

warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_fasta(filepath):
    """Load a FASTA file and return a list of sequences (strings)."""
    sequences = []
    current_seq = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    sequences.append(''.join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line.upper())
    if current_seq:
        sequences.append(''.join(current_seq))
    return sequences


# ---------------------------------------------------------------------------
# Feature computation
# ---------------------------------------------------------------------------

def compute_features(sequences):
    """Compute per-position features from aligned sequences.

    Returns dict with keys:
        P  - mutation frequency (fraction of sequences differing from consensus)
        E  - Shannon entropy
        rare  - rare variant frequency (variants appearing in <5% of sequences)
        minority - minority allele frequency (second most common allele)
    """
    n_seqs = len(sequences)
    seq_len = min(len(s) for s in sequences)

    P = np.zeros(seq_len)
    E = np.zeros(seq_len)
    rare = np.zeros(seq_len)
    minority = np.zeros(seq_len)

    for pos in range(seq_len):
        bases = [s[pos] for s in sequences if pos < len(s)]
        n = len(bases)
        if n == 0:
            continue

        counter = Counter(bases)
        # Remove gap characters from consideration
        for gap_char in ['-', '.', 'N', 'X']:
            counter.pop(gap_char, None)

        if not counter:
            continue

        total = sum(counter.values())
        if total == 0:
            continue

        # Consensus base
        consensus_base = counter.most_common(1)[0][0]
        consensus_count = counter[consensus_base]

        # P: mutation frequency
        P[pos] = 1.0 - consensus_count / total

        # E: Shannon entropy
        entropy = 0.0
        for base, count in counter.items():
            freq = count / total
            if freq > 0:
                entropy -= freq * log2(freq)
        E[pos] = entropy

        # rare: fraction of sequences with rare variants (<5% frequency)
        rare_count = 0
        for base, count in counter.items():
            if base != consensus_base and count / total < 0.05:
                rare_count += count
        rare[pos] = rare_count / total

        # minority: second most common allele frequency
        if len(counter) >= 2:
            sorted_counts = counter.most_common()
            minority[pos] = sorted_counts[1][1] / total
        else:
            minority[pos] = 0.0

    return {'P': P, 'E': E, 'rare': rare, 'minority': minority}


# ---------------------------------------------------------------------------
# Scoring formulas
# ---------------------------------------------------------------------------

def compute_scores(features):
    """Compute 9 scoring formulas from features.

    Returns dict mapping score name -> 1D numpy array.
    """
    P = features['P']
    E = features['E']
    rare_freq = features['rare']
    minority_freq = features['minority']

    scores = {}

    # 1. E*rare
    scores['E*rare'] = E * rare_freq

    # 2. P*E*rare
    scores['P*E*rare'] = P * E * rare_freq

    # 3. minority_E
    scores['minority_E'] = minority_freq * E

    # 4. P*minority_E
    scores['P*minority_E'] = P * minority_freq * E

    # 5. P*E
    scores['P*E'] = P * E

    # 6. H-score: log2(P * E * 100 + 1)
    scores['H-score'] = np.log2(P * E * 100 + 1)

    # 7. E_only
    scores['E_only'] = E.copy()

    # 8. P*E^2
    scores['P*E^2'] = P * E ** 2

    # 9. rank(P*E): rank transform of P*E
    from scipy.stats import rankdata
    pe = P * E
    if np.any(pe > 0):
        ranks = rankdata(pe, method='average')
        # Normalize to [0, 1]
        scores['rank(P*E)'] = ranks / len(ranks)
    else:
        scores['rank(P*E)'] = np.zeros_like(pe)

    return scores


# ---------------------------------------------------------------------------
# Post-processing and evaluation metrics
# ---------------------------------------------------------------------------

def postprocess(detected, max_len):
    """Filter detected positions to valid range [0, max_len)."""
    return sorted(set(int(p) for p in detected if 0 <= p < max_len))


def compute_mcc(detected, gt_set, total_len):
    """Compute Matthews Correlation Coefficient.

    Args:
        detected: list/set of detected positions
        gt_set: set of ground truth positions
        total_len: total number of positions
    """
    detected_set = set(detected)
    tp = len(detected_set & gt_set)
    fp = len(detected_set - gt_set)
    fn = len(gt_set - detected_set)
    tn = total_len - tp - fp - fn

    denom = sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    if denom == 0:
        return 0.0
    return (tp * tn - fp * fn) / denom


def compute_f1(detected, gt_set, total_len):
    """Compute precision, recall, F1 score.

    Returns (precision, recall, f1).
    """
    detected_set = set(detected)
    tp = len(detected_set & gt_set)

    precision = tp / len(detected_set) if detected_set else 0.0
    recall = tp / len(gt_set) if gt_set else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


def compute_enrichment(detected, gt_set, total_len):
    """Compute enrichment ratio: observed overlap / expected by chance."""
    detected_set = set(detected)
    if not detected_set or total_len == 0:
        return 0.0
    observed_ratio = len(detected_set & gt_set) / len(detected_set)
    expected_ratio = len(gt_set) / total_len
    if expected_ratio == 0:
        return float('inf') if observed_ratio > 0 else 0.0
    return observed_ratio / expected_ratio


# ---------------------------------------------------------------------------
# Detector base class
# ---------------------------------------------------------------------------

class BaseDetector:
    """Base class for hotspot detectors."""

    @property
    def name(self):
        raise NotImplementedError

    @property
    def family(self):
        raise NotImplementedError

    def detect(self, scores):
        """Detect hotspot positions from a score array.

        Args:
            scores: 1D numpy array of per-position scores.

        Returns:
            (positions, metadata): list of detected positions and dict of metadata.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Detector implementations
# ---------------------------------------------------------------------------

class WaveletDetector(BaseDetector):
    """Continuous wavelet transform with Mexican hat (Ricker) wavelet."""

    def __init__(self, threshold=1.5):
        self.threshold = threshold

    @property
    def name(self):
        return f"Wavelet(t={self.threshold})"

    @property
    def family(self):
        return "Wavelet"

    @staticmethod
    def _ricker(points, a):
        """Mexican hat (Ricker) wavelet."""
        A = 2 / (sqrt(3 * a) * (np.pi ** 0.25))
        wsq = a ** 2
        x = np.arange(0, points) - (points - 1.0) / 2
        mod = (1 - x ** 2 / wsq)
        gauss = np.exp(-x ** 2 / (2 * wsq))
        return A * mod * gauss

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        widths = np.arange(1, min(31, len(scores) // 2 + 1))
        if len(widths) == 0:
            return [], {}
        # Manual CWT (scipy.signal.cwt/ricker removed in scipy >= 1.12)
        n = len(scores)
        cwt_matrix = np.empty((len(widths), n))
        for i, w in enumerate(widths):
            wavelet = self._ricker(min(10 * w, n), w)
            cwt_matrix[i] = np.convolve(scores, wavelet, mode='same')
        # Take max across scales
        max_coeffs = np.max(np.abs(cwt_matrix), axis=0)
        if np.std(max_coeffs) == 0:
            return [], {}
        z_scores = (max_coeffs - np.mean(max_coeffs)) / np.std(max_coeffs)
        positions = np.where(z_scores > self.threshold)[0].tolist()
        return positions, {'z_scores': z_scores}


class KDEDetector(BaseDetector):
    """Gaussian KDE-based detection with percentile threshold."""

    def __init__(self, threshold_pct=80):
        self.threshold_pct = threshold_pct

    @property
    def name(self):
        return f"KDE(p={self.threshold_pct})"

    @property
    def family(self):
        return "KDE"

    def detect(self, scores):
        from scipy.stats import gaussian_kde
        scores = np.asarray(scores, dtype=float)
        nonzero_idx = np.where(scores > 0)[0]
        if len(nonzero_idx) < 3:
            return [], {}
        try:
            kde = gaussian_kde(nonzero_idx, weights=scores[nonzero_idx])
            x_grid = np.arange(len(scores), dtype=float)
            density = kde(x_grid)
        except (np.linalg.LinAlgError, ValueError):
            return [], {}
        threshold = np.percentile(density[density > 0], self.threshold_pct) if np.any(density > 0) else 0
        positions = np.where(density >= threshold)[0].tolist()
        return positions, {'density': density}


class SlidingWindowTest(BaseDetector):
    """Sliding window z-test comparing local window to global distribution."""

    def __init__(self, window_size=20, p_threshold=0.05):
        self.window_size = window_size
        self.p_threshold = p_threshold

    @property
    def name(self):
        return f"SlidingTest(p={self.p_threshold})"

    @property
    def family(self):
        return "SlidingTest"

    def detect(self, scores):
        from scipy import stats
        scores = np.asarray(scores, dtype=float)
        n = len(scores)
        global_mean = np.mean(scores)
        global_std = np.std(scores)
        if global_std == 0:
            return [], {}

        positions = []
        half_w = self.window_size // 2
        for i in range(n):
            start = max(0, i - half_w)
            end = min(n, i + half_w + 1)
            window = scores[start:end]
            z = (np.mean(window) - global_mean) / (global_std / sqrt(len(window)))
            p_val = 1 - stats.norm.cdf(z)
            if p_val < self.p_threshold:
                positions.append(i)
        return positions, {}


class GradientPeakDetector(BaseDetector):
    """Find peaks in the gradient of smoothed scores."""

    def __init__(self, min_prominence=0.3, smooth_window=5):
        self.min_prominence = min_prominence
        self.smooth_window = smooth_window

    @property
    def name(self):
        return f"GradPeak(p={self.min_prominence})"

    @property
    def family(self):
        return "GradPeak"

    def detect(self, scores):
        from scipy.signal import find_peaks
        from scipy.ndimage import uniform_filter1d
        scores = np.asarray(scores, dtype=float)
        smoothed = uniform_filter1d(scores, size=self.smooth_window)
        peaks, properties = find_peaks(smoothed, prominence=self.min_prominence)
        return peaks.tolist(), {'peaks': peaks, 'properties': properties}


class LocalContrastDetector(BaseDetector):
    """Compare each position to its local neighborhood via z-score."""

    def __init__(self, z_thresh=1.5, window_size=20):
        self.z_thresh = z_thresh
        self.window_size = window_size

    @property
    def name(self):
        return f"LocalContrast(z={self.z_thresh})"

    @property
    def family(self):
        return "LocalContrast"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        n = len(scores)
        half_w = self.window_size // 2
        positions = []
        for i in range(n):
            start = max(0, i - half_w)
            end = min(n, i + half_w + 1)
            local = scores[start:end]
            local_mean = np.mean(local)
            local_std = np.std(local)
            if local_std > 0:
                z = (scores[i] - local_mean) / local_std
                if z > self.z_thresh:
                    positions.append(i)
        return positions, {}


class CUSUMDetector(BaseDetector):
    """CUSUM (Cumulative Sum) change-point detection."""

    def __init__(self, drift=0.5, h_factor=4.0):
        self.drift = drift
        self.h_factor = h_factor

    @property
    def name(self):
        return f"CUSUM(d={self.drift},h={self.h_factor})"

    @property
    def family(self):
        return "CUSUM"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        n = len(scores)
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        if std_score == 0:
            return [], {}

        # Normalize
        normalized = (scores - mean_score) / std_score
        h = self.h_factor

        # Upper CUSUM
        s_pos = np.zeros(n)
        positions = []
        for i in range(1, n):
            s_pos[i] = max(0, s_pos[i - 1] + normalized[i] - self.drift)
            if s_pos[i] > h:
                positions.append(i)
                s_pos[i] = 0  # Reset after alarm

        return positions, {'cusum': s_pos}


class AdaptivePercentileDetector(BaseDetector):
    """Adaptive knee/elbow detection on sorted scores."""

    def __init__(self):
        pass

    @property
    def name(self):
        return "AdaptiveKnee"

    @property
    def family(self):
        return "AdaptiveKnee"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        if np.all(scores == 0):
            return [], {}

        # Sort scores descending
        sorted_scores = np.sort(scores)[::-1]
        n = len(sorted_scores)

        # Find knee point using maximum curvature
        # Normalize x and y to [0, 1]
        x = np.arange(n, dtype=float) / (n - 1) if n > 1 else np.array([0.0])
        y = sorted_scores / (sorted_scores[0] if sorted_scores[0] > 0 else 1.0)

        # Distance from each point to the line from (0, y[0]) to (1, y[-1])
        if n < 3:
            threshold = sorted_scores[0] * 0.5
        else:
            # Line from first to last point
            p1 = np.array([x[0], y[0]])
            p2 = np.array([x[-1], y[-1]])
            line_vec = p2 - p1
            line_len = np.linalg.norm(line_vec)
            if line_len == 0:
                threshold = sorted_scores[0] * 0.5
            else:
                line_unit = line_vec / line_len
                distances = np.abs(np.cross(line_unit, p1 - np.column_stack([x, y])))
                knee_idx = np.argmax(distances)
                threshold = sorted_scores[knee_idx]

        positions = np.where(scores >= threshold)[0].tolist()
        return positions, {'threshold': threshold}


class ScoreDBSCANDetector(BaseDetector):
    """DBSCAN clustering on (position, score) feature space."""

    def __init__(self, eps_pos=10, min_pts=3):
        self.eps_pos = eps_pos
        self.min_pts = min_pts

    @property
    def name(self):
        return f"ScoreDBSCAN(ep={self.eps_pos})"

    @property
    def family(self):
        return "ScoreDBSCAN"

    def detect(self, scores):
        from sklearn.cluster import DBSCAN
        scores = np.asarray(scores, dtype=float)
        nonzero_idx = np.where(scores > 0)[0]
        if len(nonzero_idx) < self.min_pts:
            return [], {}

        # Build feature matrix: (normalized_position, score)
        X = np.column_stack([
            nonzero_idx.astype(float),
            scores[nonzero_idx],
        ])

        # Normalize position dimension to be comparable with score dimension
        pos_range = nonzero_idx[-1] - nonzero_idx[0] if len(nonzero_idx) > 1 else 1
        score_range = np.max(scores[nonzero_idx]) if np.any(scores[nonzero_idx]) else 1
        X[:, 0] = X[:, 0] / max(pos_range, 1) * score_range

        eps = self.eps_pos / max(pos_range, 1) * score_range
        clusterer = DBSCAN(eps=eps, min_samples=self.min_pts)
        labels = clusterer.fit_predict(X)

        positions = nonzero_idx[labels >= 0].tolist()
        return positions, {'labels': labels}


class SpectralFilterDetector(BaseDetector):
    """FFT-based high-pass filtering to find local anomalies."""

    def __init__(self, z_thresh=1.5):
        self.z_thresh = z_thresh

    @property
    def name(self):
        return f"Spectral(z={self.z_thresh})"

    @property
    def family(self):
        return "Spectral"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        n = len(scores)
        if n < 4:
            return [], {}

        # FFT
        fft_vals = np.fft.rfft(scores)

        # Zero out low-frequency components (keep top half)
        cutoff = max(1, len(fft_vals) // 4)
        fft_filtered = fft_vals.copy()
        fft_filtered[:cutoff] = 0

        # Inverse FFT
        residuals = np.fft.irfft(fft_filtered, n=n)
        residuals = np.abs(residuals)

        # Z-score threshold on residuals
        mean_r = np.mean(residuals)
        std_r = np.std(residuals)
        if std_r == 0:
            return [], {}

        z_scores = (residuals - mean_r) / std_r
        positions = np.where(z_scores > self.z_thresh)[0].tolist()
        return positions, {'residuals': residuals}


class BayesianDetector(BaseDetector):
    """Simple Bayesian hotspot detection with prior probability."""

    def __init__(self, prior_hotspot=0.1, threshold=0.5):
        self.prior_hotspot = prior_hotspot
        self.threshold = threshold

    @property
    def name(self):
        return f"Bayes(prior={self.prior_hotspot})"

    @property
    def family(self):
        return "Bayes"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        if np.all(scores == 0):
            return [], {}

        # Simple Bayesian approach:
        # P(hotspot | score) proportional to P(score | hotspot) * P(hotspot)
        # Model P(score | hotspot) as proportional to score value
        # Model P(score | not hotspot) as uniform low
        max_score = np.max(scores)
        if max_score == 0:
            return [], {}

        normalized = scores / max_score

        # Likelihood ratio
        prior_h = self.prior_hotspot
        prior_nh = 1 - prior_h

        # P(score | hotspot) ~ normalized score
        # P(score | not hotspot) ~ small constant
        p_score_h = normalized + 1e-10
        p_score_nh = np.mean(normalized) + 1e-10

        posterior = (p_score_h * prior_h) / (p_score_h * prior_h + p_score_nh * prior_nh)
        positions = np.where(posterior > self.threshold)[0].tolist()
        return positions, {'posterior': posterior}


class EnsembleVoteDetector(BaseDetector):
    """Run multiple simple detectors and use voting."""

    def __init__(self, min_votes=2):
        self.min_votes = min_votes

    @property
    def name(self):
        return f"Ensemble(v>={self.min_votes})"

    @property
    def family(self):
        return "Ensemble"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        n = len(scores)

        # Simple sub-detectors: percentile thresholds at different levels
        vote_counts = np.zeros(n, dtype=int)

        # Sub-detector 1: top 10% by value
        if np.any(scores > 0):
            thresh90 = np.percentile(scores[scores > 0], 90) if np.sum(scores > 0) > 0 else 0
            vote_counts[scores >= thresh90] += 1

        # Sub-detector 2: top 20% by value
        if np.any(scores > 0):
            thresh80 = np.percentile(scores[scores > 0], 80) if np.sum(scores > 0) > 0 else 0
            vote_counts[scores >= thresh80] += 1

        # Sub-detector 3: z-score > 1.5
        mean_s = np.mean(scores)
        std_s = np.std(scores)
        if std_s > 0:
            z = (scores - mean_s) / std_s
            vote_counts[z > 1.5] += 1

        # Sub-detector 4: local contrast (above neighborhood mean by 2x)
        half_w = 10
        for i in range(n):
            start = max(0, i - half_w)
            end = min(n, i + half_w + 1)
            local_mean = np.mean(scores[start:end])
            if local_mean > 0 and scores[i] > 2 * local_mean:
                vote_counts[i] += 1

        positions = np.where(vote_counts >= self.min_votes)[0].tolist()
        return positions, {'vote_counts': vote_counts}


class AdaptiveWindowDetector(BaseDetector):
    """Seed high-scoring positions and expand windows while scores remain high."""

    def __init__(self, seed_pct=90, expand_thresh=0.5):
        self.seed_pct = seed_pct
        self.expand_thresh = expand_thresh

    @property
    def name(self):
        return f"AdaptWin(s={self.seed_pct})"

    @property
    def family(self):
        return "AdaptWin"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        n = len(scores)
        if np.all(scores == 0):
            return [], {}

        nonzero = scores[scores > 0]
        if len(nonzero) == 0:
            return [], {}

        seed_threshold = np.percentile(nonzero, self.seed_pct)
        seeds = np.where(scores >= seed_threshold)[0]

        if len(seeds) == 0:
            return [], {}

        # Expand from seeds
        detected = set(seeds.tolist())
        expand_threshold = seed_threshold * self.expand_thresh

        for seed in seeds:
            # Expand left
            pos = seed - 1
            while pos >= 0 and scores[pos] >= expand_threshold:
                detected.add(pos)
                pos -= 1
            # Expand right
            pos = seed + 1
            while pos < n and scores[pos] >= expand_threshold:
                detected.add(pos)
                pos += 1

        return sorted(detected), {}


class FrequencyThresholdDetector(BaseDetector):
    """Simple percentile-based threshold on scores."""

    def __init__(self, percentile=90):
        self.percentile = percentile

    @property
    def name(self):
        return f"FreqThresh(p={self.percentile})"

    @property
    def family(self):
        return "FreqThresh"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        nonzero = scores[scores > 0]
        if len(nonzero) == 0:
            return [], {}
        threshold = np.percentile(nonzero, self.percentile)
        positions = np.where(scores >= threshold)[0].tolist()
        return positions, {}


class SWANDetector(BaseDetector):
    """Sliding Window ANomaly detection using z-scores within windows."""

    def __init__(self, window_size=20, k=1.5):
        self.window_size = window_size
        self.k = k

    @property
    def name(self):
        return f"SWAN(w={self.window_size},k={self.k})"

    @property
    def family(self):
        return "SWAN"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        n = len(scores)
        if n < self.window_size:
            return [], {}

        global_mean = np.mean(scores)
        global_std = np.std(scores)
        if global_std == 0:
            return [], {}

        positions = set()
        half_w = self.window_size // 2

        for i in range(n):
            start = max(0, i - half_w)
            end = min(n, i + half_w + 1)
            window = scores[start:end]
            window_mean = np.mean(window)

            # Anomaly: window mean significantly above global mean
            z = (window_mean - global_mean) / (global_std / sqrt(len(window)))
            if z > self.k:
                # Mark positions in this window that are above global mean
                for j in range(start, end):
                    if scores[j] > global_mean:
                        positions.add(j)

        return sorted(positions), {}


class MutClustOriginalDetector(BaseDetector):
    """MutClust density-based clustering detector.

    Uses the MutClust algorithm from tools.mutclust.mutclust_algo.core
    or the inline implementation from tools.mutbench.variants.registry.
    """

    def __init__(self, gamma=10, d=3, minpts=5):
        self.gamma = gamma
        self.d = d
        self.minpts = minpts

    @property
    def name(self):
        return f"MutClust-Orig(g={self.gamma})"

    @property
    def family(self):
        return "MutClust-Orig"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        try:
            from tools.mutbench.variants.registry import mutclust
        except ImportError:
            try:
                from tools.mutclust.mutclust_algo.core import mutclust
            except ImportError:
                return [], {}

        clusters = mutclust(scores, gamma=self.gamma, d=self.d, minpts=self.minpts)
        positions = []
        for c in clusters:
            if hasattr(c, 'positions'):
                positions.extend(c.positions)
            elif isinstance(c, dict) and 'positions' in c:
                positions.extend(c['positions'])
        return sorted(set(positions)), {'n_clusters': len(clusters)}


# ---------------------------------------------------------------------------
# Main benchmark runner (standalone)
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent.parent / 'data'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'

PATHOGENS = {
    'SARS-CoV-2': DATA_DIR / 'ncbi_temporal' / 'spike_2020_H1.fasta',
    'H3N2': DATA_DIR / 'influenza' / 'h3n2_ha_sequences.fasta',
    'Norovirus': DATA_DIR / 'norovirus' / 'norovirus_vp1_sequences.fasta',
    'HIV-1': DATA_DIR / 'cross_pathogen' / 'hiv1_gp120_sequences.fasta',
    'Dengue': DATA_DIR / 'dengue' / 'dengue_e_sequences.fasta',
    'RSV': DATA_DIR / 'rsv' / 'rsv_f_sequences.fasta',
    'Influenza_B': DATA_DIR / 'influenza' / 'influenza_b_ha_sequences.fasta',
    'MERS': DATA_DIR / 'mers' / 'mers_spike_sequences.fasta',
    'HCV': DATA_DIR / 'hcv' / 'hcv_e2_sequences.fasta',
}

# Ground truth positions per pathogen (known functional/antigenic sites)
GROUND_TRUTH = {
    'SARS-CoV-2': set(range(319, 542)) | set(range(14, 21)) | set(range(140, 159)) |
                  set(range(245, 265)) | set(range(681, 686)) | set(range(816, 834)),
    'H3N2': set(range(120, 180)) | set(range(190, 210)) | {128, 131, 135, 137, 138,
             140, 142, 144, 145, 155, 156, 158, 159, 160, 163, 189, 193, 196, 197, 198},
    'Norovirus': set(range(280, 420)) | {294, 296, 297, 298, 310, 340, 368, 372, 373,
                  376, 394, 395, 407},
    'HIV-1': set(range(124, 200)) | set(range(275, 290)) | set(range(362, 374)) |
             set(range(425, 440)) | set(range(460, 470)),
    'Dengue': set(range(50, 130)) | set(range(150, 200)) | set(range(290, 320)) |
              set(range(380, 420)),
    'RSV': set(range(62, 76)) | set(range(196, 213)) | set(range(250, 280)) |
           {173, 209, 262, 272, 276},
    'Influenza_B': set(range(120, 180)) | set(range(190, 210)) | {140, 150, 160, 197},
    'MERS': set(range(367, 607)) | set(range(484, 567)),
    'HCV': set(range(384, 447)) | set(range(452, 494)) | set(range(496, 570)),
}


def get_detectors():
    """Return all detector instances for the benchmark."""
    return [
        WaveletDetector(threshold=1.0),
        WaveletDetector(threshold=1.5),
        WaveletDetector(threshold=2.0),
        KDEDetector(threshold_pct=75),
        KDEDetector(threshold_pct=80),
        KDEDetector(threshold_pct=85),
        SlidingWindowTest(p_threshold=0.01),
        SlidingWindowTest(p_threshold=0.05),
        GradientPeakDetector(min_prominence=0.2),
        GradientPeakDetector(min_prominence=0.5),
        LocalContrastDetector(z_thresh=1.0),
        LocalContrastDetector(z_thresh=1.5),
        LocalContrastDetector(z_thresh=2.0),
        CUSUMDetector(drift=0.3, h_factor=3.0),
        CUSUMDetector(drift=0.5, h_factor=4.0),
        CUSUMDetector(drift=0.5, h_factor=5.0),
        AdaptivePercentileDetector(),
        ScoreDBSCANDetector(eps_pos=8, min_pts=3),
        ScoreDBSCANDetector(eps_pos=15, min_pts=3),
        SpectralFilterDetector(z_thresh=1.5),
        SpectralFilterDetector(z_thresh=2.0),
        BayesianDetector(prior_hotspot=0.1, threshold=0.5),
        BayesianDetector(prior_hotspot=0.15, threshold=0.4),
        EnsembleVoteDetector(min_votes=2),
        EnsembleVoteDetector(min_votes=3),
        AdaptiveWindowDetector(seed_pct=90, expand_thresh=0.5),
        AdaptiveWindowDetector(seed_pct=85, expand_thresh=0.4),
        FrequencyThresholdDetector(percentile=80),
        FrequencyThresholdDetector(percentile=85),
        FrequencyThresholdDetector(percentile=90),
        FrequencyThresholdDetector(percentile=95),
        SWANDetector(window_size=10, k=1.0),
        SWANDetector(window_size=10, k=1.5),
        SWANDetector(window_size=10, k=2.0),
        SWANDetector(window_size=20, k=1.0),
        SWANDetector(window_size=20, k=1.5),
        SWANDetector(window_size=20, k=2.0),
        SWANDetector(window_size=50, k=1.0),
        SWANDetector(window_size=50, k=1.5),
        SWANDetector(window_size=50, k=2.0),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


def main():
    """Run the full 9-pathogen extended benchmark."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    score_names = [
        'E*rare', 'P*E*rare', 'minority_E', 'P*minority_E',
        'P*E', 'H-score', 'E_only', 'P*E^2', 'rank(P*E)',
    ]

    detectors = get_detectors()
    all_results = []

    for pathogen, fasta_path in PATHOGENS.items():
        print(f"\n{'=' * 60}")
        print(f"Processing {pathogen}...")

        if not fasta_path.exists():
            print(f"  [SKIP] {fasta_path} not found")
            continue

        gt_set = GROUND_TRUTH.get(pathogen, set())
        if not gt_set:
            print(f"  [SKIP] No ground truth for {pathogen}")
            continue

        # Load sequences
        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]
        unique_count = len(set(sequences))
        print(f"  Sequences: {len(sequences)} (unique: {unique_count}), Length: {min_len}")

        # Compute features and scores
        features = compute_features(sequences)
        all_scores = compute_scores(features)

        # Evaluate all score x detector combos
        for score_name in score_names:
            scores = all_scores[score_name]
            if np.all(scores == 0):
                continue

            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, min_len)
                    detected_set = set(detected)
                except Exception:
                    continue

                if len(detected) == 0:
                    continue

                mcc = compute_mcc(detected, gt_set, min_len)
                prec, rec, f1 = compute_f1(detected, gt_set, min_len)
                enrichment = compute_enrichment(detected, gt_set, min_len)

                all_results.append({
                    'pathogen': pathogen,
                    'score': score_name,
                    'detector': det.name,
                    'family': det.family,
                    'mcc': mcc,
                    'f1': f1,
                    'precision': prec,
                    'recall': rec,
                    'enrichment': enrichment,
                    'n_detected': len(detected),
                })

    df = pd.DataFrame(all_results)
    output_path = RESULTS_DIR / 'extended_9pathogen_results.csv'
    df.to_csv(output_path, index=False)
    print(f"\n{'=' * 60}")
    print(f"Saved {len(df)} evaluations to {output_path}")

    # Summary: best combo per pathogen
    if len(df) > 0:
        print(f"\nBest combo per pathogen (by MCC):")
        for pathogen in df['pathogen'].unique():
            pdf = df[df['pathogen'] == pathogen]
            best_idx = pdf['mcc'].idxmax()
            best = pdf.loc[best_idx]
            print(f"  {pathogen}: {best['score']} + {best['detector']} "
                  f"(MCC={best['mcc']:.4f}, F1={best['f1']:.4f})")


if __name__ == '__main__':
    main()
