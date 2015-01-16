
class Config:
    def __init__(self, input):
        self.input = input

    #where the webserver will expect the index.html, this overrides the cmdline default
    output = 'www'
    #what do we serve use // for both
    http_shema = 'http://'
    #not shure if ill actually use this
    domain = 'moebel.facchin.at'
    #array of möbel in the sequence you want them to appear on index. name=directory name
    möbels=['testmöbel', 'schuhregal']
    #array of pages in the sequence you want them to appear. name = file.rst in pages 
    pages=['möbel', 'kontakt', 'über']
