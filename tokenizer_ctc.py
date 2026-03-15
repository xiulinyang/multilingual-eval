from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer
import json


langs = ["EN","ZH", "AR", "DE","FI","RU","KO","PL","TR","FR"]
# splits = ['train', 'test', 'florestest', 'floresdev']
vocab_sizes = [8192, 32768, 49152, 65536, 81920]
splits = ['pud']
# vocab_sizes = [32768, 65536]
model_sizes = ['small']
tokenization_algorithm = ['bpe']
training_data = ['parallel10']

def read_flores(lang_name, split_s):
    lang_data = open(f'flores/{split_s}/{lang_name}.json', 'r')
    lang_data_json = json.load(lang_data)
    text = [x['text'] for x in lang_data_json]
    return text



for split in splits:
    with open(f'ctc_{split}_scale.tsv', 'w', encoding='utf-8') as f:
        f.write('LANG\tTRAINDATA\tMODELSIZE\tVOCABSIZE\tTOKALG\tCTC\n')
        for vocab_size in vocab_sizes:
            for tok_alg in tokenization_algorithm:
                for lang in langs:
                    for model_size in model_sizes:
                        for train_data in training_data:
                            token_num = 0
                            tokenizer = AutoTokenizer.from_pretrained(f'parallelm/gpt2_{model_size}_{lang}_{tok_alg}_{vocab_size}_{train_data}_42')
                            print(f'models/{lang}_{vocab_size}_{tok_alg}')

                            if split == 'train':
                                sents = Path(f'/root/xiulinyang/multilingual-tokenization/data/{train_data}/{lang}/train/{lang}.txt').read_text().strip().split('\n')
                            elif split == 'test':
                                sents = Path(
                                    f'/root/xiulinyang/multilingual-tokenization/data/{train_data}/{lang}/test/{lang}.txt').read_text().strip().split(
                                    '\n')
                            elif split == 'floresdev':
                                sents = read_flores(lang, 'dev')
                            elif split =='florestest':
                                sents = read_flores(lang, 'devtest')
                            elif split =='pud':
                                sents = Path(f'pud/{lang}.txt').read_text().strip().split('\n')

                            for sent in tqdm(sents):
                                tokens = tokenizer.encode(sent, add_special_tokens=False)
                                token_num += len(tokens)
                            print(lang, split, token_num)
                            vocab_s = str(vocab_size)
                            f.write(f'{lang}\t{train_data}\t{model_size}\t{vocab_s}\t{tok_alg}\t{token_num}\n')
