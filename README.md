# PMUMT: An Annotated -very- Noisy UGC Corpus

## Dataset

The files *norms.fr/en* contain all the combinations of errors annotated in *corpus_generation/annotations.fr/en* that are found in the original noisy data in *corpus_generation/crapbank_annotated.fr/en*, which contain a series of csv, where the specificity index and span are annotated for each occurrence, and each line contains a sentence.

By running generate_datasets_by_types.sh generate_datasets_ntypes.sh, we output the folders **1type** and **ntypes** respectively, the former contains the files with **only one** UGC specificity (indicated by X.noisy.fr/en) and the latter **N differents specificities**.

## Requirements

Python 3 and install requirements by :
> pip install -r requirements.txt

## Getting the scores and ratios

For the *1type* experiment:

> bash get_individual_type_scores.sh


For the *ntypes* experiment:

> bash get_N_types_scores.sh


According to *SacreBleu --tokenize=intl* BLEU(noisy) > BLEU(clean), contrary to *multi-bleu-detok.perl*

# Results

- 1type:


| <sub>Type | <sub>#1 | <sub>#2 | <sub>#3 | <sub>#4 | <sub>#5 | <sub>#6 | <sub>#7 | <sub>#8 | <sub>#9 | <sub>#10 | <sub>#11 | <sub>#12 | <sub>#13 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <sub>s2s | <sub>0.7982<br>±0.004 | <sub>0.9504<br>±0.001 | <sub>0.9323<br>±0.003 | <sub>0.967<br>±0.003 | <sub>0.9414<br>±0.003 | <sub>0.8763<br>±0.002  | <sub>0.945<br>±0.002 | <sub>0.7561<br>±0.004 | <sub>0.915<br>±0.004 | <sub>0.8614<br>±0.002 | <sub>0.9518<br>±0.002 | <sub>0.9017<br>±0.004 | <sub>0.9268<br>±0.003 |
| <sub>Norm |  301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269 | 254 | 100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <sub>c2c | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269 | 254 | 100 |
| <sub>Norm |  301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269 | 254 | 100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <sub>TX | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269 | 254 | 100 |
| <sub>Norm |  301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269 | 254 | 100 |



- Ntypes

| <sub>#Types | <sub>1 | <sub>2 | <sub>3 | <sub>4+ |
| --- | --- | --- | --- | --- |
| <sub>s2s | <sub>0.7982<br>±0.004 | <sub>0.9504<br>±0.001 | <sub>0.9323<br>±0.003 | <sub>0.967<br>±0.003 |
| <sub>Norm |  301 | 283 | 290 | 286 |
| --- | --- | --- | --- | --- |
| <sub>c2c | 301 | 283 | 290 | 286 |
| <sub>Norm |  301 | 283 | 290 | 286 |
| --- | --- | --- | --- | --- |
| <sub>TX | 301 | 283 | 290 | 286 |
| <sub>Norm |  301 | 283 | 290 | 286 |
