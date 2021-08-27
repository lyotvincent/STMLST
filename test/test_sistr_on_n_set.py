import subprocess, os

cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# contigs = os.listdir("../subtyping_test_backup")
record_file = open(cwd+"/subtyping/test/md_v1/n_set.md", "r")
records = record_file.readlines()
record_file.close()

contigs = list()
for record in records:
    record = record.strip()
    if record == "":
        continue
    r = record.split()
    contigs.append([r[0], " ".join(r[6:-1])])

cmd = "sistr %s/subtyping_test_contigs/%s.contigs.fa -t 8"

f = open("%s/subtyping/test/md_v2/sistr_on_n_set_record.md"%cwd, 'w')


correct = 0
sumsum = 0
for contig in contigs:
    # print(cmd % (cwd, contig[0]))
    p = subprocess.Popen(cmd % (cwd, contig[0]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    output = str(output, encoding="utf-8")
    # print(output)
    # lines = output.split('"')
    # predict = lines[-2]
    sumsum += 1
    if contig[1].lower() in output.lower() :
        correct += 1
    else:
        print(contig[0], "|", output.replace("\n", "").lower().strip()[-100:], "|", contig[1].lower())
        f.write(contig[0]+" | "+output.replace("\n", "").lower().strip()[-100:]+" | "+contig[1].lower()+"\n")

print(correct, sumsum, correct/sumsum)
f.write(str(correct)+" "+str(sumsum)+" "+str(correct/sumsum)+"\n")

f.close()