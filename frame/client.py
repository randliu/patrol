# coding:utf-8
import paramiko
import logging

ssh_client = None


def connect_host(host, port, user, passwd):
    global ssh_client
    logging.info("connecting :%s:%s"%(host,port))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port, user, passwd)


def close():
    ssh_client.close()

def send_cmd(cmd):
    #print(cmd)
    global  ssh_client

    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    outmsg, errmsg = stdout.read(), stderr.read()
    logging.debug("outmsg:"+str(outmsg))
    logging.debug("errmsg:"+str(errmsg))

    return outmsg,errmsg



def send_cmd2(cmd):
    print(cmd)

    return "1232 232"
