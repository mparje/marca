import streamlit as st
import tweepy
from datetime import datetime
from textblob import TextBlob

# Función para analizar el sentimiento del texto
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    return polaridad, subjetividad

# Función para buscar información sobre una marca en Twitter
def buscar_informacion_marca(marca, fecha):
    # Configuración de las credenciales de Twitter API
    consumer_key = "TU_CONSUMER_KEY"
    consumer_secret = "TU_CONSUMER_SECRET"
    access_token = "TU_ACCESS_TOKEN"
    access_token_secret = "TU_ACCESS_TOKEN_SECRET"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    resultados = []
    
    # Realizar la búsqueda en Twitter
    tweets = api.search(q=marca, count=100, lang="es", tweet_mode="extended")
    
    for tweet in tweets:
        # Obtener la fecha del tweet y convertirla a formato datetime
        fecha_tweet = tweet.created_at.date()
        
        # Verificar si el tweet se publicó en la fecha especificada
        if fecha_tweet == fecha:
            texto = tweet.full_text
            polaridad, subjetividad = analizar_sentimiento(texto)
            resultados.append({"usuario": tweet.user.screen_name, "texto": texto, "polaridad": polaridad, "subjetividad": subjetividad})

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
                st.write(f"Usuario: {resultado['usuario']}")
                st.write(f"Texto: {resultado['texto']}")
                st.write(f"Polaridad: {resultado['polaridad']}")
                st.write(f"Subjetividad: {resultado['subjetividad']}")
                st.write("---")
        else:
            st.write("No se encontraron resultados para la marca y fecha especificadas.")
    else:
        st.write("Por favor, ingrese una marca.")
