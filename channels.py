from playwright.sync_api import sync_playwright
import time

url_base = "https://pluto.tv"

with sync_playwright() as playwright:
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    # Navegar a la URL base
    page.goto(url_base)
    page.wait_for_timeout(5000)

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

    print(f"Canales encontrados: {len(canales)}")

    # Diccionario para almacenar programas de cada canal
    canales_programas = {}

    for canal in canales:
        a_canal = canal.locator("a.ChannelInfo-Link")
        nombre_canal = a_canal.locator("div.image").get_attribute("aria-label")
        url_canal = url_base + a_canal.get_attribute("href")

        print(f"Nombre del canal: {nombre_canal}, URL: {url_canal}")

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
                
                try:
                    programa = metadata_programas.locator("span.name-item").inner_text()
                    horario = metadata_programas.locator("//div[contains(@class,'time-0-2-') and contains(@class,'time')]").inner_text()
                    # Agregar al diccionario
                    canales_programas[nombre_canal].append({"titulo": programa, "horario": horario})
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

    # Mostrar el diccionario de programas por canal
    print(canales_programas)

    # Cerrar el navegador
    browser.close()
