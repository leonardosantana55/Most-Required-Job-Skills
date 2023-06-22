from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from difflib import SequenceMatcher
import warnings
warnings.filterwarnings('ignore')


def get_jobs_links(q):

    #faz a primeira pesquisa para captar o número de páginas resultantes da pesquisa
    response = requests.get(f'https://www.linkedin.com/jobs/search/?currentJobId=3640009990&f_TPR=r2592000&geoId=106057199&keywords={q}&location=Brasil&originalSubdomain=br', verify=False)
    soup = bs(response.text, 'html.parser')

    # recebe o número de resultados da pesquisa e cria uma lista com os parametros necessários para acessar todas as páginas.
    try:
        num_of_results = soup.find(class_ = 'results-context-header__job-count').text
        num_of_pages = int(int(num_of_results)/25)
        range_num_of_pages = list(range(0,num_of_pages))
        start_key_list = [x *25 for x in range_num_of_pages]
        start_key_list
    except ValueError:
        start_key_list = [0,25,50,75,100,125,150,175,200,225]
    
    links = {}
    #acessa cada uma das páginas do resultado da pesquisa
    for key in start_key_list:
        response = requests.get(f'https://www.linkedin.com/jobs/search/?currentJobId=3640009990&f_TPR=r2592000&geoId=106057199&keywords={q}&location=Brasil&originalSubdomain=br&start={key}', verify=False)
        soup = bs(response.text, 'html.parser')
        items = soup.findAll(class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
        
        
        #verifica se o título do item corresponde a pesquisa
        for item in items:
            job_title = str(item.span.text).strip()
            s = SequenceMatcher(None, q, job_title)
            if s.ratio() > 0.6:
                links[job_title] = item.get('href')
            
    return links 