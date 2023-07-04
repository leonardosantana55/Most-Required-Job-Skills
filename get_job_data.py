from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import warnings
warnings.filterwarnings('ignore')


def get_job_data(q):

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
    #encontrei um problema ao utilizar o link atual. Utilizar este abaixo. provavelmente vai precisar de nova lógica para captar os links
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?f_TPR=r2592000&geoId=106057199&keywords=engenheiro%20de%20software&location=Brasil&originalSubdomain=br&start=75
    for key in start_key_list:
        response = requests.get(f'https://www.linkedin.com/jobs/search/?currentJobId=3640009990&f_TPR=r2592000&geoId=106057199&keywords={q}&location=Brasil&originalSubdomain=br&start={key}', verify=False)
        soup = bs(response.text, 'html.parser')
        items = soup.findAll(class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
        
        
        #verifica se o título do item corresponde a pesquisa
        for item in items:
            job_title = str(item.span.text).strip()
            s = SequenceMatcher(None, q, job_title)
            if s.ratio() > 0.1:
                links[job_title] = item.get('href')
            
    



    list_of_prequisites = {}
    for link in list(links.values()):
        response = requests.get(link, verify=False)
        soup = bs(response.text, 'html.parser')
        try:
            list_of_prequisites[link] = soup.find(class_='description__text description__text--rich').find_all('li')
        except(AttributeError):
            pass

    unrepeated_list_of_prequisites = {}
    for key, value in list_of_prequisites.items():
        value = str(value).replace('<li>',' ').replace('</li>',' ')\
        .replace('</li>'," ")\
        .replace('<li>'," ")\
        .replace('['," ")\
        .replace(']'," ")\
        .replace('<br/>'," ")\
        .replace('<br>'," ")\
        .replace('</span>'," ")\
        .replace('<span>'," ")\
        .replace('.'," ")\
        .replace(','," ")\
        .replace(';'," ")\
        .replace(')'," ")\
        .replace('('," ")\
        .replace('/'," ")\
        .lower()\
        .split()
        
        unrepeated_list_of_prequisites[key] = list(set(value))

    stop_words = ['e','a', 'o', 'os', 'do', 'as', 'da', 'em', 'dos', 'se', 'no','com', 'na'\
            ,'para', 'ou', 'e a', 'é', '-', '/', 'de', 'um',' nos', 'que', 'das', 'por'\
            ,'como', '2', 'nos', 'off', 'e em', 'ao', 'com a', 'seu', 'são', 'etc', 'com o'\
            ,'esta', 'área', 'ano', 'dia', 'day','esta', 'nas', 'de', '–', 'à', 'x', 'ser', 'mas', 'sem', 'às', 'uma', ')', 'va', 'in', 'e/ou']


    contagem_de_termos = [[0,0]]
    
    for value in unrepeated_list_of_prequisites.values():
        for word in value:
            if word not in stop_words:
                if word not in np.array(contagem_de_termos)[:,0:1]:
                    if len(str(word)) > 1:
                        contagem_de_termos.append([word, list(np.concatenate(list(unrepeated_list_of_prequisites.values()))).count(word)])

    df = pd.DataFrame(contagem_de_termos)
    df_result = df.sort_values(by=1, ascending=False).reset_index(drop=True).head(100)

    return df_result, links, list_of_prequisites, q

if __name__ == '__main__':
    get_job_data()
