import os
from transformers import AutoTokenizer
from pathlib import Path
import argparse
from tqdm import tqdm

def count_tokens(sent, tokenizer):
    tokens = tokenizer.encode(sent, add_special_tokens=False)
    return len(tokens)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count tokens, characters, and bits in sentences.')
    parser.add_argument('language', type=str,  help='the name of the language')
    parser.add_argument('data', type=str, help='the data name')
    args = parser.parse_args()
    language = args.language
    data = args.data
    vocab_size = [32768, 65536]




    if data == 'flores':
        file = Path(f'data/flores/{language}.txt').read_text().strip().split('\n')
    elif data == 'parallel10':
        file = Path(f'data/parallel10/{language}/test/{language}.txt').read_text().strip().split('\n')
    elif data == 'pud':
        file = Path(f'data/pud/{language}.txt').read_text().strip().split('\n')
    elif data == 'parallel3':
        file = Path(f'data/parallel3/{language}/test/{language}.txt').read_text().strip().split('\n')
    else:
        raise ValueError(f"Unsupported data: {data}")




    with open(f'language_stats/{data}/{language}_token.tsv', 'w') as f:
        f.write('Sentence\tVocabSize\tTokens\n')
        for vocab in vocab_size:
            model_name = f'gpt2_medium_{language}_bpe_{vocab}_parallel3_42'
            tokenizer = AutoTokenizer.from_pretrained(f'parallelm/{model_name}')
            os.makedirs(f'language_stats/{data}', exist_ok=True)
            for sent in tqdm(file):
                token_count = count_tokens(sent, tokenizer)
                f.write(f'{sent}\t{vocab}\t{token_count}\n')