#!/bin/bash

LANGS=('EN' 'ZH' 'AR')
DATA=('parallel3' 'pud' 'flores')
for LANG in "${LANGS[@]}"; do
  for DATASET in "${DATA[@]}"; do
    echo "Running: LANG=$LANG, DATASET=$DATASET"
    #python data_stats.py "$LANG" "$DATASET"
    python ctc.py "$LANG" "$DATASET"
    echo "Finished: $LANG $DATASET"
    echo "---------------------------------------------"
  done
done
