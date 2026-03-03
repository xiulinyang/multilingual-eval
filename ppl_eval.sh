#!/bin/bash
set -e

LANGS=$1
VOCABS=(8192 32768 49152 65536 81920)
PPL_TYPES=('ppl' 'token-nll' 'bpb' 'sent-nll' 'cpb')
EVAL_DATA=('de' 'de-ar' 'de-arp' 'de-p')
TOKENIZER_TYPES=("bpe" "unigram" "superbpe")
MODEL_SIZE="gpt2_small"
EXPERIMENT="parallel10"

for vocab_size in "${VOCABS[@]}"; do
  for tokenizer_type in "${TOKENIZER_TYPES[@]}"; do
      for ppl_type in "${PPL_TYPES[@]}"; do
        for eval_data in "${EVAL_DATA[@]}"; do

        echo "Running: LANG=$LANGS, VOCAB=$vocab_size, TOKENIZER=$tokenizer_type, EVAL_DATA=$eval_data, PPL_TYPE=$ppl_type"

        model_name="${MODEL_SIZE}_${LANGS}_${tokenizer_type}_${vocab_size}_${EXPERIMENT}_42"

        python ppl_minicons.py "$model_name" "$ppl_type" "$eval_data"

        echo "Finished: $LANGS $vocab_size $tokenizer_type $eval_data $ppl_type"
        echo "---------------------------------------------"

      done
      en_model_name="${MODEL_SIZE}_EN_${tokenizer_type}_${vocab_size}_${EXPERIMENT}_42"
      python ppl_minicons.py "$en_model_name" "$ppl_type" 'en'
    done

  done
done

