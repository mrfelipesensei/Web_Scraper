import requests
from bs4 import BeautifulSoup

#URL da página do G1
URL = "https://g1.globo.com/"

def coletar_noticias():
    '''Coleta títulos e links das notícias do G1'''
    resposta = requests.get(URL)

    if resposta.status_code != 200:
        print("Erro ao acessar o site!")
        return []
    
    sopa = BeautifulSoup(resposta.text, "html.parser")

    noticias = []

    #Seleciona as manchetes principais
    elementos = sopa.find_all("a", class_="feed-post-link")

    for noticia in elementos[:20]: #Coletamos até 20 manchetes
        titulo = noticia.get_text(strip=True)
        link = noticia["href"]

        #Tenta extrair palavras-chave (se disponíveis)
        palavras_chave = noticia.find_parent().get("data-track-keywords","N/A")

        noticias.append(
            {
                "titulo": titulo,
                "link" : link,
                "palavras_chave" : palavras_chave
            }
        )

    return noticias