import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análisis de Catálogo de Libros",
    page_icon="📚",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    return pd.read_csv("libros.csv")

st.title("📚 Dashboard de Análisis: Books to Scrape")
st.markdown(
    "Explora los datos extraídos mediante **Web Scraping (BeautifulSoup)**, "
    "procesados con **Pandas** y visualizados de forma interactiva."
)

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'libros.csv'. Ejecuta primero 'python scraper.py'.")
    st.stop()

st.sidebar.header("🔍 Filtros de Búsqueda")

busqueda_titulo = st.sidebar.text_input("Buscar por título:", placeholder="Ej. A Light in the...")

precio_min = float(df["Precio_GBP"].min())
precio_max = float(df["Precio_GBP"].max())
rango_precio = st.sidebar.slider(
    "Rango de Precio (£):",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max)
)

ratings_disponibles = sorted(df["Rating"].unique())
ratings_seleccionados = st.sidebar.multiselect(
    "Valoración (Estrellas):",
    options=ratings_disponibles,
    default=ratings_disponibles
)

df_filtrado = df[
    (df["Precio_GBP"] >= rango_precio[0]) &
    (df["Precio_GBP"] <= rango_precio[1]) &
    (df["Rating"].isin(ratings_seleccionados))
]

if busqueda_titulo:
    df_filtrado = df_filtrado[
        df_filtrado["Titulo"].str.contains(busqueda_titulo, case=False, na=False)
    ]

st.subheader("📊 Resumen de Selección")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Libros", len(df_filtrado))
col2.metric("Precio Medio", f"£{df_filtrado['Precio_GBP'].mean():.2f}" if not df_filtrado.empty else "£0.00")
col3.metric("Rating Medio", f"{df_filtrado['Rating'].mean():.2f} ⭐" if not df_filtrado.empty else "0 ⭐")
col4.metric("Libro Más Caro", f"£{df_filtrado['Precio_GBP'].max():.2f}" if not df_filtrado.empty else "£0.00")

st.divider()

if df_filtrado.empty:
    st.warning("No hay libros que coincidan con los filtros seleccionados.")
else:
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Distribución de Valoraciones (Rating)")
        conteo_ratings = df_filtrado["Rating"].value_counts().reset_index()
        conteo_ratings.columns = ["Rating", "Cantidad"]
        conteo_ratings = conteo_ratings.sort_values("Rating")

        fig_barras = px.bar(
            conteo_ratings,
            x="Rating",
            y="Cantidad",
            text="Cantidad",
            color="Rating",
            labels={"Rating": "Estrellas (1 a 5)", "Cantidad": "Número de Libros"},
            title="Cantidad de libros por puntuación"
        )
        fig_barras.update_layout(xaxis=dict(tickmode="linear"))
        st.plotly_chart(fig_barras, use_container_width=True)

    with col_graf2:
        st.subheader("¿Influye el precio en la valoración?")
        fig_caja = px.box(
            df_filtrado,
            x="Rating",
            y="Precio_GBP",
            color="Rating",
            points="all",
            labels={"Rating": "Estrellas (1 a 5)", "Precio_GBP": "Precio (£)"},
            title="Distribución de precios según las estrellas"
        )
        st.plotly_chart(fig_caja, use_container_width=True)

    st.info(
        "💡 **Interpretación del análisis:** El diagrama de cajas permite comprobar si los libros "
        "mejor valorados (4 y 5 estrellas) tienen precios más elevados o si el precio es independiente "
        "de la puntuación de los usuarios."
    )

    st.divider()

    st.subheader("📋 Catálogo Detallado")
    st.dataframe(
        df_filtrado,
        column_config={
            "Portada_URL": st.column_config.ImageColumn("Portada", help="Vista previa de la portada"),
            "Precio_GBP": st.column_config.NumberColumn("Precio (£)", format="£%.2f"),
            "Rating": st.column_config.NumberColumn("Valoración", format="%d ⭐"),
        },
        use_container_width=True,
        hide_index=True
    )