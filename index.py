import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

#Configurações da Página
st.set_page_config(page_title="G1 News Scraper", page_icon="📰")


URL = "https://g1.globo.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#-- Função de Coleta (Lógica Backend) --
@st.cache_data(ttl=600) #Faz cache dos dados por 10 min para não sobrecarregar o site

def coletar_noticias():
    try:
        resposta = requests.get(URL, headers=HEADERS, timeout=10)
        resposta.raise_for_status()
        sopa = BeautifulSoup(resposta.text, "html.parser")
        noticias = []
        elementos = sopa.find_all("a", class_="feed-post-link")

        for noticia in elementos[:20]: #Coletamos até 20 manchetes
            titulo = noticia.get_text(strip=True)
            link = noticia.get("href", "Sem link disponível")
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

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar o G1: {e}")
        return []

#-- Interface (Frontend com Streamlit) --
st.title("📰 G1 - Útimas Notícias")
st.markdown("Interface interavia de monitoramento de manchetes em tempo real.")

if st.button('🔄 Atualizar Notícias'):
    st.cache_data.clear()

dados = coletar_noticias()

if dados:
    #DataFrame do Pandas para facilitar visualização e busca
    df = pd.DataFrame(dados)

    #Barra de Busca
    busca = st.text_input("🔍 Buscar por palavra-chave nas manchetes:", "")

    if busca:
        #Filta o DataFrame conforme o user digita
        df_filtrado = df[df['titulo'].str.contains(busca, case=False) | df['resumo'].str.contains(busca, case=False)]
    else:
        df_filtrado = df
    
    #Exibição dos Resultados
    st.write(f"Exibindo **{len(df_filtrado)}** notícias.")

    #Cards visuais para cada notícia
    for index, row in df_filtrado.iterrows():
        with st.container():
            st.subheader(row['titulo'])
            st.write(row['resumo'])
            st.link_button("Ler notícia completa", row['link'])
            st.divider()
    
    #Opção de Download do CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Baixar tudo como CSV",
        data=csv_data,
        file_name='noticias_g1.csv',
        mime='text/csv'
    )
