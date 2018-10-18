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
    ret = send_cmd(cmd)
    lst_ret= ret.split(" ")
    swap = int(ret[0])
    free = int(ret[1])
    buf = int(ret[2])
    cache = int(ret[3])

    msg = "swap:%d,free:%d,buf:%d,cache:%d"%(swap,free,buf,cache)
    if swap > 0:
        return (False,msg)

