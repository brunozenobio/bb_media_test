
from playwright.sync_api import sync_playwright

## libreria para el trabajo en multiprocesos
from concurrent.futures import ThreadPoolExecutor, as_completed

# libreria que inicia pluto
from scripts.init_pluto_tv import *

#librerias para el guardado y manejo de datos, json,pandas re(extraer patrones)
import json
import re
import pandas as pd

def get_data(url):
    """
    Esta funcion se encarga de buscar una pelicula o serie a traves del id del link

    Parametros:
        url(str) Url del programa

    Retorna:
        tupla : donde el primer valor es un string asociado a si es "serie" o "pelicula" y el segundo el diccionario con los datos
     """
    page, browser, playwright = init_playwright() # inicializo platwright
    

    try: 
        # abro el url y espero a que cargue
        init_pluto(page,url) 

        page.wait_for_load_state("domcontentloaded")

        page.wait_for_selector("div.inner")


        div_programa = page.locator("div.inner")



        #en funcion de si movies o series esta en url se obtienen los datos de funciones distintas
        if "movies" in url:

            movie = get_movie(div_programa)
            movie["url"] = url
            return "movie",movie

        elif "series" in url:

            serie = get_serie(page,div_programa)
            serie["url"] = url

            return "serie",serie

    except Exception as e:
        print(f"Error al procesar {url}: {e}")

    finally:
        browser.close()
        playwright.stop()





def get_movie(div_programa):
    """
    Esta funcion, la informacion de una pelicula

    Parametros:
        div_programa(locator) El div inicial que tiene la informacion de la pelicula
    Retorna: Diccionario con la informacion de la pelicula

    
    """
    
    ## asigno los valores de titulo,rating,genero,duracion, si estos no estan se pone N/A

    titulo = div_programa.locator("h2").inner_text() if div_programa.locator("h2").count() > 0  else "N/A" # titulo de la pelicula
    
    

    caracteristicas = div_programa.locator("div").all() # div con las caracteristicas

    caracteristicas_lista = caracteristicas[0].locator("li").all() # en esta lista estaran las caracteristicas rating,duracion genero
    

    if len(caracteristicas_lista) >= 2:
        if caracteristicas_lista[0].locator("span.rating").count() > 0:
            rating = caracteristicas_lista[0].locator("span.rating").inner_text() # saco rating de un span, en el primer li encontrado
            genero = caracteristicas_lista[2].inner_text() # saco el genero en el 3 li encontrado

            # aqui saco la duracion en horas en el 5 li, y luego proceso para trasnformarla a minutos
            duracion_horas = caracteristicas_lista[4].inner_text() 
        else:
            rating = "N/A"
            genero = caracteristicas_lista[0].inner_text() # saco el genero en el 3 li encontrado

            # aqui saco la duracion en horas en el 5 li, y luego proceso para trasnformarla a minutos
            duracion_horas = caracteristicas_lista[2].inner_text() 


    else:
        rating = "N/A"
        genero = "N/A"
        duracion_horas = "N/A"


    # del segun div de caracteristicas busco la etiquet p que tiene la sinopsis
    sinopsis = caracteristicas[1].locator("p").inner_text()

    return {"title":titulo,"genre":genero,"classification":rating,"duration":duracion_horas,"synopsis":sinopsis}


def get_serie(page,div_programa):

    """
    Esta funcion, la informacion de una serie

    Parametros:
        div_programa(locator) El div inicial que tiene la informacion de la serie
    Retorna: Diccionario con la informacion de la serie

    
    """
 
    div_information = div_programa.locator("div").all() 

    titulo = div_information[0].inner_text() if div_information[0].count() > 0  else "N/A"


    caracteristicas = div_information[1].locator("li").all()

    if len(caracteristicas) >= 2:

        if caracteristicas[0].locator("span.rating").count() > 0:
            rating = caracteristicas[0].locator("span.rating").inner_text()
            genero = caracteristicas[2].inner_text()


        else:
            rating =  "N/A"
            genero = caracteristicas[0].inner_text()



    else:
        rating = "N/A"
        genero = "N/A"






    sinopsis = div_programa.locator("//section[contains(@class,'description-0-2-')]").locator("p").inner_text()

    ## buscar los capitulos

    temporadas_total = get_chapters(page,div_programa) # esta funcion retorna una lista con los cpaitulos y temporadas, que luego es asignada a seasons
 
    return {"title":titulo,"genre":genero,"classification":rating,"synopsis":sinopsis,"seasons":temporadas_total}







def get_chapters(page,div_programa):
    """
     Esta funcion se en  carga de para cada serie, navegar y obtener todos sus episodios

     Parametros:
        url_base(string) : url base de pluto
        page(): del metodo de browser
        div_programa(locator): elemento locator de page
    return:
        Lista de diccionarios con los episodios de la serie 
        
        
    """


    url_base = " https://pluto.tv"
     
    selector_temporadas = div_programa.locator("select") # tomo el selector

    opciones = selector_temporadas.locator("option").all() # del selector tomo todas las opciones
    
    # las tempordas seran guardados en una lista de diccionarios con dos elementos temporada, episodios donde episodios es una lista de diccionario con cada episodio
    temporadas = []


    # itero sobre las opciones para guardar las temporadasw
    for opcion in opciones:

        selector_temporadas.select_option(opcion.get_attribute("value")) # elijo la opcion en curso
        page.wait_for_load_state() 

        li_episodios = div_programa.locator("li.episode-container-atc").all()

        
        episodios = [] 
        for episodio in li_episodios:
            info_episodio = episodio.locator("a")
            url = url_base + info_episodio.get_attribute("href")
            num_episodio = info_episodio.locator("h3.episode-name-atc").inner_text()
            duracion = info_episodio.locator("p.numbers").locator("span").all()[1].inner_text()
            sinopsis_episodio = info_episodio.locator("p.episode-description-atc").inner_text() if info_episodio.locator("p.episode-description-atc").count() > 0 else "N/A"


            episodios.append({"episode":num_episodio,"duration":duracion,"synopsis_episode":sinopsis_episodio,"url_episode":url})

        temporadas.append({'season':opcion.inner_text(),"episodes":episodios})

    return temporadas

        


def get_series_movies(datos):

    """
    Esta funcion a partir de los datos que recibe, retorna dos listas asociadas a todas las series y peliculas, trabaja con ThreadPoolExecutor para ejecutar multitareas.
    Patametros:
        datos(list) : lista con los url de series y peliculas
    Retorna:
        tupla con las listas de series y diccionarios
    """
    
    
    movies = pd.DataFrame(columns = ['title', 'genre', 'classification', 'duration', 'synopsis','url'])
    series = []

    with ThreadPoolExecutor(max_workers=5) as executor: ## clase para trabajar con multihilos
        futures = [executor.submit(get_data, url) for url in datos]

        for _, future in enumerate(as_completed(futures), 1):
            try:
                programa = future.result()
                if programa[0] == "movie":
                    movies.loc[len(movies)] = programa[1]
                elif programa[0] == "serie":
                    series.append(programa[1])
            

            except Exception as exc:
                print(f'Error: {exc}')
                

    return movies,series


def write_json(movies,series):
    movies.to_csv("./database/movies.csv",index=False)
    with open("./database/series.json", "w",encoding='utf-8') as json_file:
        json.dump(series, json_file,ensure_ascii=False, indent=5)


    
