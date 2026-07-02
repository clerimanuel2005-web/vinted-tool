import streamlit as st
import pandas as pd
import altair as alt
import time

# Configurazione globale
st.set_page_config(page_title="Vinted Pro Suite", page_icon="👕", layout="wide")

st.title("👕 Vinted Pro Seller Suite")
st.write("Suite completa per il reselling professionale.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📸 AI Studio Foto", 
    "📝 Generatore Descrizioni Pro", 
    "💰 Calcolatore Margini", 
    "📊 Analisi Trend & Strategia"
])

# ==========================================
# TAB 1: AI STUDIO (Manichini e Ambienti)
# ==========================================
with tab1:
    st.header("📸 AI Photo Studio: Ghost Mannequin & Mood")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Carica la foto del capo:", type=["jpg", "png"])
        ambiente = st.selectbox("Scegli il set fotografico:", [
            "Studio Professionale - Sfondo Grigio",
            "Showroom Moderno - Sfondo Legno",
            "Streetwear Background - Muro Urbano",
            "Ghost Mannequin - Bianco Puro"
        ])
        stile_luce = st.select_slider("Direzione luce:", ["Soft", "Drammatica", "High-Key"])
        if uploaded_file:
            st.image(uploaded_file, caption="Foto originale", use_container_width=True)

    with col2:
        if uploaded_file:
            if st.button("✨ Genera Foto Catalogo AI", type="primary"):
                with st.spinner(f"Elaborazione in corso: {ambiente}..."):
                    time.sleep(3) # Simulazione elaborazione AI
                    st.success("Foto elaborata con successo!")
                    st.info("Immagine pronta per il download.")
                    # Placeholder per immagine generata
                    st.write("---")
                    st.write("Risultato: Output stilizzato con manichino invisibile e luci ottimizzate.")
        else:
            st.warning("Carica una foto per procedere.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI (Dettagliato)
# ==========================================
with tab2:
    st.header("📝 Scrittura Annunci Avanzata")
    c1, c2 = st.columns(2)
    with c1:
        marca = st.text_input("Brand")
        tipo = st.text_input("Tipologia (es. Felpa, Jeans)")
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
               f"--- \n#vinted #reselling #{marca.lower()} #{tipo.lower()}"
        st.subheader("📋 Output Annuncio:")
        st.text_area("Copia & Incolla:", desc, height=300)

# ==========================================
# TAB 3: CALCOLATORE PREZZI
# ==========================================
with tab3:
    st.header("💰 Analisi Profitto & Pricing")
    cols = st.columns(3)
    costo = cols[0].number_input("Costo Acquisto (€)", 0.0)
    target = cols[1].number_input("Prezzo di Vendita Target (€)", 0.0)
    spese = cols[2].number_input("Costi Accessori (Spese, Buste) (€)", 0.0)
    
    if target > 0:
        netto = target - costo - spese
        st.metric("Guadagno Netto", f"{netto:.2f} €", delta=f"{(netto/target)*100:.1f}% ROI")
        st.success("Strategia di pricing impostata correttamente.")

# ==========================================
# TAB 4: TREND & STRATEGIE (Arricchito)
# ==========================================
with tab4:
    st.header("📊 Analisi di Mercato Italia")
    tab_trend, tab_rischi = st.tabs(["🔥 Trend Attuali", "⚠️ Guida Autenticità"])
    
    with tab_trend:
        df = pd.DataFrame({
            "Categoria": ["Streetwear", "Vintage Anni '90", "Workwear", "Casual/Basic"],
            "Domanda": ["Molto Alta", "Alta", "Alta", "Media"],
            "Prezzo medio": ["40-120€", "30-90€", "50-100€", "15-40€"],
            "Velocità vendite": ["< 24h", "2-3 giorni", "2-4 giorni", "1 settimana"]
        })
        st.table(df)
        
    with tab_rischi:
        st.write("### 🔍 Checklist Autenticità:")
        st.write("* ✅ **Etichette interne:** Controlla sempre i codici di lavaggio.")
        st.write("* ✅ **Cuciture:** Verifica regolarità e assenza di fili volanti.")
        st.write("* ✅ **Materiali:** Tasta la qualità del tessuto e del peso.")
        st.write("* ✅ **Hardware:** Controlla zip, bottoni e loghi incisi.")
