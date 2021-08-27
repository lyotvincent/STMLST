import os
import subprocess
import sqlite3


class MakeDB:

    def __init__(self) -> None:
        self.PUBMLSTDIR = """pubmlst"""
        self.BLASTDBDIR = """blastdb"""
        self.ST2SEROTYPE = """ST2serotype"""
        # mhominis_3 eST
        # sparasitica DST
        self.skip_organism_list = ["mbovis"]

    def build_fasta_4_blastdb(self):
        species_names = os.listdir(self.PUBMLSTDIR)
        species_names.sort()
        species_names.remove("dbases.xml") # 下载的url存储文件，这里要排除

        os.makedirs(self.BLASTDBDIR, exist_ok=True)
        out_file = open(os.path.join(self.BLASTDBDIR, "stmlst.fa"), "w")

        for organism in species_names:
            if organism in self.skip_organism_list:
                continue
            organism_dir = os.path.join(self.PUBMLSTDIR, organism)
            loci_names = os.listdir(organism_dir)
            loci_names.remove("profiles_csv") # 非序列文件，这里要排除
            for loci in loci_names:
                loci_path = os.path.join(organism_dir, loci)
                loci_file = open(loci_path, 'r')
                loci_lines = loci_file.readlines()
                for i in range(len(loci_lines)//2):
                    name, sequence = loci_lines[i*2].replace(">", ""), loci_lines[i*2+1]
                    name = ">" + organism + "." + name
                    out_file.write(name)
                    out_file.write(sequence)
                loci_file.close()

        out_file.close()

    def build_blast_db(self):
        subprocess.run("makeblastdb -in %s -dbtype nucl -parse_seqids -out %s" % (os.path.join(self.BLASTDBDIR, "stmlst.fa"), os.path.join(self.BLASTDBDIR, "stmlst")), shell=True, check=True)

    def build_sqlite(self):
        species_names = os.listdir(self.PUBMLSTDIR)
        species_names.sort()
        species_names.remove("dbases.xml") # 下载的url存储文件，这里要排除

        conn = sqlite3.connect("./stmlst.sqlite3")
        c = conn.cursor()

        sql = '''create table loci_num (organism VARCHAR(50) NOT NULL, num INT NOT NULL);'''
        print(sql)
        c.execute(sql)

        for organism in species_names:
            if organism in self.skip_organism_list:
                continue

            organism_dir = os.path.join(self.PUBMLSTDIR, organism)
            loci_names = os.listdir(organism_dir)
            loci_names.remove("profiles_csv") # 非序列文件，这里要排除

            sql = '''INSERT INTO loci_num (organism, num) values(\'%s\', %s);''' % (organism, len(loci_names))
            print(sql)
            c.execute(sql)

            f = open(os.path.join(organism_dir, "profiles_csv"))
            temp_line = f.readline().strip().split("\t")
            loci_index_list = [temp_line.index(loci_name) for loci_name in loci_names] # 找出真正存在的loci字段
            loci_index_list.append(0) # 加入ST和eST
            loci_index_list.sort()
            temp_line = [temp_line[loci_index] for loci_index in loci_index_list]
            print(temp_line)

            num_fields = len(temp_line)
            temp_line = ["_"+i for i in temp_line] # 防止有的字段是数字开头，直接在所有字段前加一个下划线
            fields_for_insert = ",".join(temp_line) # ID,NAME,AGE,ADDRESS,SALARY
            temp_line = [i+" INT NOT NULL" for i in temp_line]
            # temp_line[0] = "_ST INT NOT NULL" # 直接把第一个设置成主键ST，但是mhominis_3的第一列是eST,sparasitica第一列是DST，有可能有影响
            fields_for_create = ",".join(temp_line) # ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, AGE INT NOT NULL, ADDRESS VARCHAR(50), SALARY REAL
            sql = '''create table %s (%s);''' % (organism, fields_for_create)
            print(sql)
            c.execute(sql)
            temp_line = f.readline()
            while temp_line:
                temp_line = temp_line.strip().split("\t")
                temp_line = temp_line[:num_fields]
                sql = '''INSERT INTO %s (%s) values(%s)''' % (organism, fields_for_insert, ",".join(temp_line))
                print(sql)
                c.execute(sql)
                temp_line = f.readline()
        conn.commit()
        conn.close()


    def build_sqlite_st2serotype(self):
        species_names = os.listdir(self.ST2SEROTYPE)
        species_names.sort()

        conn = sqlite3.connect("./stmlst.sqlite3")
        c = conn.cursor()

        print(species_names)
        for species_name in species_names:

            sql = '''create table %s_S2S (ST INT NOT NULL, serotype VARCHAR(50) NOT NULL);''' % (species_name.replace(".txt", ""))
            print(sql)
            c.execute(sql)

            f = open(os.path.join(self.ST2SEROTYPE, species_name), 'r')
            lines = f.readlines()
            f.close()

            lines = lines[4:]

            serotypes = lines.pop(0)
            serotypes = serotypes.strip().split('\t')
            serotypes = serotypes[:-1]
            print(serotypes)

            # ss_dict = dict()

            for line in lines:
                if "Total" in line: break
                if "No value" in line: continue
                temp = list()
                numbers = line.strip().split('\t')
                sequence_type = numbers.pop(0)
                numbers = numbers[:-1]
                # print(len(numbers))
                total_num = 0
                for index, number in enumerate(numbers):
                    if '' == number: continue
                    serotype = serotypes[index]
                    temp.append([serotype, number])
                    total_num += int(number)
                if len(temp) > 0:
                    temp.sort(key=lambda x:x[1], reverse=True)
                    serotype_prediction = list()
                    for serotype, number in temp:
                        serotype_prediction.append("%s:%s" % (serotype, int(number)/total_num))
                    # ss_dict[sequence_type] = ";".join(serotype_prediction)
                    sql = '''INSERT INTO %s_S2S (ST, serotype) values(%s, \"%s\");''' % (species_name.replace(".txt", ""), sequence_type, ";".join(serotype_prediction))
                    print(sql)
                    c.execute(sql)
            # print(ss_dict)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    pd = MakeDB()

    pd.build_fasta_4_blastdb()
    pd.build_blast_db()

    pd.build_sqlite()
    pd.build_sqlite_st2serotype()
