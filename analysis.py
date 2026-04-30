import pandas as pd
from glob import glob
import numpy as np
import random
sampling=True
sum_results=[]
experiment='metrics' #or paraphrase
eval_dataset = 'parallel10'
for i, seed in enumerate(range(15)):
    random.seed(seed)
    if sampling:
        sample_ids_parallel10 = random.sample(range(0, 30000), 500)
        sample_ids_pud = random.sample(range(0, 1000), 500)
        sample_ids_flores = random.sample(range(0, 1012), 500)

    metric_files = sorted(glob(f'metric_results/*{eval_dataset}/*_bpe_*.csv'))

    for metric_file in metric_files:
        print(metric_file)
        if experiment!='metrics' and 'flores' in metric_file:
            continue
        # metric_type= metric_file.split('/')[2].split('_')[2]
        metric_type = metric_file.split('/')[1].split('_')[2]
        if experiment=='metrics': # compare all metrics on parallel corpus
            eval_data = metric_file.split('/')[-1].split('_')[2]
        elif experiment=='paraphrase': # compare paraphrases vs original
            eval_data = metric_file.split('/')[2].split('_')[3]
        else:
            raise ValueError(f"Unsupported experiment: {experiment}")
        model_name = metric_file.split('/')[-1].split('.')[0]
        vocab_size = model_name.split('_')[4]
        lang = model_name.split('_')[2]
        tokenization=model_name.split('_')[3]
        flores_file = f'metric_results/ppl_results_{metric_type}_flores/{model_name}.csv'
        pud_file = f'metric_results/ppl_results_{metric_type}_pud/{model_name}.csv'
        metric_df_parallel10 = pd.read_csv(metric_file, skiprows=1, names=['sent_id','sent','value'])
        metric_df_flores = pd.read_csv(flores_file, skiprows=1, names=['sent_id','sent','value'])
        metric_df_pud = pd.read_csv(pud_file, skiprows=1, names=['sent_id','sent','value'])
        if sampling:
            metric_df_parallel10 = metric_df_parallel10.set_index('sent_id').reindex(sample_ids_parallel10).dropna().reset_index().assign(dataset='parallel10')
            metric_df_flores = metric_df_flores.set_index('sent_id').reindex(sample_ids_flores).dropna().reset_index().assign(dataset='flores')
            metric_df_pud = metric_df_pud.set_index('sent_id').reindex(sample_ids_pud).dropna().reset_index().assign(dataset="pud")
            metric_df_all = pd.concat([metric_df_parallel10, metric_df_flores, metric_df_pud],
                ignore_index=True)
            metric_df = pd.concat([metric_df_parallel10, metric_df_flores, metric_df_pud],ignore_index=True)
        if metric_type=='ppl':
            mean =  np.exp(np.log(metric_df['value']).mean())

        else:
            mean = metric_df['value'].mean()

        sum_results.append({'lang':lang, 'tokenization':tokenization, 'vocab_size':vocab_size, 'eval_data':eval_data, 'metric_type':metric_type, 'mean_value':mean, 'seed': seed})

pd.DataFrame(sum_results).to_csv(f'summary_concat_sample_.csv', index=False)