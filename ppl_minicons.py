import math
import sys
from minicons import scorer
sys.path.append("..")
from pathlib import Path
from transformers import GPT2LMHeadModel,AutoTokenizer
from tqdm import tqdm
import pandas as pd
import argparse
import os


CHECKPOINTS = [10]
HF_REPO = 'parallelm'
DATA_DIR = 'data/'


parser = argparse.ArgumentParser()
parser.add_argument('model_name', type=str, help="model names")
parser.add_argument('ppl_type', help='Type of perplexity')
parser.add_argument('eval_data', help='Evaluation data')
# Get args
args = parser.parse_args()
model_name = args.model_name
ppl_type = args.ppl_type
la = model_name.split('_')[2]
# Get path to model
model_path = f"{HF_REPO}/{model_name}"
tokenizer = AutoTokenizer.from_pretrained(f'{model_path}', use_fast=True)
eval_data = args.eval_data

if eval_data =='en':
    test_file='wmt19-ende-original.en'
elif eval_data=='de':
    test_file='wmt19-ende-original.de'
elif eval_data=='de-ar':
    test_file ='wmt19-ende-ar.de'
elif eval_data=='de-arp':
    test_file ='wmt19-ende-arp.de'
elif eval_data =='de-p':
    test_file = 'wmt19-ende-p.de'
else:
    raise ValueError(f"Unsupported eval_data: {eval_data}")

test_texts = Path(test_file).read_text().strip().split('\n')
BATCH_SIZE = 8

ppl_df = pd.DataFrame({
    "Sentences": test_texts,
    # "Original": file_text_sequences, # to debug
})

device = "cuda"
for j, ckpt in enumerate(CHECKPOINTS):
    print(f"Epoch:{ckpt}")
    ilm_model = scorer.IncrementalLMScorer(f'{model_path}', 'cuda', revision=f'checkpoint-{ckpt}')

    metrics = []
    failed_batch=0
    for i in tqdm(range(0, len(test_texts), BATCH_SIZE)):
        batch_text = test_texts[i:i+BATCH_SIZE]
        batch_text = [tokenizer.decode(tokenizer.encode(x, truncation=True, max_length=512, add_special_tokens=False)) for x in batch_text]

        if ppl_type=='sent-nll':
            nll = ilm_model.sequence_score(batch_text, reduction=lambda x: -x.sum(0).item())

        elif ppl_type=='token-nll':
            nll = ilm_model.sequence_score(batch_text, reduction=lambda x: -x.mean(0).item())
        elif ppl_type=='ppl':
            nll = ilm_model.sequence_score(batch_text, reduction=lambda x: -x.mean(0).item())
            nll = [math.exp(x) for x in nll]
        elif ppl_type =='bpb':
            nll_sum = ilm_model.sequence_score(batch_text, reduction=lambda x: -x.sum(0).item())
            bytes_seq = [tokenizer.decode(tokenizer.encode(x, truncation=True, max_length=512, add_special_tokens=False)).encode('utf-8') for x in batch_text]
            assert len(nll_sum)==len(bytes_seq)
            nll = [(x/len(y))/math.log(2) for x,y in zip(nll_sum, bytes_seq)]
        elif ppl_type =='cpb':
            nll_sum = ilm_model.sequence_score(batch_text, reduction=lambda x: -x.sum(0).item())
            chars_seq = [
                len(tokenizer.decode(tokenizer.encode(x, truncation=True, max_length=512, add_special_tokens=False))) for x in batch_text]
            nll = [(x / y)/math.log(2) for x, y in zip(nll_sum, chars_seq)]
        else:
            raise ValueError(f"Unsupported ppl_type: {ppl_type}")
        metrics.extend(nll)


    ppl_df[f"Epoch-{ckpt}"] = metrics

# Write results to CSV
directory = f"ppl_results_{ppl_type}_{eval_data}"
file = directory + \
       f"/{model_name}.csv"

if not os.path.exists(directory):
    os.makedirs(directory)

print(f"Writing results to CSV: {file}")
ppl_df.to_csv(file)
