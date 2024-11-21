import streamlit as st
from supabase import create_client
from datetime import datetime
import pandas as pd
import base64

# Inicializar la conexión a Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# Inicializar la conexión a Supabase
supabase = init_connection()

# Función para generar un enlace de descarga automática
def generate_auto_download(df: pd.DataFrame, filename: str):
    """
    Genera un enlace de descarga automática para un DataFrame en formato CSV.
    """
    try:
        csv = df.to_csv(index=False)      # Convertir DataFrame a excel
        b64 = base64.b64encode(csv.encode()).decode()  # Codificar CSV a base64

        # JavaScript para automáticamente iniciar la descarga
        download_link = f"""
        <a href="data:file/csv;base64,{b64}" download="{filename}" style="display:none" id="auto-download"></a>
        <script>document.getElementById('auto-download').click();</script>
        """
        st.components.v1.html(download_link, height=0)
    except Exception as e:
        st.error(f"Error al generar el enlace de descarga: {e}")

# Función para descargar datos de Supabase
def download_data():
    """
    Obtiene datos de Supabase y activa una descarga automática.
    """
    request = supabase.table("general_data").select("*").execute()
    df = pd.DataFrame(request.data)

    if not df.empty:
        generate_auto_download(df, "datos.csv")
    else:
        st.warning("No hay datos disponibles para descargar.")

# Título de la aplicación
st.title("📅 App de Registro de Fechas")

# Selector de fecha tipo calendario
selected_date = st.date_input("Selecciona una fecha:", value=None)

# Botón para confirmar la selección y agregar los datos a la base de datos
if st.button("Registrar"):
    if selected_date:  # Verificar que la casilla esté llena
        current_datetime = datetime.now()
        date_now = current_datetime.strftime("%Y-%m-%d")
        time_now = current_datetime.strftime("%H:%M:%S")

        response = (
            supabase.table("general_data")
            .insert({
                "date_register": date_now,
                "time_register": time_now,
                "date_occurrence": selected_date.isoformat()
            })
            .execute()
        )
        st.success(f"Fecha seleccionada: {selected_date}")
        st.info(f"Fecha y hora actual registrada: {current_datetime}")
    else:
        st.error("Por favor selecciona una fecha antes de continuar.")

# Botón para descargar datos
if st.button("Descargar datos"):
    download_data()
