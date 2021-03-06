# coding:utf-8
from xml.dom import minidom
import logging

class XMLReport(object):    #Singleton
    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            logging.debug("new a XMLReport")
            cls.instance = super(XMLReport, cls).__new__(cls)
        else:
            logging.debug("use old XMLReport")
        return cls.instance

    def get_pkg_name(self):
        node = self.get_doc_root().getElementsByTagName('package')[0]
        name_node=node.getElementsByTagName('name')[0]
        name=name_node.childNodes[0].data
        #print(name)

        return name

    def clear(self):
        self.host = None
        self.port = None
        self.user = None

        self.pkg_name = None
        self.doc = None

    def init(self):
        self.clear()
        self.doc = minidom.Document()

        root = self.doc.createElement("report")
        root.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        self.doc.appendChild(root)

    def get_last_group_node(self):
        root = self.get_doc_root()
        lst_group_node = root.getElementsByTagName("group")
        cnt = len(lst_group_node)

        if cnt == 0:
            return None
        else:
            return lst_group_node[cnt-1]

    def set_pkg_name(self,name):
        self.pkg_name = name
        name_node = self.mk_text_node('name', name)
        pkg_node = self.doc.createElement("package")
        pkg_node.appendChild(name_node)

        root = self.get_doc_root()
        root.appendChild(pkg_node)

        #顺便增加结果字段
        result = self.doc.createElement("result")
        root.appendChild(result)


    """
    def __init__(self):
        self.host = None
        self.port = None
        self.user = None

        self.pkg_name = None

        self.doc = minidom.Document()

        root = self.doc.createElement("report")
        root.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        self.doc.appendChild(root)
    """

    def mk_text_node(self, name, text):
        node = self.doc.createElement(name)

        self.add_text(node,text)
        return node


    def set_host_info(self,IP,port,user):

        IP_node = self.mk_text_node('IP', IP)
        port_node = self.mk_text_node('port', port)
        user_node = self.mk_text_node('user', user)

        host = self.doc.createElement("host")

        host.appendChild(IP_node)
        host.appendChild(port_node)
        host.appendChild(user_node)


        root = self.get_doc_root()
        root.appendChild(host)


    def get_doc_root(self):
        root = self.doc.documentElement
        return root

    def append_group(self):
        root = self.get_doc_root()

        group_node = self.doc.createElement("group")
        root.appendChild(group_node)
        return group_node

    def add_text(self, node, text):
        text_node = self.doc.createTextNode(text)
        node.appendChild(text_node)

    def dump_xml(self):
        r = self.get_doc_root()
        #pkg = r.childNodes[0]
        file_name = self.get_pkg_name()
        with open("%s.xml" % file_name.replace(" ", "_"), 'w') as fx:
            self.doc.writexml(fx, newl='\n', indent='\t', addindent='\t', encoding='UTF-8')

    def to_xml(self):
        return self.doc.toxml('utf-8')