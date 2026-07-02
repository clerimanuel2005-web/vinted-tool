import streamlit as st
import pandas as pd
import altair as alt
import time
import os
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import io

# ==============================================================================
# CONFIGURAZIONE E SETUP
# ==============================================================================
st.set_page_config(
    page_title="Vinted Pro Seller Suite",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "inventario_vinted.csv"

if 'inventario' not in st.session_state:
    if os.path.exists(DB_FILE):
        st.session_state.inventario = pd.read_csv(DB_FILE)
    else:
        st.session_state.inventario = pd.DataFrame(columns=[
            "ID", "Data", "Brand", "Tipo", "Taglia", "Stato", "Costo (€)", "Prezzo Vendita (€)", "Profitto Netto (€)", "Stato Annuncio"
        ])

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #09b1ba; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛍️ Vinted Pro Seller Suite - Industrial Edition")
st.markdown("---")

# ==============================================================================
# FUNZIONI CORE
# ==============================================================================
def salva_db():
    st.session_state.inventario.to_csv(DB_FILE, index=False)

def calcola_netto(prezzo_vendita, costo, commissioni_percent):
    return prezzo_vendita - (prezzo_vendita * (commissioni_percent/100)) - costo

def elabora_foto(img_file, filtri, intensita):
    img = Image.open(img_file)
    factor = intensita / 50.0  # Normalizzazione slide
    
    if "Rimuovi Pieghe (Stiratura AI)" in filtri:
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5)) # Ammorbidisce
        img = ImageEnhance.Sharpness(img).enhance(factor * 1.2) # Riaffila
    if "Enhance Texture" in filtri:
        img = ImageEnhance.Contrast(img).enhance(factor)
    if "Background Clean" in filtri:
        img = ImageEnhance.Brightness(img).enhance(1.1)
    return img

# ==============================================================================
# TABS PRINCIPALI
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📸 AI Studio Professionale", "📝 Generatore Annunci SEO", "💰 Business & Margini", "📦 Gestione Inventario"])

# TAB 1: AI STUDIO
with tab1:
    st.header("📸 AI Studio: Ghost Mannequin & Restoration")
    col1, col2 = st.columns([0.4, 0.6])
    with col1:
        img_input = st.file_uploader("Carica foto reale del capo:", type=["jpg", "png", "jpeg"])
        opzioni_ai = ["Rimuovi Pieghe (Stiratura AI)", "Enhance Texture", "Background Clean"]
        trattamenti = st.multiselect("Azioni AI:", opzioni_ai, default=["Rimuovi Pieghe (Stiratura AI)"])
        forza = st.slider("Intensità Elaborazione (%)", 0, 100, 70)
        
    with col2:
        if img_input:
            if st.button("✨ AVVIA AI RESTORATION"):
                with st.spinner("L'AI sta analizzando la struttura del tessuto..."):
                    st.session_state.img_risultato = elabora_foto(img_input, trattamenti, forza)
            
            if 'img_risultato' in st.session_state:
                st.image(st.session_state.img_risultato, caption="Output: Professionale")
                buf = io.BytesIO()
                st.session_state.img_risultato.save(buf, format="PNG")
                st.download_button("📥 Scarica Foto Ottimizzata", buf.getvalue(), "foto_vinted_pro.png")
        else:
            st.info("Carica una foto per attivare il motore AI.")

# TAB 2: GENERATORE ANNUNCI
with tab2:
    st.header("📝 Generatore Annunci SEO-Driven")
    colA, colB = st.columns(2)
    with colA:
        brand = st.text_input("Brand / Marca")
        tipo = st.text_input("Tipologia")
        taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL", "XXL", "46", "48", "50"])
        fit = st.select_slider("Vestibilità (Fit)", ["Slim", "Regolare", "Oversize"])
    with colB:
        condizioni = st.selectbox("Condizioni", ["Nuovo con cartellino", "Ottime", "Buone"])
        colore = st.text_input("Colore / Pattern")
        prezzo_target = st.number_input("Prezzo di vendita stimato €", 0.0)
    
    descrizione = f"👕 {tipo.upper()} {brand.upper()} - Taglia {taglia}\n\nVendo {tipo} {brand}. {condizioni}. Vestibilità: {fit}. Colore: {colore}.\n\n📦 Spedizione rapida!\n#{brand.lower().replace(' ', '')} #{tipo.lower().replace(' ', '')} #vinteditalia"
    st.text_area("Descrizione Finale:", descrizione, height=200)

# TAB 3: BUSINESS
with tab3:
    st.header("💰 Business Intelligence")
    c1, c2, c3, c4 = st.columns(4)
    costo_base = c1.number_input("Costo Acquisto (€)", 0.0)
    spese = c2.number_input("Spese extra (€)", 0.0)
    comm = c3.number_input("Commissioni Vinted (%)", 0.0, 15.0, 5.0)
    prezzo_vendita = c4.number_input("Prezzo vendita finale (€)", 0.0)
    
    profitto = calcola_netto(prezzo_vendita, (costo_base + spese), comm)
    st.metric("Margine Netto Reale", f"€ {profitto:.2f}")
    
    if st.button("➕ SALVA ARTICOLO"):
        nuovo = pd.DataFrame([[len(st.session_state.inventario)+1, datetime.now().strftime("%d-%m-%Y"), brand, tipo, taglia, condizioni, costo_base, prezzo_vendita, profitto, "In Vendita"]], 
                             columns=st.session_state.inventario.columns)
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuovo], ignore_index=True)
        salva_db()
        st.success("Salvato nel DB!")

# TAB 4: GESTIONE INVENTARIO
with tab4:
    st.header("📦 Gestione Inventario & Trend")
    st.session_state.inventario = st.data_editor(st.session_state.inventario, use_container_width=True)
    if st.button("💾 Salva modifiche"):
        salva_db()
        st.rerun()
    
    if not st.session_state.inventario.empty:
        st.altair_chart(alt.Chart(st.session_state.inventario).mark_bar().encode(x='Data', y='Profitto Netto (€)', color='Tipo'), use_container_width=True)
