from types import CodeType
import xlwt, os, xlrd
import venn_for_n_set
import venn_for_s_set

def write_n_set_excel():
    t = venn_for_n_set.Venn()
    t.get_sbmlst_false()
    t.get_seqsero_false()
    t.get_sistr_false()

    stmlst_false_on_n_set = t.sbmlst_false
    seqsero_false_on_n_set = t.seqsero_false
    sistr_false_on_n_set = t.sistr_false

    f = open("test/md_v1/n_set.md", 'r')
    lines = f.readlines()
    f.close()

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("Sheet1")

    i = 0
    worksheet.write(0, 0, "accession")
    worksheet.write(0, 1, "serotype")
    worksheet.write(0, 2, "STMLST")
    worksheet.write(0, 3, "SeqSero2")
    worksheet.write(0, 4, "SISTR")
    for line in lines:
        if "RR" not in line: continue
        i += 1
        accession = line.strip().split()[0]
        serotype = " ".join(line.strip().split()[1:-1])

        worksheet.write(i, 0, accession)
        worksheet.write(i, 1, serotype)
        if accession in stmlst_false_on_n_set:
            worksheet.write(i, 2, "False")
        else:
            worksheet.write(i, 2, "True")
        if accession in seqsero_false_on_n_set:
            worksheet.write(i, 3, "False")
        else:
            worksheet.write(i, 3, "True")
        if accession in sistr_false_on_n_set:
            worksheet.write(i, 4, "False")
        else:
            worksheet.write(i, 4, "True")

    workbook.save("/home/sjl/Workspace/stmlst/test/md_v2/test_on_n_set.xlsx")

# def write_s_set_excel():TODO

def write_multiple_set_excel():
    f = open("test/md_v2/test_on_all_organisms.md", 'r')
    lines = f.readlines()
    f.close()

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("Sheet1")

    i = 0
    worksheet.write(0, 0, "accession")
    worksheet.write(0, 1, "microbial organism")
    microbial_organism = ""
    worksheet.write(0, 2, "serotype")
    worksheet.write(0, 3, "STMLST")
    worksheet.write(0, 4, "SeqSero2")
    worksheet.write(0, 5, "SISTR")
    for line in lines:
        if line.startswith("#"):
            microbial_organism = " ".join(line.strip().split()[1:3])
            continue
        if line.strip() == "" or line.startswith("<!--"):
            continue
        i += 1
        accession = line.strip().split()[0]
        serotype = line.strip().split()[1]
        worksheet.write(i, 0, accession)
        worksheet.write(i, 1, microbial_organism)
        worksheet.write(i, 2, serotype)
        if line.strip().split()[-1] != "-1":
            worksheet.write(i, 3, "True")
        else:
            worksheet.write(i, 3, "False")
        worksheet.write(i, 4, "False")
        worksheet.write(i, 5, "False")
    workbook.save("/home/sjl/Workspace/stmlst/test/md_v2/test_on_multiple_microbial_organisms_set.xlsx")


if __name__ == "__main__":
    # write_n_set_excel()
    # write_s_set_excel()
    write_multiple_set_excel()