from fastapi import FastAPI
import httpx
import requests
from bs4 import BeautifulSoup

# -------------------------------
# CONFIGURAÇÕES
# -------------------------------
WHATSAPP_TOKEN = "SEU_TOKEN_DO_META"
WHATSAPP_PHONE_ID = "SEU_PHONE_NUMBER_ID"
GROUP_ID = "ID_DO_GRUPO_OU_NUMERO"

app = FastAPI()

# -------------------------------
# WHATSAPP - ENVIO DE MENSAGEM
# -------------------------------
async def send_message(to: str, text: str):
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=data)
        return r.json()

# -------------------------------
# SCRAPING - KABUM
# -------------------------------
def get_kabum_promos():
    url = "https://www.kabum.com.br/ofertas"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    promos = []
    for item in soup.select(".sc-dkrFOg"):
        titulo = item.select_one("span.nameCard").text if item.select_one("span.nameCard") else None
        preco = item.select_one("span.priceCard").text if item.select_one("span.priceCard") else None
        link = item.find("a")["href"] if item.find("a") else None
        if titulo and preco and link:
            promos.append(f"🔹 {titulo}\n💰 {preco}\n🔗 https://www.kabum.com.br{link}")
    return promos[:3]  # pega só 3 primeiras

# -------------------------------
# SCRAPING - MAGAZINE LUIZA
# -------------------------------
def get_magalu_promos():
    url = "https://www.magazineluiza.com.br/ofertas"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    promos = []
    for item in soup.select("li.sc-dQppl"):
        titulo = item.select_one("h3").text if item.select_one("h3") else None
        preco = item.select_one("p.sc-kpDqfm").text if item.select_one("p.sc-kpDqfm") else None
        link = item.find("a")["href"] if item.find("a") else None
        if titulo and preco and link:
            promos.append(f"🔹 {titulo}\n💰 {preco}\n🔗 https://www.magazineluiza.com.br{link}")
    return promos[:3]

# -------------------------------
# ENDPOINT - ENVIAR PROMOS
# -------------------------------
@app.post("/send-promos")
async def send_promos():
    kabum = get_kabum_promos()
    magalu = get_magalu_promos()

    todas = kabum + magalu
    results = []
    for promo in todas:
        res = await send_message(GROUP_ID, promo)
        results.append(res)

    return {"enviado": len(results), "detalhes": results}
