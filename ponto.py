import requests
import time
import random
import os
from datetime import datetime

# Credenciais e GPS
USUARIO = os.getenv('CINGO_USER')
SENHA = os.getenv('CINGO_PASS')
LATITUDE = -5.80150422131498
LONGITUDE = -50.515350539205535

def executar():
    # Margem aleatória de 0 a 300 segundos (5 minutos)
    atraso = random.randint(0, 300)
    print(f"Iniciando variação humana. Aguardando {atraso} segundos...")
    time.sleep(atraso)

    session = requests.Session()
    
    # Login
    print("Realizando login no Cingo...")
    payload_login = {
        'action': 'login',
        'user': USUARIO,
        'pass': SENHA
    }
    
    url_login = "https://www.cingoportal.com/afry/portal/action/Login/view/normal"
    res_login = session.post(url_login, data=payload_login)
    
    if res_login.status_code == 200:
        print("Login bem-sucedido. Enviando marcação com GPS...")
        
        # Dados da Marcação
        url_ponto = "https://www.cingoportal.com/afry/rest/pontoeletronico/marcacaoponto/marcacaoponto/marcacoes"
        payload_ponto = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "accuracy": random.uniform(15.0, 25.0) # Precisão variável para realismo
        }
        
        res_ponto = session.post(url_ponto, json=payload_ponto)
        
        if res_ponto.status_code == 200:
            print(f"SUCESSO: Ponto batido às {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"ERRO na marcação: {res_ponto.status_code}")
    else:
        print("ERRO no login. Verifique os Secrets.")

if __name__ == "__main__":
    executar()
