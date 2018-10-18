# coding:utf-8
import os
import logging
import x_pointer
import sys
import importlib
import importlib.util
import client
import string
from xml.dom import minidom
#from xml.etree import ElementTree as ET
from string import Template


report_xml = None


#root.setAttribute(.setAttribute('xsi:noNamespaceSchemaLocation','bookstore.xsd')#引用本地XML Schema)

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

check_module = None

host = None
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
    global report_xml
    pkg_name_node = report_xml.createElement("package")
    text = report_xml.createTextNode(content)
    pkg_name_node.appendChild(text)
    #root.appendChild(pkg_name_node)
    root = report_xml.documentElement
    root.appendChild(pkg_name_node)



def load_check_package(package_name):

    global check_module
    path = os.path.join(base_dir,"packages/"+package_name+"/"+"check.py")
    logging.debug("load_check_package:" + path)
    #check_module = importlib.import_module(path)
    check_module_spec = importlib.util.spec_from_file_location("check",path)
    module = importlib.util.module_from_spec(check_module_spec)
    check_module_spec.loader.exec_module(module)
    check_module = module
    print(dir(module))




def exec_check_func(func_name):
    global check_module

    s = """check_module.%s()""" % func_name
    logging.debug("exec_check_func :"+s)
    exec(s)




def dump_xml(doc):

    r = doc.documentElement
    print(r.toxml())
    pkg = r.childNodes[0]
    print(pkg.toxml())
    file_name = pkg.childNodes[0].data
    print(file_name)
    with open("%s.xml" % file_name.replace(" ","_"),'w') as fx:
        doc.writexml(fx, newl='\n', indent='\t', addindent='\t', encoding='UTF-8')

if (__name__ == "__main__"):

    host = sys.argv[1]
    port = sys.argv[2]

    user = sys.argv[3]
    passwd = sys.argv[4]

    logging.info(base_dir)

    lst_xml_url=get_lst_xml_url()
    for xml_url in lst_xml_url:
        report_xml = minidom.Document()
        #report_xml.documentElement
        root = report_xml.createElement("Report")
        root.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        report_xml.appendChild(root)



        logging.debug("to process xml:"+xml_url)

        # 创建一个 XMLReader
        parser = x_pointer.Parser()
        parser.dic_url_handler['pkg.name'] =ON_pkg_name
        parser.dic_url_handler['pkg.package_name'] = load_check_package
        parser.dic_url_handler['pkg.patrol.group.item.func'] = exec_check_func
        client.connect_host(host, port, user, passwd)
        parser.parse(xml_url)
        client.close()




        logging.debug("end processing:"+xml_url)
        host_tag = report_xml.createElement("host")
        host_ip = report_xml.createTextNode(host)
        host_tag.appendChild(host_ip)
        root.appendChild(host_tag)

        port_tag = report_xml.createElement("port")
        port_data = report_xml.createTextNode(port)
        port_tag.appendChild(port_data)
        root.appendChild(port_tag)


        print(report_xml.toxml('utf-8'))
        dump_xml(report_xml)



