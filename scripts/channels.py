from playwright.sync_api import sync_playwright
import pandas as pd
from scripts.init_pluto_tv import *

def get_canales(url_base):
    """
    Esta función recorre la seccion Live-TV y obteiene los canales unicos

    Parametros:
        url_base(str) : Url base de plutotv
    
    Retorna:
        (tuple) : canales y nombres unicos

    """


    timeout = 400
    page, browser, playwright = init_playwright()
    init_pluto(page, url_base)

    page.wait_for_load_state("domcontentloaded")

    programas_scroller = page.locator('//div[contains(@class,"channelList-0-2-") and contains(@class,"custom-scroll")]')
    canales_url = set()
    canales_nombres = set()
    

    for _ in range(60):
        link_canales = programas_scroller.locator("a.ChannelInfo-Link").all()
        for link_canal in link_canales:
            url_canal = url_base + link_canal.get_attribute("href")
            nombre_canal = link_canal.locator("div.image").get_attribute("aria-label")
            canales_nombres.add(nombre_canal)
            canales_url.add(url_canal)

        programas_scroller.evaluate("(el) => { el.scrollTop += 100; }", programas_scroller)
        page.wait_for_timeout(timeout)


    browser.close()
    playwright.stop()

    return canales_nombres,canales_url

def channel_to_pandas(urls, nombres):

    """
    Esta función recibe los urls y nombres de canales unicos y los devuelve como dataframe
    Parametros:
        urls(set) : Url unicos de canales
        nombres(set): Nombres unicos de canales

    Retorna:
        DataFrame con los canales    
    """

    urls = list(urls)
    nombres = list(nombres)

    df_canales = pd.DataFrame({"Nombre_Canal": nombres, "Url_Canal": urls})
    return df_canales

def write_channels(df):

    """
    Esta funcion recibe un dataframe y lo exporta como csv

    Parametros:
        df(DataFrame)

    Retorna:
        Guarda en un csv
    
    """
    df.to_csv("./database/channels.csv", index=False)
