#pip install selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def ler_tabelas(url):
    # INICIALIZAR O DRIVER DO NAVEGADOR
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    #FAZER O DRIVER IR PARA A URL ESPECIFICADA
    driver.get(url)

    #esperar 10 segundos para a pagina carregar
    time.sleep(5)

    #obter o HTML da pagina
    html = driver.page_source

    #Fechar driver do chrome
    driver.quit()

    #Usar o BS4 para analisar o meu html da url
    soup = BeautifulSoup(html, 'html.parser')

    #Encontrar todas as tabelas da pagina
    tables = soup.find_all('table')

    #converter cada tabela em um Dataframe do PANDAS e analisar os Dataframes em uma lista
    dfs = [pd.read_html(str(table))[0] for table in tables]

    return dfs

url = "https://www.infomoney.com.br/cotacoes/empresas-b3/"

tabelas = ler_tabelas(url)

# if tabelas:
#     #obter o primeiro dataframe da lista de tabelas
#     df = tabelas[0]
#     df = df[df['Ativos'].isna() == False]
#     #para imprimir do indice 0 dessa url
#     # print(df)
    
#     #obter a coluna codigo desse df
#     codigos = df['Ativos'].tolist()
#     #imprimir todos os codigos em sequencia
#     # print(codigos)
    
#     # #CRIAR NOVO CODIGO PARA SER USADO NO PROXIMO PASSO
#     novos_codigos = [f"{codigo[:-1].lower()}-{codigo.lower()}" for codigo in codigos]
#     print(novos_codigos)
#     print(len(novos_codigos))

#     novos_codigos2 = [f"{codigo[:-1].lower()}-{codigo.lower()}" for codigo in codigos if len(codigo[:-1]) > 4]
#     print('-----------------------------------------------')
#     print(novos_codigos2)
#     print(len(novos_codigos2))
 
# else:
#     #informar erro ou que não foi encontraada nenhuma tabela
#     print("Não foi encontrada nenhuma tabela ou coluna")

url_historico = "https://www.infomoney.com.br/cotacoes/b3/bdr/cloudflare-n2et34/historico/"

tabelas1 = ler_tabelas(url_historico)

if tabelas1:
    #obter o primeiro dataframe da lista de tabelas
    df = tabelas1[0]
    datas = df['DATA'].tolist()
    valor_fechamento = df['FECHAMENTO'].tolist()

    # print(datas)
    # print('----------------------------')
    # print(valor_fechamento)

    #Converter a coluna de data para o tipo datetime
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')

    #filtrar as linhas que correspondem ao mes de Outubro
    df_outubro = df[df['DATA'].dt.month == 10]

    #Obter as colunas de data e valores de fechamento com base no filtro de data aplicado
    df_outubro = df_outubro[['DATA','FECHAMENTO']]
    print(df_outubro)

else:
    #informar erro ou que não foi encontraada nenhuma tabela
    print("Não foi encontrada nenhuma tabela ou coluna")