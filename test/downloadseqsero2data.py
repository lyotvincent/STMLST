from re import sub
import xlrd, subprocess, time

sheet = xlrd.open_workbook("../aem.01746-19-sd002.xlsx").sheet_by_name('Table S1 (NARMS)')

for i in range(2, 2282):
    acc = sheet.cell_value(i, 1)
    if acc != "" and acc != None:
        time.sleep(3)
        # subprocess.run("wget -c -t 0 https://sra-pub-run-odp.s3.amazonaws.com/sra/%s/%s" % (acc, acc), shell=True, check=True)
        # subprocess.run("axel -n 99999 https://sra-pub-run-odp.s3.amazonaws.com/sra/%s/%s" % (acc, acc), shell=True, check=True)
        subprocess.run("prefetch %s" % (acc), shell=True, check=True)