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
st.subheader("Nexus Protocol: Mensajería Privada")

# Usaremos los Secrets de Streamlit para no exponer tus llaves en GitHub
if "TWILIO_SID" in st.secrets:
    client = Client(st.secrets["TWILIO_SID"], st.secrets["TWILIO_TOKEN"], region='us1')
    
    with st.expander("Enviar mensaje con remitente oculto"):
        num_destino = st.text_input("Número (ej: +52122...)")
        cuerpo_msg = st.text_area("Mensaje")
        
        if st.button("Ejecutar envío"):
            try:
                # Envío desde el número de sistema de Twilio
                sent_msg = client.messages.create(
                    body=cuerpo_msg,
                    from_=st.secrets["TWILIO_NUMBER"],
                    to=num_destino
                )
                # Borramos el log del servidor de Twilio inmediatamente por privacidad
                client.messages(sent_msg.sid).delete()
                st.success("Protocolo completado. Registro eliminado.")
            except Exception as e:
            # Todo esto debe estar un nivel adentro del 'except'
            st.error(f"Error Detallado: {e}")
            error_str = str(e) # Guardamos el error en una variable clara
            if "Geo-Permissions" in error_str:
                st.info("Sugerencia: Revisa los permisos geográficos en tu consola de Twilio.")
            elif "21608" in error_str:
                st.info("Sugerencia: En cuentas Trial, solo puedes enviar a números verificados.")
                st.info("Configura las credenciales en 'Secrets' para activar esta función.")
