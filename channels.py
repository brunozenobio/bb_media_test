from playwright.sync_api import sync_playwright
import pandas as pd
from scripts.init_pluto_tv import *
url_base = "https://pluto.tv"

page, browser, playwright = init_playwright()
init_pluto(page, url_base)



page.wait_for_load_state("domcontentloaded")

programas_scroller = page.locator('//div[contains(@class,"channelList-0-2-") and contains(@class,"custom-scroll")]')
canales_url = set()
canales_nombres = set()
    
# Desplazarse y obtener canales y programas
for _ in range(60):

    link_canales = programas_scroller.locator("a.ChannelInfo-Link").all()
    for link_canal in link_canales:
        url_canal = url_base + link_canal.get_attribute("href")
        nombre_canal = link_canal.locator("div.image").get_attribute("aria-label")
        canales_nombres.add(nombre_canal)
        canales_url.add(url_canal)

    programas_scroller.evaluate("(el) => { el.scrollTop += 100; }", programas_scroller)
    page.wait_for_timeout(400)

# Cerrar el navegador
browser.close()

def get_canales(urls, nombres):
    # Convertir los sets a listas para poder indexarlos
    urls = list(urls)
    nombres = list(nombres)

    df_canales = pd.DataFrame({"Nombre_Canal":nombres,"Url_Canal":urls})

    return df_canales

print(get_canales(canales_url, canales_nombres))
