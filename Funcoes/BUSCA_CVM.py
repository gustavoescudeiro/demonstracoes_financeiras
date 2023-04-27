import pandas as pd
import zipfile
import time
#pd.options.display.float_format = '{:.2f}'.format
import requests

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def busca_informes_cvm(ano):

    url = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{:02d}.zip'.format(ano)
    r = requests.get(url)
    buf1 = BytesIO(r.content)
    dicionario_arquivos = {}
    with zipfile.ZipFile(buf1, "r") as f:
        for name in f.namelist():
            if name.endswith('.csv'):
                with f.open(name) as zd:
                    df = pd.read_csv(zd, encoding='latin1', sep=';')
                    dicionario_arquivos[name] = df

    return dicionario_arquivos

def busca_cadastro_cvm():
    url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
    return pd.read_csv(url, sep=';', encoding='ISO-8859-1')


def busca_informes_cvm_historico(ano):
    resp = urlopen(f"http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/HIST/inf_diario_fi_{ano}.zip")
    zipfile = ZipFile(BytesIO(resp.read()))
    lista_arquivos = zipfile.namelist()
    lista_df = []
    for arquivo in lista_arquivos:
        df = pd.read_csv(zipfile.open(arquivo), sep = ";", decimal = ",")
        lista_df.append(df)
    df_final = pd.concat(lista_df, axis = 0)
    return df_final

