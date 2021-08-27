from re import sub
import xlrd, subprocess, time, os

cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sheet = xlrd.open_workbook("%s/aem.01746-19-sd002.xlsx"%cwd).sheet_by_name('Table S1 (NARMS)')

f = open("%s/subtyping/test/md_v2/our_test_on_s_set_record_withs.md"%cwd, 'w')

correct = 0
sumsum = 0
for i in range(2, 2282):
    acc = sheet.cell_value(i, 1)
    serotype = sheet.cell_value(i, 3)
    if "Paratyphi" in serotype:
        serotype = "Paratyphi"
    serotype = serotype.lower()
    if ":" in serotype:
        continue
    if acc != "" and acc != None:
        # time1 = time.time()
        cmd = "python ../subtyping/bin/nkmlst.py -f %s/subtyping_test/%s.contigs.fa -n 8 -s --specified_scheme senterica_achtman_2"
        # print(cmd % (cwd, acc))
        p = subprocess.Popen(cmd % (cwd, acc), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        output = str(output, encoding="utf-8")
        # print(output)
        sumsum += 1
        if serotype in output.lower():
            correct += 1
        else:
            print(acc, "|", output.replace("\n", "").lower().strip()[:100], "|", serotype)
            f.write(acc+" | "+output.replace("\n", "").lower().strip()[:100]+" | "+serotype+"\n")
            # print("[INFO] time = %s"% str(time.time()-time1))
print(correct, sumsum, correct/sumsum)
f.write(str(correct)+" "+str(sumsum)+" "+str(correct/sumsum)+"\n")

f.close()