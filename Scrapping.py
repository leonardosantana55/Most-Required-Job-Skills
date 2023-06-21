from bs4 import BeautifulSoup as bs
import requests


def scrap_linkedin(q):
    '''recebe uma string como argumento e faz scrapping na página https://www.linkedin.com/jobs/search'''

    response = requests.get(f'https://www.linkedin.com/jobs/search/?currentJobId=3640009990&f_TPR=r86400&geoId=106057199&keywords={q}&location=Brasil&originalSubdomain=br&start=0', verify=False)
    soup = bs(response.text, 'html.parser')
    print("reponse status code: ", response.status_code)

    list_of_links = []
    for link in soup.findAll(class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'):
        list_of_links.append(link.get('href'))
    print(len(list_of_links))