import subprocess, os

class PublistDownloader:


    def __init__(self) -> None:
        self.URL = """https://pubmlst.org/static/data/dbases.xml"""
        self.OUTDIR = """pubmlst"""


    def download_dbases_xml(self):
        subprocess.run("wget -c -P %s %s" % (self.OUTDIR, self.URL), shell=True, check=True)


    def judge_scheme_or_loci(self, url):
        if "scheme" in url:
            return 1
        elif "loci" in url:
            return 0
        else:
            print(url)
            return -1


    def download(self):
        xml = open(os.path.join(self.OUTDIR, "dbases.xml"), 'r')
        line = xml.readline().strip()
        while line:
            if "<url>" in line:
                url = line.replace("<url>", "").replace("</url>", "")
                is_scheme = self.judge_scheme_or_loci(url)
                if is_scheme == 1:
                    sub_urls = url.split("/")
                    species = sub_urls[-4].split("_")
                    species.remove("pubmlst")
                    species.remove("seqdef")
                    species = "_".join(species)
                    if int(sub_urls[-2]) > 1:
                        species += "_"+sub_urls[-2]
                    species_dir = os.path.join(self.OUTDIR, species)
                    os.makedirs(species_dir, exist_ok=True)
                    while True:
                        try:
                            completed_process = subprocess.run("wget %s -P %s -t 0 -T 10" % (url, species_dir), shell=True, check=True)
                        except Exception as e:
                            print(e)
                        finally:
                            print(completed_process.returncode)
                            if completed_process.returncode == 0:
                                break
                elif is_scheme == 0:
                    while True:
                        try:
                            completed_process = subprocess.run("wget %s -O %s -t 0 -T 10" % (url, os.path.join(species_dir, url.split("/")[-2])), shell=True, check=True)
                        except Exception as e:
                            print(e)
                        finally:
                            print(completed_process.returncode)
                            if completed_process.returncode == 0:
                                break
            line = xml.readline().strip()
        xml.close()


if __name__ == '__main__':
    pd = PublistDownloader()
    pd.download_dbases_xml()
    pd.download()

