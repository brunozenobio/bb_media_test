from playwright.sync_api import sync_playwright, Playwright
import time
import re
import json


## usare la libreria de playwright



def init_playwright(playwright: Playwright):
    """"
    Esta funcion, se encarga de inicializar un contexto de pagina para realizar el scrapping
    
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        return page


def init_pluto(page,url):
    """
    Esta funcion, inicializa la pagina de pluto tv.
        Parametros:
            page() : metodo new_page() de la clase browser
            url(string) : url base de la pagina de pluto

    
    """
    page.goto(url) # va a la pagina
    page.wait_for_load_state('networkidle') #espera que se cargue


##### On Demand######
def goto_on_demand(page):
    """
    Esta funcion,hace click enb la seccion on demand de pluto tv.
        Parametros:
            page() : metodo new_page() de la clase browse
    """


    page.wait_for_selector("a.l1-on-demand-atc",timeout=9000)
    button_on_demand = page.locator("a.l1-on-demand-atc")
    button_on_demand.scroll_into_view_if_needed()
    button_on_demand.click()



def get_url_secciones(page,url_base):
    """
    Esta funcion, scrollea por las secciones y obtiene los url de cada seccion.
        Parametros:
            page() : metodo new_page() de la clase browser
            url_base(string) : url base de la pagina de pluto

        return:
            programas(set) : un set con las url unicas de cada seccion de series y peliculas

    """
    page.wait_for_selector("div.custom-scroll.content-list",timeout=4000)
    div_programas = page.locator("div.custom-scroll.content-list")

    programas = set() # aca voy a agregar los elementos de la url de view all, donde par acada seccion puedo ver todos los programas al acceder a este.

        
    ###las películas y series tienen identificadores unicos, los cuales usare para distindir en el set, las peliculas de las series, ademas no dejare que se carguen otros programas
    id_series = "nada"
    id_movies = "nada"


    ### ACA VOY A SCROLLEAR EN LA SECCION ON DEMAND, PARA EXTRAER EL VIEW ALL LINK DE CADA SECCION
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


        ## Agrego a los programas solo series y peliculas
        for seccion in secciones:
            view_all_link = seccion.locator("a[class^='viewAllLink-0-2-']")
            if view_all_link.count() > 0 and (id_movies in view_all_link.get_attribute("href") or id_series in view_all_link.get_attribute("href")):
                programas.add(url_base + view_all_link.get_attribute("href"))

            

        ## por ultimo realizo un scroll iterativo de pocos pixeles para que se vayan cargando , la altura es la del cuadro de cada programa.
        page.evaluate("() => { document.querySelector('div.custom-scroll.content-list').scrollTop += 200; }")
        page.wait_for_timeout(700)

    return programas
    
def get_url_series_movies(page,programas,url_base):

    """
    Esta funcion, por cada url de seccion navega y toma todos los url de series y peliculas .
        Parametros:
            page() : metodo new_page() de la clase browser
            progrmas(set): un set con las url unicas de cada seccion
            url_base(string) : url base de la pagina de pluto

        return:
            series_and_movies(list) : una lista con los url de  series y peliculas.

    """

    ## ahora quiero agregar el link de cada serie o pelicula a una lista
    series_and_movies = []

    ## A PARTIR DE  TODAS LAS SECCIONES OBTENCIÓN DE LOS URL SERIES Y PELICULAS
            
    for link_programa in programas:  #itero sobre los enlaces de view all
        url_link = set()  # sset para guardar los links sin duplicados
        page.goto(link_programa)
            
        ##tomo el div que me permitira ahcer el scoll
        page.wait_for_timeout(5000)
        div_container = page.locator("div#overlay-container")
        scroll_programs = div_container.locator("//div[contains(@class, 'container-0-2-') and contains(@class, 'custom-scroll')]")
            
        ## Bucle para hacer scroll en la página y obtener todos los enlaces
        while True:
            altura = scroll_programs.evaluate("el => el.scrollHeight")

            # Selecciono todas las etiquetas <li> que contienen los enlaces
            page.wait_for_selector("li[class ^= 'itemContainer-0-2-']", timeout=2000)
            programas = scroll_programs.locator("li[class ^= 'itemContainer-0-2-']").all()

            for program in programas:
                href = program.locator("a").get_attribute("href")
                if href:
                    url_link.add(url_base + href)

            ## Scroll hasta el final del contenedor
            page.evaluate("document.querySelector('div[class^=\"container-0-2-\"]').scrollTop += document.querySelector('div[class^=\"container-0-2-\"]').scrollHeight")
            page.wait_for_timeout(1000)

            ## Condición de corte cuando la altura no cambie
            nueva_altura = scroll_programs.evaluate("el => el.scrollHeight")
            if nueva_altura == altura:
                break

        ## Agrego los enlaces obtenidos a la lista final
        for movie_link in url_link:
            series_and_movies.append(movie_link)

    return series_and_movies    
    

#### Live TV#####

def get_canales(page):
    """
    Esta funcion, por cada url de seccion navega y toma todos los url de series y peliculas .
        Parametros:
            page() : metodo new_page() de la clase browser

        return:
            canales(set) : todos los canales unicos.

    """
    programas_scroller = page.locator('//div[contains(@class,"channelList-0-2-") and contains(@class,"custom-scroll")]')
    canales = set()

    # Recorrer los canales
    for _ in range(60):
        div_canales = programas_scroller.locator('//div[contains(@class,"channelListItem-0-2-") and contains(@class,"channel")]').all()

        for canal in div_canales:
            canales.add(canal)

        # Desplazar hacia abajo en el scroller
        programas_scroller.evaluate("(el) => { el.scrollTop += 100; }", programas_scroller)
        page.wait_for_timeout(900)

        return canales
    
def get_grilla(page,canales,url_base):
    """
    Esta funcion, por cada url de seccion navega y toma todos los url de series y peliculas .
        Parametros:
            page() : metodo new_page() de la clase browser
            canales(set) : canales unicos
            url_base(string) url base de pluto

        return:
            canales(set) : todos los canales unicos.

    """
    for canal in canales:
        a_canal = canal.locator("a.ChannelInfo-Link")
        nombre_canal = a_canal.locator("div.image").get_attribute("aria-label")
        url_canal = url_base + a_canal.get_attribute("href")

        print(f"Nombre del canal: {nombre_canal}, URL: {url_canal}")

        url_programas_div = set()
        while True:
            # Agregar las URLs de los programas
            url_programas_div.add(canal.locator(f"//a[contains(@href,'{url_canal}')]").all())
            for url_canal_div in url_programas_div:
                url = a_canal.get_attribute("href")
                metadata_programas = url_canal_div.locator("//div[contains(@class,'timelineSkeletonContainer') and contains(@class,'timelineSkeletonContainer-0-2-')]")
                
                # Obtener información del programa
                try:
                    programa = metadata_programas.locator("span.name-item").inner_text()
                    horario = metadata_programas.locator("//div[contains(@class,'time-0-2-') and contains(@class,'time')]").inner_text()
                    print(f"Programa: {programa}, Horario: {horario}")
                except Exception as e:
                    print(f"Error al obtener datos del programa: {e}")

            # Comprobar si hay más programas
            button_desplazar = page.locator("//button[contains(@class,'paginateRightButton-0-2-') and contains(@class,'paginateButton-0-2-')]")

            if button_desplazar.count() != 1:
                break
            
            # Desplazar si hay más programas
            button_desplazar.click()
            page.wait_for_timeout(800)






def run():
    page = init_playwright(playwright=Playwright)
    url_base = "https://pluto.tv" # url base de la plataforma de pluto
    init_pluto(page,url_base)
    goto_on_demand(page)

    programas = get_url_secciones(page,url_base)

    series_movies = get_url_series_movies(page,programas,url_base)

    return series_movies

print(run())



"""def run():
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

        
        ###las películas y series tienen identificadores unicos, los cuales usare para distindir en el set, las peliculas de las series, ademas no dejare que se carguen otros programas
        id_series = "nada"
        id_movies = "nada"


        ### ACA VOY A SCROLLEAR EN LA SECCION ON DEMAND, PARA EXTRAER EL VIEW ALL LINK DE CADA SECCION
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


            ## Agrego a los programas solo series y peliculas
            for seccion in secciones:
                view_all_link = seccion.locator("a[class^='viewAllLink-0-2-']")
                if view_all_link.count() > 0 and (id_movies in view_all_link.get_attribute("href") or id_series in view_all_link.get_attribute("href")):
                    programas.add(url_base + view_all_link.get_attribute("href"))

            

            ## por ultimo realizo un scroll iterativo de pocos pixeles para que se vayan cargando , la altura es la del cuadro de cada programa.
            page.evaluate("() => { document.querySelector('div.custom-scroll.content-list').scrollTop += 200; }")
            page.wait_for_timeout(700)



        ## ahora quiero agregar el link de cada serie o pelicula a una lista
        series_and_movies = []

        ## A PARTIR DE  TODAS LAS SECCIONES OBTENCIÓN DE LOS URL SERIES Y PELICULAS
            
        for link_programa in programas:  #itero sobre los enlaces de view all
            url_link = set()  # sset para guardar los links sin duplicados
            page.goto(link_programa)
            
            ##tomo el div que me permitira ahcer el scoll
            page.wait_for_timeout(5000)
            div_container = page.locator("div#overlay-container")
            scroll_programs = div_container.locator("//div[contains(@class, 'container-0-2-') and contains(@class, 'custom-scroll')]")
            
            ## Bucle para hacer scroll en la página y obtener todos los enlaces
            while True:
                altura = scroll_programs.evaluate("el => el.scrollHeight")

                # Selecciono todas las etiquetas <li> que contienen los enlaces
                page.wait_for_selector("li[class ^= 'itemContainer-0-2-']", timeout=2000)
                programas = scroll_programs.locator("li[class ^= 'itemContainer-0-2-']").all()

                for program in programas:
                    href = program.locator("a").get_attribute("href")
                    if href:
                        url_link.add(url_base + href)

                ## Scroll hasta el final del contenedor
                page.evaluate("document.querySelector('div[class^=\"container-0-2-\"]').scrollTop += document.querySelector('div[class^=\"container-0-2-\"]').scrollHeight")
                page.wait_for_timeout(1000)

                ## Condición de corte cuando la altura no cambie
                nueva_altura = scroll_programs.evaluate("el => el.scrollHeight")
                if nueva_altura == altura:
                    break

            ## Agrego los enlaces obtenidos a la lista final
            for movie_link in url_link:
                series_and_movies.append(movie_link)

    return series_and_movies    """

    

