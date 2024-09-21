from playwright.sync_api import sync_playwright, Playwright
import time
def run(playwright: Playwright):
    url_base = "https://pluto.tv"


    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url_base)

    page.wait_for_selector("a.l1-on-demand-atc",timeout=9000)
    button_on_demand = page.locator("a.l1-on-demand-atc")
    button_on_demand.scroll_into_view_if_needed()
    button_on_demand.click()

    


    page.wait_for_selector("div.custom-scroll.content-list",timeout=4000)
    div_movies = page.locator("div.custom-scroll.content-list")

    movies = set()
    
    clase = "nada"
    for _ in range(55):
        if div_movies.locator("div.mainCategory").count() > 0 :
            if div_movies.locator("div.mainCategory").inner_text().lower() == "películas":
                clase  = "películas"
            
            elif div_movies.locator("div.mainCategory").inner_text().lower() == "series":
                clase = "series"
            else:
                clase = "nada"

        if clase == "películas":
            movies.add(div_movies.locator("section.category"))

        




        page.evaluate("() => { document.querySelector('div.custom-scroll.content-list').scrollTop += 150; }")
        page.wait_for_timeout(500)

    print(len(list(movies)))


    browser.close()

with sync_playwright() as playwright:
    run(playwright)