from bs4 import BeautifulSoup
import requests

from playwright.sync_api import sync_playwright
import re
import json

def get_data(datos):
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(headless=False)

        page = browser.new_page()

        datos_movies_series = {}

        for key,valores in datos.items():
            for valor in valores:

                page.goto(valor)
                page.wait_for_timeout(3000)
                div_programa = page.locator("div.inner")
                titulo = div_programa.locator("h2").inner_text() if div_programa.locator("h2") else "N/A"   
                print(titulo)
                metadata = div_programa.locator("div").all()


                informacion = metadata[0].locator("li").all() if len(metadata) > 0 else []
                genero = informacion[0].inner_text() if len(informacion) > 0 else "N/A"
                duracion = informacion[1].inner_text() if len(informacion) > 1 else "N/A"

                sinopsis = metadata[1].locator("p").inner_text() if len(metadata) > 1 else "Sin sinopsis disponible"

                if type == "serie":
                    duracion = re.search(r"\d",duracion)

                datos_movies_series[titulo] = {
                        'genero': genero,
                        'duracion': duracion,  
                        'sinopsis': sinopsis,
                        
                    }

        return datos_movies_series




with open('mi_diccionario.json', 'r') as archivo_json:
    datos = json.load(archivo_json)

print(get_data(datos))
