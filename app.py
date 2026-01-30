import streamlit as st
st.write(f"DEBUG: SID cargado comienza con {st.secrets['TWILIO_SID'][:5]}")
from twilio.rest import Client
import math

# Configuración de la página
st.set_page_config(page_title="Sistema EVA & CCA", page_icon="🛡️")

st.title("🛡️ Sistema de Gestión Humana: EVA & CCA")
st.markdown("---")

# --- BARRA LATERAL (ENTRADAS) ---
st.sidebar.header("Variables de Control")
a = st.sidebar.slider("Ánimo (Energía Interna)", 1.0, 10.0, 7.5, 0.1)
b = st.sidebar.slider("Brío (Ambición/Meta)", 1.0, 10.0, 5.0, 0.1)
c = st.sidebar.slider("Caos (Entorno/Ruido)", 1.0, 10.0, 3.0, 0.1)
r = st.sidebar.slider("Recuperación (Descanso)", 1.0, 10.0, 8.0, 0.1)
f = st.sidebar.number_input("Frecuencia (Días seguidos)", min_value=1, value=1)

# --- CÁLCULOS ---
# Fórmula EVA
raiz_caos = math.sqrt((c * a * b) / 2)
eva = (a**2 + b**2 - raiz_caos) / 2

# Fórmula CCA
cca = ((b * f) + a) / (11 - r)

# --- VISUALIZACIÓN DE RESULTADOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Estado EVA (Hoy)")
    st.metric(label="Índice de Equilibrio", value=f"{eva:.2f}")
    
    if eva <= 30:
        st.success("ZONA ÓPTIMA: Estás en flujo.")
    elif eva <= 60:
        st.warning("ESFUERZO ALTO: Procede con cuidado.")
    elif eva <= 85:
        st.error("ZONA DE RIESGO: Reduce la carga.")
    else:
        st.error("¡COLAPSO!: Detente inmediatamente.")

with col2:
    st.subheader("Estado CCA (Resistencia)")
    st.metric(label="Índice de Fortalecimiento", value=f"{cca:.2f}")
    
    if cca >= 21 and cca <= 50:
        st.success("CRECIMIENTO: Te estás volviendo más fuerte.")
    elif cca > 50:
        st.error("SOBREESFUERZO: Necesitas descansar (R) más.")
    else:
        st.info("MANTENIMIENTO: Sin cambios significativos.")

st.markdown("---")
st.info(f"**Análisis del Entrenador:** Con un EVA de {eva:.2f}, tu plan para hoy es {'sostenible' if eva <= 60 else 'peligroso'}. {'¡Sigue así!' if cca >= 21 else 'Busca retarte un poco más para fortalecerte.'}")
st.divider()

import requests
st.divider()
st.subheader("Nexus Protocol: Telegram Link")

def enviar_telegram(mensaje):
    token = st.secrets["TELEGRAM_TOKEN"]
    chat_id = st.secrets["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

with st.expander("Enviar reporte de estado"):
    msg = st.text_area("Mensaje para el Centro de Mando")
    if st.button("Ejecutar Protocolo"):
        try:
            # Enviamos el mensaje y un resumen de tus métricas
            reporte = f"🚨 ALERTA NEXUS\nEstado: {msg}\nEVA: {eva:.2f}\nCCA: {cca:.2f}"
            enviar_telegram(reporte)
            st.success("Mensaje enviado al encriptado de Telegram.")
        except Exception as e:
            st.error(f"Fallo de conexión: {e}")
