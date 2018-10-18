# coding:utf-8
import os
import logging
import x_pointer
import sys
import importlib
import importlib.util
import client
from xml.dom import minidom
from report import XMLReport




#root.setAttribute(.setAttribute('xsi:noNamespaceSchemaLocation','bookstore.xsd')#引用本地XML Schema)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

check_module = None

IP = None
port = None
user = None
passwd = None



def get_lst_xml_url():
    lst_xml_url=[]
    pkgs_path = os.path.join(base_dir, 'packages/')
    logging.debug("pkgs_path:"+pkgs_path)
    l_pkg_dir_name = os.listdir(pkgs_path)
    logging.debug("l_pkg_dir_name:" + str(l_pkg_dir_name))

    for pkg_dir in l_pkg_dir_name:
        logging.debug("pkg_dir:"+pkg_dir)

        pkg_abs_path = os.path.join(pkgs_path,pkg_dir)
        logging.debug("pkg_abs_path:"+pkg_abs_path)

        xml_url = os.path.join(pkg_abs_path,"info.xml")

        lst_xml_url.append(xml_url)
        logging.debug(str(lst_xml_url))

    return lst_xml_url


def ON_pkg_name(content):
    #global report_xml
    report_xml = XMLReport()

    report_xml.set_pkg_name(content)





def load_check_package(package_name):

    global check_module
    path = os.path.join(base_dir,"packages/"+package_name+"/"+"check.py")
    logging.debug("load_check_package:" + path)
    #check_module = importlib.import_module(path)
    check_module_spec = importlib.util.spec_from_file_location("check",path)
    module = importlib.util.module_from_spec(check_module_spec)
    check_module_spec.loader.exec_module(module)
    check_module = module





def exec_check_func(func_name):
    global check_module

    s = """check_module.%s()""" % func_name
    logging.debug("exec_check_func :"+s)
    exec(s)


if (__name__ == "__main__"):

    IP = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]

    logging.info(base_dir)

    lst_xml_url=get_lst_xml_url()
    for xml_url in lst_xml_url:
        report = XMLReport()
        report.init()
        report.set_host_info(IP, port, user)
        print(report.to_xml())
        logging.debug("to process xml:"+xml_url)

        # 创建一个 XMLReader
        parser = x_pointer.Parser()
        parser.dic_url_handler['pkg.name'] =ON_pkg_name
        parser.dic_url_handler['pkg.package_name'] = load_check_package
        parser.dic_url_handler['pkg.patrol.group.item.func'] = exec_check_func
        client.connect_host(IP, port, user, passwd)
        parser.parse(xml_url)
        client.close()


        logging.debug("end processing:"+xml_url)


        print(report.to_xml())
        report.dump_xml()


