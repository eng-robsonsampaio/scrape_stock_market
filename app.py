import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
df_result = pd.read_csv('output/stoks.csv', sep=';')
df_list_of_stoks = pd.read_csv('output/stock_list.csv', sep=';')


@app.route('/')
def display_stock_list():

    # Obter o número de linhas a serem exibidas (padrão para 10 se não especificado)
    rows = request.args.get('rows', 5)
    ativo = request.args.get('ativo', '')
    # Filtrar o DataFrame pelo ativo, se fornecido
    df_filtered = df_list_of_stoks[df_list_of_stoks['value'].str.contains(ativo, case=False, na=False)]


    # Obter as linhas do DataFrame conforme a seleção do usuário
    if rows == 'All':
        # Criar uma tabela HTML usando o método to_html() do DataFrame
        table_html = df_filtered.to_html(classes='table table-striped')
    else:
        # Criar uma tabela HTML usando o método to_html() do DataFrame
        table_html = df_filtered.head(int(rows)).to_html(classes='table table-striped')

    # Renderizar a página HTML com a tabela e o dropdown
    return render_template('index.html', table=table_html, rows=rows, current_route='display_stock_list')

@app.route('/display_historical_data')
def display_historical_data():

    # Obter o número de linhas a serem exibidas (padrão para 10 se não especificado)
    rows = request.args.get('rows', 5)
    ativo = request.args.get('ativo', '')
    # Filtrar o DataFrame pelo ativo, se fornecido
    df_filtered = df_result[df_result['ATIVO'].str.contains(ativo, case=False, na=False)]


    # Obter as linhas do DataFrame conforme a seleção do usuário
    if rows == 'All':
        # Criar uma tabela HTML usando o método to_html() do DataFrame
        table_html = df_filtered.to_html(classes='table table-striped')
    else:
        # Criar uma tabela HTML usando o método to_html() do DataFrame
        table_html = df_filtered.head(int(rows)).to_html(classes='table table-striped')

    # Renderizar a página HTML com a tabela e o dropdown
    return render_template('index.html', table=table_html, rows=rows, current_route='display_historical_data')

@app.route('/display_average_by_type')
def display_average_by_type():

    # df_avg_by_type = df_result.copy()
     # Filtrar o DataFrame pelo ativo, se fornecido
     # Obter o ativo a ser pesquisado
    ativo = request.args.get('ativo', '')
    df_filtered = df_result[df_result['ATIVO'].str.contains(ativo, case=False, na=False)]

    colunas_numericas = ['ABERTURA', 'FECHAMENTO', 'VARIACAO', 'MINIMO', 'MAXIMO']
    df_filtered[colunas_numericas] = df_filtered[colunas_numericas].replace(',', '.', regex=True).apply(pd.to_numeric, errors='coerce')
    media_por_tipo = df_filtered.groupby('TIPO')[colunas_numericas].mean()
    media_por_tipo.reset_index(inplace=True)

    # Criar uma tabela HTML usando o método to_html() do DataFrame
    table_html = media_por_tipo.to_html(classes='table table-striped')

    # Renderizar a página HTML com a tabela de médias
    return render_template('index.html', table=table_html, current_route='display_average_by_type')

@app.route('/display_average_by_stock')
def display_average_by_stock():
    rows = request.args.get('rows', 5)
    ativo = request.args.get('ativo', '')
    # Filtrar o DataFrame pelo ativo, se fornecido
    df_filtered = df_result[df_result['ATIVO'].str.contains(ativo, case=False, na=False)]
    colunas_numericas = ['ABERTURA', 'FECHAMENTO', 'VARIACAO', 'MINIMO', 'MAXIMO']
    df_filtered[colunas_numericas] = df_filtered[colunas_numericas].replace(',', '.', regex=True).apply(pd.to_numeric, errors='coerce')
    media_por_tipo = df_filtered.groupby('ATIVO')[colunas_numericas].mean()
    media_por_tipo.reset_index(inplace=True)
    # Obter as linhas do DataFrame conforme a seleção do usuário
    if rows == 'All':
        # Criar uma tabela HTML usando o método to_html() do DataFrame
        table_html = media_por_tipo.to_html(classes='table table-striped')
    else:
        # Criar uma tabela HTML usando o método to_html() do DataFrame
        table_html = media_por_tipo.head(int(rows)).to_html(classes='table table-striped')
    # table_html = media_por_tipo.to_html(classes='table table-striped')

    # Renderizar a página HTML com a tabela de médias
    return render_template('index.html', table=table_html, rows=rows, current_route='display_average_by_stock')

if __name__ == '__main__':
    app.run(debug=True)
