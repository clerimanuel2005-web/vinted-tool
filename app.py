import streamlit as st
import pandas as pd
import requests
import io
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from rembg import remove, new_session

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# Sessione AI (Caricata una sola volta)
if "session" not in st.session_state:
    st.session_state.session = new_session(model_name="u2net_clothing")

st.title("🛍️ Vinted Power Seller Suite")

# Schede
tab1, tab2, tab3, tab4 = st.tabs(["📸 Manichino AI", "📝 Annunci", "💰 Prezzi", "📊 Trend"])

# TAB 1: FOTO
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        foto_file = st.file_uploader("Carica foto:", type=["jpg", "jpeg", "png"])
        if st.button("✨ Genera Foto"):
            if foto_file:
                with st.spinner("Elaborazione in corso..."):
                    try:
                        img = Image.open(foto_file).convert("RGBA")
                        # Scontornamento standard con modello clothing (senza filtri complessi che causano errori)
                        img_pulita = remove(img, session=st.session_state.session)
                        
                        # Composizione semplice
                        dim = 1000
                        risultato = Image.new("RGBA", (dim, dim), (255, 255, 255, 255))
                        img_pulita.thumbnail((800, 800))
                        pos = (100, 100)
                        risultato.paste(img_pulita, pos, img_pulita)
                        
                        st.image(risultato, caption="Risultato", width=400)
                    except Exception as e:
                        st.error(f"Errore: {e}")
            else:
                st.warning("Carica una foto prima.")

# TAB 2: DESCRIZIONI
with tab2:
    st.header("Generatore Descrizioni")
    brand = st.text_input("Brand")
    tipo = st.text_input("Tipo")
    st.text_area("Descrizione", f"Vendo {tipo} originale {brand}. In ottime condizioni.")

# TAB 3: CALCOLATORE
with tab3:
    st.header("Calcolatore")
    costo = st.number_input("Costo", value=15.0)
    vendita = st.number_input("Vendita", value=45.0)
    st.write(f"Profitto: {vendita - costo}€")

# TAB 4: TREND
with tab4:
    st.header("Trend")
    df = pd.DataFrame({"Categoria": ["Streetwear", "Vintage"], "Valore": ["Alto", "Medio"]})
    # Senza use_container_width per evitare crash
    st.dataframe(df)
