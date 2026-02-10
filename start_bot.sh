#!/bin/bash
echo "========================================"
echo "🤖 TWITCH BOT - GitHub Codespaces"
echo "========================================"

# Configurar Ngrok
echo "📡 Configurando Ngrok..."
python3 -c "
from pyngrok import ngrok, conf
import os
token = os.getenv('NGROK_AUTH_TOKEN')
if token:
    conf.get_default().auth_token = token
    print('✅ Ngrok configurado con token')
else:
    print('⚠️  No hay token de Ngrok, usando versión limitada')
"

# Iniciar Ngrok tunnel para Twitch IRC
echo "🌐 Iniciando túnel Ngrok..."
NGROK_TUNNEL=$(python3 -c "
from pyngrok import ngrok
try:
    tunnel = ngrok.connect(6667, 'tcp')
    print(tunnel.public_url)
except Exception as e:
    print(f'Error: {e}')
")

echo "🔗 URL pública: $NGROK_TUNNEL"
echo "💡 Esta URL es temporal, cambia cada vez que reinicies"

# Iniciar bot
echo "🚀 Iniciando bot de Twitch..."
python3 bot_twitch.py
