from curl_cffi import requests
from bs4 import BeautifulSoup
import schedule
import time
import os
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- CONFIGURAÇÃO DO ALVO ---
URL_PRODUTO = "https://www.kabum.com.br/produto/920419/placa-de-video-xfx-speedster-qick308-radeon-rx-7600-white-amd-edition-8gb-gddr6-128-bit-rx-76pqickwy"

PRECO_ALVO = 2500.00          # Avise se for MENOR que isso
PRECO_MINIMO_ACEITAVEL = 1000.00  # Ignore valores menores que isso (para não pegar parcelas)

def enviar_telegram(mensagem):
    try:
        import requests as req_padrao 
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": mensagem}
        req_padrao.post(url, data=data)
    except Exception as e:
        print(f"❌ Erro Telegram: {e}")

def verificar_preco():
    print(f"🔎 Verificando KaBuM...")
    
    try:
        response = requests.get(URL_PRODUTO, impersonate="chrome110")
        
        if 200 <= response.status_code < 300:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            titulo = soup.find("h1")
            nome_produto = titulo.text.strip() if titulo else "Produto KaBuM"
            
            texto_pagina = soup.get_text()
            
            # Procura preços (R$ xxx,xx)
            padrao_preco = r'R\$\s*(\d{1,3}(?:\.\d{3})*,\d{2})'
            precos_encontrados = re.findall(padrao_preco, texto_pagina)

            if precos_encontrados:
                lista_valores = []
                for p in precos_encontrados:
                    valor_limpo = p.replace(".", "").replace(",", ".")
                    lista_valores.append(float(valor_limpo))
                
                # --- FILTRO INTELIGENTE ---
                # Só aceita valores maiores que o mínimo (evita parcelas de R$ 100,00)
                valores_validos = [v for v in lista_valores if v >= PRECO_MINIMO_ACEITAVEL]
                
                if valores_validos:
                    # Pega o menor preço válido (que será o à vista)
                    preco_atual = min(valores_validos) 
                    
                    print(f"📦 {nome_produto}")
                    print(f"💰 Preço Real Identificado: R$ {preco_atual:.2f}")

                    if preco_atual <= PRECO_ALVO:
                        msg = f"🚨 OFERTA KABUM!\n\n📦 {nome_produto}\n💰 R$ {preco_atual:.2f}\n🔗 {URL_PRODUTO}"
                        enviar_telegram(msg)
                    else:
                        print(f"   Ainda caro (Meta: R$ {PRECO_ALVO})")
                else:
                    print(f"⚠️ Achei valores, mas todos parecem parcelas (menores que R$ {PRECO_MINIMO_ACEITAVEL})")
            else:
                print("⚠️ Não encontrei nenhum 'R$' na página.")

        else:
            print(f"❌ Erro de conexão: {response.status_code}")

    except Exception as e:
        print(f"❌ Erro no script: {e}")

# --- INÍCIO ---
print("🤖 SNIPER KABUM V4 (COM FILTRO) INICIADO!")
enviar_telegram("🚀 Sniper V4 rodando e filtrando parcelas!")

verificar_preco()
schedule.every(1).minutes.do(verificar_preco)

while True:
    schedule.run_pending()
    time.sleep(1)