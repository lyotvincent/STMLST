import subprocess, time

cmd = "sistr %s -t 8"

f = open("/home/sjl/Workspace/subtyping/test/md_v2/sistr_single_size_time_test_on_s_set_record.md", 'w')

for i in range(100):
    next_file = "/home/sjl/Workspace/subtyping_test_time/Enteritides_%s.fa" % i

    start_time = time.time()
    subprocess.run(cmd % next_file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(str(i)+" "+str(time.time()-start_time))
    f.write(str(i)+" "+str(time.time()-start_time)+"\n")
f.close()