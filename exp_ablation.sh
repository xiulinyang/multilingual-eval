#!/bin/bash


MODEL_NAME=$1
EVAL_LANG=$2

PPL_TYPES=( 'bpb' )
EVAL_DATA=( 'pud' 'flores')



for ppl_type in "${PPL_TYPES[@]}"; do
  for eval_data in "${EVAL_DATA[@]}"; do

    echo "Running: MODEL_NAME=$MODEL_NAME, EVAL_LANG=$EVAL_LANG, PPL_TYPE=$ppl_type, EVAL_DATA=$eval_data"

    python ppl_minicons_model_specific.py "$MODEL_NAME" "$EVAL_LANG" "$ppl_type" "$eval_data"

    echo "---------------------------------------------"
#          y | rm -rf ~/.cache/huggingface/*
  done
done
