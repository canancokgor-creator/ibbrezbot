import time
import requests
from bs4 import BeautifulSoup
import re

BOT_TOKEN = "5794911180:AAEkXt6D6O5S_q0d0_U75_qRGFJfDJrrru"
CHAT_ID = "7739708593"

TARGET_URL = "https://tesislerrezervasyon.ibb.istanbul/reservation/create/6"
CHECK_INTERVAL = 60  # saniye

def find_available():
    try:
        resp = requests.get(TARGET_URL)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        dates = re.findall(r"(\d{2}\.\d{2}\.\d{4}).+?(Dolu|Boş)", text)
        return [d[0] for d in dates if "Boş" in d[1]]
    except:
        return []

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

send("Bot çalıştı ❤️ Rezervasyonları takip ediyorum.")

while True:
    empty = find_available()
    if empty:
        send("BOŞ GÜN VAR AŞKIM!!!\n" + "\n".join(empty))
    time.sleep(CHECK_INTERVAL)
