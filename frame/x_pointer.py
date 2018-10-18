# coding:utf-8
import xml.sax
import logging
import traceback

"""
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
"""
class Stack:
    def __init__(self):
        self.stack = []


    def append(self,node):
        self.stack.append(node)

    def pop(self):
        node = self.stack.pop()
        return node

    def __eq__(self, other):

        try:
            o = other.strip()
            lst_componet = o.split(".")
            l_s = len(self.stack)
            l_o = len(lst_componet)
            if  l_s == l_o:
                i = 0
                while i < l_s:
                    if self.stack[i] == l_o[i]:
                        i = i+1
                        continue
                    else:
                        return False
            else:
                return False
        except:
            pass
        finally:
            return False

        return True

    def __str__(self):
        path = None

        for s in self.stack:
            if path is None:
                path = s
            else:
                path = path + "." + s

        return path


    def __len__(self):
        return len(self.stack)


class PointerHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.path = Stack()
        self.dic_pointer_handler={}
        self.cur_path=""


    # 元素开始事件处理
    def startElement(self, tag, attributes):
        #logging.debug("current tag:"+tag)
        self.path.append(tag)
        self.cur_path = str(self.path)
        #logging.debug("cur path:"+self.cur_path)

    # 元素结束事件处理
    def endElement(self, tag):
        #logging.debug("end processing tag:"+tag)
        self.path.pop()
        if len(self.path) == 0:
            self.cur_path = ""
        else:
            self.cur_path = str(self.path)

    # 内容事件处理
    def characters(self, content):
        #logging.debug("content:"+content)

        try:
            if self.dic_pointer_handler.__contains__(self.cur_path):
                handler = self.dic_pointer_handler[self.cur_path]
                print("handler name:"+handler.__name__)
                return handler(content)
            else:
                return None
        except:
            traceback.print_exc()
            logging.debug("error on "+self.cur_path)
        finally:
            return None


class Parser:

    def __init__(self):
        self.parser = xml.sax.make_parser()

        #{url,(handler,data)}
        self.dic_url_handler = {}
        self.lst_node_stack = []

    def parse(self,file_xml):
        # 创建一个 XMLReader
        sax_parser = xml.sax.make_parser()
        # turn off namepsaces
        sax_parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # 重写 ContextHandler
        handler = PointerHandler()

        handler.dic_pointer_handler = self.dic_url_handler

        sax_parser.setContentHandler(handler)

        sax_parser.parse(file_xml)




