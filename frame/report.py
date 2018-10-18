# coding:utf-8
from xml.dom import minidom
import logging

class XMLReport(object):    #Singleton
    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            logging.info("new a XMLReport")
            cls.instance = super(XMLReport, cls).__new__(cls)
        else:
            logging.info("use old XMLReport")
        return cls.instance

    def get_pkg_name(self):
        node = self.get_doc_root().getElementsByTagName('package')[0]
        name = node.childNodes[0].data
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

    def set_pkg_name(self,name):
        self.pkg_name = name
        pkg_node = self.mk_node('package',name)
        root = self.get_doc_root()
        print("XXXX")
        print(root.toxml())

        self.get_doc_root().appendChild(pkg_node)
        print(root.toxml())

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

    def mk_node(self,name,text):
        node = self.doc.createElement(name)

        self.add_text(node,text)
        return node


    def set_host_info(self,IP,port,user):

        IP_node = self.mk_node('IP', IP)
        port_node = self.mk_node('port', port)
        user_node = self.mk_node('user', user)

        host = self.doc.createElement("host")

        host.appendChild(IP_node)
        host.appendChild(port_node)
        host.appendChild(user_node)


        root = self.get_doc_root()
        root.appendChild(host)

        print("FDFD")
        print(user_node.parentNode.nodeName)
        print(self.doc.toxml())

    def get_doc_root(self):
        root = self.doc.documentElement
        print ("Ffff")
        print(root.nodeName)
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