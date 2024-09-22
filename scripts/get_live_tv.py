from init_pluto_tv import *

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