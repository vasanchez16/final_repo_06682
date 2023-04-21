import time
import requests
import click
from collections.abc import Iterable
class works:
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f'https://api.openalex.org/works/{oaid}')
        self.data = self.req.json()
        
    def __str__(self):
        return 'str'
        
    def __repr__(self):
        _authors = [au['author']['display_name'] for au in self.data['authorships']]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ', '.join(_authors[0:-1]) + ' and' + _authors[-1]
            
        title = self.data['title']
        
        journal = self.data['host_venue']['display_name']
        volume = self.data['biblio']['volume']
        
        issue = self.data['biblio']['issue']
        if issue is None:
            issue = ', '
        else:
            issue = ', ' + issue

        pages = '-'.join([self.data['biblio'].get('first_page', '') or '',
                          self.data['biblio'].get('last_page', '') or ''])
        year = self.data['publication_year']
        citedby = self.data['cited_by_count']
        
        oa = self.data['id']
        s = f'{authors}, {title}, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. {oa}'
        return s
    
    def _repr_markdown_(self):
        _authors = [f'[{au["author"]["display_name"]}]({au["author"]["id"]})' for au in self.data['authorships']]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ', '.join(_authors[0:-1]) + ' and ' + _authors[-1]
            
        title = self.data['title']
        
        journal = f"[{self.data['host_venue']['display_name']}]({self.data['host_venue']['id']})"
        volume = self.data['biblio']['volume']
        
        issue = self.data['biblio']['issue']
        if issue is None:
            issue = ', '
        else:
            issue = ', ' + issue
            
        pages = '-'.join([self.data['biblio'].get('first_page', '') or '',
                          self.data['biblio'].get('last_page', '') or ''])
        year = self.data['publication_year']
        citedby = self.data['cited_by_count']
        
        oa = self.data['id']
        
        # Citation counts by year
        years = [e['year'] for e in self.data['counts_by_year']]
        counts = [e['cited_by_count'] for e in self.data['counts_by_year']]
    
        fig, ax = plt.subplots()
        ax.bar(years, counts)
        ax.set_xlabel('year')
        ax.set_ylabel('citation count')
        data = print_figure(fig, 'png') # save figure in string
        plt.close(fig)
        
        b64 = base64.b64encode(data).decode('utf8')
        citefig = (f'![img](data:image/png;base64,{b64})')
        
        s = f'{authors}, *{title}*, **{journal}**, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. [Open Alex]({oa})'
        
        s += '<br>' + citefig
        return s
    #######################################################################################################################
    def citing_works(self):
        cited_by_list = []
        
        url2 = self.data['cited_by_api_url']
        data2 = requests.get(url2).json()
        data2 = data2['results']
        
        for el in data2:
            
            new_req_list = el['title'] + ' ' + str(el['publication_year'])
            cited_by_list.append(new_req_list)
            
        print('\n'.join(cited_by_list)) 
        
    def references(self):
        ref = []
        ID_list = [ID[21:] for ID in self.data['referenced_works']]
        test_ind = 0
        for work_id in ID_list:
            new_url = 'https://api.openalex.org/works/' + work_id
            time.sleep(1.0)
            try:
                new_req = requests.get(new_url).json()
            except:
                print('new req failed on ind:' + str(test_ind))
        
            new_req_list = new_req['title'] + ' ' + str(new_req['publication_year'])
            ref.append(new_req_list)
            
            test_ind += 1
        print('\n'.join(ref))
        
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
    
    def related_works(self):
        rworks = []
        for rw_url in self.data['related_works']:
            rw = Works(rw_url)
            rworks += [rw]
            time.sleep(0.101)
        return rworks
    
    

