import matplotlib.pyplot as plt
import os

fontdict = {'family' : 'Times New Roman', 'size' : 6}

# num = [0, 5, 9, 15, 19, 25, 29, 35, 39, 45, 49, 55, 59, 65, 69, 75, 79, 85, 89, 95, 99]
num = [i for i in range(100)]
sizes = list()
depth = list()
stmlst = list()
seqsero = list()
sistr = list()

f_stmlst = open("/home/sjl/Workspace/subtyping/test/md_v2/our_single_size_time_test_on_s_set_record_withs.md", 'r')
f_seqsero = open("/home/sjl/Workspace/subtyping/test/md_v2/seqsero_single_size_time_test_on_s_set_record.md", 'r')
f_sistr = open("/home/sjl/Workspace/subtyping/test/md_v2/sistr_single_size_time_test_on_s_set_record.md", 'r')

for i in range(100):
    tmp0 = float(os.path.getsize("/home/sjl/Workspace/subtyping_test_time/Enteritides_%s.fa"%i)/1000000)
    tmp4 = i+1
    tmp1 = f_stmlst.readline().strip().split()[1]
    tmp2 = f_seqsero.readline().strip().split()[1]
    tmp3 = f_sistr.readline().strip().split()[1]
    if i in num:
        sizes.append(tmp0)
        depth.append(tmp4)
        stmlst.append(float(tmp1))
        seqsero.append(float(tmp2))
        sistr.append(float(tmp3))

f_stmlst.close()
f_seqsero.close()
f_sistr.close()

print(len(sizes))
print(len(depth))
print(len(stmlst))
print(len(seqsero))
print(len(sistr))

# plt.style.use('ggplot')
plt.figure(figsize=(4,3), dpi=350)

plt.yticks(fontproperties = 'Times New Roman', size = 6) 
plt.xticks(fontproperties = 'Times New Roman', size = 6)

# plt.plot(sizes, stmlst, "r", label="STMLST")
# plt.plot(sizes, seqsero, "g", label="SeqSero2")
# plt.plot(sizes, sistr, "b", label="SISTR")
plt.scatter(depth, stmlst, color="r", s=1, label="STMLST")
plt.scatter(depth, seqsero, color="g", s=1, label="SeqSero2")
plt.scatter(depth, sistr, color="b", s=1, label="SISTR")

# plt.title("Size/Time", fontdict=fontdict)
# plt.xlabel("Size (MB)", fontdict=fontdict)
plt.xlabel("Depth (x)", fontdict=fontdict)
# plt.xticks(rotation=45)
plt.ylabel("Time (second)", fontdict=fontdict)

plt.legend(prop=fontdict)
plt.show()