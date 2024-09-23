from init_pluto_tv import *
from get_series_movies import * 
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


def run():
    page, browser, playwright = init_playwright()
    url_base = "https://pluto.tv"
    init_pluto(page, url_base)
    goto_on_demand(page)

    programas = get_url_secciones(page, url_base)
    series_movies = get_url_series_movies(page, programas, url_base)



    browser.close()  # Cerramos el navegador al finalizar
    playwright.stop()  # Detenemos Playwright para evitar el error del loop

    print(len(series_movies))
    movies,series = get_series_movies(series_movies)

    write_json(movies=movies,series=series_movies)

run()


