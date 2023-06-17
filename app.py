import streamlit as st
import tweepy
from datetime import datetime
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

# Función para analizar el sentimiento del texto
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    return polaridad, subjetividad

# Función para buscar información sobre una marca en Twitter
def buscar_informacion_marca(marca, fecha):
    # Configuración de las credenciales de Twitter API
    consumer_key = "fr9FM4cAAEoMpvak8fKk5kDOp"
    consumer_secret = "7P025Egxnib5dogMvOLgdo1uHJPJg2lx98Rvg3XYvIjf4Eo59u"
    access_token = "113763054-GQQ7L2Pa9yfhX386G0khrBhecdTMgIgpadwGglDv"
    access_token_secret = "o5ggZAOJrq1AotVlg2gGJ7MpVpHnh0eg4xYsKX2EsbFvT"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    resultados = []
    
    # Realizar la búsqueda en Twitter
    tweets = api.search_tweets(q=marca, count=100, lang="es", tweet_mode="extended")
    
    for tweet in tweets:
        # Obtener la fecha del tweet y convertirla a formato datetime
        fecha_tweet = tweet.created_at.date()
        
        # Verificar si el tweet se publicó en la fecha especificada
        if fecha_tweet == fecha:
            texto = tweet.full_text
            polaridad, subjetividad = analizar_sentimiento(texto)
            resultados.append({"Usuario": tweet.user.screen_name, "Texto": texto, "Polaridad": polaridad, "Subjetividad": subjetividad})

    return resultados

# Configuración de la aplicación Streamlit
st.title("Análisis de Sentimientos y Búsqueda de Información de Marcas")
marca = st.text_input("Ingrese una marca:")

if st.button("Analizar"):
    if marca:
        fecha = datetime.now().date()  # Obtenemos la fecha actual en lugar de solicitarla al usuario
        resultados = buscar_informacion_marca(marca, fecha)
        if resultados:
            df = pd.DataFrame(resultados)
            st.write(f"Resultados encontrados para la marca '{marca}' en la fecha {fecha}:")
            st.dataframe(df)
            
            # Calcular el número de tweets positivos, negativos y neutrales
            polaridades = df["Polaridad"]
            positivos = sum(p > 0 for p in polaridades)
            negativos = sum(p < 0 for p in polaridades)
            neutrales = sum(p == 0 for p in polaridades)
            
            # Crear la gráfica de pie
            labels = ["Positivos", "Negativos", "Neutrales"]
            sizes = [positivos, negativos, neutrales]
            plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
            plt.axis("equal")  # Hace que el gráfico de pie sea circular
            plt.title("Sentimiento de los tweets")
            
            # Mostrar la gráfica en Streamlit
            st.pyplot(plt)
        else:
            st.write("No se encontraron resultados para la marca especificada en la fecha actual.")
    else:
        st.write("Por favor, ingrese una marca.")
