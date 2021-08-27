from re import sub
import xlrd, subprocess, time

sheet = xlrd.open_workbook("../aem.01746-19-sd002.xlsx").sheet_by_name('Table S1 (NARMS)')

for i in range(2, 2282):
    acc = sheet.cell_value(i, 1)
    if acc != "" and acc != None:
        time1 = time.time()
        subprocess.run("fastq-dump --split-files %s.sra" % (acc), shell=True, check=True)
        subprocess.run("megahit -1 %s_1.fastq -2 %s_2.fastq" % (acc, acc), shell=True, check=True)
        subprocess.run("mv ./megahit_out/final.contigs.fa ./%s.contigs.fa" % (acc), shell=True, check=True)
        subprocess.run("rm ./%s*.fastq" % (acc), shell=True, check=True)
        subprocess.run("rm -r ./megahit_out/", shell=True, check=True)
        print("[INFO] time = %s"% str(time.time()-time1))