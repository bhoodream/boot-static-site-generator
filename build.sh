#!/bin/bash
BASEPATH=${1:-"/boot-static-site-generator/"}
DEST_DIR=${2:-"./docs"}
python3 src/main.py "$BASEPATH" "$DEST_DIR"
