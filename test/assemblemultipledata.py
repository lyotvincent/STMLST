from re import sub
import xlrd, subprocess, time

srr = ['SRR2071002', 'SRR2071003', 'SRR2071004', 'SRR2071005', 'SRR2071006', 'SRR2071007', 'SRR2071008', 'SRR2071010', 'SRR2071011', 'SRR2071012', 'SRR2071021', 'SRR2071086', 'SRR2075978', 'SRR2076013', 'SRR2076014', 'SRR2076018', 'SRR2076029', 'SRR2079425', 'SRR2082799', 'SRR2082819', 'SRR2082820', 'SRR2082829', 'SRR2082858', 'SRR2082863', 'SRR2082939', 'SRR2082962', 'SRR2082963']
srr = ['SRR2082799', 'SRR2082819', 'SRR2082820', 'SRR2082829', 'SRR2082858', 'SRR2082863', 'SRR2082939', 'SRR2082962', 'SRR2082963']

drr = ['DRR015774', 'DRR015775', 'DRR015776', 'DRR015777', 'DRR015778', 'DRR015779', 'DRR015780', 'DRR015781', 'DRR015782', 'DRR015783', 'DRR015784', 'DRR015785', 'DRR015881', 'DRR016066']

for acc in srr:
    if acc != "" and acc != None:
        subprocess.run("megahit -1 %s.man_1.fastq -2 %s.man_2.fastq" % (acc, acc), shell=True, check=True)
        subprocess.run("mv ./megahit_out/final.contigs.fa ./%s.contigs.fa" % (acc), shell=True, check=True)
        subprocess.run("rm ./%s*.fastq" % (acc), shell=True, check=True)
        subprocess.run("rm -r ./megahit_out/", shell=True, check=True)

for acc in drr:
    if acc != "" and acc != None:
        subprocess.run("megahit -1 %s.man_1.fastq -2 %s.man_2.fastq" % (acc, acc), shell=True, check=True)
        subprocess.run("mv ./megahit_out/final.contigs.fa ./%s.contigs.fa" % (acc), shell=True, check=True)
        subprocess.run("rm ./%s*.fastq" % (acc), shell=True, check=True)
        subprocess.run("rm -r ./megahit_out/", shell=True, check=True)