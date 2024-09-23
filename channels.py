from playwright.sync_api import sync_playwright
import time

url_base = "https://pluto.tv"

with sync_playwright() as playwright:
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    # Navegar a la URL base
    page.goto(url_base)
    page.wait_for_load_state()

    button_feature = page.locator("//div[@data-id='live-tv-featured-category-id']").locator("button")

    button_feature.click()

    page.wait_for_timeout(400)

    programas_scroller = page.locator('//div[contains(@class,"channelList-0-2-") and contains(@class,"custom-scroll")]')
    canales_programas = {}

    # Desplazarse y obtener canales y programas
    for _ in range(60):
        # Obtener los canales visibles
        div_canales = programas_scroller.locator("div.channel").all()


        for canal in div_canales:

            a_canal = canal.locator("a.ChannelInfo-Link")

            nombre_canal = a_canal.locator("div.image").get_attribute("aria-label")
            url_canal = a_canal.get_attribute("href")

            # Inicializar la lista para los programas de este canal
            canales_programas[nombre_canal] = []

            url_programas_div = set()
            while True:
                # Agregar las URLs de los programas
                programas_locators = canal.locator(f"//a[contains(@href,'{url_canal}')]").all()
                
                for programa_locator in programas_locators:
                    url_programas_div.add(programa_locator)

                    # Obtener información del programa
                    metadata_programas = programa_locator.locator("//div[contains(@class,'timelineSkeletonContainer') and contains(@class,'timelineSkeletonContainer-0-2-')]")
                    
                    ## uso un bloque try catch ya que los programas en emision tienen clase distinta
                    try:
                        programa = metadata_programas.locator("span.name-item").inner_text()
                        try:
                            horario = metadata_programas.locator("//div[contains(@class,'time-0-2-') and contains(@class,'time')]").inner_text()
                        except:
                            try:
                                horario = metadata_programas.locator("//div[contains(@class,'remainderTime-0-2-') and contains(@class,'remainderTime')]").inner_text()
                            except Exception as e:
                                horario = "no disponible"
                        

                        # Agregar al diccionario
                        canales_programas[nombre_canal].append({"titulo": programa, "horario": horario})
                        print(f"Programa: {programa}, Horario: {horario}")
                    except Exception as e:
                        print(f"Error al obtener datos del programa: {e}")

                # Comprobar si hay más programas
                button_desplazar_derecha = page.locator("//button[contains(@class,'paginateRightButton-0-2-') and contains(@class,'paginateButton-0-2-')]")

                if button_desplazar_derecha.count() != 1 :
                    button_desplazar_izquierda = page.locator("//button[contains(@class,'paginateLeftButton-0-2-') and contains(@class,'paginateButton-0-2-')]")
                    while button_desplazar_izquierda.count() > 0:
                        button_desplazar_izquierda.click()
                        page.wait_for_timeout(500)


                    break
                
                # Desplazar si hay más programas
                button_desplazar_derecha.click()
                page.wait_for_timeout(500)

        # Desplazar hacia abajo en el scroller para cargar más canales
        programas_scroller.evaluate("(el) => { el.scrollTop += 100; }", programas_scroller)
        page.wait_for_timeout(900)

     # Mostrar el diccionario de programas por canal
    print(canales_programas)

    # Cerrar el navegador
    browser.close()
