import streamlit as st
import tweepy
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt

# Función para analizar el sentimiento del texto
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    return polaridad

# Función para buscar información sobre una marca en Twitter
def buscar_informacion_marca(marca, fecha):
    # Acceder a las credenciales de Twitter API desde los secrets de Streamlit
    consumer_key = st.secrets["twitter"]["consumer_key"]
    consumer_secret = st.secrets["twitter"]["consumer_secret"]
    access_token = st.secrets["twitter"]["access_token"]
    access_token_secret = st.secrets["twitter"]["access_token_secret"]
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    resultados = {"Positivo": 0, "Negativo": 0, "Neutral": 0}
    
    # Realizar la búsqueda en Twitter
    tweets = api.search(q=marca, count=100, lang="es", tweet_mode="extended")
    
    for tweet in tweets:
        # Obtener la fecha del tweet y convertirla a formato datetime
        fecha_tweet = tweet.created_at.date()
        
        # Verificar si el tweet se publicó en la fecha especificada
        if fecha_tweet == fecha:
            texto = tweet.full_text
            polaridad = analizar_sentimiento(texto)
            
            if polaridad > 0:
                resultados["Positivo"] += 1
            elif polaridad < 0:
                resultados["Negativo"] += 1
            else:
                resultados["Neutral"] += 1

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
            st.write(resultados)
            
            # Generar la gráfica de pie
            labels = resultados.keys()
            values = resultados.values()
            
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.set_title("Análisis de Sentimientos")
            
            st.pyplot(fig)
        else:
            st.write("No se encontraron resultados para la marca y fecha especificadas.")
    else:
        st.write("Por favor, ingrese una marca.")
