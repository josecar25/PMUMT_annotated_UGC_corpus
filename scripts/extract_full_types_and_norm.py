import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--errors_file", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_src", type=argparse.FileType("r"), required=True)
#parser.add_argument("--in_pred", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_ref", type=argparse.FileType("r"), required=True)


args = parser.parse_args()


src = args.in_src.read().split("\n")
n_lines = len(src)
ref = args.in_ref.read().split("\n")
#pred = args.in_pred.read().split("\n")
errors = args.errors_file.read().split("\n")

for t in range(1,14):
    t = str(t)
    src_noisy_out = []  # src[count]]
    src_norm_out = []

    ref_noisy_out = []  # ref[count]]
    ref_norm_out = []

#    pred_noisy_out = []  # pred[count]]
#    pred_norm_out = []

    li = [0] * n_lines
    l_src_norm = [0] * n_lines
    system = 'TX'
    out_file_src_norm = "./ntypes/"  + t + ".norm.fr"
    out_file_src_noisy = "./ntypes/" +  t + ".noisy.fr"

    out_file_ref_norm = "./ntypes/" + t + ".norm.en"
 #   out_file_pred_norm = "./ntypes/" + t + ".pred.norm.en"

    out_file_ref_noisy = "./ntypes/" + t + ".noisy.en"
#    out_file_pred_noisy = "./ntypes/" + t + ".pred.noisy.en"

    count_norm = [0]*n_lines
    count_norm_tmp = 0

    for cc, l in zip(errors, range(0,n_lines)):
        cc_s = cc.strip('')
        if cc_s.strip()[2:4].isnumeric():
            cc_prop = cc_s.strip()[2:4]
        else:
            cc_prop = cc_s.strip()[2]
        le = len(cc_s.split(']'))
        if le == 2 and cc_prop == t:
            li[l] = 1
            count_norm_tmp +=1
        elif cc == "['N']":
            l_src_norm[l] = 1
            count_norm[l] = count_norm_tmp
            count_norm_tmp = 0

    total_noisy = sum(li)
    total_norm = sum([a*b for a, b in zip(l_src_norm, count_norm)])

    for sr, re, l, ls, count in zip(src, ref, li, l_src_norm, count_norm):
        if l ==1:
            src_noisy_out.append(sr)
            ref_noisy_out.append(re)
#            pred_noisy_out.append(pr)
        if ls ==1:
            for i in range(0,count):
                src_norm_out.append(sr)
                ref_norm_out.append(re)
 #               pred_norm_out.append(pr)

    out_ref_norm = open(out_file_ref_norm, "w")
#    out_pred_norm = open(out_file_pred_norm, "w")

    out_ref_noisy = open(out_file_ref_noisy, "w")
#    out_pred_noisy = open(out_file_pred_noisy, "w")

    out_src_noisy = open(out_file_src_noisy, "w")
    out_src_norm = open(out_file_src_norm, "w")

    for s, r, p, s_norm, r_norm, p_norm in zip(src_noisy_out, ref_noisy_out, pred_noisy_out, src_norm_out, ref_norm_out, pred_norm_out):
        out_src_noisy.write(s)
        out_src_noisy.write("\n")

        out_ref_noisy.write(r)
        out_ref_noisy.write("\n")

#        out_pred_noisy.write(p)
#        out_pred_noisy.write("\n")

        out_src_norm.write(s_norm)
        out_src_norm.write("\n")

        out_ref_norm.write(r_norm)
        out_ref_norm.write("\n")

#        out_pred_norm.write(p_norm)
#        out_pred_norm.write("\n")

    out_src_noisy.close()
#    out_pred_noisy.close()
    out_ref_noisy.close()

    out_src_norm.close()
 #   out_pred_norm.close()
    out_ref_norm.close()



