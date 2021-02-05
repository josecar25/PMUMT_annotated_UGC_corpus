import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--in_line_divisions", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_src", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_pred", type=argparse.FileType("r"), required=True)
parser.add_argument("--out_pred", type=argparse.FileType("w"), required=True)
parser.add_argument("--out_src", type=argparse.FileType("w"), required=True)
parser.add_argument("--in_ref", type=argparse.FileType("r"), required=True)
parser.add_argument("--out_ref", type=argparse.FileType("w"), required=True)

args = parser.parse_args()

count = 0
src = args.in_src.read().split("\n")
ref = args.in_ref.read().split("\n")
pred = args.in_pred.read().split("\n")

src_out = [src[count]]
ref_out = [ref[count]]
pred_out = [pred[count]]

for l in args.in_line_divisions.read().split("\n"):
    if l != '':
        count += int(l)
        src_out.append(src[count])
        ref_out.append(ref[count])
        pred_out.append(pred[count])
#all_corrs_idx = args.in_line_divisions.read().split('\n')

#corrs = args.corr_file.read().split('\n')

for s, r, p in zip(src_out, ref_out, pred_out):
    args.out_src.write(s)
    args.out_src.write("\n")

    args.out_ref.write(r)
    args.out_ref.write("\n")

    args.out_pred.write(p)
    args.out_pred.write("\n")


