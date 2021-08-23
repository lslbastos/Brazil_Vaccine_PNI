## Imponrt SI-PNI data
import pandas as pd
import numpy as np
import requests
import json


#### Read CSV data directly from URL (OpenDataSUS)


def get_pni_data_csv(csv_url):

    df_si_pni = pd.read_csv(csv_url, delimiter=";")
 
    return df_si_pni


#df_si_pni = pd.DataFrame(final_data, columns=colnames)




##### Imponrt SI-PNI data directly from API


import json

def get_pni_data_api(uf):

    credentials = ('imunizacao_public', 'qlto5t&7r_@+#Tlstigi')

    headers = {
        'authorization': "qwerty",
        'content-type': "application/json",
        'accept': "text/plain, */*; q=0.01"
        }

    ##################### Step 1: Request for the entire Data with Scroll API
    url = 'https://imunizacao-es.saude.gov.br/_search?scroll=1m'

    ## API
    #query_path = 'INDEX_NAME/_search?scroll=1m'
    #query_params = {"path" : query_path, "method" : "POST"}
    #uf  = "AC"

    query_payload = '''
    {
      "size": 10000,
      "query": {
            "match" : {
                "estabelecimento_uf" : "''' + uf + '''" 
                }
            }
    }
    '''
    #print(query_payload)

    query_response = requests.request("POST", url, data=query_payload, headers=headers, auth = credentials)

    #print(query_response)

    query_page = json.loads(query_response.text)

    final_data = query_page['hits']['hits'] # extracting the first page
    scroll_id = query_page['_scroll_id'] # getting the scroll_id




    ##################### Step 2: Request to scroll with the scroll_id
    scroll_url = 'https://imunizacao-es.saude.gov.br/_search/scroll'

    scroll_payload = '''{
        "scroll" : "1m", 
        "scroll_id" : "'''+ scroll_id +'''"
    }'''

    scroll_page = {'hits': {'hits' : [1]}} #just adding a demo hit

    hits_data = scroll_page['hits']['hits']


    i = 1


    while len(hits_data) > 0:
        scroll_response = requests.request("POST", url = scroll_url, 
                                           data=scroll_payload, headers=headers, auth = credentials)
        #print(scroll_response)

        scroll_page = json.loads(scroll_response.text)
        hits_data = scroll_page['hits']['hits']

        final_data = final_data + hits_data

        i = i + 1

        if (i % 20 == 0):
            print(i)

    print(i)

    colnames = ['scroll_index', 'scroll_type', 'scroll_id', 'scroll_score',
                'paciente_endereco_coIbgeMunicipio', 'document_id',
                'data_importacao_rnds', 'sistema_origem',
                'version', 'estabelecimento_razaoSocial',
                'paciente_nacionalidade_enumNacionalidade',
                'timestamp', 'paciente_endereco_coPais',
                'vacina_grupoAtendimento_nome',
                'vacina_grupoAtendimento_codigo',
                'vacina_categoria_codigo', 'vacina_descricao_dose',
                'vacina_categoria_nome', 'vacina_lote',
                'paciente_enumSexoBiologico',
                'paciente_endereco_nmMunicipio', 'paciente_endereco_uf',
                'paciente_endereco_nmPais', 'vacina_nome',
                'dt_deleted', 'paciente_racaCor_valor',
                'paciente_id', 'estabelecimento_valor',
                'paciente_dataNascimento', 'vacina_fabricante_nome',
                'vacina_dataAplicacao', 'paciente_endereco_cep',
                'estabelecimento_municipio_nome',
                'estabelecimento_municipio_codigo', 'status',
                'estabelecimento_uf', 'id_sistema_origem',
                'paciente_idade', 'vacina_fabricante_referencia',
                'vacina_codigo', 'paciente_racaCor_codigo',
                'redshift', 'estalecimento_noFantasia']


    df_si_pni = pd.json_normalize(final_data)
    df_si_pni.columns = colnames
    
    return df_si_pni


#df_si_pni = pd.DataFrame(final_data, columns=colnames)

