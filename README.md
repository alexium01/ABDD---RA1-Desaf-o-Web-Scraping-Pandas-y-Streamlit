Este proyecto extrae datos de libros de la pagina Books to Scrape utilizando Python, BeautifulSoup y Requests. Los datos extraidos se limpian y se guardan en un archivo CSV mediante Pandas, respetando las buenas practicas de scraping con User-Agent y pausas entre peticiones.

A partir del archivo generado, la aplicacion desarrollada con Streamlit y Plotly permite visualizar los resultados de forma interactiva. La interfaz incluye filtros por titulo, rango de precios y valoracion, ademas de graficos para analizar la relacion entre el precio y la puntuacion de los libros.

Para ejecutar el proyecto se deben instalar las librerias indicadas en el archivo requirements.txt, ejecutar el script scraper.py para generar los datos y arrancar la interfaz web con el comando streamlit run app.py.
