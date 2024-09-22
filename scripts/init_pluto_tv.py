from playwright.sync_api import sync_playwright, Playwright




def init_playwright(playwright: Playwright):
    """"
    Esta funcion, se encarga de inicializar un contexto de pagina para realizar el scrapping
    
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        return page


def init_pluto(page,url):
    """
    Esta funcion, inicializa la pagina de pluto tv.
        Parametros:
            page() : metodo new_page() de la clase browser
            url(string) : url base de la pagina de pluto

    
    """
    page.goto(url) # va a la pagina
    page.wait_for_load_state('networkidle') #espera que se cargue