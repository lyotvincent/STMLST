from re import sub
import xlrd, subprocess, time, os, random
from extract_3_from_s_set import *

sero_dict = extract_3_from_s_set()

cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
f = open("%s/subtyping/test/md_v2/seqsero_on_3_gt_10_s_set_record.md"%cwd, 'a+')
correct = 0
sumsum = 0
for serotype in sero_dict:
    if len(sero_dict[serotype]) <10: continue
    for acc in random.sample(sero_dict[serotype], 3):
        # time1 = time.time()
        cmd = "SeqSero2_package.py -t 4 -m k -i %s/subtyping_test/%s.contigs.fa -c"
        # print(cmd % (cwd, acc))
        p = subprocess.Popen(cmd % (cwd, acc), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        output = str(output, encoding="utf-8")
        # print(output)
        lines = output.split("\n")
        predict = lines[7]+lines[8]
        predict = predict.lower()
        sumsum += 1
        serotype = serotype.lower()
        if serotype in predict:
            correct += 1
        else:
            print(acc, "|", predict, "|", serotype)
            f.write(acc+" | "+predict+" | "+serotype+"\n")
            # print("[INFO] time = %s"% str(time.time()-time1))
print(correct, sumsum, correct/sumsum)
f.write(str(correct)+" "+str(sumsum)+" "+str(correct/sumsum)+"\n")

f.close()