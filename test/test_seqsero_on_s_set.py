from re import sub
import xlrd, subprocess, time, os

cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sheet = xlrd.open_workbook("%s/aem.01746-19-sd002.xlsx"%cwd).sheet_by_name('Table S1 (NARMS)')

f = open("%s/subtyping/test/md_v2/seqsero_on_s_set_record.md"%cwd, 'w')

correct = 0
sumsum = 0
for i in range(2, 2282):
    acc = sheet.cell_value(i, 1)
    serotype = sheet.cell_value(i, 3)
    if ":" in serotype:
        continue
    if acc != "" and acc != None:
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