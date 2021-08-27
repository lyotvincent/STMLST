from re import sub
import xlrd, subprocess, time, os


cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sheet = xlrd.open_workbook("%s/aem.01746-19-sd002.xlsx"%cwd).sheet_by_name('Table S1 (NARMS)')

f = open("%s/subtyping/test/md_v2/sistr_on_s_set_record.md"%cwd, 'w')

cmd = "sistr %s/subtyping_test/%s.contigs.fa -t 8"
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
        # print(cmd % (cwd, acc))
        p = subprocess.Popen(cmd % (cwd, acc), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        output = str(output, encoding="utf-8")
        # print(output)
        # lines = output.split('"')
        # print(lines)
        # predict = lines[-2]
        sumsum += 1
        if serotype in output.lower():
            correct += 1
        else:
            print(acc, "|", output.replace("\n", "").lower().strip()[-100:], "|", serotype)
            f.write(acc+" | "+output.replace("\n", "").lower().strip()[-100:]+" | "+serotype+"\n")

print(correct, sumsum, correct/sumsum)
f.write(str(correct)+" "+str(sumsum)+" "+str(correct/sumsum)+"\n")

f.close()