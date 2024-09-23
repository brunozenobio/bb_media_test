from scripts.get_on_demand import *
import time
from scripts.init_pluto_tv import *
from scripts.get_series_movies import * 


def run():

    url_base = "https://pluto.tv"

    tiempo_inicial = time.time()

    print("=======Inicia la ejecución=======")

    ### obtención de series y peliculas


    # iniciamos playwright en pluto
    page, browser, playwright = init_playwright()
    
    init_pluto(page, url_base)

    ## obtenemos la  lista de pelicukas y series unicas.
    goto_on_demand(page)
    programas = get_url_secciones(page, url_base)
    series_movies = get_url_series_movies(page, programas, url_base)

    browser.close()  # Cerramos el navegador al finalizar
    playwright.stop()  # Detenemos Playwright para evitar el error del loop

    time_medio = time.time()
    print(f"Tiempo hasta obtener la lista de peliculas y series {time_medio - tiempo_inicial}")
    
    ## obtenemos los json de series y peliculas y las guardamos
    movies,series = get_series_movies(series_movies)
    write_json(movies=movies,series=series)

    tiempo_series_and_movies = time.time()

    print(f"Tiempo en guardar todas las peliculas y series {tiempo_series_and_movies - tiempo_inicial}" )


    ### canales



    tiempo_final = time.time()
    print(f"Tiempo final de la ejecución {tiempo_final - tiempo_inicial}")


run()