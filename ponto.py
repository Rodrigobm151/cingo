import json
import os
from datetime import datetime

def verificar_autorizacao():
    if not os.path.exists('config.json'):
        return True # Se não houver config, roda por padrão

    with open('config.json', 'r') as f:
        config = json.load(f)

    # Verifica Play/Pause
    if config.get('status') != 'rodando':
        print("SISTEMA PAUSADO NO PAINEL.")
        return False

    # Verifica se hoje está marcado no calendário
    hoje = datetime.now().strftime("%Y-%m-%d")
    if hoje not in config.get('dias_permitidos', []):
        print(f"HOJE ({hoje}) ESTÁ DESMARCADO NO CALENDÁRIO.")
        return False

    return True

# No seu def executar():
# if not verificar_autorizacao(): return
