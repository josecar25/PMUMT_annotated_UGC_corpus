# PMUMT: An Annotated -very- Noisy UGC Corpus

## Requirements

These third-party frameworks are only needed for reproducing our MT evaluation. For the data, please refer to the following section.

Python 3 and install requirements by :
> pip install -r requirements.txt


## Dataset

The files **norms.fr/en** contain all the combinations of errors, correspondign to the parallel **errors.fr** file, which contain by line the specificities presented in a csv format.
For of such annotations, the format is as follows:

[SPECIF_ID, Normalization, span]

From these files, we provide 2 sub-corpora configurations:

- Individual types of scpecifities:
By running generate_datasets_by_types.sh, the folder **1type** (by default) contains the files with **only one** UGC specificity (indicated by SPECIF_ID.noisy.fr/en).

- Grouping specificities by cardinality (in bins of 1, 2, 3 and 4+):
By running generate_datasets_by_bins.sh the succorpora containing sentences grouped by number of specificities' occurrences are generated in the folder **ntypes** by default.



### Raw annotations

annotated in *corpus_generation/annotations.fr/en* that are found in the original noisy data in *corpus_generation/crapbank_annotated.fr/en*, the former containing a series of csv, where the specificity index, correxponding normalization and span are annotated for each occurrence, and each line contains a sentence.

## Getting the scores and ratios

Regarding evaluation, we provide a script that reads the predictions for each of our sample models (*s2s*, *c2c*, *Tx*) in the generated data folders (*1type* and *ntypes*, named as **X.norm/noisy.pred_SYSTEM.en**) to compute machine translation scores and robustness ratios for each of our experiments using a 95% confidence interval:

For the *1type* experiment:

> bash get_individual_type_scores.sh


For the *ntypes* experiment:

> bash get_N_types_scores.sh

## Citation

If you found this evaluation framework useful for your research, please cite the following publication:

```
@inproceedings{rosales-nunez-etal-2021-understanding,
    title = "Understanding the Impact of {UGC} Specificities on Translation Quality",
    author = "Rosales N{\'u}{\~n}ez, Jos{\'e} Carlos  and
      Seddah, Djam{\'e}  and
      Wisniewski, Guillaume",
    booktitle = "Proceedings of the Seventh Workshop on Noisy User-generated Text (W-NUT 2021)",
    month = nov,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.wnut-1.22",
    pages = "189--198",
}
```
