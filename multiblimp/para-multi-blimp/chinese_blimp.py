import json
from pathlib import Path
from glob import glob
import pandas as pd
chinese_minimal_pairs = glob('verb_*.jsonl')
all_minimal_pairs = []
with open('zh_multiblimp.tsv', 'w') as ch_tsv:
    ch_tsv.write('sent_correct\tsent_wrong\n')
    for c_p in chinese_minimal_pairs:
        c_sents = Path(c_p).read_text().strip().split('\n')
        for c_sent in c_sents:
            c_sent = json.loads(c_sent)
            sent_good = c_sent["sentence_good"]
            sent_bad = c_sent["sentence_bad"]
            all_minimal_pairs.append({'sent_correct':sent_good, 'sent_wrong': sent_bad})
            ch_tsv.write(f'{sent_good}\t{sent_bad}\n')



