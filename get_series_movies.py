from playwright.async_api import async_playwright
import asyncio
import json

async def get_data(url):
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)

        # Usa wait_for_selector en lugar de un timeout
        await page.wait_for_selector("div.inner")

        div_programa = page.locator("div.inner")
        programa = {}

        print(url)

        if "movies" in url:
            titulo = div_programa.locator("h2").inner_text() if div_programa.locator("h2") else "N/A"
            metadata = div_programa.locator("div").all()
            caracteristicas = metadata[0].locator("li:not([class])").all()
            sinopsis = metadata[1].locator("p").inner_text() if len(metadata) > 1 else "Sin sinopsis disponible"

        elif "series" in url:
            metadata = div_programa.locator("div").all()
            titulo = metadata[0].inner_text() if len(metadata) > 1 else "N/A"
            caracteristicas = metadata[1].locator("li:not([class])").all() if len(metadata) > 0 else "N/A"
            sinopsis = div_programa.locator("section").all()[0].locator("p").inner_text() if len(div_programa.locator("section").locator("p").all()) > 0 else "N/A"

        print(titulo)
        programa[titulo] = {"genero": caracteristicas, "sinopsis": sinopsis}
        
        await browser.close()  # Cierra el navegador después de usarlo
        return programa

async def get_series_movies(datos):
    serie_and_movie = {}
    tasks = []

    for key, valores in datos.items():
        for valor in valores:
            tasks.append(get_data(valor))  # Agrega tareas a la lista

    results = await asyncio.gather(*tasks)  # Ejecuta todas las tareas concurrentemente

    for programa in results:
        serie_and_movie.update(programa)

    return serie_and_movie

if __name__ == "__main__":
    with open('mi_diccionario.json', 'r') as archivo_json:
        datos = json.load(archivo_json)

    resultado = asyncio.run(get_series_movies(datos))
    print(resultado)
