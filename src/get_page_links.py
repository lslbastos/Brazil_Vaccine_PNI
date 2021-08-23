#### Scrapping source URL with CSV links (OpenDataSUS)
## Code based/adapted from 'https://pyshark.com/extract-links-from-a-web-page-using-python/' and 'https://www.geeksforgeeks.org/extract-all-the-urls-from-the-webpage-using-python/'


## Scrapping OpendataSUS webpages
import requests
from bs4 import BeautifulSoup
  
def get_page_links():

    # Targe URL    
    url='https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/ef3bd0b8-b605-474b-9ae5-c97390c197a8'

    # Resqueting page data with GET 
    url_req = requests.get(url)
    
    # Parsing page request into HTML data
    html_soup = BeautifulSoup(url_req.text, 'html.parser')

    # Creating links and state (labels) objects
    links=[]
    states=[]

    # Obtaining CSV URLs for each State in the page (link may be updated)
    for link in html_soup.find_all('a'):
        if (('Completos' in link.text) or ('Dicionário' in link.text)):
            continue
        elif ('Dados' in link.text):
                links.append(link.get('href'))
                states.append(link.text[-2:])

    ## Merge State and Link info into a dictionary
    state_links = dict(zip(states, links))

    return state_links
    