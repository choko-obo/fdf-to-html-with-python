import rst_helpers
import re

global http_shema
global domain
global moebels
global pages
http_shema = 'http://'
domain = 'moebel.facchin.at'

moebels=['testmoebel']
pages=['moebel', 'kontakt', 'ueber']

#In general the translator class is tooo insane. and i lost patience.
#will leave it at the "full" translator. will write my own postprocessor to add jumpmarks, anchors, qrcodes, and previews.
#grrrr
class Page:
    def __init__(self, page_name):
        self.page_name = page_name

    def get_body(self):
        if self.page_name == 'moebel':
            self.body=''
        else:
            self.body=rst_helpers.full(open('pages/' + self.page_name + '.rst').read(), '', self.page_name)
        return self.body



class Moebel:
    def __init__(self, item_name):
        self.item_name=item_name
        self.item_path='moebel/' + item_name + '/'
        self.content=rst_helpers.full(open(self.item_path + 'text.rst').read(), self.item_path, self.item_name)
        self.uri='%s%s/%s%s.html' % (http_shema, domain, self.item_path, self.item_name)

    def get_content(self):
        return self.content

    def write_content(self):
        with open(self.item_path + 'moebel.html', 'w') as f:
            f.write(self.content) 
        f.close

    def write_content_standalone(self):
        with open(self.item_path + self.item_name + '.html', 'w') as f:
            with open('static/head_standalone') as h:
                for line in h:
                    f.write(line)
            h.close
            f.write(rst_helpers.full(open(self.item_path + 'text.rst').read(), '', self.item_name))
            with open('static/tail') as h:
                for line in h:
                    f.write(line)
            h.close
        f.close

    def get_preview_html(self):
        self.preview_html=''
        previewp=self.get_preview_programmatically()
        self.preview_html = '%s<h1 id="%s">%s</h1>\n' % (self.preview_html, previewp['anchor'], previewp['title'])
        for image in previewp['images']:
            self.preview_html= '%s<img src="%s" alt="%s"/>\n' % (self.preview_html, image['src'], image['alt'])

        return self.preview_html

    def get_preview_programmatically(self):
    #returns objects of format = {'title': 'Titel. z.B. Tisch Eiche', 'anchor': 'foldername hust hust', 'images': [{'alt': 'S', 'src': 'moebel/testmoebel/titel.jpg'}, {'alt': 'U', 'src': 'moebel/testmoebel/detail_fach.jpg'}]}

        retval=[]
        for line in self.content.split('\n'):
            if re.search('(<img|<h1)', line):
                retval.append(line)

        self.preview_prog={}
        self.preview_prog['images']=[]
        for line in retval:
            if re.search('<img', line):
                image = re.search('<img src="(.+)" alt="(.+)"', line)
                self.preview_prog['images'].append({'src': image.group(1), 'alt': image.group(2)}) 
            else:
                title = re.search('<h1 id="(.+)">(.+)</h1>', line)
                self.preview_prog['anchor'] = title.group(1)
                self.preview_prog['title'] = title.group(2)
        return self.preview_prog



    def get_qr(self):
        pass

    def get_uri(self):
        return self.uri




for page in pages:
    page=Page(page)
    print(page.get_body())

'''
for moebel in moebels:
    moebel = Moebel(moebel)
    #print(moebel.get_content())
    print(moebel.get_uri())
    #print(moebel.get_preview_programmatically()['images'][0]['src'])
    moebel.write_content()
    moebel.write_content_standalone()
'''

'''
with open('static/head') as h:
    for line in h:
        print(line)    
with open('static/tail') as t:
    for line in t:
        print(line)
'''