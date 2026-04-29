from glob import glob
import os
from transformers import AutoTokenizer
from pathlib import Path
import argparse
def count_tokens(sent, tokenizer):
    tokens = tokenizer.encode(sent, add_special_tokens=False)
    return len(tokens)

def count_characters(sent):
    return len(''.join(sent.split()))

def count_bytes(sent):
    sent = ''.join(sent.split())
    return len(sent.encode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count tokens, characters, and bits in sentences.')
    parser.add_argument('data', type=str, required=True, help='the data name')
    args = parser.parse_args()
    model_name = args.model_name
    data = args.data
    language = model_name.split('_')[2]
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

    tokenizer = AutoTokenizer.from_pretrained(f'parallelm/{model_name}')
    os.makedirs(f'language_stats/{data}', exist_ok=True)
    with open(f'language_stats/{data}/{language}_char_bit.tsv', 'w') as f:
        f.write('Sentence\tCharacters\tBytes\n')
        for sent in file:
            char_count = count_characters(sent)
            bit_count = count_bytes(sent)
            f.write(f'{sent}\t{char_count}\t{bit_count}\n')