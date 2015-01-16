import rst_helpers
import re
import argparse
import shutil
import importlib.machinery
import sys
import glob
import os
#In general the translator class is tooo insane. and i lost patience.
#will leave it at the "full" translator. will write my own postprocessor to add jumpmarks, anchors, qrcodes, and previews.
#grrrr

#parse stdin
argument_parser = argparse.ArgumentParser(description="Renders a homepage from a very specific folder/file format")
argument_parser.add_argument("-i", "--input", type=str, default="", help="the input directroy.")
argument_parser.add_argument("-o", "--output", type=str, default="www", help='the output directory. defaults to "www"')
argument_parser.add_argument("-d", "--debug", help="don't write just run everything else")
args = argument_parser.parse_args()

if args.input == "" or args.debug:
    print("\nOH NOES!!!! \n\n I need at leats input to be specified \n")
    print(argument_parser.print_help())
    sys.exit(1)

#get the config. gah this looks horrid
config_loader = importlib.machinery.SourceFileLoader("Config", args.input + '/config.py')
config = config_loader.load_module()
c=config.Config(args.input)
#c == ['domain', 'http_shema', 'moebels', 'output_directory', 'pages']

class Navigation:
    def __init__(self):
        self.nav_urls = {}
        self.nav_urls['order'] = []
        for page in c.pages:
            self.nav_urls[page]='/pages/' + page + '.html'
            self.nav_urls['order'].append(page)

    def add(self, another_pagename, another_url):
        self.nav_urls[another_pagename]=another_url
        self.nav_urls['order'].append(another_pagename)

    def get_html(self):
        self.html = '<div id="nav">\n'
        for page in self.nav_urls['order']:
            self.html = '%s<a href="%s">%s</a>\n' % (self.html, self.nav_urls[page], page.upper())
        self.html = self.html + '</div>'
        return self.html


class Page:
    def __init__(self, page_name):
        self.page_name = page_name

    def get_body(self):
        if self.page_name == 'möbel':
            self.body='<h1>Möbel</h1>'
            for möbel in c.möbels:
                möbel = Möbel(möbel)
                uri=möbel.get_uri()
                möbel = möbel.get_preview_programmatically()
                self.body='''%s<div class="moebel">
                <a href="%s"><img src="%s" alt="%s" /></a><h2><span><a href="%s">%s</a></span></h2></a>
                </div>
                ''' % (self.body, uri, möbel['images'][0]['src'], möbel['images'][0]['alt'], uri, möbel['title'])
        else:
            self.body=rst_helpers.full(open(c.input + '/pages/' + self.page_name + '.rst').read(), '', self.page_name)
        return self.body

    def get_head(self):
        self.head='''
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>%s</title>
        <link rel="stylesheet" type="text/css" href="static/style.css">
        <script type="text/javascript" src="static/live.js"></script>
    </head>

    <body>
        <div id="container">''' % self.page_name.title()
        return self.head

    def get_tail(self):
        self.tail ='''
        </div> 
    </body>
</html>'''
        return self.tail

    def get_all(self):
        nav=Navigation()
        self.all=self.get_head()
        self.all=self.all + nav.get_html()
        self.all=self.all + self.get_body()
        self.all=self.all + self.get_tail()
        return self.all

    def write_html(self):
        #this writes a toplevel page.
        with open(c.output + '/pages/' + self.page_name +'.html', 'w') as f:
            f.write(self.get_all()) 
        f.close  



class Möbel:
    def __init__(self, item_name):
        self.item_name=item_name
        self.input_path=c.input + '/möbel/' + item_name + '/'
        self.output_path=c.output + '/möbel/' + item_name + '/'
        self.relative_path='/möbel/' + item_name + '/'
        self.content=rst_helpers.full(open(self.input_path + 'text.rst').read(), self.relative_path, self.item_name)
        self.uri='%s%s/%s%s.html' % (c.http_shema, c.domain, self.relative_path, self.item_name)

    def get_content(self):
        return self.content

    def write_content(self):
        with open(self.output_path + 'möbel.html', 'w') as f:
            f.write(self.content) 
        f.close

    def write_content_standalone(self):
        page_so=Page(self.item_name)
        nav=Navigation()
        with open(self.output_path + self.item_name + '.html', 'w') as f:
            f.write(page_so.get_head())
            f.write(nav.get_html())
            f.write(rst_helpers.full(open(self.input_path + 'text.rst').read(), '', self.item_name))
            f.write(page_so.get_tail())
        f.close
        os.symlink('../../static', self.output_path + '/static')

    def get_preview_html(self):
        self.preview_html=''
        previewp=self.get_preview_programmatically()
        self.preview_html = '%s<h1 id="%s">%s</h1>\n' % (self.preview_html, previewp['anchor'], previewp['title'])
        for image in previewp['images']:
            self.preview_html= '%s<img src="%s" alt="%s"/>\n' % (self.preview_html, image['src'], image['alt'])

        return self.preview_html

    def get_preview_programmatically(self):
        '''returns objects of format = {'title': 'Titel. z.B. Tisch Eiche', 
        'anchor': 'foldername hust hust', 'images': [{'alt': 'S', 'src': 'moebel/testmoebel/titel.jpg'},
        {'alt': 'U', 'src': 'moebel/testmoebel/detail_fach.jpg'}]}'''
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

def create_output_dir():
    #delete old and create new output dir
    shutil.rmtree(c.output,ignore_errors=True)
    shutil.copytree(c.input, c.output, ignore=shutil.ignore_patterns('*.pyc', '*.py', '*.rst', '__pycache__'))    


def create_pages():
    os.symlink('../static', c.output + '/pages/static')
    for page in c.pages:
        page = Page(page)
        page.write_html()

def create_möbels():
    for möbel in c.möbels:
        möbel = Möbel(möbel)
        möbel.write_content_standalone()
        möbel.write_content()


create_output_dir()
create_pages()
create_möbels()