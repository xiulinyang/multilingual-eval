from datasets import load_dataset

langs_dict={
    'pol': 'pl',
    'rus': 'ru',
    'deu': 'de',
    'fin': 'fi',
    'fra': 'fr',
    'arb': 'ar',
    'tur': 'tr',
    'eng': 'en',
}

for k, v in langs_dict.items():
    ds = load_dataset("jumelet/multiblimp", k)
    print(ds)
    ds['train'].to_csv(f"{v}_multiblimp.csv")

    with open(f"{v}_multiblimp.tsv", 'w') as f:
        f.write(f'sent_correct\tsent_wrong\n')
        for item in ds['train']:
            correct = item['sen']
            wrong = item['wrong_sen']
            f.write(f'{correct}\t{wrong}\n')