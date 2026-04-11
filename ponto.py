import requests
import time
import random
import os
from datetime import datetime

USUARIO = os.getenv('CINGO_USER')
SENHA = os.getenv('CINGO_PASS')
LATITUDE = -5.80150422131498
LONGITUDE = -50.515350539205535

def executar():
    atraso = random.randint(0, 300)
    print(f"Aguardando {atraso} segundos para simular comportamento humano...")
    time.sleep(atraso)

    session = requests.Session()
    # Identificação de navegador real para evitar o 404 de redirecionamento
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    })
    
    print("Realizando login...")
    payload_login = {'action': 'login', 'user': USUARIO, 'pass': SENHA}
    url_login = "https://www.cingoportal.com/afry/portal/action/Login/view/normal"
    
    res_login = session.post(url_login, data=payload_login)
    
    if res_login.status_code == 200:
        print("Login OK. Enviando GPS...")
        url_ponto = "https://www.cingoportal.com/afry/rest/pontoeletronico/marcacaoponto/marcacaoponto/marcacoes"
        
        payload_ponto = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "accuracy": round(random.uniform(15.0, 30.0), 2)
        }
        
        res_ponto = session.post(url_ponto, json=payload_ponto)
        
        # Se for 200 ou 201, é sucesso garantido.
        if res_ponto.status_code in [200, 201]:
            print(f"SUCESSO TOTAL: Ponto registrado às {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"AVISO: O servidor respondeu com status {res_ponto.status_code}")
            print(f"RESPOSTA DO SERVIDOR: {res_ponto.text}")
            print("Verifique no site da Cingo se o ponto entrou, pois pode ser apenas erro de redirecionamento.")
    else:
        print("ERRO CRÍTICO: Falha no Login.")

if __name__ == "__main__":
    executar()
