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

# Función para buscar información en Twitter y realizar el análisis de sentimientos
def buscar_informacion_sentimientos(termino):
    # Configuración de las credenciales de Twitter API
    consumer_key = "fr9FM4cAAEoMpvak8fKk5kDOp"
    consumer_secret = "7P025Egxnib5dogMvOLgdo1uHJPJg2lx98Rvg3XYvIjf4Eo59u"
    access_token = "113763054-GQQ7L2Pa9yfhX386G0khrBhecdTMgIgpadwGglDv"
    access_token_secret = "o5ggZAOJrq1AotVlg2gGJ7MpVpHnh0eg4xYsKX2EsbFvT"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    resultados = []
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()
    
    # Realizar la búsqueda en Twitter
    tweets = api.search_tweets(q=termino, count=100, lang="es", tweet_mode="extended", until=fecha_actual)
    
    for tweet in tweets:
        texto = tweet.full_text
        polaridad, subjetividad = analizar_sentimiento(texto)
        resultados.append({"Usuario": tweet.user.screen_name, "Texto": texto, "Polaridad": polaridad, "Subjetividad": subjetividad})

    return resultados

# Configuración de la aplicación Streamlit
st.title("Análisis de Sentimientos sobre Términos en Twitter")
st.sidebar.title("Información")
st.sidebar.write("Esta aplicación permite realizar un análisis de sentimientos sobre cualquier término en Twitter. Se basa en los tweets del día actual.")
st.sidebar.write("Autor: Moris Polanco")

termino = st.text_input("Ingrese un término:")

if st.button("Analizar"):
    if termino:
        resultados = buscar_informacion_sentimientos(termino)
        if resultados:
            df = pd.DataFrame(resultados)
            st.write(f"Resultados encontrados para el término '{termino}' en el día de hoy:")
            st.dataframe(df)
            
            # Calcular el número de tweets positivos, negativos y neutrales
            polaridades = df["Polaridad"]
            positivos = sum(p > 0 for p in polaridades)
            negativos = sum(p < 0 for p in polaridades)
            neutrales = sum(p == 0 for p in polaridades)
            
            # Crear la gráfica de barras
            labels = ["Positivos", "Negativos", "Neutrales"]
            values = [positivos, negativos, neutrales]
            plt.bar(labels, values)
            plt.title("Sentimiento de los tweets")
            plt.xlabel("Sentimiento")
            plt.ylabel("Cantidad")
            
            # Mostrar la gráfica en Streamlit
            st.pyplot(plt)
            
            # Mostrar los tweets
            st.write("Tweets encontrados:")
            for index, row in df.iterrows():
                st.write(f"Usuario: @{row['Usuario']}")
                st.write(f"Tweet: {row['Texto']}")
                st.write("----")
        else:
            st.write("No se encontraron resultados para el término especificado en el día de hoy.")
    else:
        st.write("Por favor, ingrese un término.")
