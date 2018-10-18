# coding:utf-8
import client


def check_mem_swap_usage():
    msg = ""
    cmd = """vmstat|sed -n '3p'|awk '{print $3}' """
    out,err = client.send_cmd(cmd)

    #ret = int(ret)

    msg = "swap:%s %s" % (out,err)
    print(msg)
    return False,msg




def check_mem_usage():
    msg=""
    cmd = """vmstat|sed -n '3p'|awk '{print $3" "t$4" " $5" "$6}' """
    out,err = client.send_cmd(cmd)
    print("FFFDDD")
    print(out)
    ret= str(out, encoding='utf-8').strip().split(" ")
    swap = ret[0]
    free = int(ret[1])
    buf = int(ret[2])
    cache = ret[3]

    msg = "swap:%s,free:%d,buf:%d,cache:%s"%(swap,free,buf,cache)
    return False,msg

