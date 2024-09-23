from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import json



def get_data(url):
    programa = {}
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

            page.wait_for_load_state()

            div_programa = page.locator("div.inner")


            if "movies" in url:
                
                titulo = div_programa.locator("h2").inner_text() if div_programa.locator("h2") else "N/A"
                print(f"pelicula {titulo} ")
                caracteristicas = div_programa.locator("div").all()
                sinopsis = caracteristicas[1].locator("p").inner_text() if len(caracteristicas) > 1 else "Sin sinopsis disponible"

            elif "series" in url:
                caracteristicas = div_programa.locator("div").all()
                titulo = caracteristicas[0].inner_text() if len(caracteristicas) > 1 else "N/A"
                sinopsis = div_programa.locator("section").locator("p").all()[0].inner_text() if len(div_programa.locator("section").locator("p").all()) > 0 else "N/A"

            programa[titulo] = {"genero": caracteristicas, "sinopsis": sinopsis}

        except Exception as e:
            print(f"Error al procesar {url}: {e}")

        finally:
            browser.close()

    return programa

def get_series_movies(datos):
    serie_and_movie = {}
    cantidad_error = 0  #cantidad de errores
    total = sum(len(valores) for valores in datos.values())  # cantidad de urls

    with ThreadPoolExecutor(max_workers=4) as executor: ## clase para trabajar con multihilos
        futures = [executor.submit(get_data, valor) for key, valores in datos.items() for valor in valores]

        for i, future in enumerate(as_completed(futures), 1):
            try:
                programa = future.result()
                serie_and_movie.update(programa)
            except Exception as exc:
                print(f'Error: {exc}')
                cantidad_error += 1  # si da error se incrementa

            # Imprimir estado actual
            cantidad_sin_error = i - cantidad_error
            print(f'Iteración {i}/{total} - Sin errores: {cantidad_sin_error}, Errores: {cantidad_error}')

    return serie_and_movie

if __name__ == "__main__":
    with open('mi_diccionario.json', 'r') as archivo_json:
        datos = json.load(archivo_json)

    resultado = get_series_movies(datos)
    print(resultado)
