class Venn:

    def __init__(self) -> None:
        self.nkmlst_false = list()
        self.seqsero_false = list()
        self.nkmlst_false_organism_num = set()
        self.seqsero_false_organism_num = set()

    def get_nkmlst_false(self):
        f = open("our_test_set_record.md", 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            # if "-1" in line or "noST" in line:
            if "-1" in line:
                self.nkmlst_false.append(line.split()[0])
                self.nkmlst_false_organism_num.add(line.split()[-2])
        self.nkmlst_false = set(self.nkmlst_false)
    
    def get_seqsero_false(self):
        f = open("seqsero_record.md", 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            if "RR" in line:
                self.seqsero_false.append(line.split()[0])
                self.seqsero_false_organism_num.add(line.split()[-1])
        self.seqsero_false = set(self.seqsero_false)
    
    def get_intersection_and_diff(self):
        self.intersection = self.nkmlst_false.intersection(self.seqsero_false)
        self.nkmlst_diff = self.nkmlst_false.difference(self.intersection)
        self.seqsero_diff = self.seqsero_false.difference(self.intersection)

t = Venn()
t.get_nkmlst_false()
t.get_seqsero_false()
print(len(t.nkmlst_false))
print(t.nkmlst_false)
print(len(t.seqsero_false))
print(t.seqsero_false)
t.get_intersection_and_diff()

print("intersection", len(t.intersection))
print(t.intersection)
print(len(t.nkmlst_false_organism_num))
print("nkmlst_diff", len(t.nkmlst_diff))
print(t.nkmlst_diff)
print(len(t.seqsero_false_organism_num))
print("seqsero_diff", len(t.seqsero_diff))
print(t.seqsero_diff)
