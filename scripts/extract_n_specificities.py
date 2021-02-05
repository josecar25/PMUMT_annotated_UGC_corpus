import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--errors_file", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_src", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_pred", type=argparse.FileType("r"), required=True)

parser.add_argument("--in_ref", type=argparse.FileType("r"), required=True)
#parser.add_argument("--type", required=True)

#parser.add_argument("--out_pred", type=argparse.FileType("w"), required=True)
#parser.add_argument("--out_src", type=argparse.FileType("w"), required=True)
#parser.add_argument("--out_ref", type=argparse.FileType("w"), required=True)

args = parser.parse_args()

#count = 2
src = args.in_src.read().split("\n")
ref = args.in_ref.read().split("\n")
pred = args.in_pred.read().split("\n")
errors = args.errors_file.read().split("\n")
#t = '1' #args.type
ntypes = []
for i in errors:
    i_s = i.strip('')
    typsi = i.replace("][", "]ņ[").split("ņ")
    present_types = [typsi[j].split(",")[0][1:] for j in range(0,len(typsi))]

    ntypes.append(len(set(present_types)))
ntypes_max = max(ntypes)
  #  if len(typsi) == 2 and (typs[0].split(",")[0][1:] != typs[1].split(",")[0][1:]):

for t in range(1,ntypes_max+1):


    t = str(t)
    src_noisy_out = []  # src[count]]
    src_norm_out = []

    ref_noisy_out = []  # ref[count]]
    ref_norm_out = []

    pred_noisy_out = []  # pred[count]]
    pred_norm_out = []

    li = [0] * 12900
    l_src_norm = [0] * 12900
    system = 's2s'
    out_file_src_norm = "./ntypes/" + system + "/" + t + ".norm.fr"
    out_file_src_noisy = "./ntypes/" + system + "/" + t + ".noisy.fr"

    out_file_ref_norm = "./ntypes/" + system + "/" + t + ".norm.en"
    out_file_pred_norm = "./ntypes/" + system + "/" + t + ".pred.norm.en"

    out_file_ref_noisy = "./ntypes/" + system + "/" + t + ".noisy.en"
    out_file_pred_noisy = "./ntypes/" + system + "/" + t + ".pred.noisy.en"

    count_norm = [0]*12900
    count_norm_tmp = 0

    for cc, l in zip(errors, range(0,12900)):
        cc_s = cc.strip('')
        typs = cc.replace("][", "]ņ[").split("ņ")
        present_types = [typs[j].split(",")[0][1:] for j in range(0,len(typs))]

        if len(typs) == int(t) and len(set(present_types)) == int(t) and cc!= "['N']": #and (typs[0].split(",")[0][1:] != typs[1].split(",")[0][1:]):
          #  if cc_s.strip()[2:4].isnumeric():
           #     cc_prop = cc_s.strip()[2:4]
           # else:
           #     cc_prop = cc_s.strip()[2]
            #le = len(cc_s.split(']'))
            #if le == 2 and cc_prop == t:
            li[l] = 1
            count_norm_tmp +=1
        elif cc == "['N']":
            l_src_norm[l] = 1
            count_norm[l] = count_norm_tmp
            count_norm_tmp = 0

 #       if ls ==20:
  #          break
    total_noisy = sum(li)
    total_norm = sum([a*b for a, b in zip(l_src_norm, count_norm)])

    for sr, re, pr, l, ls, count in zip(src, ref, pred, li, l_src_norm, count_norm):
        if l ==1:
            src_noisy_out.append(sr)
            ref_noisy_out.append(re)
            pred_noisy_out.append(pr)
        if ls ==1:
            for i in range(0,count):
                src_norm_out.append(sr)
                ref_norm_out.append(re)
                pred_norm_out.append(pr)
#all_corrs_idx = args.in_line_divisions.read().split('\n')

#corrs = args.corr_file.read().split('\n')
    out_ref_norm = open(out_file_ref_norm, "w")
    out_pred_norm = open(out_file_pred_norm, "w")

    out_ref_noisy = open(out_file_ref_noisy, "w")
    out_pred_noisy = open(out_file_pred_noisy, "w")

    out_src_noisy = open(out_file_src_noisy, "w")
    out_src_norm = open(out_file_src_norm, "w")

    for s, r, p, s_norm, r_norm, p_norm in zip(src_noisy_out, ref_noisy_out, pred_noisy_out, src_norm_out, ref_norm_out, pred_norm_out):
        out_src_noisy.write(s)
        out_src_noisy.write("\n")

        out_ref_noisy.write(r)
        out_ref_noisy.write("\n")

        out_pred_noisy.write(p)
        out_pred_noisy.write("\n")

        out_src_norm.write(s_norm)
        out_src_norm.write("\n")

        out_ref_norm.write(r_norm)
        out_ref_norm.write("\n")

        out_pred_norm.write(p_norm)
        out_pred_norm.write("\n")

    out_src_noisy.close()
    out_pred_noisy.close()
    out_ref_noisy.close()

    out_src_norm.close()
    out_pred_norm.close()
    out_ref_norm.close()



