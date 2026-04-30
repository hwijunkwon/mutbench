#!/bin/bash
# Launch a containerised EVE/VAE shell or one-off command.
# Usage:
#   ./tools/eve_container/run.sh                # interactive bash
#   ./tools/eve_container/run.sh python -V      # one-off command
#   ./tools/eve_container/run.sh bash examples/Step1_train_VAE.sh
#
# Mounts (read-write):
#   /proj/paper/tools/EVE   -> /workspace/EVE
#   /proj/paper/data        -> /workspace/data
#   /proj/paper/results     -> /workspace/results
#   /proj/paper/scripts     -> /workspace/scripts
#
# All GPUs are exposed and shared memory is raised to 8 GiB so DataLoader
# worker processes do not crash on /dev/shm exhaustion.

set -euo pipefail

IMAGE_TAG="mutbench-eve:pt2.1.2-cu118"
PROJECT_ROOT="/proj/paper"

if ! docker image inspect "${IMAGE_TAG}" >/dev/null 2>&1; then
    echo "[run.sh] image ${IMAGE_TAG} not found — run tools/eve_container/build.sh first." >&2
    exit 1
fi

# Pass UID/GID through so files written inside the container land owned by
# the host user instead of root. This is the standard --user trick.
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

if [ "$#" -eq 0 ]; then
    set -- bash
fi

# Only request a TTY when stdin actually is one. This lets ./container/run.sh
# work both as an interactive shell (TTY available) and as a one-off command
# from non-interactive scripts like smoke_test.sh (no TTY).
TTY_FLAGS="-i"
if [ -t 0 ] && [ -t 1 ]; then
    TTY_FLAGS="-it"
fi

exec docker run --rm ${TTY_FLAGS} \
    --gpus all \
    --shm-size=8g \
    --user "${HOST_UID}:${HOST_GID}" \
    -e HOME=/tmp \
    -v "${PROJECT_ROOT}/tools/EVE:/workspace/EVE" \
    -v "${PROJECT_ROOT}/data:/workspace/data" \
    -v "${PROJECT_ROOT}/results:/workspace/results" \
    -v "${PROJECT_ROOT}/scripts:/workspace/scripts" \
    -w /workspace/EVE \
    "${IMAGE_TAG}" \
    "$@"
