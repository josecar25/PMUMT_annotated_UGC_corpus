# An Annotated -very- Noisy UGC corpus

## Dataset

The files *norms.fr/en* contain all the combinations of errors annotated in *corpus_generation/annotations.fr/en* that are found in the original noisy data in *corpus_generation/crapbank_annotated.fr/en*.

The predictions for this file with all the combinations of errors are in files *norms.pred_seq2seq.sust_unk*, *norms.pred_c2c_300.en* and *norms.pred_TX.en*, for each of the 3 systems.

By using scripts/extract_full_types_and_norm.py and scripts/extract_n_specificities.py we output the folders **1type** and **ntypes** respectively, the former contains the files with **only one** UGC specificity (indicated by X.pred.noisy.fr) and the latter **N differents specificities** (also indicated as X.pred.noisy.fr). Each one contains the folder *s2s*, *c2c* and *TX*, which refer to the files output by each system.

## Requirements

Python 3 and install requirements by :
> pip install -r requirements.txt

## Getting the scores and ratios

For the *1type* experiment:

> bash get_individual_type_scores.sh


For the *ntypes* experiment:

> bash get_N_types_scores.sh


## Specific files where difference between SacreBleu and Multi-Bleu-detok.perl are notable
