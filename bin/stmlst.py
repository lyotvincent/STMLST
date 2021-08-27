import subprocess, re, os, sqlite3, argparse, math

class STMLST:

    def __init__(self, file_name, num_threads=1, min_id=95, min_cov=10, specified_scheme=None, seqsero=False) -> None:
        self.file_name = file_name
        self.BLASTDB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/blastdb/stmlst")
        self.SQLITEDB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/stmlst.sqlite3")
        self.num_threads = num_threads
        self.min_id = min_id # Percent identity <Real, 0..100> # DNA %identity of full allelle to consider 'similar' [~]
        self.min_cov = min_cov # DNA %cov to report partial allele at all [?]
        self.mask_null_serotype = False
        self.specified_scheme = specified_scheme
        self.seqsero = seqsero

    def run(self):
        cmd = """any2fasta -q %s | blastn -db %s -num_threads %s -ungapped -dust no -word_size 32 -max_target_seqs 10000 -perc_identity %s -evalue 1E-20 -outfmt '6 sseqid slen length nident'""" % (self.file_name, self.BLASTDB, self.num_threads, self.min_id)
        # print("[INFO][CMD] %s" % cmd)
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
        blastout = completed_process.stdout

        hit_records = dict()

        lines = blastout.splitlines()
        # print(lines)
        for line in lines:
            # fields: sseqid. format: scheme.gene_num
            fields = line.decode("utf-8").split("\t")
            scheme = fields[0].split(".")
            gene = scheme[1].split("_")
            scheme = scheme[0]
            gene, num = "_".join(gene[:-1]), gene[-1]
            # slen means Subject sequence length
            # length means Alignment length
            # nident means Number of identical matches
            slen, length, nident = fields[1], fields[2], fields[3]
            
            # mlst said "need min-cov to reach min_id"
            if float(nident)/float(slen) < float(self.min_cov)/100:
                continue

            if self.specified_scheme and self.specified_scheme != scheme:
                continue
            if slen == length and nident == slen: # need full length 100% hits
                num = str(num)
            elif slen == length:
                num = "~%s" % num
            else:
                num = "%s?" % num

            if scheme in hit_records:
                if gene in hit_records[scheme]:
                    if re.search(r"[?]", hit_records[scheme][gene]):
                        signal_current = 1
                    elif re.search(r"[~]", hit_records[scheme][gene]):
                        signal_current = 2
                    else:
                        signal_current = 3
                    if re.search(r"[?]", num):
                        signal_new = 1
                    elif re.search(r"[~]", num):
                        signal_new = 2
                    else:
                        signal_new = 3
                    if signal_new > signal_current:
                        hit_records[scheme][gene] = num
                    elif signal_new == signal_current and num not in hit_records[scheme][gene]:
                        hit_records[scheme][gene] += ",%s" % num
                else:
                    hit_records[scheme][gene] = num
            else:
                hit_records[scheme] = dict()
                hit_records[scheme][gene] = num
        # print(hit_records)

        loci_num_dict = self.get_loci_num_dict()

        organism_score_list = list()
        for organism in hit_records:
            temp_score = 0
            loci_dict = hit_records[organism]
            
            score_weight = len(loci_dict.keys())/loci_num_dict[organism]
            temp_score += 100 * score_weight
            for loci in loci_dict:
                if "~" in loci_dict[loci]:
                    temp_score -= self.get_inverse_sigmoid( loci_dict[loci].count("~")/100 ) * score_weight
                elif "?" in loci_dict[loci]:
                    temp_score -= self.get_inverse_sigmoid( loci_dict[loci].count("?")/300 ) * score_weight
            organism_score_list.append([organism, temp_score, loci_dict])
        organism_score_list.sort(key=lambda x: x[1], reverse=True)
        # print("[INFO] organism_score_list len=%s" % len(organism_score_list))
        # print("[INFO] organism_score_list=%s" % [i[0] for i in organism_score_list])
        print("[INFO] highest probability organism: %s" % organism_score_list[0])
        # print("[INFO] highest probability organism: ", organism_score_list[0][0], organism_score_list[0][1])
        # print("[INFO] 2nd probability organism: %s" % organism_score_list[1])
        # print("[INFO] 2nd probability organism: ", organism_score_list[1][0], organism_score_list[1][1])
        # print("[INFO] 3rd probability organism: %s" % organism_score_list[2])
        # print("[INFO] 3rd probability organism: ", organism_score_list[2][0], organism_score_list[2][1])

        # 获取字段名
        sql = "PRAGMA table_info([%s]);" % organism_score_list[0][0]
        field_names = self.search_from_sqlite(sql)
        field_names = [i[1].replace("_", "") for i in field_names]

        # sequence type sql code v1
        best_organism_loci_dict = organism_score_list[0][2]
        for loci in best_organism_loci_dict:
            best_organism_loci_dict[loci] = best_organism_loci_dict[loci].replace("~", "").replace("?", "").split(",")
        # print("[INFO] best_organism_loci_dict=%s" % best_organism_loci_dict)
        sql_num = 1
        for i in best_organism_loci_dict.values():
            sql_num *= len(i)
        if sql_num < 10:
            st_sql_results = self.search_st_v1(best_organism_loci_dict, organism_score_list[0][0])
        else: # sequence type sql code v3
            st_sql_results = self.search_st_v3(best_organism_loci_dict, organism_score_list[0][0], field_names)
        # print(st_sql_results)

        field_names.append("serotype")
        # 输出字段名作为一行
        print("[INFO] %s" % "\t".join(field_names))

        seqsero_prediction = ""
        if st_sql_results:
            for result in st_sql_results:
                sql = "SELECT serotype FROM %s_S2S WHERE ST=%s" % (organism_score_list[0][0], result[0])
                serotype_sql_result = self.search_from_sqlite(sql)
                if len(serotype_sql_result) != 0:
                    serotype = serotype_sql_result[0][0]
                    if_consist_of_other_and_unknown = self.check_other_unknown(serotype)
                    if not if_consist_of_other_and_unknown: # 如果不包含other和unknown
                        print("[INFO] %s\t%s" % ("\t".join([str(i) for i in result]), serotype))
                    elif if_consist_of_other_and_unknown and not self.mask_null_serotype: # 如果包含other和unknown，但是不屏蔽这种空值
                        if self.seqsero:
                            if seqsero_prediction == "":
                                seqsero_prediction = "seqsero prediction: %s" % self.run_seqsero()
                            print("[INFO] %s\t%s" % ("\t".join([str(i) for i in result]), seqsero_prediction))
                        else:
                            print("[INFO] %s\t%s" % ("\t".join([str(i) for i in result]), serotype))
                else:
                    if self.seqsero:
                        if seqsero_prediction == "":
                            seqsero_prediction = "seqsero prediction: %s" % self.run_seqsero()
                    if not self.mask_null_serotype: # 如果不屏蔽空值
                        print("[INFO] %s\t%s" % ("\t".join([str(i) for i in result]), seqsero_prediction))
        else:
            if self.seqsero:
                if seqsero_prediction == "":
                    seqsero_prediction = "seqsero prediction: %s" % self.run_seqsero()
                print("[INFO] %s\t%s" % ("".join(["\t" for i in range(8)]), seqsero_prediction))
            else:
                print("Sorry, no result.")


    def get_loci_num_dict(self):

        loci_num_dict = dict()

        sql = "SELECT organism, num from loci_num;"
        sql_results = self.search_from_sqlite(sql)
        for row in sql_results:
            loci_num_dict[row[0]] = row[1]

        # print(loci_num_dict)
        return loci_num_dict


    def search_from_sqlite(self, sql):
        # print("[INFO][SQL] %s" % sql)
        # print("[INFO][SQL] len = %s" % len(sql))
        conn = sqlite3.connect(self.SQLITEDB)
        c = conn.cursor()
        cursor = c.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results

    def get_inverse_sigmoid(self, x):
        return 1/ ( 1 +  math.exp( x ) )
    

    def check_other_unknown(self, serotype):
        s = serotype.split(";")
        if len(s) > 2:
            return False # False 是不包含other和unknown
        if len(s) == 2:
            if ( "other" in s[0] and "unknown" in s[1] ) or ( "other" in s[1] and "unknown" in s[0] ):
                return True # True 是包含other和unknown，如果屏蔽了空血清型，就不输出
            else:
                return False
        if len(s) == 1:
            if "other" in s[0] or "unknown" in s[0]:
                return True
            else:
                return False

    def search_st_v1(self, best_organism_loci_dict, scheme):
        # print("[INFO] search_st_v1")
        temp_and_list = list()
        for loci in best_organism_loci_dict:
            temp_or_list = list()
            num_csv = best_organism_loci_dict[loci]
            for num in num_csv:
                temp_or_list.append("_%s=%s" % (loci, num))
            temp_and_list.append("(%s)" % (" OR ".join(temp_or_list)))
        sql = "SELECT * FROM %s WHERE %s;" % (scheme, " AND ".join(temp_and_list))
        st_sql_results = self.search_from_sqlite(sql)
        return st_sql_results

    def search_st_v2(self, best_organism_loci_dict, scheme):
        keys = list(best_organism_loci_dict.keys())
        max_loci_num_list = [len(best_organism_loci_dict[loci]) for loci in best_organism_loci_dict]
        end_list = [i-1 for i in max_loci_num_list]
        current_loci_num_list = [0 for loci in best_organism_loci_dict]
        sql = "SELECT * FROM %s WHERE %s;"
        st_sql_results = list()
        while current_loci_num_list != end_list:

            where_list = list()
            for i, current_loci_num in enumerate(current_loci_num_list):
                where_list.append("_%s=%s" % (keys[i], best_organism_loci_dict[keys[i]][current_loci_num]))
            sql_results = self.search_from_sqlite(sql % (scheme, " AND ".join(where_list)))
            if len(sql_results) > 0:
                st_sql_results.extend(sql_results)

            current_loci_num_list[-1] += 1
            for i in range(len(current_loci_num_list)-1, -1, -1):
                if current_loci_num_list[i] == max_loci_num_list[i]:
                    current_loci_num_list[i] = 0
                    current_loci_num_list[i-1] += 1

        where_list = list()
        for i, current_loci_num in enumerate(current_loci_num_list):
            where_list.append("_%s=%s" % (keys[i], best_organism_loci_dict[keys[i]][current_loci_num]))
        sql_results = self.search_from_sqlite(sql % (scheme, " AND ".join(where_list)))
        if len(sql_results) > 0:
            st_sql_results.extend(sql_results)

    def search_st_v3(self, best_organism_loci_dict, scheme, field_names):
        # print("[INFO] search_st_v3")
        sql = "SELECT * FROM %s;" % scheme
        st_sql_results = self.search_from_sqlite(sql)
        # print(st_sql_results)
        # 删除不该被检索到的条目
        for result in st_sql_results:
            for i, field_name in enumerate(field_names):
                if i == 0: continue
                if field_name not in best_organism_loci_dict.keys(): continue
                if result[i] not in best_organism_loci_dict[field_name]:
                    st_sql_results.remove(result)
                    break
        return st_sql_results

    def run_seqsero(self):
        cmd = "SeqSero2_package.py -t 4 -m k -p %s -i %s -c"
        # print("[INFO] ", cmd % (self.file_name))
        try:
            p = subprocess.Popen(cmd % (self.num_threads, self.file_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = p.communicate()
            output = str(output, encoding="utf-8")
            # print(output)
            lines = output.split("\n")
            # print(lines)
            predict = lines[7].split("\t")[1]
            if "\'" in lines[8]:
                predict += " | " + lines[8].split("\'")[1]
        except Exception as e:
            print(e)
        finally:
            predict = "Error in seqsero process."
        return predict

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="STMLST", description="STMLST description:")
    parser.add_argument("-f", "--file_name", type=str, help="input file", required=True)
    parser.add_argument("-n", "--num_threads", type=int, default=1, help="number of threads", required=False)
    parser.add_argument("--min_id", type=float, default=95, help="Percent identity <Real, 0..100> DNA identity of full allelle to consider 'similar' [~]", required=False)
    parser.add_argument("--min_cov", type=float, default=10, help="DNA cov to report partial allele at all [?]", required=False)
    parser.add_argument("--specified_scheme", type=str, default=None, help="specified a scheme", required=False)
    parser.add_argument("-s", "--seqsero", action="store_true", help="fill null serotype with seqsero", required=False)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")
    args = parser.parse_args()
    # print(args)

    pd = STMLST(file_name=args.file_name, num_threads=args.num_threads, min_id=args.min_id, min_cov=args.min_cov, specified_scheme=args.specified_scheme, seqsero=args.seqsero)

    pd.run()