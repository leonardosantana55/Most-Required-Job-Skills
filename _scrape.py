from bs4 import BeautifulSoup as bs
import requests
from difflib import SequenceMatcher
import warnings
warnings.filterwarnings('ignore')


class getJobsData:
    num_of_pages = 0
    title_n_links = {}
    link_n_list = {}
    scrape_result = [] #link, title, description, q

    def __init__(self, q):
        self.q = q
        
    def get_n_keys(self):
        link = f'https://www.linkedin.com/jobs/search?keywords={self.q}&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        response = requests.get(link, verify=False)
        soup = bs(response.text, 'html.parser')
        num_of_results = str(soup.find(class_ = 'results-context-header__job-count').text).replace(',','').replace('+','')
        num_of_pages = int(int(num_of_results)/25)
        range_num_of_pages = list(range(0,num_of_pages))
        key_list = [x *25 for x in range_num_of_pages]
        self.num_of_pages = num_of_pages
        return key_list

    def get_title_n_links(self):    
        key_list = self.get_n_keys()
        title_n_links = {}
        titles_list =[]
        links_list = []
        for key in key_list:
            link = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?f_TPR=r2592000&geoId=106057199&keywords={self.q}&location=Brasil&originalSubdomain=br&start={key}'
            response = requests.get(link, verify=False)
            soup = bs(response.text, 'html.parser')
            items = soup.findAll(class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
            for item in items:
                job_title = str(item.span.text).strip()
                s = SequenceMatcher(None, self.q, job_title)
                if s.ratio() > 0.6:
                    title_n_links[job_title] = item.get('href')
                    titles_list.append(job_title)
                    links_list.append(item.get('href'))
        self.scrape_result.append(links_list)
        self.scrape_result.append(titles_list)
        return title_n_links

    def get_descriptions(self):
        title_n_links = self.get_title_n_links()
        link_n_list = {}
        q_list = []
        description_list = []
        for title, link in title_n_links.items():
            response = requests.get(link, verify=False)
            soup = bs(response.text, 'html.parser')
            try:
                link_n_list[link] = [title, (soup.find(class_='description__text description__text--rich').find_all('li'))]
                q_list.append(self.q)
                description_list.append(str(soup.find(class_='description__text description__text--rich').find_all('li')))
            except(AttributeError):
                pass
        self.scrape_result.append(description_list)
        self.scrape_result.append(q_list)
        return link_n_list
    

if __name__ == "__main__":
    q = input()
    scrape = getJobsData(q)
    scrape.get_descriptions()
    print(scrape.scrape_result)
