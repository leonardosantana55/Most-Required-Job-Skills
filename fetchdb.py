#connect to the database and cehck if query is present to fecth the corresponding data
import psycopg2
import pandas as pd
import numpy as np
from _scrape import getJobsData
from psycopg2.extras import execute_values

credentials = "host=localhost port=5432 dbname=linkedin_scrapping user=adminleo password=fica, client_encoding=utf8"

def check_if_q_exists(q):
    # Tem que pesquisar sobre como armazenar esses dados de maneira segura
    conn = psycopg2.connect(credentials)
    cur = conn.cursor()
    cur.execute("SELECT q FROM main_table")
    records = [r[0] for r in cur.fetchall()]

    if q in records:
        print('q found in database')
        return True
    else:
        print('q not in database')
        return False

def count_descriptions_words(list_of_descriptions):

    unrepeated_list_of_prequisites = []
    for value in list_of_descriptions:
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
        
        unrepeated_list_of_prequisites.append(list(set(value)))

    stop_words = ['e','a', 'o', 'os', 'do', 'as', 'da', 'em', 'dos', 'se', 'no','com', 'na'\
            ,'para', 'ou', 'e a', 'é', '-', '/', 'de', 'um',' nos', 'que', 'das', 'por'\
            ,'como', '2', 'nos', 'off', 'e em', 'ao', 'com a', 'seu', 'são', 'etc', 'com o'\
            ,'esta', 'área', 'ano', 'dia', 'day','esta', 'nas', 'de', '–', 'à', 'x', 'ser', 'mas', 'sem', 'às', 'uma', ')', 'va', 'in', 'e/ou']

    contagem_de_termos = [[0,0]]
    
    for value in unrepeated_list_of_prequisites:
        for word in value:
            if word not in stop_words:
                if word not in np.array(contagem_de_termos)[:,0:1]:
                    if len(str(word)) > 1:
                        contagem_de_termos.append([word, list(np.concatenate(unrepeated_list_of_prequisites)).count(word)])

    df = pd.DataFrame(contagem_de_termos)
    df_result = df.sort_values(by=1, ascending=False).reset_index(drop=True).head(100)
    return df_result

def store_scrape_data(data):
    data = list(zip(*data))
    conn = psycopg2.connect(credentials)
    cur = conn.cursor()
    query = "INSERT INTO main_table (link, title, description, q)\
                VALUES %s \
                ON CONFLICT (link) DO NOTHING \
                RETURNING link;"    
    execute_values(cur, query, data)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    print(result)

def query_descriptions(q):
    conn = psycopg2.connect(credentials)
    cur = conn.cursor()
    cur.execute("SELECT description \
                FROM main_table \
                WHERE q = %s", (q,))
    records = cur.fetchall()
    cur.close()
    conn.close()
    return records

def run(q):
    if check_if_q_exists(q):
        list_of_descriptions = query_descriptions(q)        
    else:
        data = getJobsData(q)
        data.get_descriptions()
        data = data.scrape_result
        print(data)
        store_scrape_data(data)
        list_of_descriptions = query_descriptions(q)

    result = count_descriptions_words(list_of_descriptions)
    print(result)    
    return result

 

if __name__ == '__main__':
    print('Informe uma profissão: ')
    q = input()
    run(q)

