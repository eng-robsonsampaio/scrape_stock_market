# README: Web Scraping e Classificação de Ativos - Solução em Python

---

### Descrição

Este projeto consiste em uma solução de web scraping para coletar informações sobre ações, Fundos de Investimento Imobiliário (FIIS) e Brazilian Depositary Receipts (BDRs). A solução realiza a classificação desses ativos, calcula médias relevantes e utiliza o paradigma **MapReduce** para processamento eficiente dos dados.

### Requisitos

- **Python 3.x** instalado
- Bibliotecas necessárias (instaláveis via `pip install`):
  - `beautifulsoup4` para parsing HTML
  - `requests` para fazer requisições HTTP
  - Outras bibliotecas específicas do projeto

### Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
  
# Script de Web Scraping e Análise de Dados de Ações

Este script em Python realiza web scraping de informações de ações de uma fonte específica e realiza análise de dados, incluindo o cálculo de médias e a geração de um arquivo Excel com os resultados.

## Funcionalidades Principais

### `scrape_stock_list`

Esta função utiliza a biblioteca BeautifulSoup para extrair informações sobre ações de uma página web específica. Retorna um dicionário contendo dados como nome da empresa, tipo de ativo, link e valor.

### `click_on_element`

Uma função utilitária que simula um clique em um elemento da página web. Utiliza Selenium WebDriver para interagir com a página.

### `get_stock_data`

Obtém dados detalhados sobre uma ação específica, incluindo datas, preços de abertura e fechamento, variação, mínimos, máximos e volumes. Utiliza Selenium WebDriver para navegação interativa na página.

### `calculation`

Realiza o processamento dos dados, calcula médias de fechamento por ativo, por mês e por ano. Os resultados são arredondados e salvos em um arquivo Excel.

### Fluxo Principal

1. Obtém uma lista de ações usando `scrape_stock_list`.
2. Filtra a lista de ações para excluir aquelas que terminam com 'F'.
3. Itera sobre as ações restantes, obtendo dados detalhados com `get_stock_data`.
4. Realiza cálculos de média e salva os resultados em um arquivo Excel usando `calculation`.

## Como Executar

Certifique-se de ter as bibliotecas necessárias instaladas, incluindo Selenium, BeautifulSoup, pandas, etc. O script também faz uso do WebDriver do Chrome, portanto, certifique-se de ter o ChromeDriver instalado.

Execute o script fornecendo as informações necessárias, como a URL da página web e as ações desejadas.

```bash
python nome_do_script.py

