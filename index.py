import requests
from bs4 import BeautifulSoup

#URL da página do G1
URL = "https://g1.globo.com/"

def coletar_noticias():
    '''Coleta títulos e links das notícias do G1'''
    resposta = requests.get(URL)

    if resposta.status_code != 200:
        print("Erro ao acessar o site!")
        return
    
    sopa = BeautifulSoup(resposta.text, "html.parser")

    #Seleciona as manchetes principais
    noticias = sopa.find_all("a",class_="feed-post-link")

    for i, noticia in enumerate(noticias[:10],start=1):
        titulo = noticia.get_text(strip=True)
        link = noticia["href"]
        print(f"{i}.{titulo}")
        print(f"{link}\n")

#Executar o scraper
coletar_noticias()