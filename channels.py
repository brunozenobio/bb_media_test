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

    page.wait_for_load_state("domcontentloaded")



    programas_scroller = page.locator('//div[contains(@class,"channelList-0-2-") and contains(@class,"custom-scroll")]')
    canales_programas = {}

    # Desplazarse y obtener canales y programas
    for _ in range(60):

        div_canal = programas_scroller.locator("div.channel")
        link_canal = div_canal.locator("div.ChannelInfo-Link").get_attribute("href")



        print(link_canal)
        

        
        programas_scroller.evaluate("(el) => { el.scrollTop += 100; }", programas_scroller)
        page.wait_for_timeout(900)



    # Cerrar el navegador
    browser.close()
