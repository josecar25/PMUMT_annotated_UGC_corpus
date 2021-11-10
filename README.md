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

##Citation

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
