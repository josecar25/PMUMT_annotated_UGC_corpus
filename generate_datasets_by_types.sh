#!/bin/sh
python ./scripts/extract_full_types_and_norm.py  --errors_file errors.fr --in_src norms.fr --in_ref norms.en #--in_pred norms.pred_seq2seq.sust_unk.en
