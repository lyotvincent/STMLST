from re import sub
import xlrd, subprocess, time, os, random
from extract_3_from_s_set import *

sero_dict = extract_3_from_s_set()

cmd = "sistr %s/subtyping_test/%s.contigs.fa -t 8"
cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

f = open("%s/subtyping/test/md_v2/sistr_on_3_gt_10_s_set_record.md"%cwd, 'a+')

correct = 0
sumsum = 0
for serotype in sero_dict:
    if len(sero_dict[serotype]) <10: continue
    # for acc in sero_dict[serotype][:3]:
    for acc in random.sample(sero_dict[serotype], 3):
        # time1 = time.time()
        # print(cmd % (cwd, acc))
        p = subprocess.Popen(cmd % (cwd, acc), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        output = str(output, encoding="utf-8")
        # print(output)
        # lines = output.split('"')
        # print(lines)
        # predict = lines[-2]
        sumsum += 1
        if serotype.lower() in output.lower() :
            correct += 1
        else:
            print(acc, "|", output.replace("\n", "").lower().strip()[-100:], "|", serotype.lower())
            f.write(acc+" | "+output.replace("\n", "").lower().strip()[-100:]+" | "+serotype.lower()+"\n")
print(correct, sumsum, correct/sumsum)
f.write(str(correct)+" "+str(sumsum)+" "+str(correct/sumsum)+"\n")

f.close()