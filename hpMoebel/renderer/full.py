import rst_helpers

class Item:
    def __init__(self, item_name):
        self.item_name=item_name
        self.item_path='moebel/' + item_name + '/'

    def get_content(self):
        print(rst_helpers.full(open(self.item_path + 'text.rst').read(), self.item_path, self.item_name))

    def get_preview(self):
        print(rst_helpers.prev(open(self.item_path + 'text.rst').read(), self.item_path, self.item_name))

    def get_qr(self):
        pass

    def get_uri(self):
        pass


class Page:
    def __init__(self, name):
        name=self.name
    def get_title():
        pass
    def get_content():
        pass


moebels=['testmoebel']

with open('static/head') as h:
    for line in h:
        print(line)

for moebel in moebels:
    path = 'moebel/' + moebel + '/'
    moebel = Item(moebel)
    print(moebel.get_content())


with open('static/tail') as t:
    for line in t:
        print(line)
