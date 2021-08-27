
def s(f):
    ff = open(f, 'r')
    lines = ff.readlines()
    ff.close()

    lines = [i.strip().split("|")[-1].strip() for i in lines if "RR" in i]
    # print(lines)
    return len(set(lines))

if __name__ == "__main__":
    print(s("/home/sjl/Workspace/subtyping/test/md_v2/our_test_on_n_set_record_withs.md"))
    print(s("/home/sjl/Workspace/subtyping/test/md_v2/seqsero_on_n_set_record.md"))
    print(s("/home/sjl/Workspace/subtyping/test/md_v2/sistr_on_n_set_record.md"))
    print("===")
    print(s("/home/sjl/Workspace/subtyping/test/md_v2/our_test_on_s_set_record_withs.md"))
    print(s("/home/sjl/Workspace/subtyping/test/md_v2/seqsero_on_s_set_record.md"))
    print(s("/home/sjl/Workspace/subtyping/test/md_v2/sistr_on_s_set_record.md"))