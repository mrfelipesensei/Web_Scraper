import requests
from bs4 import BeautifulSoup
import csv
import logging

#Configuração básica de logs para substituir o 'print' nos erros
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

#URL da página do G1
URL = "https://g1.globo.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def coletar_noticias():
    try:
        resposta = requests.get(URL, headers=HEADERS, timeout=10)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar o G1: {e}")
        return []

    sopa = BeautifulSoup(resposta.text, "html.parser")
    noticias = []
    #Seleciona as manchetes principais
    elementos = sopa.find_all("a", class_="feed-post-link")

    for noticia in elementos[:20]: #Coletamos até 20 manchetes
        titulo = noticia.get_text(strip=True)
        link = noticia["href"]

        #Melhoria na busca por metadados - pega o resumo da notícia se houver
        parent = noticia.find_parent("div", class_="feed-post-body")
        resumo = parent.find("div", class_="feed-post-body-resumo") if parent else None
        resumo_text = resumo.get_text(strip=True) if resumo else "Sem resumo disponível"


        noticias.append(
            {
                "titulo": titulo,
                "link" : link,
                "resumo" : resumo_text
            }
        )

    return noticias


def salvar_csv(noticias, nome_arquivo="noticias_g1.csv"):
    if not noticias:
        return
    
    try:
        keys = noticias[0].keys()
        with open(nome_arquivo,"w",newline="",encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=["titulo","link","resumo"])
            escritor.writeheader()
            escritor.writerows(noticias)
        logging.info(f"Dados salvos com sucesso em {nome_arquivo}")
    except IOError as e:
        logging.error(f"Erro ao salvar arquivo: {e}")




def buscar_noticias(noticias,palavra):
    resultados = [
        n for n in noticias
        if palavra.lower() in  n["titulo"].lower() or palavra.lower() in n["resumo"].lower()
    ]

    if not resultados:
        print(f"Nenhuma notíficia encontrada com '{palavra}'.")
    else:
        print(f"\n Notícias encontradas para '{palavra}':\n")
        for i, noticia in enumerate(resultados,start=1):
            print(f"{i}. {noticia['titulo']}")
            print(f"{noticia['link']}")
            print(f"Resumo: {noticia['resumo']}\n")


#Coleta notícias
noticias_coletadas = coletar_noticias()

#Salva no CSV
salvar_csv(noticias_coletadas)

#Permite busca por palavra-chave
while True:
    palavra_chave = input("\nDigite uma palavra-chave para buscar (ou 'sair' para finalizar): ").strip()

    if palavra_chave.lower() == "sair":
        break

    buscar_noticias(noticias_coletadas,palavra_chave)