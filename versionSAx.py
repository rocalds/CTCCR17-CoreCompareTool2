import xml.sax

class SongHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ''
        self.artist = ''
        self.year = ''
        self.album = ''

def startElement(self,tag,attributes):
    self.CurrentData=tag
    if tag=='song':
        print('Song:')
    title=attributes['title']
    print(f'Title: {title}')

def endElement(self,tag):
    if self.CurrentData=='artist':
        print(f'Artist: {self.artist}')
    elif self.CurrentData=='year':
        print(f'Year: {self.year}')
    elif self.CurrentData=='album':
        print(f'Album: {self.album}')
        self.CurrentData=''

def Characters(self,content):
    if self.CurrentData=='artist':
        self.artist=content
    elif self.CurrentData=='year':
        self.year=content
    elif self.CurrentData=='album':
        self.album=content

if __name__=='__main__':
    parser=xml.sax.make_parser() #creating an XMLReader
    parser.setFeature(xml.sax.handler.feature_namespaces,0) #turning off namespaces
    Handler=SongHandler()
    parser.setContentHandler(Handler) #overriding default ContextHandler
    parser.parse('D:\\_Input\\songs.xml')
