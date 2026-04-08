import requests
import time
import random
import os
from datetime import datetime

# Pega os dados que você acabou de salvar nos Secrets
USUARIO = os.getenv('CINGO_USER')
SENHA = os.getenv('CINGO_PASS')

URL_LOGIN = "https://www.cingoportal.com/afry/portal/action/Login/view/normal"
URL_MARCACAO = "https://www.cingoportal.com/afry/rest/pontoeletronico/marcacaoponto/marcacaoponto/marcacoes"

def check_excecoes():
    hoje = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists("excecoes.txt"):
        with open("excecoes.txt", "r") as f:
            if hoje in f.read():
                return True
    return False

def executar():
    if check_excecoes():
        print(f"Hoje ({datetime.now().strftime('%d/%m/%Y')}) está na lista de exceções. Pulando...")
        return

    # Margem aleatória de 5 minutos (Ponto 3 da sua lista)
    espera = random.randint(0, 300)
    print(f"Aguardando {espera} segundos para variação aleatória...")
    time.sleep(espera)

    session = requests.Session()
    
    # Payload do Login baseado no seu cURL
    dados_login = {
        'action': 'login',
        'user': USUARIO,
        'pass': SENHA,
        'domain': '',
        'code': '',
        'bornDate': ''
    }

    print("Tentando logar no portal...")
    res = session.post(URL_LOGIN, data=dados_login)
    
    # Se o login der certo, tentamos marcar o ponto
    if res.status_code == 200:
        print("Login OK. Registrando o ponto...")
        res_ponto = session.get(URL_MARCACAO)
        
        if res_ponto.status_code == 200:
            print(f"SUCESSO! Ponto batido às {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"Falha na marcação: Status {res_ponto.status_code}")
    else:
        print(f"Erro no login: Status {res.status_code}")

if __name__ == "__main__":
    executar()
