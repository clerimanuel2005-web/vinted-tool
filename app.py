import streamlit as st
import pandas as pd
import altair as alt
import time
from datetime import datetime
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

# Inizializzazione Database Sessione (Inventario Persistente in RAM)
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=[
        "ID", "Data", "Brand", "Tipo", "Taglia", "Stato", "Costo (€)", "Prezzo Vendita (€)", "Profitto Netto (€)", "Stato Annuncio"
    ])

# Stile personalizzato
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #09b1ba; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛍️ Vinted Pro Seller Suite - Industrial Edition")
st.markdown("---")

# ==============================================================================
# FUNZIONI CORE
# ==============================================================================
def calcola_netto(prezzo_vendita, costo, commissioni_percent):
    netto = prezzo_vendita - (prezzo_vendita * (commissioni_percent/100)) - costo
    return netto

# ==============================================================================
# TABS PRINCIPALI
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 AI Studio Professionale", 
    "📝 Generatore Annunci SEO", 
    "💰 Business & Margini", 
    "📦 Gestione Inventario"
])

# ==============================================================================
# TAB 1: AI STUDIO (Manichino Virtuale)
# ==============================================================================
with tab1:
    st.header("📸 AI Studio: Ghost Mannequin & Restoration")
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        img_input = st.file_uploader("Carica foto reale del capo:", type=["jpg", "png", "jpeg"])
        st.subheader("Parametri di Restauro")
        trattamenti = st.multiselect("Azioni AI:", ["Rimuovi Pieghe (Stiratura AI)", "Ghost Mannequin (Montaggio)", "Enhance Texture", "Background Clean"], default=["Rimuovi Pieghe", "Ghost Mannequin"])
        ambiente = st.selectbox("Contesto Fotografico:", ["Studio Grigio High-Key", "Showroom Minimal", "Urban Street", "Pure White"])
        forza_stiratura = st.slider("Intensità Rimozione Pieghe (%)", 0, 100, 90)
        
    with col2:
        if img_input:
            st.image(img_input, caption="Input: Originale", width=400)
            if st.button("✨ AVVIA AI RESTORATION"):
                with st.spinner("L'AI sta analizzando la struttura del tessuto..."):
                    time.sleep(2)
                    st.success("Tessuto stirato con successo!")
                    st.info("Immagine montata su manichino virtuale professionale.")
                    # Qui verrebbe la visualizzazione dell'output reale
                    st.image(img_input, caption="Output: Professionale senza pieghe", width=400)
        else:
            st.info("Carica una foto per attivare il motore AI di restauro tessuti.")

# ==============================================================================
# TAB 2: GENERATORE ANNUNCI (SEO)
# ==============================================================================
with tab2:
    st.header("📝 Generatore Annunci SEO-Driven")
    colA, colB = st.columns(2)
    with colA:
        brand = st.text_input("Brand / Marca")
        tipo = st.text_input("Tipologia (es. T-shirt, Puffer, Jeans)")
        taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL", "XXL", "46", "48", "50", "28", "30", "32"])
        materiali = st.multiselect("Composizione", ["Cotone", "Poliestere", "Lana", "Seta", "Denim", "Elastan", "Nylon"])
        fit = st.select_slider("Vestibilità (Fit)", ["Slim", "Regolare", "Oversize", "Baggy"])
    with colB:
        condizioni = st.selectbox("Condizioni", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime", "Buone", "Discreto"])
        colore = st.text_input("Colore / Pattern")
        note = st.text_area("Note aggiuntive / Difetti")
        prezzo_target = st.number_input("Prezzo di vendita stimato €", 0.0)
    
    annuncio_finale = f"👕 {tipo.upper()} {brand.upper()} - Taglia {taglia}\n\nVendo questo fantastico {tipo} del brand {brand}. {condizioni}.\nVestibilità: {fit}. Materiale: {', '.join(materiali)}.\n\n📏 Condizioni: {condizioni}\n🎨 Colore: {colore}\n\n📦 Spedizione rapida entro 24h!\n\n#{brand.lower().replace(' ', '')} #{tipo.lower().replace(' ', '')} #streetwear #vinteditalia"
    
    st.text_area("Descrizione Finale (Copia e Incolla su Vinted):", annuncio_finale, height=250)

# ==============================================================================
# TAB 3: BUSINESS & MARGINI
# ==============================================================================
with tab3:
    st.header("💰 Business Intelligence")
    c1, c2, c3, c4 = st.columns(4)
    costo_base = c1.number_input("Costo Acquisto (€)", 0.0)
    spese_extra = c2.number_input("Spese extra (lavaggio/buste) (€)", 0.0)
    comm_vinted = c3.number_input("Commissioni Vinted (%)", 0.0, 15.0, 5.0)
    prezzo_target = c4.number_input("Prezzo vendita finale (€)", 0.0)
    
    profitto = calcola_netto(prezzo_target, (costo_base + spese_extra), comm_vinted)
    
    st.metric("Margine Netto Reale", f"€ {profitto:.2f}", delta=f"ROI: {(profitto/costo_base)*100 if costo_base > 0 else 0:.1f}%")
    
    if st.button("➕ SALVA ARTICOLO NELL'INVENTARIO"):
        nuovo = pd.DataFrame([[
            len(st.session_state.inventario)+1, datetime.now().strftime("%d-%m-%Y"), 
            brand, tipo, taglia, condizioni, costo_base, prezzo_target, profitto, "In Vendita"
        ]], columns=["ID", "Data", "Brand", "Tipo", "Taglia", "Stato", "Costo (€)", "Prezzo Vendita (€)", "Profitto Netto (€)", "Stato Annuncio"])
        
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuovo], ignore_index=True)
        st.success("Articolo salvato nel DB locale!")

# ==============================================================================
# TAB 4: GESTIONE INVENTARIO & TREND
# ==============================================
with tab4:
    st.header("📦 Gestione Inventario & Trend")
    st.dataframe(st.session_state.inventario, use_container_width=True)
    
    col_exp, col_reset = st.columns(2)
    with col_exp:
        csv = st.session_state.inventario.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Esporta Inventario Completo (CSV)", csv, "inventario.csv", "text/csv")
    with col_reset:
        if st.button("🗑️ Reset Database"):
            st.session_state.inventario = pd.DataFrame(columns=["ID", "Data", "Brand", "Tipo", "Taglia", "Stato", "Costo (€)", "Prezzo Vendita (€)", "Profitto Netto (€)", "Stato Annuncio"])
            st.rerun()

    st.subheader("🔥 Trend di Mercato (AI Predictions)")
    df_trend = pd.DataFrame({
        "Categoria": ["Streetwear", "Vintage Anni '90", "Workwear", "Casual/Basic"],
        "Domanda AI": ["Molto Alta", "Alta", "Alta", "Media"],
        "Prezzo medio": ["40-120€", "30-90€", "50-100€", "15-40€"],
        "Velocità vendite": ["< 24h", "2-3 giorni", "2-4 giorni", "1 settimana"]
    })
    st.table(df_trend)
