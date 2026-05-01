from minicons import scorer
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import pandas as pd
import os



def read_data(lang):
    lang_lower = lang.lower()
    sentences = pd.read_csv(f'para-multi-blimp/{lang_lower}_multiblimp.tsv', sep='\t').to_dict(orient='records')
    sent_pair = [[sent['sent_correct'], sent['sent_wrong']] for sent in sentences if not pd.isna(sent['sent_wrong'])]
    return sent_pair

def eval_sent_pair(ilm_model, tokenizer, sent_pair):
    correct = 0
    for sent in tqdm(sent_pair):
        # distribution = []
        sent[0] = tokenizer.decode(tokenizer.encode(sent[0], truncation=True, max_length=128, add_special_tokens=False))
        sent[1] = tokenizer.decode(tokenizer.encode(sent[1], truncation=True, max_length=128, add_special_tokens=False))
        num_token0 = len(tokenizer.encode(sent[0], add_special_tokens=False))
        num_token1 = len(tokenizer.encode(sent[1], add_special_tokens=False))

        nll0, nll1 = ilm_model.sequence_score(sent, reduction=lambda x: -x.sum(0).item())
        ppl0 = nll0/num_token0
        ppl1 = nll1/num_token1
        # distribution.append([(0, ppl0), (1, ppl1)])
        if ppl0 < ppl1:
            correct+=1
    acc = correct/len(sent_pair)
    return acc



if __name__ == '__main__':
    args = argparse.ArgumentParser('eval language models')
    args.add_argument('model_name', type=str, help='model name')
    args.add_argument('lang', type=str, help='language')
    args = args.parse_args()
    result_dir = 'multiblimp_results'
    os.makedirs(f'{result_dir}', exist_ok=True)
    model_name = args.model_name
    lang = args.lang
    test = read_data(lang)

    f_results = {}
    model = AutoModelForCausalLM.from_pretrained(f'{model_name}')
    tokenizer = AutoTokenizer.from_pretrained(f'{model_name}')
    print("embedding size:", model.get_input_embeddings().num_embeddings)

    print(len(tokenizer))
    ilm_model = scorer.IncrementalLMScorer(f'{model_name}', 'cuda')

    acc = eval_sent_pair(ilm_model, tokenizer, test)
    f_results['acc'] = acc
    df = pd.DataFrame(
        [{"accuracy": acc} for _, acc in f_results.items()]
    )
    df.to_csv(f'{result_dir}/results_{model_name}.csv')