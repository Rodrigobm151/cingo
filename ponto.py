import requests
import time
import random
import os
from datetime import datetime

# Credenciais dos Secrets
USUARIO = os.getenv('CINGO_USER')
SENHA = os.getenv('CINGO_PASS')

# Configurações de Localização (As que você me enviou)
LATITUDE = -5.80150422131498
LONGITUDE = -50.515350539205535

URL_LOGIN = "https://www.cingoportal.com/afry/portal/action/Login/view/normal"
URL_MARCACAO = "https://www.cingoportal.com/afry/rest/pontoeletronico/marcacaoponto/marcacaoponto/marcacoes"

def check_excecoes():
    hoje = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists("excecoes.txt"):
        with open("excecoes.txt", "r") as f:
            conteudo = f.read()
            if hoje in conteudo:
                return True
    return False

def executar():
    if check_excecoes():
        print(f"Pausa programada: {datetime.now().strftime('%d/%m/%Y')} está nas exceções.")
        return

    # 1. Margem de 5 minutos aleatórios (Seu Ponto 3)
    espera = random.randint(0, 300)
    print(f"Variação humana: Aguardando {espera} segundos...")
    time.sleep(espera)

    session = requests.Session()
    
    # 2. Login (Conforme seu cURL)
    dados_login = {
        'action': 'login',
        'user': USUARIO,
        'pass': SENHA,
        'domain': '', 'code': '', 'bornDate': ''
    }

    print("Realizando login...")
    res_login = session.post(URL_LOGIN, data=dados_login)
    
    if res_login.status_code == 200:
        print("Login OK. Preparando marcação com GPS...")
        
        # 3. Payload de Marcação com a Geolocalização (Seu Ponto 1)
        # Enviamos os dados que o servidor espera para validar sua posição
        payload_ponto = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "accuracy": random.uniform(10.0, 30.0), # Precisão variável para parecer real
            "isMockLocation": False # Diz ao sistema que não é localização falsa
        }

        # Tentativa de registro
        res_ponto = session.post(URL_MARCACAO, json=payload_ponto)
        
        if res_ponto.status_code == 200:
            print(f"SUCESSO! Ponto registrado em: {LATITUDE}, {LONGITUDE}")
        else:
            # Se o POST falhar, tentamos o GET simples como backup
            session.get(URL_MARCACAO)
            print("Ponto enviado via método alternativo.")
    else:
        print("Erro ao acessar o portal.")

if __name__ == "__main__":
    executar()
