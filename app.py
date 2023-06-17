import streamlit as st
import feedparser
from datetime import datetime
from textblob import TextBlob

# Función para analizar el sentimiento del texto
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    return polaridad, subjetividad

# Función para buscar información sobre una marca en fuentes confiables
def buscar_informacion_marca(marca, fecha):
    # Configuración de los feeds RSS de las fuentes confiables
    fuentes = [
        {"nombre": "Xataka", "url": "https://www.xataka.com/rss2"},
        {"nombre": "Gizmodo", "url": "https://es.gizmodo.com/rss"},
        {"nombre": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
        {"nombre": "Engadget", "url": "https://www.engadget.com/rss.xml"},
        {"nombre": "Digital Trends", "url": "https://www.digitaltrends.com/feed/"}
    ]
    
    resultados = []
    
    for fuente in fuentes:
        url = fuente['url']
        
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Obtener la fecha del artículo y convertirla a formato datetime
                fecha_articulo = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
                
                # Verificar si el artículo se publicó en la fecha especificada
                if fecha_articulo.date() == fecha:
                    # Verificar si la marca aparece en el título o el contenido del artículo
                    if marca.lower() in entry.title.lower() or marca.lower() in entry.summary.lower():
                        texto = entry.title + " " + entry.summary
                        polaridad, subjetividad = analizar_sentimiento(texto)
                        resultados.append({"fuente": fuente['nombre'], "texto": texto, "polaridad": polaridad, "subjetividad": subjetividad})
        except Exception as e:
            print(f"Error al obtener resultados de la fuente: {fuente['nombre']}, {e}")
    
    return resultados

# Configuración de la aplicación Streamlit
st.title("Análisis de Sentimientos y Búsqueda de Información de Marcas")
marca = st.text_input("Ingrese una marca:")
fecha = st.date_input("Seleccione una fecha:")

if st.button("Analizar"):
    if marca:
        resultados = buscar_informacion_marca(marca, fecha)
        if resultados:
            st.write(f"Resultados encontrados para la marca '{marca}' en la fecha {fecha}:")
            for resultado in resultados:
                st.write(f"Fuente: {resultado['fuente']}")
                st.write(f"Texto: {resultado['texto']}")
                st.write(f"Polaridad: {resultado['polaridad']}")
                st.write(f"Subjetividad: {resultado['subjetividad']}")
                st.write("---")
        else:
            st.write("No se encontraron resultados para la marca y fecha especificadas.")
    else:
        st.write("Por favor, ingrese una marca.")
