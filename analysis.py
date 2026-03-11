import pandas as pd
from glob import glob
import numpy as np

metric_files = sorted(glob('*mrr_*/*.csv'))
sum_results=[]
for metric_file in metric_files:
    if 'flores' in metric_file:
        continue
    metric_type= metric_file.split('/')[0].split('_')[2]
    eval_data = metric_file.split('/')[0].split('_')[3]
    # eval_data = metric_file.split('/')[-1].split('_')[2]
    model_name = metric_file.split('/')[1].split('.')[0]
    vocab_size = model_name.split('_')[4]
    lang = model_name.split('_')[2]
    tokenization=model_name.split('_')[3]
    metric_df = pd.read_csv(metric_file, skiprows=1, names=['sent_id','sent','value'])
    if metric_type=='ppl':
        mean =  np.exp(np.log(metric_df['value']).mean())

    else:
        mean = metric_df['value'].mean()

    sum_results.append({'lang':lang, 'tokenization':tokenization, 'vocab_size':vocab_size, 'eval_data':eval_data, 'metric_type':metric_type, 'mean_value':mean})

pd.DataFrame(sum_results).to_csv('summary_parallels_mrr.csv', index=False)