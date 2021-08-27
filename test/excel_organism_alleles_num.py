import xlwt, glob

workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet("Sheet1")

folders = glob.glob("/home/sjl/Workspace/subtyping/db/pubmlst/*")
# print(len(folders))
folders.remove("/home/sjl/Workspace/subtyping/db/pubmlst/dbases.xml")
# print(len(folders))

for i, folder_path in enumerate(folders):
    organism = folder_path.split("/")[-1]
    worksheet.write(i, 0, organism)
    # print(folder_path)
    files = glob.glob(folder_path+"/*")
    files.remove(folder_path+"/profiles_csv")
    print(files)
    for j, file in enumerate(files):
        allele = file.split("/")[-1]
        f = open(file, 'r')
        n = int(len(f.readlines())/2)
        f.close()
        worksheet.write(i, j+1, allele+" ("+str(n)+")")

workbook.save("/home/sjl/Workspace/subtyping/test/md_v2/organism_alleles_num.xlsx")