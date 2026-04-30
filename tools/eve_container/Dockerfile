# MutBench EVE/VAE container — workaround for the PyTorch 2.5 memory-leak
# regression that crashed train_VAE.py during 100k-step training (see notes
# in container/README.md and the dissertation's "EVE abandoned" memory).
#
# Pinning rationale:
#   - PyTorch 2.1.2  : first stable line that supports RTX 4090 (sm_89) and
#                      pre-dates the 2.5 caching-allocator regression.
#   - CUDA 11.8      : matches PyTorch 2.1.2 official wheels; host driver
#                      535.288.01 (CUDA 12.2 capable) is forward-compatible.
#   - Python 3.10    : bundled with the official PyTorch image; replaces
#                      EVE's original Python 3.7 (EOL'd in conda channels).
#   - cudnn8 runtime : we do not compile CUDA kernels; runtime image keeps
#                      the layer ~1.5 GB smaller than -devel.
#
# All other EVE deps are pinned to versions known to be ABI-compatible with
# this PyTorch line; numpy/pandas/scipy stay at the PyTorch image defaults
# to avoid breaking torch's bundled wheels.

FROM pytorch/pytorch:2.1.2-cuda11.8-cudnn8-runtime

# System packages needed by matplotlib backends, biopython parsing of large
# MSAs, and pip wheel builds for older sklearn versions.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        ca-certificates \
        libgomp1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# EVE-side dependencies. We do NOT repin numpy/pandas/scipy: the base image
# ships compatible versions and overriding them tends to break torch's CUDA
# extension import path.
RUN pip install --no-cache-dir \
        scikit-learn==1.3.2 \
        tqdm==4.66.1 \
        matplotlib==3.7.4 \
        seaborn==0.13.0 \
        biopython==1.83

# Caching-allocator hardening. expandable_segments=True is the official PyTorch
# remedy for the kind of fragmentation that produced EVE's progressive OOM
# under PyTorch 2.5; max_split_size_mb caps the largest free block so a long
# training run cannot starve the allocator of contiguous space.
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,max_split_size_mb:512
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Non-root work dir. The EVE source tree and result/data dirs are bind-mounted
# at run time via container/run.sh; the image itself ships no project data.
WORKDIR /workspace
