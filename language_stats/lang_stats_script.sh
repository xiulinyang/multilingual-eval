#!/bin/bash

MODEL=$1
LANGS=('EN' 'ZH' 'AR' 'RU')
DATA=('pud' 'flores')
for LANG in "${LANGS[@]}"; do
  for DATASET in "${DATA[@]}"; do
    echo "Running: LANG=$LANG, DATASET=$DATASET"
    #python data_stats.py "$LANG" "$DATASET"
    python data_stats_model_specific.py "$MODEL" "$LANG" "$DATASET"
    echo "Finished: $LANG $DATASET"
    echo "---------------------------------------------"
  done
done
