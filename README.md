# multilingual-eval

This is the repository for the paper: Apples to Apples? Towards Comparable Crosslingual
Language Model Evaluation by Xiulin Yang, Ethan Gotlieb Wilcox, and Catherine Arnett.

## repo structure
- `data/`: contains the evaluation datasets used in the paper
- `language_stats/`: contains the statistical results of the languages, including CTC, #chars and #bytes.
- `r_script/`: contains the R script for the statistical analysis in the paper.
- `sample_size/`: contains the sampled datasets for the sample size experiments
- `case_study/`: contains the exploratory word with bloom and GPT2
- `results_summary`: contains the concat results for all the experiments 

## to replicate our experiment results
- Create a virtual enviroment and install the required packages in `requirements.txt`:
```bash
conda create -n eval python==3.11
conda activate eval
pip install -r requirements.txt
```

- Run the `exp.sh` for metric calculation for each dataset and each model.
- You can visualize the results with the R script in `r_script/` and the data in `language_stats/` and `results_summary/`.