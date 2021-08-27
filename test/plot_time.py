import matplotlib.pyplot as plt
import numpy as np

fontdict = {'family' : 'Times New Roman', 'size' : 6}

# num = [0, 5, 9, 15, 19, 25, 29, 35, 39, 45, 49, 55, 59, 65, 69, 75, 79, 85, 89, 95, 99]
num = [i for i in range(100)]
stmlst = list()
seqsero = list()
sistr = list()

f_stmlst = open("/home/sjl/Workspace/subtyping/test/md_v2/our_time_test_on_s_set_record_withs.md", 'r')
f_seqsero = open("/home/sjl/Workspace/subtyping/test/md_v2/seqsero_time_on_s_set_record.md", 'r')
f_sistr = open("/home/sjl/Workspace/subtyping/test/md_v2/sistr_time_on_s_set_record.md", 'r')

for i in range(100):
    tmp1 = f_stmlst.readline().strip().split()[1]
    tmp2 = f_seqsero.readline().strip().split()[1]
    tmp3 = f_sistr.readline().strip().split()[1]
    if i in num:
        stmlst.append(float(tmp1))
        seqsero.append(float(tmp2))
        sistr.append(float(tmp3))

f_stmlst.close()
f_seqsero.close()
f_sistr.close()

print(len(num))
print(len(stmlst))
print(len(seqsero))
print(len(sistr))

# plt.style.use('ggplot')
plt.figure(figsize=(4,3), dpi=350)

plt.yticks(fontproperties = 'Times New Roman', size = 6) 
plt.xticks(fontproperties = 'Times New Roman', size = 6)

# plt.plot(num, stmlst, "r", label="STMLST")
# plt.plot(num, seqsero, "g", label="SeqSero2")
# plt.plot(num, sistr, "b", label="SISTR")
plt.scatter(num, stmlst, color="r", s=1, label="STMLST")
plt.scatter(num, seqsero, color="g", s=1, label="SeqSero2")
plt.scatter(num, sistr, color="b", s=1, label="SISTR")

# plt.title("Number of sequencing data/Time", fontdict=fontdict)
plt.xlabel("Number of sequencing data", fontdict=fontdict)
# plt.xticks(rotation=45)
plt.ylabel("Time (second)", fontdict=fontdict)


plt.legend(prop=fontdict)
plt.show()