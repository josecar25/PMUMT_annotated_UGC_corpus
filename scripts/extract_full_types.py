import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--errors_file", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_src", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_pred", type=argparse.FileType("r"), required=True)

parser.add_argument("--in_ref", type=argparse.FileType("r"), required=True)
#parser.add_argument("--type", required=True)

parser.add_argument("--out_pred", type=argparse.FileType("w"), required=True)
parser.add_argument("--out_src", type=argparse.FileType("w"), required=True)
parser.add_argument("--out_ref", type=argparse.FileType("w"), required=True)

args = parser.parse_args()

#count = 2
src = args.in_src.read().split("\n")
ref = args.in_ref.read().split("\n")
pred = args.in_pred.read().split("\n")
t = '1' #args.type
system = 'TX'

for t in range(13,14):
    t = str(t)
    src_out = []  # src[count]]
    ref_out = []  # ref[count]]
    pred_out = []  # pred[count]]

    li = [0] * 12900

    out_file_ref = "./types/" + system + "/" + t + ".noisy.ref.en"
    out_file_pred = "./types/" + system + "/" + t + ".noisy.pred.en"

    for cc, l in zip(args.errors_file.read().split("\n"), range(0,12900)):
        cc = cc.strip('')
        if cc.strip()[2:4].isnumeric():
            cc_prop = cc.strip()[2:4]
        else:
            cc_prop = cc.strip()[2]
        le = len(cc.split(']'))
        if le == 2 and cc_prop == t:
            li[l] = 1

    for sr, re, pr, l in zip(src, ref, pred, li):
        if l ==1:
            src_out.append(sr)
            ref_out.append(re)
            pred_out.append(pr)
#all_corrs_idx = args.in_line_divisions.read().split('\n')

#corrs = args.corr_file.read().split('\n')
    out_ref = open(out_file_ref, "w")
    out_pred = open(out_file_pred, "w")
    for s, r, p in zip(src_out, ref_out, pred_out):
        out_ref.write(r)
        out_ref.write("\n")

        out_pred.write(p)
        out_pred.write("\n")
    out_pred.close()
    out_ref.close()




