
# Instalo las librerias necesarias
from selenium.webdriver.chrome.service import Service  # la clase servicio para usar el driver.

from selenium import webdriver # webdriver principal para usar Selenium
from webdriver_manager.chrome import ChromeDriverManager #el instalador del driver de chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with
import time


chrome_options = Options()
#chrome_options.add_argument("--headless")  # Modo headless
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-software-rasterizer")  


service = Service(ChromeDriverManager().install()) # instancio la clase servicio con el instalador de chrome

driver = webdriver.Chrome(service = service,options=chrome_options) # instancio Chrome con el servicio del driver

# creo una variable para la url de la web

url_base = "https://pluto.tv"

driver.get(url_base) # uso el metodo get para empear el scrapping

time.sleep(5) # dejo cargar la pagina


###### Series Y Peliculas

# busco la seccion on_demand donde estan todas las series y peliculas, espero que cargue y hago click

on_demand_button = driver.find_element(By.XPATH,'//a[@class="l1-on-demand-atc"]')
on_demand_button.click()

time.sleep(3)



botones_tipo_programa = driver.find_elements(By.XPATH,'//button[@class="iconButton-0-2-243 iconButton"]')

# busco el boton de peliculas y hago click en el

for boton in botones_tipo_programa:
    if boton.text.lower() == "películas":
        boton.click()
        time.sleep(3)
        
        on_demand = driver.find_element(By.XPATH,'//section[@class="catalogContainer-0-2-320"]')
        print(on_demand.text)
        break



"""
section_categorias = []

bandera = True
while bandera:
    sections = driver.find_elements(By.XPATH,'//section[@class="contentListRow-0-2-329 category"]')
    for section in sections:
        if section not in section_categorias:
            section_categorias.append(section)
        try:
            div = section.find_element(locate_with(By.TAG_NAME,'div').below())
            if  div:
                print("No hay mas peliculas")
                bandera = False
                break
        except:
            continue
    driver.execute_script("window.scrollTo(0,100);")
    time.sleep(2) """