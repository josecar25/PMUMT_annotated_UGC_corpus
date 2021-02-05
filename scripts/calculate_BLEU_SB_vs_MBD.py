import sys
import argparse
import sacrebleu
import random
import numpy as np
import scipy.stats as st
import os
import uuid
import signal

parser = argparse.ArgumentParser()
parser.add_argument("--experiment", help="choose between [1type] and [ntypes]", required=True)
parser.add_argument("--MT_system", help="choose between [s2s], [c2c] and [TX]", required=True)
parser.add_argument("--confidence", help="choose the confidence interval (default: 0.95)", type=float, default=0.95)
parser.add_argument("--number_tirages", help="choose the number of tirages for confidence interval (default: 300)", type=int, default=300)
parser.add_argument("--mix_N4plus", help="whether to mix N>=4 for the ntypes experiment", default='Y')
parser.add_argument("--out_file", help="the output .csv files with scores (default ./scores.csv)",  default='./scores')
args = parser.parse_args()


exp = args.experiment
confidence = args.confidence
tirages = args.number_tirages
out_file = open(args.out_file + exp + '.csv.', 'w')
system = args.MT_system

tmp_file_p_norm = str(uuid.uuid4())
tmp_file_p_noisy = str(uuid.uuid4())
tmp_file_r_norm = str(uuid.uuid4())
tmp_file_r_noisy = str(uuid.uuid4())

def delete_tmp_files_exit(signum, frame):
    os.remove('./scripts/tmp/'+tmp_file_p_norm)
    os.remove('./scripts/tmp/'+tmp_file_r_norm)
    os.remove('./scripts/tmp/'+tmp_file_p_noisy)
    os.remove('./scripts/tmp/'+tmp_file_r_noisy)
    sys.exit(1)

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, delete_tmp_files_exit)

if exp == '1type':
    t_max = 14
elif exp == 'ntypes':
    if args.mix_N4plus == 'Y':
        t_max = 5
    else:
        t_max = 7

for t in range(1,t_max):
    t = str(t)
    src_noisy_out = []  # src[count]]
    src_norm_out = []

    ref_noisy_out = []  # ref[count]]
    ref_norm_out = []

    pred_noisy_out = []  # pred[count]]
    pred_norm_out = []

    scores_norm_MB = []
    scores_noisy_MB = []
    scores_norm_SB = []
    scores_noisy_SB = []
    
    ##### for ntypes and mix_N4plus experiment ####

    if args.mix_N4plus == 'Y' and t = 4:
        t = '4to6'

    ###############################################

#    system = 'TX'
    out_file_src_norm = "../" + exp + "/" + system + "/" + t + ".norm.fr"
    out_file_src_noisy = "../" + exp + "/" + system + "/" + t + ".noisy.fr"

    out_file_ref_norm = "../" + exp + "/" + system + "/" + t + ".norm.en"
    out_file_pred_norm = "../" + exp + "/" + system + "/" + t + ".pred.norm.en"

    out_file_ref_noisy = "../" + exp + "/" + system + "/" + t + ".noisy.en"
    out_file_pred_noisy = "../" + exp + "/" + system + "/" + t + ".pred.noisy.en"

    out_ref_norm = open(out_file_ref_norm, "r")
    out_pred_norm = open(out_file_pred_norm, "r")

    out_ref_noisy = open(out_file_ref_noisy, "r")
    out_pred_noisy = open(out_file_pred_noisy, "r")

#    out_src_noisy = open(out_file_src_noisy, "r")
#    out_src_norm = open(out_file_src_norm, "r")
    
    for i in range(0,tirages+1):
        p_norm = []
        r_norm = []
        p_noisy = []
        r_noisy = []
        p_norm_MB = []
        r_norm_MB = []
        p_noisy_MB = []
        r_noisy_MB = []
        

        with open(out_file_pred_norm) as f_pred_norm, open(out_file_ref_norm) as f_ref_norm, open(out_file_pred_noisy) as f_pred_noisy, open(out_file_ref_noisy) as f_ref_noisy:
            lines = list(zip(f_pred_norm, f_ref_norm, f_pred_noisy, f_ref_noisy))
        for j in range(int(len(lines)*0.9)):
            l = random.choice(lines)
            p_norm_MB.append(l[0])#.replace('\n', ''))
            r_norm_MB.append(l[1])#.replace('\n', ''))
            p_noisy_MB.append(l[2])#.replace('\n', ''))
            r_noisy_MB.append(l[3])#.replace('\n', ''))
            p_norm.append(l[0].replace('\n', ''))
            r_norm.append(l[1].replace('\n', ''))
            p_noisy.append(l[2].replace('\n', ''))
            r_noisy.append(l[3].replace('\n', ''))
        f_p_norm = open('./scripts/tmp/'+tmp_file_p_norm, 'w')
        f_r_norm = open('./scripts/tmp/'+tmp_file_r_norm, 'w')
        f_p_noisy = open('./scripts/tmp/'+tmp_file_p_noisy, 'w')
        f_r_noisy = open('./scripts/tmp/'+tmp_file_r_noisy, 'w')
        f_p_norm.write(''.join(p_norm_MB))
        f_r_norm.write(''.join(r_norm_MB))
        f_p_noisy.write(''.join(p_noisy_MB))
        f_r_noisy.write(''.join(r_noisy_MB))
        f_p_norm.close()
        f_r_norm.close()
        f_p_noisy.close()
        f_r_noisy.close()

        r_norm = [r_norm]
        r_noisy = [r_noisy]
        stream_norm = os.popen('perl ./scripts/multi-bleu-detok.perl -lc ./scripts/tmp/'+tmp_file_r_norm+' < ./scripts/tmp/'+tmp_file_p_norm)
        stream_noisy = os.popen('perl ./scripts/multi-bleu-detok.perl -lc ./scripts/tmp/'+tmp_file_r_noisy+' < ./scripts/tmp/'+tmp_file_p_noisy)
        output_norm = stream_norm.read().split(" ")[2].replace(',', '')
        output_noisy = stream_noisy.read().split(" ")[2].replace(',', '')
        #print(output_norm)
        #print(output_noisy)
        #print(sacrebleu.corpus_bleu(p_noisy, r_noisy, tokenize='intl').score)
        scores_norm_MB.append(float(output_norm))
        scores_norm_SB.append(sacrebleu.corpus_bleu(p_norm, r_norm, tokenize='intl').score)
        scores_noisy_MB.append(float(output_noisy))
        scores_noisy_SB.append(sacrebleu.corpus_bleu(p_noisy, r_noisy, tokenize='intl').score)
        ratio_scores_MB = [m / n for m, n in zip(scores_noisy_MB, scores_norm_MB)]
        ratio_scores_SB = [m / n for m, n in zip(scores_noisy_SB, scores_norm_SB)]
        p_norm = []
        r_norm = []
        p_noisy = []
        r_noisy = []
        p_norm_MB = []
        r_norm_MB = []
        p_noisy_MB = []
        r_noisy_MB = []

    ci_ratio = st.t.interval(alpha=confidence, df=len(ratio_scores_MB) - 1, loc=np.mean(ratio_scores_MB), scale=st.sem(ratio_scores_MB))
    ci_scores_norm = st.t.interval(alpha=confidence, df=len(scores_norm_MB) - 1, loc=np.mean(scores_norm_MB), scale=st.sem(scores_norm_MB))
    ci_scores_noisy = st.t.interval(alpha=confidence, df=len(scores_noisy_MB) - 1, loc=np.mean(scores_noisy_MB), scale=st.sem(scores_noisy_MB))

    ci_ratio_SB = st.t.interval(alpha=confidence, df=len(ratio_scores_SB) - 1, loc=np.mean(ratio_scores_SB), scale=st.sem(ratio_scores_SB))
    ci_scores_norm_SB = st.t.interval(alpha=confidence, df=len(scores_norm_SB) - 1, loc=np.mean(scores_norm_SB), scale=st.sem(scores_norm_SB))
    ci_scores_noisy_SB = st.t.interval(alpha=confidence, df=len(scores_noisy_SB) - 1, loc=np.mean(scores_noisy_SB), scale=st.sem(scores_noisy_SB))
    ci_ratio = (round(ci_ratio[0],4),round(ci_ratio[1],4))
    ci_ratio_SB = (round(ci_ratio_SB[0],4),round(ci_ratio_SB[1],4))
    ci_scores_norm_SB = (round(ci_scores_norm_SB[0],3),round(ci_scores_norm_SB[1],3))
    ci_scores_noisy_SB = (round(ci_scores_noisy_SB[0],3),round(ci_scores_noisy_SB[1],3))
    ci_scores_norm = (round(ci_scores_norm[0],3),round(ci_scores_norm[1],3))
    ci_scores_noisy = (round(ci_scores_noisy[0],3),round(ci_scores_noisy[1],3))

    ci_ratio = (round(ci_ratio[0],4),round(ci_ratio[1],4))
    print("Multi-Bleu_detok.perl:")
    print("CI RATIO for system " + system + " for type " + t + " = " + str(ci_ratio) + " total: " +  str(round(((ci_ratio[1]+ci_ratio[0])/2.0),4)) + "±" + str(round(ci_ratio[1]-((ci_ratio[1]+ci_ratio[0])/2.0),4)))
    print("CI SCORE NORM for system " + system + " for type " + t + " = " + str(ci_scores_norm) + " total: " +  str(round(((ci_scores_norm[1]+ci_scores_norm[0])/2.0),2)) + "±" + str(round(ci_scores_norm[1]-((ci_scores_norm[1]+ci_scores_norm[0])/2.0),2)))
    print("CI SCORE NOISY for system " + system + " for type " + t + " = " + str(ci_scores_noisy) + " total: " +  str(round(((ci_scores_noisy[1]+ci_scores_noisy[0])/2.0),2)) + "±" + str(round(ci_scores_noisy[1]-((ci_scores_noisy[1]+ci_scores_noisy[0])/2.0),2)))
    print("-----------------")
    print("SacreBleu --tokenize=intl:")
    print("CI RATIO for system " + system + " for type " + t + " = " + str(ci_ratio_SB) + " total: " +  str(round(((ci_ratio_SB[1]+ci_ratio_SB[0])/2.0),4)) + "±" + str(round(ci_ratio_SB[1]-((ci_ratio_SB[1]+ci_ratio_SB[0])/2.0),4)))
    print("CI SCORE NORM for system " + system + " for type " + t + " = " + str(ci_scores_norm_SB) + " total: " +  str(round(((ci_scores_norm_SB[1]+ci_scores_norm_SB[0])/2.0),2)) + "±" + str(round(ci_scores_norm_SB[1]-((ci_scores_norm_SB[1]+ci_scores_norm_SB[0])/2.0),2)))
    print("CI SCORE NOISY for system " + system + " for type " + t + " = " + str(ci_scores_noisy_SB) + " total: " +  str(round(((ci_scores_noisy_SB[1]+ci_scores_noisy_SB[0])/2.0),2)) + "±" + str(round(ci_scores_noisy_SB[1]-((ci_scores_noisy_SB[1]+ci_scores_noisy_SB[0])/2.0),2)))
    print("#################")
    print("#################")
    print("#################")
    scores_norm = []
    scores_noisy = []
    ratio_scores = []
    scores_norm_MB = []
    scores_noisy_MB = []
    ratio_scores_MB = []
    #    out_src_noisy.close()
    out_pred_noisy.close()
    out_ref_noisy.close()

#    out_src_norm.close()
    out_pred_norm.close()
    out_ref_norm.close()
    os.remove('./scripts/tmp/'+tmp_file_p_norm)
    os.remove('./scripts/tmp/'+tmp_file_r_norm)
    os.remove('./scripts/tmp/'+tmp_file_p_noisy)
    os.remove('./scripts/tmp/'+tmp_file_r_noisy)

