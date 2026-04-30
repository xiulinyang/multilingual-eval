#!/bin/bash


MODEL_NAME=$1
LANGS=('ZH' 'AR' 'RU' 'EN')

PPL_TYPES=( 'cpb' 'sent-nll' 'token-nll' 'ppl')
EVAL_DATA=( 'pud' 'flores')


for EVAL_LANG in "${LANGS[@]}"; do
  for ppl_type in "${PPL_TYPES[@]}"; do
    for eval_data in "${EVAL_DATA[@]}"; do

      echo "Running: MODEL_NAME=$MODEL_NAME, EVAL_LANG=$EVAL_LANG, PPL_TYPE=$ppl_type, EVAL_DATA=$eval_data"

      python ppl_minicons_model_specific.py "$MODEL_NAME" "$EVAL_LANG" "$ppl_type" "$eval_data"

      echo "---------------------------------------------"
  #          y | rm -rf ~/.cache/huggingface/*
    done
  done
done
