import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProyectoEducativoScraping/1.0"
}
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def extraer_libros(num_paginas=5):
    lista_libros = []
    print(f"Iniciando scraping de {num_paginas} páginas...")

    for pagina in range(1, num_paginas + 1):
        url = BASE_URL.format(pagina)
        print(f"Procesando página {pagina}: {url}")

        try:
            respuesta = requests.get(url, headers=HEADERS, timeout=10)
            respuesta.raise_for_status()
            respuesta.encoding = "utf-8"
        except requests.RequestException as e:
            print(f"Error al acceder a la página {pagina}: {e}")
            continue

        soup = BeautifulSoup(respuesta.text, "html.parser")
        articulos = soup.find_all("article", class_="product_pod")

        for libro in articulos:
            titulo = libro.h3.a["title"].strip()
            precio_texto = libro.find("p", class_="price_color").text.strip()
            precio_limpio = float(precio_texto.replace("£", ""))

            clases_rating = libro.find("p", class_="star-rating")["class"]
            rating_texto = clases_rating[1] if len(clases_rating) > 1 else "Zero"
            rating_num = RATING_MAP.get(rating_texto, 0)

            stock_texto = libro.find("p", class_="instock availability").text.strip()
            en_stock = True if "In stock" in stock_texto else False

            img_relativa = libro.find("div", class_="image_container").img["src"]
            url_portada = "https://books.toscrape.com/" + img_relativa.replace("../", "")

            lista_libros.append({
                "Titulo": titulo,
                "Precio_GBP": precio_limpio,
                "Rating": rating_num,
                "Disponible": en_stock,
                "Portada_URL": url_portada
            })

        time.sleep(1)

    return lista_libros

if __name__ == "__main__":
    datos = extraer_libros(num_paginas=5)
    df = pd.DataFrame(datos)
    archivo_salida = "libros.csv"
    df.to_csv(archivo_salida, index=False, encoding="utf-8")

    print(f"\n¡Scraping completado! Se han guardado {len(df)} libros limpios en '{archivo_salida}'.")
    print(df.head())