

# Prueba Tenica 


## **Tabla de Contenidos**

- [Introducción](#introducción)
- [Desarrollo](#desarrollo)
- [Instalación](#instalación)
- [Conclusión](#conclusión)
- [Contacto](#contacto)

## **Tecnolgías usadas**

![](https://img.shields.io/badge/Python-grey?style=for-the-badge&logo=python)
![](https://img.shields.io/badge/playwright%201.47.0-blue?style=for-the-badge)
![](https://img.shields.io/badge/pandas%202.2.3-blue?style=for-the-badge&logo=)




---

# Introducción

A continuación, se explicará el proyecto realizado para la prueba técnica. El objetivo era hacer web scraping en la página de Pluto TV, y extraer todas las películas y series junto a su metadata, así como todos los canales.

Es un plus obtener más datos de cada sección, como episodios por serie y grilla de canales, que el código se ejecute en menos de 2 horas, identificar modelos de negocio y hacer análisis y/o procesamiento de los datos.



---

# Desarrollo


Para esto, se ha usado la librería **`Playwright`**, que permite hacer scraping en sitios web flexibles e interactivos, lo cual fue esencial para realizar esta tarea. También, para lograr la mayor optimización del tiempo de scraping, se utilizó la librería de Python base **`concurrentt`**, que me permitió trabajar en hilos y cargar conjuntamente muchas películas y series.

### Entorno de codigo

El script principal que ejecuta todo el proceso es [scrapping.py](./scrapping.py),este se encarga de realizar las siguientes tareas:
- **`realizar la obtención de series y peliculas`**: Para en la carpeta [scripts](./scripts/), estan todos los scripts necesarios para realizar esas tareas:
    - [init_pluto_tv.py](./scripts/init_pluto_tv.py) : Inicia Playwright y abre un enlace
    - [get_series_demand.py](./scripts/get_on_demand.py) : Con pluto iniciado va a la seccion On Demand, y obtiene los enlaces de todas las series y películas.

    - [get_series_movies.py](./scripts/get_series_movies.py) : Para cada serie y película, guarda las peliculas en un csv y las series con sus episodios en un json.

    - [get_channels](./scripts/get_channels.py) : Obtiene todos los canales y sus url y los guarda en un csv.
- **`Monitorear el tiempo de ejecución`**:  Para cada proceso realizado, se imprime el tiempo que tardó en ejecutarse, lo que permite tener un mejor control y conocer qué secciones optimizar.





Finalmente se guardaron los datos en la carpeta [database](./database), la cual contiene:
- [**`movies.csv `**](./database/movies.csv): Una tabla con las peliculas y su metadata.
- [**`series.json`**](./database/series.json): Un json con las series y su metadata los episodios de cada serie y sus metadatas
- [**`channels.csv`**](./database/channels.csv): Una tabla con la información (nombre y url) de cada canal

# 🛠️ Instalación

## 1. Primero clona el repositorio.
```bash
git clone https://github.com/brunozenobio/bb_media_test.git
```
## 2. Muevete al directorio del repositorio.

```bash
cd  bb_media_test
```
## 3. Luego crea un entorno de python.
Ejemplo.
```bash
python -m venv myvenv
```
## 4. Inicia el entorno

🔹 En Linux/Mac:
```bash
source myvenv/bin/activate
```
Windows

🔹 En Windows:
```bash
myvenv/Scripts/activate
```
## 5. Luego instala el archivo requirements para tener las librerias necesarias.
```bash
pip install -r requirements.txt
```
## 6. Luego instala playwright
```bash
playwright install
```
## 7.Finalmente ejecuta el script
```bash
python scrapping.py  > output.txt
```

# Conclusiones y Resultados

En el archivo output.txt se puede ver el tiempo demorado en cada ejecución:
```bash
Tiempo total de ejecución:  1.7 horas
```

Este fue posible, gracias a la optimización lograda trabajando con multiprocesos.

### Peliculas:
!  

Se obtuvo un total de 1589 peliculas y un total de 22 generos

### Series:
![](./images/series.png)
Se obtuvo un total de 211 series con 18 generos.

La serie con mayor cantidad de temporadas es South Park con 25 temporadas.

### Canales
![](./images/channels.png)

Se obtuvo un total de 53 canales 


## Contacto

<div style="display: flex; align-items: center;">
  <a href="https://www.linkedin.com/in/brunozenobio/" style="margin-right: 10px;">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="40" height="40">
  </a>
  <a href="mailto:brunozenobio4@gmail.com" style="margin-right: 10px;">
    <img src="https://cdn-icons-png.flaticon.com/512/281/281769.png" alt="Gmail" width="40" height="40">
  </a>
</div>
