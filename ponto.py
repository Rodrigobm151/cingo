import requests, time, random, os, json
from datetime import datetime

# Configurações
USUARIO = os.getenv('CINGO_USER')
SENHA = os.getenv('CINGO_PASS')
LATITUDE = -5.80150422131498
LONGITUDE = -50.515350539205535

def verificar_autorizacao():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        if config.get('status') != 'rodando':
            print("Sistema pausado no controle remoto.")
            return False
        hoje = datetime.now().strftime("%Y-%m-%d")
        if hoje not in config.get('dias_permitidos', []):
            print(f"Hoje ({hoje}) está desmarcado no calendário.")
            return False
        return True
    except:
        return True

def atualizar_ultimo_ponto(session):
    # Endpoint que vimos nas suas capturas de tela
    URL_LISTA = "https://www.cingoportal.com/afry/rest/pontoeletronico/marcacaoponto/marcacaoponto/marcacoes"
    
    res = session.get(URL_LISTA)
    if res.status_code == 200:
        dados = res.json()
        # Pega a última marcação da lista enviada pelo Cingo
        if dados and len(dados) > 0:
            ultima = dados[-1].get('horaMarcação', 'Horário não encontrado')
            
            # Atualiza o config.json para o HTML ler
            with open('config.json', 'r+') as f:
                config = json.load(f)
                config['ultimo_ponto'] = f"Hoje às {ultima}"
                f.seek(0)
                json.dump(config, f, indent=2)
                f.truncate()
            print(f"Painel atualizado com o horário real: {ultima}")

def executar():
    if not verificar_autorizacao(): return
    
    time.sleep(random.randint(0, 300)) # Atraso humano
    session = requests.Session()
    
    # Login
    payload = {'action': 'login', 'user': USUARIO, 'pass': SENHA}
    res = session.post("https://www.cingoportal.com/afry/portal/action/Login/view/normal", data=payload)
    
    if res.status_code == 200:
        # Marcação com GPS
        dados_ponto = {"latitude": LATITUDE, "longitude": LONGITUDE, "accuracy": 20.0}
        session.post("https://www.cingoportal.com/afry/rest/pontoeletronico/marcacaoponto/marcacaoponto/marcacoes", json=dados_ponto)
        print("Ponto registrado com sucesso!")

if __name__ == "__main__":
    executar()
