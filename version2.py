from xml.dom.minidom import parse
import xml.dom.minidom
import os

os.chdir('D:\\MergeCollections\\Output')
DOMTree = xml.dom.minidom.parse("RDB_article_031420_Books and Multimedia.xml")
collection = DOMTree.documentElement

datafield = collection.getElementsByTagName('marc:datafield')
for data in datafield:
    if data.hasAttribute('tag'):
        print(data.getAttribute("tag"))
    codea = data.getElementsByTagName('<marc:subfield')
    # print(codea.firschild.data)