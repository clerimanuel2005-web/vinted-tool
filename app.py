import streamlit as st
import pandas as pd
import altair as alt
import time
import io
from datetime import datetime

# ==========================================
# CONFIGURAZIONE PAGINA E LAYOUT
# ==========================================
st.set_page_config(
    page_title="Vinted Power Seller Pro Suite",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializzazione Database Sessione
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=[
        "Data", "Brand", "Tipo", "Taglia", "Costo (€)", "Vendita (€)", "Netto (€)", "Stato"
    ])

# ==========================================
# FUNZIONI DI SUPPORTO (Business Logic)
# ==========================================
def calcola_profitto(costo, vendita, commissioni=0.10):
    # Simulazione commissioni Vinted
    netto = vendita - (vendita * commissioni) - costo
    return netto

# ==========================================
# HEADER E SIDEBAR
# ==========================================
st.title("🛍️ Vinted Power Seller Pro Suite")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Pannello di Controllo")
    st.info("Benvenuto nel tuo centro di comando per il Reselling.")
    st.write(f"Data Odierna: {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    st.markdown("### 📈 Statistiche Globali")
    tot_investito = st.session_state.inventario["Costo (€)"].sum()
    st.metric("Totale Investito", f"€ {tot_investito:.2f}")

# ==========================================
# TABS PRINCIPALI
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 AI Studio Professionale", 
    "📝 Generatore Descrizioni AI", 
    "💰 Gestione Margini & Lotti", 
    "📊 Analisi Inventory & Data"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO AI (Espanso)
# ==========================================
with tab1:
    st.header("📸 AI Photo Studio: Ghost Mannequin & Mood")
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        st.subheader("Configurazione Setup")
        uploaded_file = st.file_uploader("Carica foto originale:", type=["jpg", "png", "jpeg"])
        tipo_set = st.selectbox("Set Fotografico:", ["Studio Bianco (Manichino Invisible)", "Lifestyle Indoor", "Urban Street", "Minimalist Lookbook"])
        qualita = st.select_slider("Risoluzione Output:", ["Standard", "HD", "4K Ultra-Res"])
        filtri = st.multiselect("Filtri colore:", ["HDR", "Warm Tone", "Cool Contrast", "Vibrant"], default=["HDR"])
        
    with col2:
        if uploaded_file:
            st.image(uploaded_file, caption="Input Originale", use_container_width=True)
            if st.button("🚀 Avvia Processamento AI", type="primary"):
                with st.spinner("Applicazione filtri AI e rimozione sfondo in corso..."):
                    time.sleep(4) # Simulazione processamento pesante
                    st.success("Foto elaborata con successo!")
                    st.markdown("### Anteprima Elaborazione")
                    # Qui verrebbe la visualizzazione dell'immagine post-AI
                    st.image("https://via.placeholder.com/600x400.png?text=Ghost+Mannequin+Result", caption="Output Professionale")
                    st.download_button("📥 Scarica Foto Pro", data=b"fake", file_name="foto_vinted.jpg")
        else:
            st.warning("Carica un file per abilitare il motore di rendering AI.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI (Avanzato)
# ==========================================
with tab2:
    st.header("📝 Generatore di Annunci SEO")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        brand = st.text_input("Marca")
        tipo = st.text_input("Articolo")
    with c2:
        taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL", "XXL"])
        cond = st.selectbox("Stato", ["Nuovo con cartellino", "Nuovo", "Ottime", "Buone"])
    with c3:
        materiale = st.text_input("Materiale")
        misure = st.text_input("Misure (es. 50x70)")

    desc = f"✨ **{tipo.upper()} {brand.upper()}**\n\nVendo questo fantastico capo {brand}, in condizioni {cond.lower()}. Materiale: {materiale}. \n\n📏 Misure: {misure}\n\nSpedizione immediata! 📦"
    st.text_area("Annuncio Generato:", desc, height=250)
    if st.button("Copia Testo"): st.success("Testo copiato nella cache!")

# ==========================================
# TAB 3: CALCOLATORE MARGINI & LOTTI (Dettagliato)
# ==========================================
with tab3:
    st.header("💰 Gestione Economica")
    c1, c2 = st.columns(2)
    with c1:
        costo_acq = st.number_input("Costo Acquisto (€)", min_value=0.0)
        prezzo_v = st.number_input("Prezzo Vendita (€)", min_value=0.0)
    with c2:
        tipo_vendita = st.radio("Tipo Vendita:", ["Singola", "Lotto (Sconto 20%)"])
        if tipo_vendita == "Lotto (Sconto 20%)":
            prezzo_v = prezzo_v * 0.8
        
        netto = calcola_profitto(costo_acq, prezzo_v)
        st.metric("Profitto Netto Stimato", f"€ {netto:.2f}")

    if st.button("💾 Aggiungi all'Inventario"):
        nuova_riga = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), brand, tipo, taglia, costo_acq, prezzo_v, netto, "In Vendita"]],
                                 columns=["Data", "Brand", "Tipo", "Taglia", "Costo (€)", "Vendita (€)", "Netto (€)", "Stato"])
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuova_riga], ignore_index=True)
        st.success("Articolo salvato!")

# ==========================================
# TAB 4: ANALISI TREND & EXPORT (Sistema Completo)
# ==========================================
with tab4:
    st.header("📊 Database & Analisi")
    
    st.dataframe(st.session_state.inventario, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Esporta CSV", st.session_state.inventario.to_csv(index=False), "export.csv", "text/csv")
    with col2:
        if st.button("🗑️ Reset Database"):
            st.session_state.inventario = pd.DataFrame(columns=["Data", "Brand", "Tipo", "Taglia", "Costo (€)", "Vendita (€)", "Netto (€)", "Stato"])
            st.rerun()

    st.subheader("Analisi Trend")
    chart_data = pd.DataFrame({'Mese': ['Gen', 'Feb', 'Mar'], 'Guadagni': [120, 250, 400]})
    st.altair_chart(alt.Chart(chart_data).mark_bar().encode(x='Mese', y='Guadagni'), use_container_width=True)
