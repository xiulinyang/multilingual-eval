#!/bin/bash


LANGS=('ZH' 'FI' 'PL' 'TR' 'RU' 'FR' 'KO' 'AR')
#LANGS=('EN')
#LANGS=('FR' 'KO' 'AR')
VOCABS=(8192 32768 49152 65536 81920)
PPL_TYPES=('ppl' 'token-nll' 'bpb' 'sent-nll' 'cpb' 'mrr')
#PPL_TYPES=('mrr')
EVAL_DATA=('parallel10')
#EVAL_DATA=('en')
TOKENIZER_TYPES=("bpe")
MODEL_SIZE="gpt2_small"
EXPERIMENT="parallel10"

for lang in "${LANGS[@]}"; do
  for vocab_size in "${VOCABS[@]}"; do
    for tokenizer_type in "${TOKENIZER_TYPES[@]}"; do
        for ppl_type in "${PPL_TYPES[@]}"; do
          for eval_data in "${EVAL_DATA[@]}"; do

          echo "Running: LANG=$lang, VOCAB=$vocab_size, TOKENIZER=$tokenizer_type, EVAL_DATA=$eval_data, PPL_TYPE=$ppl_type"

          model_name="${MODEL_SIZE}_${lang}_${tokenizer_type}_${vocab_size}_${EXPERIMENT}_42"

          python ppl_minicons.py "$model_name" "$ppl_type" "$eval_data"

          echo "Finished: $lang $vocab_size $tokenizer_type $eval_data $ppl_type"
          echo "---------------------------------------------"
#          y | rm -rf ~/.cache/huggingface/*
        done
      done
    done
    rm -rf ~/.cache/huggingface/hub/*
  done
done

