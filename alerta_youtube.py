import feedparser
import requests
import os

# CONFIGURAÇÕES
BOT_TOKEN = "8515291853:AAGaI2d6KFEgB7u0jfyTYAF3HxGQpDQWLiI"
CHAT_ID = "6668960094"
CHANNEL_ID = "UCY3HJfADCXTiF9kMGH5zrMg"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
ULTIMO_ARQUIVO = "ultimo_video.txt"

print(f"📡 Iniciando consulta no canal: {CHANNEL_ID}")
feed = feedparser.parse(RSS_URL)

if len(feed.entries) > 0:
    ultimo_video = feed.entries[0]
    video_id = ultimo_video.yt_videoid
    titulo = ultimo_video.title
    link = ultimo_video.link
    print(f"📺 Vídeo mais recente no YouTube agora: {titulo}")

    if os.path.exists(ULTIMO_ARQUIVO):
        with open(ULTIMO_ARQUIVO, "r") as f:
            ultimo_salvo = f.read().strip()
        print(f"💾 ID salvo na memória: {ultimo_salvo}")
    else:
        ultimo_salvo = ""
        print("ℹ️ Memória vazia (primeira execução ou arquivo deletado).")

    if video_id != ultimo_salvo:
        print("🚀 NOVO VÍDEO DETECTADO! Enviando para o Telegram...")
        mensagem = f"🎬 Novo vídeo no canal!\n\n{titulo}\n{link}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        resposta = requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})
        
        if resposta.status_code == 200:
            print("✅ SUCESSO: Mensagem entregue ao Telegram!")
            with open(ULTIMO_ARQUIVO, "w") as f:
                f.write(video_id)
        else:
            print(f"❌ ERRO NO TELEGRAM: {resposta.status_code} - {resposta.text}")
    else:
        print(f"😴 O vídeo '{titulo}' já é o mesmo que está na memória. Nada a enviar.")
else:
    print("⚠️ O YouTube não retornou nenhum vídeo. O ID do canal pode estar instável ou errado.")
