import glob, os, subprocess

cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(cwd, "subtyping_test_nanopore")
print(path)

x = glob.glob(path+"/*.fastq")
print(len(x))

cmd = """canu -d %s -p %s genomeSize=5.1M -nanopore %s"""

for i in x:
    acc = i.split("/")[-1].split(".")[0]
    print(acc)
    subprocess.run(cmd % (acc, acc, i), shell=True, check=True)