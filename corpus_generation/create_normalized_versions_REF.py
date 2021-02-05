import argparse
import matplotlib.pyplot as plt
import numpy as np
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument("--inn", type=argparse.FileType("r"), required=True)
parser.add_argument("--in_annotations", type=argparse.FileType("r"), required=True)
parser.add_argument("--ref_file", type=argparse.FileType("r"), required=True)
parser.add_argument("--out_dir", required=True)

args = parser.parse_args()
pattern = re.compile('\[(.*)\]')
#pattern2 = re.compile('[0-12]-[0-100]')

f_norms = open(args.out_dir+'norms.fr', 'w')
f_ref = open(args.out_dir+'ref.en', 'w')
f_errors = open(args.out_dir+'errors.fr', 'w')
f_lines = open(args.out_dir+'lines_division.fr', 'w')

out_src = []
out_ref = []
errors = []
lines_out = []
corrections = []
annotations = []

replace_NE = ['John']
count_NE = 0

import itertools
import math

for  idx, (sent, annot, ref) in enumerate(zip(args.inn.read().split("\n"), args.in_annotations.read().split("\n"), args.ref_file.read().split("\n"))):
    out_tmp_src = []
    out_tmp_ref = []
    errors_tmp = []
    corrections_tmp = []
    tokens = []
    #print(sent)
    #print(annot)
    #print(str(idx+1))
    annotations_sent = []
    sent_sp = sent.split(" ")
    for annot_w in annot.split(","):
        p1 = annot_w.split("-")
#        print(annot_w)
#        print(p1)
        if len(p1) > 1 and annotations != 'N' and idx < 400:
            typ = p1[0]
            p2 = p1[1].split(":")
            st = ''.join(p1[1].split(":"))
            #print(p2)
            match = pattern.search(st).groups()[0].replace('ǫ', ',').replace('ȯ', '-').replace('į', ':')
            #print(match)
            #corrections_tmp.append((match, p2))

            if len(p2) > 1:
                #print(p2)
                #print(p1)
                p2_2 = p2[1].split("[")
                corrections_tmp.append((typ, match, p2[0], p2_2[0]))
                ###########tokens.append(sent_sp[int(p2[0])-1:int(p2[1])-1])
                #annotations_sent.append((typ, p2[0], p2[1], sent_sp[int(p2[0])-1:int(p2[1])]))
            else:
               p2_2 = p2[0].split("[")
               corrections_tmp.append((typ, match, p2_2[0]))
               # print(p2)
               #W  print(p1)
               # print(sent_sp)
                #W pos = p1[1]
                #############tokens.append(list(itertools.chain(*sent_sp[int(pos)-1])))
                ############annotations_sent.append((typ, pos, 999, list(itertools.chain(*sent_sp[int(pos)-1]))))
                #annotations_sent.append((typ, pos, 999, sent_sp[int(pos)-1]))
        else: ## No types
            corrections_tmp.append(('N'))
    ############# Permutations of corrections ##########
    ######################print((math.factorial(int(len(corrections_tmp)/2))+int(len(corrections_tmp))))
        
        ###length_perm = int(math.factorial(int(len(corrections_tmp)))/2)
        #perm_corr = list(list(itertools.combinations(corrections_tmp, len(corrections_tmp)+1)))
#        for ii in range(1, len(corrections_tmp)):
#            perm_corr = perm_corr + list(list(itertools.combinations(corrections_tmp, ii)))
#        print(perm_corr)
        #perm_corr = list(itertools.combinations(corrections_tmp, length_perm)) + corrections_tmp
    #else:
    #    perm_corr = list(itertools.combinations(corrections_tmp, int(math.factorial(int(len(corrections_tmp)))/2)))
    #print(len(corrections_tmp))
    
    #Eres = [list(i) for i in set(map(frozenset, itertools.product(corrections_tmp, corrections_tmp))) if len(i) > 1]
    #####res = [[list(i) for i in itertools.combinations(corrections_tmp, r)] for r in range(1, len(corrections_tmp))] # if len(i) > 1]
    res = []
    for r in range(1, len(corrections_tmp)+1):
        for i in itertools.combinations(corrections_tmp, r):
            res.append(list(i))
    if not res:
        res=[corrections_tmp]
    f_lines.write(str(len(res)+1))
    f_lines.write('\n')
    #print(res)
    #print('----------------------------')
    #print(len(res))
    #print("!!!!!!!!!!!!!!!!!!!!")
    #print(res)
    #print(length_perm)
    sents_out = [' '.join(sent.split(" "))]
    ref_out = [' '.join(ref.split(" "))]
    errors_sent = [] #['N']
    for line, elem in enumerate(res,1):
        errors_tmp = [] #['N']
        el = [i if i != 'N' else '' for i in elem]
        #el = [i for i in elem if i != 'N']
       # sents_tmp = []
      #  ref_tmp = []
        sent_t = sent.split(" ")
        for error in el:
            sents_tmp=[]
            ref_tmp = []
            #print(error)
            if error == '':
                sents_t = ' '.join(sent.split(" "))
            elif  error[0] == '9' or error[0] =='13' or error[0] == '6': #False: #error[0] == '10' or error[0] == '6' or error[0] == '9' or error[0] =='N':
                #sents_tmp.append(' '.join(sent.split(" ")))
                if len(error) >3:
                    sent_t[int(error[2]) - 1:int(error[3])] = ''
                else:
                    sent_t[int(error[2]) - 1] = "" #error[1].split(" ")
                #Rsents_tmp.append(' '.join(sent_t).replace('ķ', '').replace('  ', ' '))
                errors_tmp.append((error[0], error[1]))
                ref_tmp.append(ref)
                #continue
            else:
                if len(error) > 3:
                    ###########################################################sent_t = sent.split(" ")
                    #sent_t[int(error[2])-1:int(error[3])] = error[1]+'ķ'*(int(error[3])-int(error[2])-1)
                    ####sent_t[int(error[2]) - 1:int(error[3])] = error[1].split(" ") #+ 'ķ' * (int(error[3]) - int(error[2]) - 1)
                    len_error = len(''.join(sent_t[int(error[2])-1:int(error[3])]).split(" "))
                    len_corr = len(error[1].split(" "))
                    di = len_error-len_corr
                    if error[0] == '10':
                        span = len(error[1].split(" "))
                        name = replace_NE[count_NE%len(replace_NE)]
                        count_NE+=1
                        if ''.join(error[1].strip()[-2:]) == "'s":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+"'s"] + ['ķ'] * (int(error[3]) - int(error[2]))
                        elif ''.join(error[1].strip()[-3:]) == "...":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+"..."] + ['ķ'] * (int(error[3]) - int(error[2]))
                        elif ''.join(error[1].strip()[-2:]) == "..":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+".."] + ['ķ'] * (int(error[3]) - int(error[2]))
                        elif ''.join(error[1].strip()[-4:]) == "!!!!":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+"!!!!"] + ['ķ'] * (int(error[3]) - int(error[2]))
                        elif ''.join(error[1].strip()[-1:]) == ",":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+""] + ['ķ'] * (int(error[3]) - int(error[2]))
                        elif ''.join(error[1].strip()[-1:]) == ".":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+"."] + ['ķ'] * (int(error[3]) - int(error[2]))
                        elif ''.join(error[1].strip()[-1:]) == "?":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+"?"] + ['ķ'] * (int(error[3]) - int(error[2]))
                        elif ''.join(error[1].strip()[-1:]) == "!":
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)+"!"] + ['ķ'] * (int(error[3]) - int(error[2]))
                        else:
                            sent_t[int(error[2]) - 1:int(error[3])] = [' '.join([name]*span)] + ['ķ'] * (int(error[3]) - int(error[2]))
                    else:
                        if len_error < len_corr:
                            sent_t[int(error[2]) - 1:int(error[3])] = error[1].split(" ") + ['ķ'] * (int(error[3]) - int(error[2]) - len(' '.join(sent_t[int(error[2]) - 1:int(error[3])]).split(" ")))

                        else:
                            sent_t[int(error[2])-1:int(error[3])] = error[1].split(" ") + ['ķ']*(int(error[3]) - int(error[2])) #- len(''.join(sent_t[int(error[2])-1:int(error[3])]).split(" ")))

                     #   if len(sent_t) > int(error[3]):
                      #      sent_t.pop(int(error[3]))
                    #Rsents_tmp.append(' '.join(sent_t).replace('ķ', '').replace('  ',' '))
                    errors_tmp.append((error[0], error[1], error[2], error[3]))
                    ref_tmp.append(ref)
                    #errors_out.append(error[0])
                else:
                    #print("D!!!!!")
                    #print(sent_sp)
                    #print(error)
                    #print("-------------")
                    #########################################################sent_t = sent.split(" ")
                    if error[0] == '10':
                        span = len(error[1].split(" "))
                        name = replace_NE[count_NE%len(replace_NE)]
                        count_NE+=1
                        if ''.join(error[1].strip()[-2:]) == "'s":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+"'s"
                        elif ''.join(error[1].strip()[-3:]) == "...":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+"..."
                        elif ''.join(error[1].strip()[-2:]) == "..":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+".."
                        elif ''.join(error[1].strip()[-4:]) == "!!!!":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+"!!!!"
                        elif ''.join(error[1].strip()[-1:]) == ",":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+","
                        elif ''.join(error[1].strip()[-1:]) == ".":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+"."
                        elif ''.join(error[1].strip()[-1:]) == "!":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+"!"
                        elif ''.join(error[1].strip()[-1:]) == "?":
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)+"?"
                        else:
                            sent_t[int(error[2]) - 1] = ' '.join([name]*span)
                    else:
                        sent_t[int(error[2])-1] = error[1]
                    #Rsents_tmp.append(' '.join(sent_t).replace('ķ', '').replace('  ',' '))
                    errors_tmp.append((error[0], error[1], error[2]))
                    ref_tmp.append(ref)
           # sents_tmp.append(' '.join(sent_t).replace('  ', ' ').replace(' ķ', ''))
            sents_tmp.append(re.sub(r"^\s+|\s+$", "", ' '.join(sent_t).replace('ķ', '').replace('  ', ' ').replace('  ', ' ')))
                    #errors_out.append(error[0])
          #  errors_tmp.append((error[0], error[1]))
      #  sents_tmp.insert(0,sents_tmp[-1])
        sents_out.append(''.join(sents_tmp))
        errors_sent.append(errors_tmp)
        ref_out.append(ref_tmp)
        #errors_sent.append(errors_tmp)
    out_src.append(sents_out)
    print("generated_sent:\n")
    for elem in sents_out: #zip(sents_out, errors_sent, ref_out): #, err in zip(sent_out, errors_sent):
        print(elem)
        #print(err)
       # print(ref)
        print("============")
        print('\n')
        ######f_ref.write(''.join(ref))
       ######## f_ref.write('\n')
       # f_errors.write(str(list(err)))
       ####### for elem2 in err:
        #######    if not len(elem2):
        ########        f_errors.write('N')
         #######   else:
        #######        f_errors.write(str(list(itertools.chain(elem2))))
        #######f_errors.write('\n')

        f_norms.write(''.join(elem))
        f_norms.write('\n')

f_norms.close()
f_ref.close()
f_lines.close()
f_errors.close()

    #R perm_corr = []
    #R for i in range(1, len(corrections_tmp) +1):
    #R    perm_corr += list(itertools.combinations(corrections_tmp, i))

    #R print(set(perm_corr))
    #R print("\n\n\n\n\n")
    #####print(perm_corr)
    ########WWWW out_src.append(' '.join(sent_sp
            #annotations_sent.append((999, 999, 999, []))
    #annotations.append(annotations_sent)





#elems = []
#print(annotations[0])
#print(len(annotations))
######[print(elem) for elem in annotations]
#######for elem in enumerate(annotations, 1):
######    print(elem)
#for idd, elem in enumerate(annotations, 1): #itertools.chain(*annotations), 1):
#    #print(elem)
#    line_elems = []
#    for el in elem:
#        typ, p1, p2, tokens = el
        #line_elems = []
        #print(tokens)
    #print("------------")
    #print(typ)
    #print(p1)
    #print(p2)
    #print(tokens)
#        if typ != 999:
#            if p2 != 999:
#                line_elems.append([typ+"-"+p1+":"+p2+"["+(" ").join(tokens)+"]"])
#            else:
#                line_elems.append([typ+"-"+p1+"["+("").join(tokens)+"]"])
#        else:
#            line_elems.append(["N"])
#    elems.append(line_elems)

#for elem in elems:
#    #print(*elem)
#    args.out.write(','.join(list(itertools.chain(*elem))))
#    args.out.write('\n')
