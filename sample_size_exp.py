from glob import glob
import numpy as np
import pandas as pd
import random
from tqdm import tqdm

vocab_size = [8192, 32768, 49152, 65536, 81920]
metrics = ['bpb', 'cpb', 'ppl', 'sent-nll', 'mrr', 'token-nll']
random_seeds = [32, 42, 53, 67, 100, 99, 68, 69, 72, 101, 88, 77, 66, 55, 44]
sample_sizes = [1, 10, 100, 500, 1000, 1500, 1997]

for sample_size in tqdm(sample_sizes):
    for random_seed in random_seeds:
        random.seed(random_seed)
        paraphrase = []
        sampled_ids = set(random.sample(range(0, 1997), sample_size))

        for metric in metrics:
            for vocab in vocab_size:
                en= pd.read_csv(f'ppl_results_{metric}_en/gpt2_small_EN_bpe_{vocab}_parallel10_42.csv').to_dict(orient='records')
                de= pd.read_csv(f'ppl_results_{metric}_de/gpt2_small_DE_bpe_{vocab}_parallel10_42.csv').to_dict(orient='records')
                de_ar = pd.read_csv(f'ppl_results_{metric}_de-ar/gpt2_small_DE_bpe_{vocab}_parallel10_42.csv').to_dict(orient='records')
                # de_p  = pd.read_csv(f'ppl_results_{metric}_de-p/gpt2_small_DE_bpe_{vocab}_parallel10_42.csv').to_dict(orient='records')
                # de_ap = pd.read_csv(f'ppl_results_{metric}_de-arp/gpt2_small_DE_bpe_{vocab}_parallel10_42.csv').to_dict(orient='records')
                sent_e_list   = []
                sent_d_list   = []
                sent_d_p_list = []
                lowest        = []
                highest       = []
                sent_a_p_list = []
                sent_a_r_list = []

                for i, (e, d, d_ar), in enumerate(zip(en, de, de_ar)):

                    if i not in sampled_ids:
                        continue
                    sent_e_list.append(e['Epoch-10'])
                    sent_d_list.append(d['Epoch-10'])
                    sent_d_p_list.append(d_ar['Epoch-10'])
                    # sent_a_p_list.append(d_p['Epoch-10'])
                    # sent_a_r_list.append(d_ap['Epoch-10'])
                    lowest.append(min(d['Epoch-10'], d_ar['Epoch-10']))
                    highest.append(max(d['Epoch-10'], d_ar['Epoch-10']))

                if metric == 'ppl':
                    sent_e_ave    = np.exp(np.mean(np.log(sent_e_list)))
                    sent_d_ave    = np.exp(np.mean(np.log(sent_d_list)))
                    sent_d_p_ave  = np.exp(np.mean(np.log(sent_d_p_list)))
                    # sent_a_p_ave  = np.exp(np.mean(np.log(sent_a_p_list)))
                    # sent_a_r_ave  = np.exp(np.mean(np.log(sent_a_r_list)))
                    lowest_ave    = np.exp(np.mean(np.log(lowest)))
                    highest_ave   = np.exp(np.mean(np.log(highest)))
                else:
                    sent_e_ave    = np.mean(sent_e_list)
                    sent_d_ave    = np.mean(sent_d_list)
                    sent_d_p_ave  = np.mean(sent_d_p_list)
                    # sent_a_p_ave  = np.mean(sent_a_p_list)
                    # sent_a_r_ave  = np.mean(sent_a_r_list)
                    lowest_ave    = np.mean(lowest)
                    highest_ave   = np.mean(highest)

                paraphrase.append({'lang':'EN','tokenization':'bpe','vocab_size':vocab,'eval_data':'en',        'metric_type':metric,'mean_value':sent_e_ave,   'seed':random_seed})
                paraphrase.append({'lang':'DE','tokenization':'bpe','vocab_size':vocab,'eval_data':'de',        'metric_type':metric,'mean_value':sent_d_ave,   'seed':random_seed})
                # paraphrase.append({'lang':'DE','tokenization':'bpe','vocab_size':vocab,'eval_data':'de-ap',        'metric_type':metric,'mean_value':sent_a_p_ave,   'seed':random_seed})
                # paraphrase.append({'lang':'DE','tokenization':'bpe','vocab_size':vocab,'eval_data':'de-ar',        'metric_type':metric,'mean_value':sent_a_r_ave,   'seed':random_seed})

                paraphrase.append({'lang':'DE','tokenization':'bpe','vocab_size':vocab,'eval_data':'de-p',      'metric_type':metric,'mean_value':sent_d_p_ave, 'seed':random_seed})
                paraphrase.append({'lang':'DE','tokenization':'bpe','vocab_size':vocab,'eval_data':'DE_lowest', 'metric_type':metric,'mean_value':lowest_ave,   'seed':random_seed})
                paraphrase.append({'lang':'DE','tokenization':'bpe','vocab_size':vocab,'eval_data':'DE_highest','metric_type':metric,'mean_value':highest_ave,  'seed':random_seed})

        pd.DataFrame(paraphrase).to_csv(f'sample_size/paraphrase_results_{sample_size}_{random_seed}.csv', index=False)


for sample_size in sample_sizes:
    paraphrases = glob(f'sample_size/paraphrase_results_{sample_size}_*.csv')
    with open(f'sample_size/paraphrase_results_{sample_size}.csv', 'w') as out:
        results = []
        for p in paraphrases:
            sents = pd.read_csv(p).to_dict(orient='records')
            for s in sents:
                s['seed'] = int(p.split('/')[-1].split('.')[0].split('_')[-1])
                results.append(s)
        pd.DataFrame(results).to_csv(out, index=False)