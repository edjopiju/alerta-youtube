import feedparser
import requests
import os

# CONFIGURAÇÕES
BOT_TOKEN = "8515291853:AAGaI2d6KFEgB7u0jfyTYAF3HxGQpDQWLiI"
CHAT_ID = "6668960094"
CHANNEL_ID = "UCY3HJfADCXTiF9kMGH5zrMg"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
ULTIMO_ARQUIVO = "ultimo_video.txt"

feed = feedparser.parse(RSS_URL)
if len(feed.entries) > 0:
    ultimo_video = feed.entries[0]
    video_id = ultimo_video.yt_videoid
    titulo = ultimo_video.title
    link = ultimo_video.link

    if os.path.exists(ULTIMO_ARQUIVO):
        with open(ULTIMO_ARQUIVO, "r") as f:
            ultimo_salvo = f.read().strip()
    else:
        ultimo_salvo = ""

    if video_id != ultimo_salvo:
        mensagem = f"🎬 Novo vídeo no canal!\n\n{titulo}\n{link}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})
        with open(ULTIMO_ARQUIVO, "w") as f:
            f.write(video_id)
        print("Novo vídeo enviado!")
    else:
        print("Sem vídeos novos.")
