<p align="center"><img src="./images/OIG.Lo7.dES.jpeg"></p>

# Prueba Tenica 


## **Tabla de Contenidos**

- [Introducción](#introducción)
- [Desarrollo](#desarrollo)
- [Instalación](#instalación)
- [Conclusión](#conclusión)
- [Contacto](#contacto)

## **Tecnolgías usadas**

![](https://img.shields.io/badge/Python-grey?style=for-the-badge&logo=python)
![](https://img.shields.io/badge/playwright%201.47.0-yellow?style=for-the-badge)
![](https://img.shields.io/badge/pandas%202.2.3-yellow?style=for-the-badge&logo=)


---

# Introducción

A continuación se explicara el proyecto realizado para la prueba tecnica. En este tenía como objetivo hacer web scrapping en la pagina de Pluto Tv, y de estas extraer todas las peliculas y series junto a su metadata, así tambien como todos los canales.

Es un plus obtener mas data de cada sección, como episodios por serie, y grilla de canales, que el codigo se ejecute en menos de 2 horas, indentificar modelos de negocios y hacer analisis y/o procesamiento de los datos.



---

# Desarrollo


Para esto, se ha usado la libreria de **`Playwright`**, la cual permite hacer scrapping en sitios web flexibles e interactivos, lo cual fue esencial para realizar esta tarea.
Tambien, para logral la mayor optimización del tiempo de scrapping, se uso la libreria de python base **`concurrent`** la cual me permitio trabajar en hilos, y asi poder cargar conjuntamente muchas peliculas y series.

### Entorno de codigo

El script principal que ejecuta todo el proceso es [scrapping.py](./scrapping_py.py),este se encarga de realizar las siguientes tareas:
- **`realizar la obtención de series y peliculas`**: Para en la carpeta [scripts](./scripts/), estan todos los scripts necesarios para realizar esas tareas:
    - [init_pluto_tv.py](./scripts/init_pluto_tv.py) : Inicia Playwright y abre un enlace
    - [get_series_demand.py](./scripts/get_on_demand.py) : Con pluto iniciado va a la seccion On Demand, y obtiene los enlaces de todas las series y peliculas.

    - [get_series_movies.py](./scripts/get_series_movies.py) : Para cada serie y pelicula, guarda las peliculas en un csv y las series con sus episodios en un json.

    - [get_channels](./scripts/channels.py) : Obtiene todos los canales y sus url y los guarda en un csv.
- **`Monitorear el tiempo de ejecución`**: Para cada proceso realizo, imprime el tiempo tardado en ejecutarse, lo cual permite tener un mejor control y poder conocer que secciones optimizar.





Finalmente se guardaron los datos en la carpeta [database](./database), la cual contiene:
- **`movies.csv `**: Una tabla con las peliculas y su metadata.
- **`series.json`**: Un json con las series y su metadata los episodios de cada serie y sus metadatas
- **`channels.csv`**: Una tabla con la información (nombre y url) de cada canal

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
Tiempo total de ejecución:  segundos
```

Este fue posible, gracias a la optimización lograda trabajando con multiprocesos.



## Bibliografias
- [Instituto geografico nacional](https://www.ign.gob.ar/)
- [ENACOM](https://www.baenegocios.com/negocios/El-desafio-de-la-Argentina-en-el-camino-de-la-fibra-optica-20200610-0092.html)

## Contacto

<div style="display: flex; align-items: center;">
  <a href="https://www.linkedin.com/in/brunozenobio/" style="margin-right: 10px;">
    <img src="./images/in_linked_linkedin_media_social_icon_124259.png" alt="LinkedIn" width="40" height="40">
  </a>
  <a href="mailto:brunozenobio4@gmail.com" style="margin-right: 10px;">
    <img src="./images/gmail_new_logo_icon_159149.png" alt="Gmail" width="40" height="40">
  </a>
</div>