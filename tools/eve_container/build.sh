#!/bin/bash
# Build the MutBench EVE/VAE container image.
# Usage: ./tools/eve_container/build.sh [--no-cache]
#
# The image is tagged mutbench-eve:pt2.1.2-cu118 so successive rebuilds and
# rollbacks are addressable by tag. The Dockerfile uses no COPY, so the build
# context is just the (small) directory holding this script.

set -euo pipefail

cd "$(dirname "$0")"

IMAGE_TAG="mutbench-eve:pt2.1.2-cu118"

echo "=== Building ${IMAGE_TAG} ==="
docker build "$@" \
    -f Dockerfile \
    -t "${IMAGE_TAG}" \
    .

echo
echo ">>> Build complete: ${IMAGE_TAG}"
docker images "${IMAGE_TAG}"
