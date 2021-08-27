import subprocess, xlrd


sheet = xlrd.open_workbook("/home/sjl/Workspace/aem.01746-19-sd002.xlsx").sheet_by_name('Table S1 (NARMS)')

temp_file = "/home/sjl/Workspace/subtyping_test_time/tmp"

f = open(temp_file, 'w')
f.close()

j = 0
for i in range(2, 2282):
    if sheet.cell_value(i, 3) == 'Enteritidis' and sheet.cell_value(i, 1) != "":

        acc = "/home/sjl/Workspace/subtyping_test/%s.contigs.fa" % sheet.cell_value(i, 1)
        next_file = "/home/sjl/Workspace/subtyping_test_time/Enteritides_%s.fa" % j
        print("cat %s %s > %s" % (temp_file, acc, next_file))
        subprocess.run("cat %s %s > %s" % (temp_file, acc, next_file), shell=True, check=True)
        # subprocess.run("cp %s /home/sjl/Workspace/subtyping_test_time/Enteritides_%s.fa" % (temp_file, j), shell=True, check=True)
        j+=1
        if j == 100: break
        temp_file = next_file