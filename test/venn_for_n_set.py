class Venn:

    def __init__(self) -> None:
        self.sbmlst_false = set()
        self.seqsero_false = set()
        self.sistr_false = set()
        self.sbmlst_false_organism_num = set()
        self.seqsero_false_organism_num = set()
        self.sistr_false_organism_num = set()

    def get_sbmlst_false(self):
        f = open("test/md_v2/our_test_on_n_set_record_withs.md", 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            if "RR" not in line: continue
            self.sbmlst_false.add(line.split()[0])
            self.sbmlst_false_organism_num.add(line.split()[-1])
    
    def get_seqsero_false(self):
        f = open("test/md_v2/seqsero_on_n_set_record.md", 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            if "RR" in line:
                self.seqsero_false.add(line.split()[0])
                self.seqsero_false_organism_num.add(line.split()[-1])

    def get_sistr_false(self):
        f = open("test/md_v2/sistr_on_n_set_record.md", 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            if "RR" in line:
                self.sistr_false.add(line.split()[0])
                self.sistr_false_organism_num.add(line.split()[-1])

    def get_intersection_and_diff(self):
        self.sbmlst_and_seqsero = self.sbmlst_false.intersection(self.seqsero_false)
        self.sbmlst_and_sistr = self.sbmlst_false.intersection(self.sistr_false)
        self.seqsero_and_sistr = self.seqsero_false.intersection(self.sistr_false)
        self.sbmlst_and_seqsero_and_sistr = self.sbmlst_and_seqsero.intersection(self.sbmlst_and_sistr)
        # self.nkmlst_diff = self.nkmlst_false.difference(self.intersection)

t = Venn()
t.get_sbmlst_false()
t.get_seqsero_false()
t.get_sistr_false()
print(len(t.sbmlst_false))
print(len(t.seqsero_false))
print(len(t.sistr_false))

t.get_intersection_and_diff()
print(len(t.sbmlst_and_seqsero_and_sistr))
print(len(t.sbmlst_and_seqsero))
print(len(t.sbmlst_and_sistr))
print(len(t.seqsero_and_sistr))


