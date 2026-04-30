import pandas as pd
from glob import glob
import numpy as np

experiment='metrics' #or paraphrase
eval_dataset = 'flores'
model= 'gpt2'
metric_files = sorted(glob(f'results_ppl_flores/{model}_*.csv'))
sum_results=[]
for metric_file in metric_files:
    if len(metric_file.split('/')[-1].split('_'))>2:
        continue
    print(metric_file)
    if experiment!='metrics' and 'flores' in metric_file:
        continue
    metric_type= metric_file.split('_')[1]

    if experiment=='metrics': # compare all metrics on parallel corpus
        eval_data = metric_file.split('_')[1]
    elif experiment=='paraphrase': # compare paraphrases vs original
        eval_data = metric_file.split('/')[2].split('_')[3]
    else:
        raise ValueError(f"Unsupported experiment: {experiment}")

    lang = metric_file.split('_')[-1]

    metric_df = pd.read_csv(metric_file, skiprows=1, names=['sent_id','sent','value'])
    if metric_type=='ppl':
        mean =  np.exp(np.log(metric_df['value']).mean())

    else:
        mean = metric_df['value'].mean()

    sum_results.append({'lang':lang, 'eval_data':eval_data, 'metric_type':metric_type, 'mean_value':mean})

pd.DataFrame(sum_results).to_csv(f'summary_{eval_dataset}_{model}_{metric_type}.csv', index=False)