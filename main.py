import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)

# Título de la aplicación
st.title("App de Registro de Fechas")

# Selector de fecha tipo calendario
selected_date = st.date_input("Selecciona una fecha:")

# Inicializar variable para almacenar la fecha y hora actual
current_datetime = None

# Botón para confirmar
if st.button("Registrar"):
    if selected_date:  # Verificar que la casilla esté llena
        # Guardar la fecha y hora actual
        current_datetime = datetime.now()
        st.success(f"Fecha seleccionada: {selected_date}")
        st.info(f"Fecha y hora actual registrada: {current_datetime}")
    else:
        st.error("Por favor selecciona una fecha antes de continuar.")

