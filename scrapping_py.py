from playwright.sync_api import sync_playwright, Playwright
import time
import re
import json


## usare la libreria de playwright



def init_playwright(playwright: Playwright):
    # selecciono el navegador a usar, e inicio la configuración, luego abro la pagina base.
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)

    page = browser.new_page()
    return page




"""def scroll_pluto_section(page,elemento_scrolleable,altura = 200,tipo="parcial"):

    if tipo == "parcial":

        while True:
            if altura:
                page.evaluate("(el, px) => { el.scrollTop += px; }", elemento_scrolleable, altura)
                page.wait_for_timeout(1000)
            else:
                break  
    elif tipo == "completa":

        while True:
            altura_actual = elemento_scrolleable.evaluate("el => el.scrollHeight")
            page.evaluate("el => { el.scrollTop = el.scrollHeight; }", elemento_scrolleable)
            page.wait_for_timeout(1000)
            nueva_altura = elemento_scrolleable.evaluate("el => el.scrollHeight")
            if nueva_altura == altura_actual:
                break  """

def run():
    url_base = "https://pluto.tv" # url base de la plataforma de pluto
    
    with sync_playwright() as playwright:
        page = init_playwright(playwright)
        
        page.goto(url_base)

        ### espero hasta que el boton de la seccion on demand sea visible, luego lo presiono.

        page.wait_for_selector("a.l1-on-demand-atc",timeout=9000)
        button_on_demand = page.locator("a.l1-on-demand-atc")
        button_on_demand.scroll_into_view_if_needed()
        button_on_demand.click()

        
        ### ahora espero al div que me permite scrollear por sobre los programas

        page.wait_for_selector("div.custom-scroll.content-list",timeout=4000)
        div_programas = page.locator("div.custom-scroll.content-list")

        programas = set() # aca voy a agregar los elementos de la url de view all, donde par acada seccion puedo ver todos los programas al acceder a este.

        
        ### las películas y series tienen identificadores unicos, los cuales usare para distindir en el set, las peliculas de las series, ademas no dejare que se carguen otros programas
        id_series = "nada"
        id_movies = "nada"

                ### aca voy a iterar, para poder scrollear mientras se va cargando dinamicamente los programas
        for _ in range(55):

            div_cateogira = div_programas.locator("div.mainCategory")
            
            ## sentencia que define la variable id_movies y id_series en funcion del contenido
            if div_cateogira.count() == 1:
                if div_cateogira.inner_text().lower() == "películas":
                    id_movies = div_cateogira.get_attribute("data-id")
                if div_cateogira.inner_text().lower() == "series":
                    id_series = div_cateogira.get_attribute("data-id")

            # cada sección ya sea series o peliculas es tomado, para luego iterar sobre estas, y finalmente sacar el view all de cada seccion.
            secciones = div_programas.locator("section.category").all()


            for seccion in secciones:
                view_all_link = seccion.locator("a[class^='viewAllLink-0-2-']")
                if view_all_link.count() > 0 and (id_movies in view_all_link.get_attribute("href") or id_series in view_all_link.get_attribute("href")):
                    programas.add(url_base + view_all_link.get_attribute("href"))

            

            ## por ultimo realizo un scroll iterativo de pocos pixeles para que se vayan cargando , la altura es la del cuadro de cada programa.
            page.evaluate("() => { document.querySelector('div.custom-scroll.content-list').scrollTop += 200; }")
            page.wait_for_timeout(1000)



        ## aca voy a separar el link de view all entre series y peliculas en funcion de su id.
        series_and_movies_category = {"películas": [], "series": []} 
        for programa in programas:
            if id_movies in programa:
                series_and_movies_category["películas"].append(programa)
            else :
                series_and_movies_category["series"].append(programa)


        ## ahora quiero agregar el link de cada serie o pelicula a un diccionario
        series_and_movies = {"peliculas": [], "series": []} 

        ## para hacerlo itereo sobre los url de secciones, y generando un set
        
        for key,programa in series_and_movies_category.items():
            url_link = set()
            for link_programa in programa:
                ## primero voy a la pagina de la seccion.
                page.goto(link_programa)

                ## tomo el div que me permitira hacer el scroll
                page.wait_for_timeout(5000)
                div_container = page.locator("div#overlay-container")
                scroll_programs = div_container.locator("//div[contains(@class, 'container-0-2-') and contains(@class, 'custom-scroll')]")

                ## voy a hacer un blucle While True, ya que quiero scrollear la pagina siempre que se puede, y si la altura no cambia simplemente se corta el bucle
                while True:
                    
                    altura = scroll_programs.evaluate("el => el.scrollHeight")


                    ## dentro de esto selecciono todas las etiquetas li, para luego iterar y agregar los url de la etiqueta a dentro de esta para agregarla al set
                    page.wait_for_selector("li[class ^= 'itemContainer-0-2-']",timeout=2000)
                    programas = scroll_programs.locator("li[class ^= 'itemContainer-0-2-']").all()

                    for program in programas:
                        href = program.locator("a").get_attribute("href")
                        if href:
                            url_link.add(url_base + href)
                            
                    ## aqui realizo el scroll hasta el final del contenedor
                    page.evaluate("document.querySelector('div[class^=\"container-0-2-\"]').scrollTop += document.querySelector('div[class^=\"container-0-2-\"]').scrollHeight")

                    page.wait_for_timeout(1000)

                    ## condicion de corte para el while, cuando no se cambie la altura
                    nueva_altura = scroll_programs.evaluate("el => el.scrollHeight")

                    if nueva_altura == altura:
                        break

                    ## por ultimo agrego los url de cada pelicula o serie a un diccionario que sera el retornado por la funcion

            if key == "películas":
                for movie in url_link:
                    series_and_movies["peliculas"].append(movie)
            else:
                for movie in url_link:
                    series_and_movies["series"].append(movie)
        return series_and_movies

    


with open('mi_diccionario.json', 'w') as archivo_json:
    json.dump(run(), archivo_json, indent=4)

    

