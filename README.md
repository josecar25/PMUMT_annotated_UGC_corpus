# An Annotated -very- Noisy UGC Corpus

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


## Specific files where difference between SacreBleu and Multi-Bleu-detok.perl are most notable

- cat 1type/TX/3.pred.noisy.en | sacrebleu --tokenize=intl 1type/TX/3.noisy.en
> BLEU+case.mixed+numrefs.1+smooth.exp+tok.intl+version.1.4.9 = **33.2** 62.2/40.7/28.2/20.0 (BP = 0.960 ratio = 0.961 hyp_len = 1809 ref_len = 1882)

- cat 1type/TX/3.pred.norm.en | sacrebleu --tokenize=intl 1type/TX/3.norm.en
> BLEU+case.mixed+numrefs.1+smooth.exp+tok.intl+version.1.4.9 = **32.4** 60.8/39.3/26.9/18.8 (BP = 0.976 ratio = 0.976 hyp_len = 1837 ref_len = 1882)


- scripts/multi-bleu-detok.perl -lc 1type/TX/3.noisy.en < 1type/TX/3.pred.noisy.en
> BLEU = **28.78**, 62.9/38.0/24.6/15.8 (BP=0.928, ratio=0.931, hyp_len=1527, ref_len=1641)

- scripts/multi-bleu-detok.perl -lc 1type/TX/3.norm.en < 1type/TX/3.pred.norm.en
> BLEU = **29.36**, 61.5/37.7/24.9/16.1 (BP=0.946, ratio=0.948, hyp_len=1555, ref_len=1641)

According to *SacreBleu --tokenize=intl* BLEU(noisy) > BLEU(clean), contrary to *multi-bleu-detok.perl*
