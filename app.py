import streamlit as st
import pandas as pd
import altair as alt
import os
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import io

# ==============================================================================
# CONFIGURAZIONE E SETUP
# ==============================================================================
st.set_page_config(page_title="Vinted Pro Seller Suite", page_icon="🛍️", layout="wide")

DB_FILE = "inventario_vinted.csv"

# Inizializzazione Database
if 'inventario' not in st.session_state:
    if os.path.exists(DB_FILE):
        st.session_state.inventario = pd.read_csv(DB_FILE)
    else:
        st.session_state.inventario = pd.DataFrame(columns=[
            "ID", "Data", "Brand", "Tipo", "Taglia", "Stato", "Costo (€)", "Prezzo Vendita (€)", "Profitto Netto (€)", "Stato Annuncio"
        ])

# Stile CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; background-color: #09b1ba; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛍️ Vinted Pro Seller Suite - Industrial Edition")

# ==============================================================================
# FUNZIONI CORE
# ==============================================================================
def salva_db():
    st.session_state.inventario.to_csv(DB_FILE, index=False)

def processa_immagine(img_file, azioni):
    img = Image.open(img_file)
    if "Rimuovi Pieghe (Stiratura AI)" in azioni:
        img = img.filter(ImageFilter.MedianFilter(size=3))
        img = ImageEnhance.Sharpness(img).enhance(1.5)
    if "Enhance Texture" in azioni:
        img = ImageEnhance.Contrast(img).enhance(1.3)
    if "Background Clean" in azioni:
        img = ImageEnhance.Brightness(img).enhance(1.1)
    return img

# ==============================================================================
# INTERFACCIA TABS
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📸 AI Studio", "📝 Generatore Annunci", "💰 Business & Margini", "📦 Inventario"])

# TAB 1: AI STUDIO
with tab1:
    st.header("📸 AI Image Processor Pro")
    c1, c2 = st.columns(2)
    with c1:
        img_file = st.file_uploader("Carica foto del capo:", type=["jpg", "png", "jpeg"])
        opzioni = ["Rimuovi Pieghe (Stiratura AI)", "Enhance Texture", "Background Clean"]
        scelte = st.multiselect("Azioni AI:", opzioni)
        if img_file and st.button("🚀 ESEGUI TRASFORMAZIONE"):
            st.session_state.img_elaborata = processa_immagine(img_file, scelte)
    with c2:
        if 'img_elaborata' in st.session_state:
            st.image(st.session_state.img_elaborata, caption="Risultato Elaborato")
            buf = io.BytesIO()
            st.session_state.img_elaborata.save(buf, format="PNG")
            st.download_button("💾 Scarica Risultato", buf.getvalue(), "foto_vinted.png")

# TAB 2: GENERATORE ANNUNCI
with tab2:
    st.header("📝 Generatore Annunci SEO")
    colA, colB = st.columns(2)
    with colA:
        brand = st.text_input("Brand")
        tipo = st.text_input("Tipologia")
        taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL", "XXL"])
    with colB:
        condizioni = st.selectbox("Condizioni", ["Nuovo", "Ottime", "Buone"])
        colore = st.text_input("Colore")
    
    annuncio = f"👕 {tipo.upper()} {brand.upper()} - Taglia {taglia}. {condizioni}. Colore: {colore}. Spedizione veloce 24h!\n\n#{brand.lower().replace(' ', '')} #{tipo.lower().replace(' ', '')} #vinteditalia"
    st.text_area("Copia questo testo per Vinted:", annuncio, height=150)

# TAB 3: BUSINESS
with tab3:
    st.header("💰 Business Intelligence")
    c1, c2, c3, c4 = st.columns(4)
    costo = c1.number_input("Costo Acquisto (€)", 0.0)
    extra = c2.number_input("Extra/Buste (€)", 0.0)
    comm = c3.number_input("Commissioni (%)", 0.0, 15.0, 5.0)
    prezzo = c4.number_input("Prezzo Vendita (€)", 0.0)
    
    profitto = prezzo - (prezzo * (comm/100)) - (costo + extra)
    st.metric("Margine Netto", f"€ {profitto:.2f}")
    
    if st.button("➕ SALVA ARTICOLO"):
        nuovo = pd.DataFrame([[len(st.session_state.inventario)+1, datetime.now().strftime("%d-%m-%Y"), brand, tipo, taglia, condizioni, costo, prezzo, profitto, "In Vendita"]], 
                             columns=st.session_state.inventario.columns)
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuovo], ignore_index=True)
        salva_db()
        st.success("Articolo archiviato nel DB!")

# TAB 4: INVENTARIO & TREND
with tab4:
    st.header("📦 Gestione Inventario")
    st.session_state.inventario = st.data_editor(st.session_state.inventario, use_container_width=True)
    if st.button("💾 Salva modifiche tabella"):
        salva_db()
        st.rerun()
    
    st.subheader("📊 Performance Vendite")
    if not st.session_state.inventario.empty:
        chart = alt.Chart(st.session_state.inventario).mark_bar().encode(x='Data', y='Profitto Netto (€)', color='Tipo')
        st.altair_chart(chart, use_container_width=True)
