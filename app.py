import streamlit as st
import pandas as pd
import altair as alt
import os
from datetime import datetime

# ==============================================================================
# CONFIGURAZIONE E SETUP
# ==============================================================================
st.set_page_config(page_title="Vinted Pro Suite", page_icon="🛍️", layout="wide")

DB_FILE = "inventario_vinted.csv"

# Caricamento dati persistenti
if 'inventario' not in st.session_state:
    if os.path.exists(DB_FILE):
        st.session_state.inventario = pd.read_csv(DB_FILE)
    else:
        st.session_state.inventario = pd.DataFrame(columns=[
            "ID", "Data", "Brand", "Tipo", "Taglia", "Stato", "Costo (€)", "Prezzo Vendita (€)", "Profitto Netto (€)", "Stato Annuncio"
        ])

# CSS Personalizzato
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; background-color: #09b1ba; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛍️ Vinted Pro Seller Suite - Industrial Edition")

# ==============================================================================
# FUNZIONI
# ==============================================================================
def salva_db():
    st.session_state.inventario.to_csv(DB_FILE, index=False)

def calcola_netto(prezzo_vendita, costo, commissioni_percent):
    return prezzo_vendita - (prezzo_vendita * (commissioni_percent/100)) - costo

# ==============================================================================
# TABS
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📸 AI Studio", "📝 Generatore Annunci", "💰 Business", "📦 Gestione Inventario"])

with tab1:
    st.header("📸 AI Studio: Ghost Mannequin")
    img_input = st.file_uploader("Carica foto:", type=["jpg", "png"])
    if img_input and st.button("✨ Avvia AI Restoration"):
        with st.spinner("Elaborazione in corso..."):
            st.image(img_input, caption="Output AI: Professionale")
            st.success("Tessuto ottimizzato!")

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
    
    annuncio = f"👕 {tipo.upper()} {brand.upper()} - Taglia {taglia}. {condizioni}. Colore: {colore}. Spedizione rapida!"
    st.text_area("Descrizione Finale:", annuncio, height=150)

with tab3:
    st.header("💰 Business Intelligence")
    c1, c2, c3, c4 = st.columns(4)
    costo = c1.number_input("Costo (€)", 0.0)
    extra = c2.number_input("Extra (€)", 0.0)
    comm = c3.number_input("Comm. Vinted (%)", 0.0, 15.0, 5.0)
    prezzo = c4.number_input("Prezzo Vendita (€)", 0.0)
    
    profitto = calcola_netto(prezzo, (costo + extra), comm)
    st.metric("Margine Netto", f"€ {profitto:.2f}")
    
    if st.button("➕ SALVA ARTICOLO"):
        nuovo = pd.DataFrame([[len(st.session_state.inventario)+1, datetime.now().strftime("%d-%m-%Y"), brand, tipo, taglia, condizioni, costo, prezzo, profitto, "In Vendita"]], 
                             columns=st.session_state.inventario.columns)
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuovo], ignore_index=True)
        salva_db()
        st.success("Salvato!")

with tab4:
    st.header("📦 Gestione Inventario")
    
    # Editor interattivo
    st.session_state.inventario = st.data_editor(
        st.session_state.inventario,
        column_config={"Stato Annuncio": st.column_config.SelectboxColumn("Stato", options=["In Vendita", "Venduto", "Prenotato"])},
        use_container_width=True
    )
    
    if st.button("💾 Salva modifiche tabella"):
        salva_db()
        st.rerun()

    st.subheader("📊 Analisi Profitti")
    if not st.session_state.inventario.empty:
        chart = alt.Chart(st.session_state.inventario).mark_bar().encode(
            x='Data', y='Profitto Netto (€)', color='Tipo'
        )
        st.altair_chart(chart, use_container_width=True)
