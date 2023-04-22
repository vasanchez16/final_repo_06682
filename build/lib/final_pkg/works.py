#!/usr/bin/env python
import time
import requests
import click
from collections.abc import Iterable
import base64
import matplotlib.pyplot as plt
class works:
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f'https://api.openalex.org/works/{oaid}')
        self.data = self.req.json()
        
    #######################################################################################################################
        
    def bibtex(self):
        import bibtexparser
        import datetime
        
        
        title = self.data["title"]
        author = self.data['authorships'][0]['author']['display_name']
        last_name = author.split(' ')[-1]
        journal = self.data['host_venue']['publisher']
        address = self.data['authorships'][0]['raw_affiliation_string']
        volume = self.data['biblio']['volume']
        issue = self.data['biblio']['issue']
        number = issue
        pages = str(self.data['biblio']['first_page']) + ' - ' + str(self.data['biblio']['last_page'])
        year = self.data['publication_year']
        url = self.data['doi']
        doi = url.split('doi.org/')[-1]
        now = datetime.datetime.now()
        
        bibtex = f'''@article{{{last_name}{year},
        author =	 {{{author}}},
        title =	 {{{title}}},
        journal =	 {{{journal}}},
        volume =	 {volume},
        number =	 {number},
        pages =	 {{{pages}}},
        year =	 {year},
        doi =		 {{{doi}}},
        url =		 {{{url}}},
        DATE_ADDED =	 {{{now}}},
        }}
        '''
        with open('bibtex.bib', 'w') as bibfile:
            bibfile.write(bibtex)
        with open('bibtex.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        # print(bibtex,bib_database.entries)
        print(bib_database.entries ,'\n\n\n', bibtex)
        
        #######################################################################################################################
    
    @property
    def ris(self):
        fields = []
        if self.data['type'] == 'journal-article':
            fields += ['TY  - JOUR']
        else:
            raise Exception(f"Unsupported type {self.data['type']}")
        
        for author in self.data['authorships']:
            fields += [f'AU  - {author["author"]["display_name"]}']
            
        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']
        
        if self.data['biblio']['issue']:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']
        
        
        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ['ER  -']
                
        ris = '\n'.join(fields)

        ris64 = base64.b64encode(ris.encode('utf-8')).decode('utf8')
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}" download="ris">Download RIS</a>'

        from IPython.display import HTML
        return HTML(uri)
    
    def ris2(self):
        fields = []
        if self.data['type'] == 'journal-article':
            fields += ['TY  - JOUR']
        else:
            raise Exception(f"Unsupported type {self.data['type']}")
        
        for author in self.data['authorships']:
            fields += [f'AU  - {author["author"]["display_name"]}']
            
        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']
        
        if self.data['biblio']['issue']:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']
        
        
        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ['ER  -']
                
        ris = '\n'.join(fields)

        ris64 = base64.b64encode(ris.encode('utf-8')).decode('utf8')
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}" download="ris">Download RIS</a>'

        from IPython.display import HTML

        return ris

    
@click.command(help='Print the output for the given doi.')
@click.option('--format', default='bibtex', help='Setting for the format of the output (bibtex or ris).')
@click.argument('query')
def main(query,format):
    if format == 'bibtex':
        w = works(query)
        a = w.bibtex()
        print(a)
    elif format == 'ris':
        w = works(query)
        a = w.ris2()
        print(a)
    
if __name__ == '__main__':
    main()

