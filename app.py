import streamlit as st
from datetime import datetime
from textblob import TextBlob
import requests

# Función para analizar el sentimiento del texto
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    return polaridad, subjetividad

# Función para buscar información sobre una marca en fuentes confiables
def buscar_informacion_marca(marca, fecha):
    # Aquí puedes incluir tu lógica para buscar información en las fuentes confiables mencionadas
    # y obtener los resultados para la marca y fecha específica
    # En este ejemplo, usaremos una solicitud GET a una API ficticia para obtener los resultados
    
    # Fuentes confiables
    fuentes = [
        {"nombre": "Xataka", "url": "https://www.xataka.com/"},
        {"nombre": "Gizmodo", "url": "https://es.gizmodo.com/"},
        {"nombre": "The Verge", "url": "https://www.theverge.com/"},
        {"nombre": "Engadget", "url": "https://www.engadget.com/"},
        {"nombre": "Digital Trends", "url": "https://www.digitaltrends.com/"}
    ]
    
    resultados = []
    
    for fuente in fuentes:
        url = f"{fuente['url']}buscar?marca={marca}&fecha={fecha}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                noticias = response.json()
                for noticia in noticias:
                    texto = noticia['texto']
                    polaridad, subjetividad = analizar_sentimiento(texto)
                    resultados.append({"fuente": fuente['nombre'], "texto": texto, "polaridad": polaridad, "subjetividad": subjetividad})
            else:
                print(f"Error al obtener resultados de la fuente: {fuente['nombre']}")
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con la fuente: {fuente['nombre']}, {e}")
    
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
