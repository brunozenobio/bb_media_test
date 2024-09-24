from playwright.sync_api import sync_playwright
from scripts.init_pluto_tv import *
import json


def get_channels(url_base):
    """
    Esta funcion busca todos los canales y sus episodios en la pagina base de plut

    Parametros:
        url(str): url base de pluto tv

    Retorna:
        canales(list): lista de diccionario con los canales y sus episodios, estos podrian repetirse.

    """
    page, browser, _ = init_playwright()
    init_pluto(page, url_base)

    page.wait_for_selector('//div[contains(@class,"channelList-0-2") and contains(@class,"custom-scroll")]')
    div_scroll_channel = page.locator('//div[contains(@class,"channelList-0-2") and contains(@class,"custom-scroll")]')

    canales = []

    page.locator("//button[@aria-label='Expand Guide']").click() # expando la guia de canales
    page.wait_for_load_state("domcontentloaded")

    while True: # ralizo el scroll
        
        

        ## inicio un while mientras que el boton para scrollear a la derecha exista, y lo presiono luego de hacer toda la logica
        while page.locator("//button[contains(@class,'paginateRightButton-0-2')]").count() > 0:
            div_secciones_channels = div_scroll_channel.locator('//div[contains(@class,"channelListItem-0-2") and contains(@class,"channel")]').all()
            
            #primero extraigo todos los canales visibles
            for div_channel in div_secciones_channels:

                try:
                    programas = []
                    if div_channel.locator("//div[@role='rowheader']").count() > 0:

                        info_canal = div_channel.locator("//div[@role='rowheader']")

                        url_channel = url_base + info_canal.locator("a.ChannelInfo-Link").get_attribute("href")
                        nombre_channel = info_canal.locator("div.image").get_attribute("aria-label")

                        nuevo_canal = {"name": nombre_channel, "url": url_channel, "programas": []}
                        canales.append(nuevo_canal)  

                        
                        div_programa_grilla = div_channel.locator("//span[@class='timelines']").locator("div").locator("a").all()


                        # por cada canal visible extraigo los programas y sus horarios
                        for boton_programa in div_programa_grilla:
                            
                            url_programa = url_base + boton_programa.get_attribute("href")
                            nombre_programa = boton_programa.locator("div.name-container").inner_text()
                            horario_programa = boton_programa.locator("//div[contains(@class,'vitalInfoContainer-0-2')]").locator("//div[contains(@class,'time') or contains(@class,'Time')]").inner_text()

                            programa = {"name_program": nombre_programa, "hour_program": horario_programa, "url_program": url_programa}
                            programas.append(programa)

                        
                        canales[-1]["programas"] = programas  
                    else:
                        div_programa_grilla = []
                except:
                    continue
            
            #presiono el boton para scrollear a la derehca
            page.locator("//button[contains(@class,'paginateRightButton-0-2')]").click()
            page.wait_for_load_state("networkidle")


        # el ultimo div de live tv
        ultimo_div = div_scroll_channel.locator("div[data-lastcell='true']")
        # si existe el ultimo div se rompe el bucle
        if ultimo_div.count() > 0:
            break
        # cuando se scrolleo a la derecha y existe el boton para scrollear a la izquierda lo presiono para volver al inicio, para buscar mas secciones
        while page.locator("//button[contains(@class,'paginateLeftButton-0-2')]").count() > 0:
            page.locator("//button[contains(@class,'paginateLeftButton-0-2')]").click()

        # scrolleo para navegar por las secciones
        div_scroll_channel.evaluate("(el) => { el.scrollTop += 400; }", div_scroll_channel)
        page.wait_for_load_state("networkidle")

    browser.close()
    return canales




def get_channels_unique(canales):

    """
    Esta funcion toma la lista de canales y retorna los unicos junto con los episodios unicos

    Parametros:
        canales(list): Lista de diccionarios de los canales

    Retorna:
        resultado_canales(list) : lista de diccionario de los canales y programas unicos
    
    """
    canal_urls = set()
    resultado_canales = []

    for canal in canales:
        
        # pregunto si el url ya esta en set, de no estar lo agrega
        if canal["url"] not in canal_urls:
            canal_urls.add(canal["url"])

           
            programa_urls = set()
            programas_unicos = []

            #pregunto si el url del programa esta en la lista
            for programa in canal["programas"]:
                if programa["url_program"] not in programa_urls:
                    programa_urls.add(programa["url_program"])

                    programas_unicos.append(programa)

            
            resultado_canales.append({
                "name": canal["name"],
                "url": canal["url"],
                "programas": programas_unicos
            })
    return resultado_canales


def write_json_channels(channels):
    """
    Guarda la lista de diccionario en un json

    Parametros:
        channels: lista de diccionarios.
    """
    with open("./database/channels.json", "w",encoding='utf-8') as json_file:
        json.dump(channels, json_file,ensure_ascii=False, indent=5)
