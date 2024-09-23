from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import json
import re


def get_data(url):
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        try:
            page.goto(url)

            page.wait_for_load_state("domcontentloaded")

            page.wait_for_selector("div.inner")


            div_programa = page.locator("div.inner")




            if "movies" in url:

                movie = get_movie(div_programa)
                movie["url"] = url
                return "movie",movie

            elif "series" in url:

                serie = get_serie(page,div_programa)
                serie["url"] = url
                print(serie)
                return "serie",serie

        except Exception as e:
            print(f"Error al procesar {url}: {e}")

        finally:
            browser.close()





def get_movie(div_programa):
    """
    Esta funcion, la informacion de una pelicula

    Parametros:
        div_programa(locator) El div inicial que tiene la informacion de la pelicula
    Retorna: Diccionario con la informacion de la pelicula

    
    """
    
    titulo = div_programa.locator("h2").inner_text() if div_programa.locator("h2").count() > 0  else "N/A" # titulo de la pelicula
    
    

    caracteristicas = div_programa.locator("div").all() # div con las caracteristicas

    caracteristicas_lista = caracteristicas[0].locator("li").all() # en esta lista estaran las caracteristicas rating,duracion genero
    

    if len(caracteristicas_lista) >= 2:
        rating = caracteristicas_lista[0].locator("span.rating").inner_text() if caracteristicas_lista[0].locator("span.rating").count() > 0 else "N/A" # saco rating de un span, en el primer li encontrado
        genero = caracteristicas_lista[2].inner_text() # saco el genero en el 3 li encontrado

        # aqui saco la duracion en horas en el 5 li, y luego proceso para trasnformarla a minutos
        duracion_horas = caracteristicas_lista[4].inner_text() 
        extract_horas = re.search(r"(\d*)hr[ ]*(\d*)[ min]*",duracion_horas)
        print(extract_horas)
    else:
        rating = "N/A"
        genero = "N/A"
        extract_horas = None

    duracion_movie = 0
    if extract_horas:
        horas = extract_horas.group(1)
        minutos = extract_horas.group(2)
        if horas is not None:
            duracion_movie += int(horas) * 60
        if minutos is not None:
            duracion_movie += int(minutos) if minutos else 0

    print(duracion_movie)
    

    # del segun div de caracteristicas busco la etiquet p que tiene la sinopsis
    sinopsis = caracteristicas[1].locator("p").inner_text()

    return {"title":titulo,"genre":genero,"classification":rating,"duration(min)":duracion_movie,"synopsis":sinopsis}


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

        rating = caracteristicas[0].locator("span.rating").inner_text() if caracteristicas[0].locator("span.rating").count() > 0 else "N/A"
        genero = caracteristicas[2].inner_text()

        temporadas_text = re.search(r"\d+",caracteristicas[6].inner_text())

    else:
        rating = "N/A"
        genero = "N/A"
        temporadas_text = None

    if temporadas_text:
        temporadas = int(temporadas_text.group(0))
    else:
        temporadas = 0


    print(temporadas)

    sinopsis = div_programa.locator("//section[contains(@class,'description-0-2-')]").locator("p").inner_text()

    ## buscar los capitulos

    temporadas_total = get_chapters(page,div_programa)

    return {"title":titulo,"genre":genero,"classification":rating,"seasons":temporadas,"synopsis":sinopsis,"seasons":temporadas_total}







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
            duracion_min = int(re.search(r"\d"),duracion)

            episodios.append({"episode":num_episodio,"duration(min)":duracion_min,"url_episode":url})

        temporadas.append({'season':selector_temporadas.inner_text(),"episodes":episodios})

    return temporadas

        


def get_series_movies(datos):

    """
    Esta funcion a partir de los datos que recibe, retorna dos listas asociadas a todas las series y peliculas, trabaja con ThreadPoolExecutor para ejecutar multitareas.
    Patametros:
        datos(list) : lista con los url de series y peliculas
    Retorna:
        tupla con las listas de series y diccionarios
    """
    
    
    movies = []
    series = []

    with ThreadPoolExecutor(max_workers=5) as executor: ## clase para trabajar con multihilos
        futures = [executor.submit(get_data, valor) for key, valores in datos.items() for valor in valores]

        for i, future in enumerate(as_completed(futures), 1):
            try:
                programa = future.result()
                if programa[0] == "movie":
                    movies.append(programa[1])
                elif programa[0] == "serie":
                    series.append(programa[1])
            

            except Exception as exc:
                print(f'Error: {exc}')
                

    return movies,series

if __name__ == "__main__":
    with open('mi_diccionario.json', 'r') as archivo_json:
        datos = json.load(archivo_json)

    resultado = get_series_movies(datos)
    with open("movies.json", "w") as json_file:
        json.dump(resultado[0], json_file, indent=4)
    with open("series.json", "w") as json_file:
        json.dump(resultado[1], json_file, indent=4)
