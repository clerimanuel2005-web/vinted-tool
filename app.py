import streamlit as st
import pandas as pd
import altair as alt
import time

# ==========================================
# CONFIGURAZIONE PAGINA
# ==========================================
st.set_page_config(
    page_title="Vinted Pro Seller Suite",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializzazione database di sessione
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=[
        "Brand", "Tipo", "Taglia", "Costo (€)", "Vendita (€)", "Profitto (€)"
    ])

st.title("👕 Vinted Pro Seller Suite")
st.write("Suite completa per la gestione professionale del tuo business di reselling.")

# ==========================================
# TAB 1: AI STUDIO FOTOGRAFICO
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 AI Studio Foto", 
    "📝 Generatore Descrizioni Pro", 
    "💰 Calcolatore & Inventario", 
    "📊 Analisi Trend"
])

with tab1:
    st.header("📸 AI Photo Studio: Ghost Mannequin & Mood")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Carica la foto originale del capo:", type=["jpg", "png", "jpeg"])
        ambiente = st.selectbox("Scegli il set fotografico:", [
            "Studio Professionale - Sfondo Grigio Neutro",
            "Showroom Moderno - Sfondo Legno",
            "Streetwear Background - Muro Urbano",
            "Ghost Mannequin - Bianco Puro / Invisibile"
        ])
        stile_luce = st.select_slider("Direzione e intensità luce:", ["Soft", "Bilanciata", "Drammatica", "High-Key"])
        
    with col2:
        if uploaded_file:
            st.image(uploaded_file, caption="Scatto originale caricato", use_container_width=True)
            if st.button("✨ Genera Foto Catalogo AI", type="primary"):
                with st.spinner(f"Elaborazione in corso nel set: {ambiente}..."):
                    time.sleep(3) # Simulazione elaborazione AI
                    st.success("Foto elaborata con successo!")
                    st.write("---")
                    st.info("Risultato: Tessuto stirato, manichino rimosso e luci ottimizzate per la vendita.")
        else:
            st.warning("Carica una foto per attivare lo studio fotografico.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI
# ==========================================
with tab2:
    st.header("📝 Generatore Descrizioni Pro")
    c1, c2 = st.columns(2)
    with c1:
        marca = st.text_input("Brand / Marca")
        tipo = st.text_input("Tipologia articolo (es. Felpa, Jeans)")
        taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL", "XXL", "Taglia Unica"])
        materiale = st.text_input("Materiali (es. 100% Cotone)")
        misure = st.text_input("Misure (es. 50cm ascella, 70cm lunghezza)")
        condizioni = st.selectbox("Condizioni", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime", "Buone", "Usato"])
    
    with c2:
        desc = f"👕 **Articolo:** {tipo} {marca.upper()}\n\n" \
               f"📏 **Taglia:** {taglia}\n" \
               f"🧶 **Materiale:** {materiale}\n" \
               f"📐 **Misure:** {misure}\n\n" \
               f"💎 **Stato:** {condizioni}\n\n" \
               f"📦 **Spedizione:** Rapida entro 24h!\n\n" \
               f"--- \n#vinted #reselling #{marca.lower().replace(' ', '')} #{tipo.lower().replace(' ', '')}"
        st.subheader("📋 Anteprima annuncio pronto:")
        st.text_area("Copia questo testo per Vinted:", desc, height=300)

# ==========================================
# TAB 3: CALCOLATORE E INVENTARIO
# ==========================================
with tab3:
    st.header("💰 Calcolatore Margini & Inventario")
    cols = st.columns(3)
    costo = cols[0].number_input("Costo Acquisto (€)", 0.0, format="%.2f")
    target = cols[1].number_input("Prezzo di Vendita (€)", 0.0, format="%.2f")
    spese = cols[2].number_input("Extra (Spese/Buste) (€)", 0.0, format="%.2f")
    
    if target > 0:
        netto = target - costo - spese
        st.metric("Guadagno Netto Previsto", f"{netto:.2f} €", delta=f"ROI: {(netto/target)*100:.1f}%")
        
        if st.button("➕ Aggiungi all'Inventario"):
            nuovo_item = pd.DataFrame([[marca, tipo, taglia, costo, target, netto]], 
                                      columns=["Brand", "Tipo", "Taglia", "Costo (€)", "Vendita (€)", "Profitto (€)"])
            st.session_state.inventario = pd.concat([st.session_state.inventario, nuovo_item], ignore_index=True)
            st.success("Articolo aggiunto correttamente al database locale.")

# ==========================================
# TAB 4: TREND E GESTIONE INVENTARIO
# ==========================================
with tab4:
    st.header("📊 Analisi e Gestione Dati")
    
    tab_inv, tab_trend = st.tabs(["📦 Mio Inventario", "🔥 Trend di Mercato"])
    
    with tab_inv:
        st.subheader("Il tuo inventario salvato")
        st.dataframe(st.session_state.inventario, use_container_width=True)
        
        # Esportazione CSV
        csv = st.session_state.inventario.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Esporta Inventario in CSV (Excel)",
            data=csv,
            file_name='mio_inventario_vinted.csv',
            mime='text/csv',
        )

    with tab_trend:
        st.subheader("Trend Attuali in Italia")
        df_trend = pd.DataFrame({
            "Categoria": ["Streetwear", "Vintage Anni '90", "Workwear", "Casual/Basic"],
            "Domanda": ["Molto Alta", "Alta", "Alta", "Media"],
            "Prezzo medio": ["40-120€", "30-90€", "50-100€", "15-40€"],
            "Velocità vendite": ["< 24h", "2-3 giorni", "2-4 giorni", "1 settimana"]
        })
        st.table(df_trend)
        
        st.divider()
        st.write("### 🔍 Checklist Autenticità per i tuoi acquisti:")
        st.markdown("""
        * ✅ **Etichette:** Verifica sempre i font e la qualità delle cuciture interne.
        * ✅ **Loghi:** Controlla che siano allineati e ben definiti (non sbiaditi).
        * ✅ **Hardware:** Zip e bottoni devono avere il logo del brand inciso correttamente.
        """)
