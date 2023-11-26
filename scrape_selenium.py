from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pyspark import SparkContext
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import requests
import os

def scrape_stock_list(url="https://www.infomoney.com.br/cotacoes/empresas-b3/"):
    """
    Retrieves stock information from the given URL.

    Parameters:
        url (str, optional): The URL to fetch stock information from. Defaults to
                            "https://www.infomoney.com.br/cotacoes/empresas-b3/".

    Returns:
        dict: A dictionary containing stock information with keys 'stock', 'value','type', and 'link'.

    The function fetches stock information from the specified webpage, including
    stock names, values, types, and links. It returns the data in a dictionary format.

    Example:
        stock_data = get_stock_list()
        print(stock_data)
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    stocks = []
    values = []
    links = []
    types = []

    tables = soup.find_all('table')

    # Iterate through each table
    for table in tables:
        # Find all rows (tr) in the table
        rows = table.find_all('tr')

        # Iterate through each row
        for row in rows:
            # Find the <td class='higher'> containing the name of the stock
            stock_name_td = row.find('td', class_='higher')
            if stock_name_td:
                stock_name = stock_name_td.text.strip()

                # Find all <td class='strong'> containing <a> tags with links and values
                strong_tds = row.find_all('td', class_='strong')
                for strong_td in strong_tds:
                    link_a = strong_td.find('a')
                    if link_a:
                        link = link_a['href']
                        value = link_a.text.strip()

                        # Extract the 'type' from the link
                        type_start = link.find('/b3/') + 4
                        type_end = link.find('/', type_start)
                        asset_type = link[type_start:type_end]

                        # Append data to lists
                        stocks.append(stock_name)
                        values.append(value)
                        links.append(link)
                        types.append(asset_type)

    # Create a DataFrame
    return {'EMPRESA': stocks, 'ATIVO': values, 'TIPO': types, 'LINK': links}

def click_on_element(driver, method, path, wait_time=15):
    '''
    Clica em um elemento na página da web.

    Args:
        driver (WebDriver): O driver do navegador web.
        method (By): O método de localização do elemento (por exemplo, By.ID, By.XPATH).
        path (str): O caminho para localizar o elemento.
        wait_time (int, opcional): Tempo máximo de espera em segundos (padrão é 15).

    Returns:
        bool: Retorna True se o clique for bem-sucedido, False caso contrário.
    '''
    try:
        WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((method, path))).click()
        return True
    except:
        return False

def get_stock_data(url, tipo, ativo):
    '''
    Obtém dados de uma página da web sobre ações.

    Args:
        url (str): URL da página da web contendo os dados das ações.
        tipo (str): Tipo de ação (por exemplo, "Ação" ou "Opção").
        ativo (str): Nome do ativo.

    Returns:
        dict: Um dicionário contendo os dados das ações, incluindo:
            - 'ATIVO': Lista do nome do ativo.
            - 'TIPO': Lista do tipo de ação.
            - 'DATA': Lista de datas.
            - 'ABERTURA': Lista de preços de abertura.
            - 'FECHAMENTO': Lista de preços de fechamento.
            - 'VARIACAO': Lista de variações.
            - 'MINIMO': Lista de preços mínimos.
            - 'MAXIMO': Lista de preços máximos.
            - 'VOLUME': Lista de volumes.
            Os dados são organizados em listas correspondentes a cada categoria.
            Retorna um dicionário vazio se ocorrerem problemas durante a obtenção dos dados.
    '''
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=chrome_options)
    # driver.maximize_window()
    driver.get(url)
    _ativo = []
    _tipo = []
    data = []
    abertura = []
    fechamento = []
    variacao = []
    minimo = []
    maximo = []
    volume = []
    # driver.maximize_window()

    #esperar entre 2 e 10 segundos para a pagina carregar
    time.sleep(random.uniform(2, 5))

    # print('Switching to iFrame')
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))

    click_on_element(driver=driver, method=By.XPATH, path='//*[@id="fechar"]')
    # print('Click on close button')

    # print('Switching to the main frame')
    driver.switch_to.default_content()

    driver.implicitly_wait(3)

    date_min_state = click_on_element(driver=driver, method=By.XPATH, path='//*[@id="dateMin"]')
    if date_min_state:
        datemin = driver.find_element(by=By.XPATH, value='//*[@id="dateMin"]')
        datemin.send_keys('01/01/2021')
    else:
        driver.quit()
        return {
                'ATIVO': [],
                'TIPO': [],
                'DATA': [], 
                'ABERTURA': [], 
                'FECHAMENTO': [], 
                'VARIACAO': [],
                'MINIMO': [], 
                'MAXIMO': [], 
                'VOLUME': [], 
            }

    today = datetime.now().strftime("%d/%m/%Y").strip()
    date_max_state = click_on_element(driver=driver, method=By.XPATH, path='//*[@id="dateMax"]')
    if date_max_state:
        datemax = driver.find_element(by=By.XPATH, value='//*[@id="dateMax"]')
        datemax.send_keys(today)
    else:
        driver.quit()
        return {
                'ATIVO': [],
                'TIPO': [],
                'DATA': [], 
                'ABERTURA': [], 
                'FECHAMENTO': [], 
                'VARIACAO': [],
                'MINIMO': [], 
                'MAXIMO': [], 
                'VOLUME': [], 
            }
    
    see_history_state = click_on_element(driver=driver, method=By.XPATH, path='//*[@id="see_all_quotes_history"]')
    if see_history_state:
        # print('Click on see data')
        pass
    else:
        driver.quit()
        return {
                'ATIVO': [],
                'TIPO': [],
                'DATA': [], 
                'ABERTURA': [], 
                'FECHAMENTO': [], 
                'VARIACAO': [],
                'MINIMO': [], 
                'MAXIMO': [], 
                'VOLUME': [], 
            }
    # hold for three seconds fo the page to load
    # time.sleep(2)
    try:
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,  '//*[@id="img_load_more_quotes_history"]')))
    except:
        # print('Loading not completed')
        driver.quit()
        return {
                'ATIVO': [],
                'TIPO': [],
                'DATA': [], 
                'ABERTURA': [], 
                'FECHAMENTO': [], 
                'VARIACAO': [],
                'MINIMO': [], 
                'MAXIMO': [], 
                'VOLUME': [], 
            }

    time.sleep(5)
    #obter o HTML da pagina
    html = driver.page_source

    #Fechar driver do chrome
    driver.quit()

    #Usar o BS4 para analisar o meu html da url
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrar todas as linhas <tr>
    rows = soup.find('table').find_all('tr')

    # Iterar sobre as linhas e extrair os valores
    for row in rows[1:]:
        _ativo.append(ativo)
        _tipo.append(tipo)
        for index, row_value in enumerate(row):
            # row_value.text.
            if index == 0:
                data.append(row_value.text)
            elif index == 1:
                abertura.append(row_value.text)
            elif index == 2:
                fechamento.append(row_value.text)
            elif index == 3:
                variacao.append(row_value.text)
            elif index == 4:
                minimo.append(row_value.text)
            elif index == 5:
                maximo.append(row_value.text)
            elif index == 6:
                volume.append(row_value.text)

    # Create a DataFrame
    return  {
                'ATIVO': _ativo,
                'TIPO': _tipo,
                'DATA': data, 
                'ABERTURA': abertura, 
                'FECHAMENTO': fechamento, 
                'VARIACAO': variacao,
                'MINIMO': minimo, 
                'MAXIMO': maximo,
                'VOLUME': volume, 
            }


# Definindo a função de mapeamento paa converter cada valor de fechamento
def mapper(value):
    return(value, 1)

# Definindo a função de redução para domar os valores de fechamento
def reducer(a,b):
    return a + b

def calculation(df_final: pd.DataFrame):
    '''
    Realiza o processamento dos dados em df_final, calcula médias e salva em um arquivo Excel.

    Args:
        df_final (DataFrame): DataFrame contendo dados a serem processados.

    Returns:
        None
    '''
    # Calculando a media
    print("MÉDIA")
    media_fechamento = df_final.groupby('ATIVO')['FECHAMENTO'].mean()
    media_fechamento = media_fechamento.rename('MÉDIA_POR_ATIVO')

    # Converter a coluna 'DATA' para o tipo datetime
    df_final['DATA'] = pd.to_datetime(df_final['DATA'], format='%d/%m/%Y')

    # Criar uma nova coluna 'MÊS' para extrair o mês da data
    df_final['MÊS'] = df_final['DATA'].dt.month
    df_final['ANO'] = df_final['DATA'].dt.year

    # Calcular a média do fechamento por mês, ano e ativo
    media_fechamento_por_mes = df_final.groupby(['ATIVO', 'ANO', 'MÊS'])['FECHAMENTO'].mean()
    media_fechamento_por_mes = media_fechamento_por_mes.rename('MÉDIA_FECHAMENTO_POR_MÊS')

    # Arredondamento de média
    print("ROUND 2")
    media_fechamento = media_fechamento.round(2)
    media_fechamento_por_mes = media_fechamento_por_mes.round(2)

    print("TRY TO MERGE")
    df_final['DATA'] = df_final['DATA'].dt.strftime('%d/%m/%Y')
    # Adicionando a media ao df_final com uma nova colunas
    df_final = df_final.merge(media_fechamento, on='ATIVO')
    # Merge dos DataFrames usando múltiplas colunas como critério
    df_final = df_final.merge(media_fechamento_por_mes, on=['ATIVO', 'MÊS', 'ANO'])

    df_final.drop(['ANO', 'MÊS'], axis=1, inplace=True)

    print("MERGED")
    # Criando um escritor no excel
    writer = pd.ExcelWriter('dados_com_spark.xlsx', engine='xlsxwriter')

    # Gravando o df_final na guia 'Analise_PYSPARK'
    df_final.to_excel(writer, sheet_name='Analise_PYSPARK', index=False)
    print("ARQUIVO SALVO")
    # Salvando
    writer.close()

if __name__ == '__main__':

    df_stocks = pd.DataFrame(scrape_stock_list())
    df_stocks.to_csv('output/stocks_list.csv', sep=';', index=False)
    df_stocks = df_stocks[~df_stocks['ATIVO'].str.endswith('F')].copy()

    header_df = ['ATIVO', 'TIPO', 'DATA', 'ABERTURA', 'FECHAMENTO', 'VARIACAO', 'MINIMO', 'MAXIMO', 'VOLUME']
    df_resultados = pd.DataFrame(columns=header_df)
    df_fail = pd.DataFrame(columns=['ATIVO', 'TIPO', 'LINK'])

    num_of_assets = df_stocks.shape[0]
    num_loaded = 0
    num_failed = 0
    couting = 0

    ativos = ['BHIA3','AERI3','ICBR3'] #'DOTZ3','GOLL3', 'ARML3', 'MLAS3', 'CBAV3', 'TTEN3', 'BRBI11', 'NINJ3', 'ATEA3', 'MODL4', 'MODL11', 'MODL3', 'VITT3', 'KRSA3']
    for index, row in df_stocks[df_stocks['ATIVO'].isin(ativos)].iterrows():
        link = row['LINK']
        tipo = row['TIPO']
        ativo = row['ATIVO']
        print(f'########  Loading: {ativo} ########')
        for i in range(2):
            # Chamar o método de busca
            resultado = get_stock_data(f"{link}historico/", tipo, ativo)
            if len(resultado['ATIVO']) == 0:
                if i == 1:
                    print(f'########  Add {ativo} to df_fail')
                    df_fail = pd.concat([df_fail, pd.DataFrame.from_dict({'ATIVO':[ativo], 'TIPO':[tipo], 'LINK':[link]})], ignore_index=True)
                    num_failed = num_failed + 1  
            else:
                df_resultados = pd.concat([df_resultados, pd.DataFrame.from_dict(resultado)], ignore_index=True)
                print(f'########  {ativo} loaded!')
                num_loaded = num_loaded + 1          
                break
        couting = couting + 1
        print(f'########  Done: {couting}/{num_of_assets} ########')
        print(f'########  Loaded: {num_loaded}/{num_of_assets} ########')
        print(f'########  Failed: {num_failed}/{num_of_assets} ########\n')

    colunas_numericas = ['ABERTURA', 'FECHAMENTO', 'VARIACAO', 'MINIMO', 'MAXIMO']
    df_resultados[colunas_numericas] = df_resultados[colunas_numericas].replace(',', '.', regex=True).apply(pd.to_numeric, errors='coerce')

    calculation(df_resultados)