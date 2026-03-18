#!/bin/bash
# Build script for KNU PhD Thesis
# Usage:
#   ./build.sh          — builds both digital and print versions
#   ./build.sh digital  — digital submission only
#   ./build.sh print    — print version only

set -e
cd "$(dirname "$0")"

build_digital() {
    echo "=== Building DIGITAL submission version ==="
    xelatex -interaction=nonstopmode "\def\printmode{0}\input{thesis_en}"
    bibtex thesis_en 2>/dev/null || true
    xelatex -interaction=nonstopmode "\def\printmode{0}\input{thesis_en}"
    xelatex -interaction=nonstopmode "\def\printmode{0}\input{thesis_en}"
    cp thesis_en.pdf thesis_digital.pdf
    echo ">>> Saved: thesis_digital.pdf"
}

build_print() {
    echo "=== Building PRINT version (with spine page) ==="
    xelatex -interaction=nonstopmode "\def\printmode{1}\input{thesis_en}"
    bibtex thesis_en 2>/dev/null || true
    xelatex -interaction=nonstopmode "\def\printmode{1}\input{thesis_en}"
    xelatex -interaction=nonstopmode "\def\printmode{1}\input{thesis_en}"
    cp thesis_en.pdf thesis_print.pdf
    echo ">>> Saved: thesis_print.pdf"
}

case "${1:-both}" in
    digital) build_digital ;;
    print)   build_print ;;
    both)    build_digital; build_print ;;
    *)       echo "Usage: $0 [digital|print|both]"; exit 1 ;;
esac

echo ""
echo "=== Build complete ==="
ls -lh thesis_digital.pdf thesis_print.pdf 2>/dev/null
