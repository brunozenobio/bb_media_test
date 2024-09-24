from playwright.sync_api import sync_playwright, Playwright




def init_playwright():
    """"
    Inicializa Playwright y crea un contexto de navegador.
    """
    playwright = sync_playwright().start()
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    page = context.new_page()
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    """)
    page.wait_for_load_state()
    return page, browser, playwright


def init_pluto(page,url):
    """
    Esta funcion, inicializa la pagina de pluto tv.
        Parametros:
            page() : metodo new_page() de la clase browser
            url(string) : url base de la pagina de pluto

    
    """
    page.goto(url) # va a la pagina
    page.wait_for_load_state() #espera que se cargue