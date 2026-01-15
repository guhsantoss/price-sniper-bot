# 🎯 Price Sniper Bot

Bot de monitoramento de preços desenvolvido em Python. Ele monitora produtos em e-commerces (como a KaBuM!) e envia alertas automáticos via Telegram quando o preço atinge o valor desejado.

## 🛠 Tecnologias
- **Python 3.12**
- **Curl_cffi** (para simular browser real e evitar bloqueios)
- **BeautifulSoup4** (Web Scraping)
- **Telegram API** (Envio de notificações)
- **Regex** (Filtragem inteligente de preços e parcelas)

## 🚀 Como funciona
1. O script acessa a URL do produto a cada minuto.
2. Utiliza "Impersonate Chrome" para evitar detecção de robôs.
3. Escaneia todo o texto da página buscando padrões de preço (`R$`).
4. Filtra valores baixos (parcelas) para encontrar o preço real à vista.
5. Se o preço for menor que o alvo, você recebe um aviso no celular.

## 📦 Como rodar
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` com seu TOKEN do Telegram.
4. Rode: `python main.py`