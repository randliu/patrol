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

    isPassed,msg = eval(s)

    txt_isPassed=str(isPassed)


    report = XMLReport()
    root = report.get_doc_root()

    item = root.getElementsByTagName('item')[-1]
    pass_node = report.mk_text_node("isPassed",txt_isPassed)

    msg_node = report.mk_text_node('msg',msg)

    item.appendChild(pass_node)
    item.appendChild(msg_node)



def append_group(group_name):
    """
    report = XMLReport()

    #root = report.get_doc_root()

    last_group = report.get_last_group_node()

    if last_group is None:
        last_group = report.doc.createElement("group")
        report.get_doc_root().getElementsByTagName('result')[0].appendChild(last_group)

    print("f")
    return last_group
    """

    report = XMLReport()
    name = report.mk_text_node("name", group_name)
    last_group = report.doc.createElement("group")
    last_group.appendChild(name)
    report.get_doc_root().getElementsByTagName('result')[0].appendChild(last_group)


    return last_group

def append_item(item_name):
    report = XMLReport()
    name = report.mk_text_node("name", item_name)
    last_item = report.doc.createElement("item")
    last_item.appendChild(name)
    report.get_doc_root().getElementsByTagName('group')[-1].appendChild(last_item)

def append_item_description(desc):
    report =XMLReport()
    root = report.get_doc_root()
    item = root.getElementsByTagName('item')[-1]
    description = report.mk_text_node("description",desc)
    item.appendChild(description)
    return

def append_pkg_description(desc):
    report = XMLReport()
    description = report.mk_text_node('description',desc)
    pkg = report.get_doc_root().getElementsByTagName('package')[-1]
    pkg.appendChild(description)

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
        parser.dic_url_handler['pkg.description'] = append_pkg_description
        parser.dic_url_handler['pkg.package_name'] = load_check_package
        parser.dic_url_handler['pkg.patrol.group.item.func'] = exec_check_func
        parser.dic_url_handler['pkg.patrol.group.item.'] = append_item
        parser.dic_url_handler['pkg.patrol.group.name'] = append_group
        parser.dic_url_handler['pkg.patrol.group.item.name'] = append_item
        parser.dic_url_handler['pkg.patrol.group.item.description'] = append_item_description

        client.connect_host(IP, port, user, passwd)
        parser.parse(xml_url)
        client.close()


        logging.debug("end processing:"+xml_url)


        print(report.to_xml())
        report.dump_xml()


