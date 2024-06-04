import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

os.system('cls')

diretorio = 'C:/Users/Beffa/Documents/Python/webScraping/Steam/'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
url_case = 'https://csgostash.com/containers/skin-cases'
url_souvenir = 'https://csgostash.com/containers/souvenir-packages?name=Copenhagen+2024'

dic_caixas = {'Nome':[],'Quantidade':[],'Preco':[]}
my_box = ['Dreams & Nightmares','Fracture','Revolution','Snakebite','Anubis Souvenir','Ancient Souvenir']
my_box_qtd = ['1','4','1','4','1','1',]

def caixas_steam(dic, url_page):
    
    print(f"Inicializando Programa.")  

    for i in range(0,1):
        
        site = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        games = soup.find_all('div', class_=re.compile('text-center'))
        time.sleep(1)
        
        for game in games:
            try:
                data_title = game.find('div', class_=re.compile('result-box'))
                title = data_title.find('h4').text.strip()

            except Exception as erro:
                continue

            try:
                quantidade_data = game.find('div', class_=re.compile('btn-group-sm '))
                quantidade_full = quantidade_data.text.split()
                quantidade = quantidade_full[0]
                        
            except Exception as erro:
                continue

            try:
                preco_data = game.find('div', class_=re.compile('margin-top-sm'))
                preco = preco_data.text.strip()

            except Exception as erro:
                continue

            dic['Nome'].append(title)
            dic['Quantidade'].append(quantidade)
            dic['Preco'].append(preco)

            print(f'Nome: {title} Quantiade: {quantidade} Preco: {preco}')
        
        print(f'Fim da pagina.')

def my_box_value(end_arq_csv):
    
    df = pd.read_csv(f'{end_arq_csv}caixas_cs2.csv', sep=';')
    df['Preco'] = df['Preco'].str.replace('R$', '', regex=False).str.replace(',', '.').astype(float)

    valor_total = 0
    for indx, qtd in zip(my_box, my_box_qtd):
        if df['Nome'].str.contains(indx,case=False).any():
            preco = df.loc[df['Nome'].str.contains(indx, case=False), 'Preco'].iloc[0]
            total = int(qtd) * preco
            valor_total += total

    print(f'O valor total das caixas sao: R${valor_total}')   

caixas_steam(dic_caixas, url_case)
caixas_steam(dic_caixas, url_souvenir)

df = pd.DataFrame(dic_caixas)
df.to_csv(f'{diretorio}caixas_cs2.csv', encoding='utf-8', sep=';', index=False)

my_box_value()
