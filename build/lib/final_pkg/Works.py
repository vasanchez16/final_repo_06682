#!/usr/bin/env python
"This is the main package function for use."
import datetime
import base64
import requests
import click
from IPython.display import display, HTML

class Works:
    "The class object create with DOI key."
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f'https://api.openalex.org/works/{oaid}')
        self.data = self.req.json()

    @property
    def bibtex(self):
        "Bibtex function."

        title = self.data["title"]
        author = self.data['authorships'][0]['author']['display_name']
        last_name = author.split(' ')[-1]
        journal = self.data['host_venue']['publisher']
        volume = self.data['biblio']['volume']
        issue = self.data['biblio']['issue']
        number = issue
        pages = str(
            self.data['biblio']['first_page']) + ' - ' + str(self.data['biblio']['last_page']
                                                                    )
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
        return bibtex

    @property
    def ris(self):
        "RIS function."
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
        uri = (
            f'<pre>{ris}<pre><br><a href="data:text/plain;base64'
            +
            f',{ris64}" download="ris">Download RIS</a>'
              )
        display(HTML(uri))
        return ris

@click.command(help='Print the output for the given doi.')
@click.option(
    '--works_format', default='bibtex', help='Setting for the format of the output (bibtex or ris).'
             )
@click.argument('query')
def main(query,works_format):
    "My command line utility."
    if works_format == 'bibtex':
        works_example = Works(query)
        print(works_example.bibtex)
        # print(a)
    elif works_format == 'ris':
        works_example = Works(query)
        print(works_example.ris)

if __name__ == '__main__':
    main()
