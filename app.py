import streamlit as st
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt

# Función para analizar el sentimiento del texto
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    return polaridad, subjetividad

# Función para buscar información sobre una marca en Twitter
def buscar_informacion_marca(marca):
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
    tweets = api.search(q=marca, count=100, lang="es", tweet_mode="extended")
    
    for tweet in tweets:
        texto = tweet.full_text
        polaridad, subjetividad = analizar_sentimiento(texto)
        resultados.append({"usuario": tweet.user.screen_name, "texto": texto, "polaridad": polaridad, "subjetividad": subjetividad})

    return resultados

# Configuración de la aplicación Streamlit
st.title("Análisis de Sentimientos y Búsqueda de Información de Marcas")
marca = st.text_input("Ingrese una marca:")

if st.button("Analizar"):
    if marca:
        resultados = buscar_informacion_marca(marca)
        if resultados:
            st.write(f"Resultados encontrados para la marca '{marca}':")
            for resultado in resultados:
                st.write(f"Usuario: {resultado['usuario']}")
                st.write(f"Texto: {resultado['texto']}")
                st.write(f"Polaridad: {resultado['polaridad']}")
                st.write(f"Subjetividad: {resultado['subjetividad']}")
                st.write("---")

            # Generar la gráfica de pastel
            polaridades = [resultado['polaridad'] for resultado in resultados]
            labels = ['Positivo', 'Neutral', 'Negativo']
            values = [len([p for p in polaridades if p > 0]),
                      len([p for p in polaridades if p == 0]),
                      len([p for p in polaridades if p < 0])]
            
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.set_title("Análisis de Sentimientos")
            
            st.pyplot(fig)
        else:
            st.write("No se encontraron resultados para la marca especificada.")
    else:
        st.write("Por favor, ingrese una marca.")
