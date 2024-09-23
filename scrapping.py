from scripts.get_on_demand import *
import time
from scripts.init_pluto_tv import *
from scripts.get_series_movies import * 
from scripts.get_channels import *


def scrape_pluto_tv_data():

    url_base = "https://pluto.tv"
    tiempo_inicial = time.time()

    print("=======Inicia la ejecución=======")

    # iniciamos pluto
    page, browser, playwright = init_playwright()
    init_pluto(page, url_base)

    # obtenemos las secciones de peliculas y series
    goto_on_demand(page)
    programas = get_url_secciones(page, url_base)
    print(f"Se obtuvieron {len(programas)} secciones en {time.time() - tiempo_inicial:.2f} segundos")

    # se obtienen los url de cada serie y pelicula
    series_movies = get_url_series_movies(page, programas, url_base)
    browser.close()
    playwright.stop()

    
    tiempo_medio = time.time()
    print(f"Se obtuvieron {len(series_movies)} series y películas en {tiempo_medio - tiempo_inicial:.2f} segundos")

   # para cada serie y pelicula obtenemos la data
    movies, series = get_series_movies(series_movies)

    # se guardan los datos
    print("Guardando películas y series...")
    write_json(movies=movies, series=series)
    tiempo_series_and_movies = time.time()
    print(f"Tiempo en guardar todas las películas y series: {tiempo_series_and_movies - tiempo_inicial:.2f} segundos")

    # se obtienen todos los canales
    print("Cargando los canales...")
    name_channel, url_channel = get_canales(url_base)
    df_channels = channel_to_pandas(url_channel, name_channel)
    print(f"Se obtuvieron {len(df_channels)} canales en {time.time() - tiempo_inicial:.2f} segundos")

    # se guardan en la base de datos
    print("Guardando canales...")
    write_channels(df_channels)
    tiempo_canales = time.time()
    print(f"Tiempo en guardar todos los canales: {tiempo_canales - tiempo_series_and_movies:.2f} segundos")

    # se calcula el tiempo final del script
    tiempo_final = time.time()
    print(f"Tiempo total de ejecución: {tiempo_final - tiempo_inicial:.2f} segundos")
    print("======Ejecución finalizada=======")


if __name__ == "__main__":
    scrape_pluto_tv_data()
