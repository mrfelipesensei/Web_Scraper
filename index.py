import requests
from bs4 import BeautifulSoup
import csv

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


def salvar_csv(noticias):
    with open("noticias_g1.csv","w",newline="",encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["titulo","link","palavras_chave"])
        escritor.writeheader()
        escritor.writerows(noticias)


def buscar_noticias(noticias,palavra):
    resultados = [n for n in noticias if palavra.lower() in  n["titulo"].lower() or palavra.lower() in n["palavras_chave"].lower()]

    if not resultados:
        print(f"Nenhuma notíficia encontrada com '{palavra}'.")
    else:
        print(f"\n Notícias encontradas para '{palavra}':\n")
        for i, noticia in enumerate(resultados,start=1):
            print(f"{i}. {noticia['titulo']}")
            print(f"{noticia['link']}")
            print(f"Palavras-chave: {noticia['palavras_chave']}\n")


