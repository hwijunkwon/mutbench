# EVE/VAE containerised workaround

**Why this exists.** The dissertation memory `stage3_progress.md` records that
`tools/EVE/train_VAE.py` produced a progressive memory leak under PyTorch 2.5,
crashing every full 100k-step run after only `E2_HCV` and `E_DENV` had
completed. Multiple in-environment fixes (smaller batch sizes, MSA
subsampling, header rewrites) all failed; the project's standing rule was
"do not attempt EVE again in this environment." This directory is the
container-level workaround for codex full-rigor experiment slate item 10
(VAE/EVE/PLM site-effect layer).

**Pinning strategy.**

| Component | Original (2020) | This container |
|-----------|-----------------|----------------|
| Python    | 3.7             | 3.10 (PyTorch image default) |
| PyTorch   | 1.7             | **2.1.2** |
| CUDA      | 11.0            | **11.8** |
| cuDNN     | 8 (implicit)    | 8 |
| GPU arch  | up to sm_80     | sm_89 supported (RTX 4090) |

PyTorch 2.0 was the first release with official RTX 4090 (sm_89) kernels, so
we cannot stay on the original 1.7 line. PyTorch 2.5 (Oct 2024) is the
release that introduced the caching-allocator regression that broke EVE on
this host, so we deliberately step **back** to the last "research-stable"
2.1.x line. CUDA 11.8 matches PyTorch 2.1.2's official wheels; the host
driver (535.288.01, CUDA 12.2 capable) is forward-compatible.

**Allocator hardening.** The Dockerfile sets:

```
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,max_split_size_mb:512
```

`expandable_segments` is PyTorch's official remedy for the fragmentation
pattern that EVE's long training loops produced; `max_split_size_mb=512`
caps the largest free block so a multi-hour run cannot starve the allocator
of contiguous space. Both are runtime-only, no recompilation needed.

## Files

- `Dockerfile`    — image recipe, ~5 GB final.
- `build.sh`      — `docker build` wrapper, tags as `mutbench-eve:pt2.1.2-cu118`.
- `run.sh`        — `docker run` wrapper with `--gpus all`, `--shm-size=8g`,
                    UID-mapped writes, and `/proj/paper/{tools,data,results,scripts}`
                    bind-mounts.
- `smoke_test.sh` — three-step verification: torch+GPU visibility, EVE module
                    import, 10-step VAE forward/backward on dummy data.

## Quick start

```bash
cd /proj/paper

# 1. Build (10–20 min on first run, mostly base-image download).
./tools/eve_container/build.sh

# 2. Verify the image works end-to-end.
./tools/eve_container/smoke_test.sh

# 3. Open an interactive shell for real training.
./tools/eve_container/run.sh
# inside the container:
#   cd /workspace/EVE
#   bash examples/Step1_train_VAE.sh   # adapt for MutBench MSAs
```

The `tools/eve_container/` directory deliberately lives **outside** the
upstream `tools/EVE/` source tree (which is itself a separate git checkout)
so the MutBench parent repo can track these scripts without colliding with
the EVE upstream's own version control boundary.

## Known fallbacks

If `smoke_test.sh` fails at step 1 (`expected sm_89` assertion), the host
driver is too old; the image cannot help — re-image the host driver to a
535.x or newer release. If step 2 fails (`from EVE import VAE_model`), the
EVE source tree was not bind-mounted; check `run.sh` mount paths. If step 3
fails with `CUDA out of memory` on this 24 GB RTX 4090, drop the encoder/
decoder hidden layer sizes in `EVE/default_model_params.json` before
retrying — the smoke test is not the leak's natural trigger and any OOM at
this stage indicates a configuration error, not the original regression.

If the leak resurfaces during real 100k-step training, the next mitigation
is patching `EVE/VAE_model.py` to call `torch.cuda.empty_cache()` and
`gc.collect()` on every checkpoint boundary instead of the current
conditional schedule (line 244). That patch is intentionally **not**
applied here so the upstream code stays vanilla until the workaround is
proven necessary by data.

## What this is not

This container does not yet run the actual MutBench EVE training; it is
infrastructure. Codex experiment slate item 10 lists HCV E2, Dengue E,
SARS-CoV-2 Spike RBD/S1, HIV-1 Env/gp120, H3N2 HA1, RSV F, and (post-
curation) WNV/JEV E as the target proteins. Real training jobs should be
launched from `run.sh` once `smoke_test.sh` passes.
