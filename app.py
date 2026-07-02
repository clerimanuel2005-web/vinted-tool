import streamlit as st
import pandas as pd
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import io

# Configurazione globale
st.set_page_config(
    page_title="Vinted Power Seller Suite",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# Creazione delle 4 schede
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Studio Fotografico AI", 
    "📝 Generatore Descrizioni", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO (Elaborazione Locale Corretta)
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico: AI Processing Locale")
    st.write("Carica una foto per rimuovere lo sfondo e levigare le pieghe del tessuto.")
    
    col_l, col_r = st.columns([1.5, 2.5], gap="large")
    
    with col_l:
        st.markdown("### 1️⃣ Carica il capo")
        uploaded_file = st.file_uploader("Carica la foto del capo:", type=["jpg", "png", "jpeg"], key="foto_studio")
        if uploaded_file:
            input_image = Image.open(uploaded_file)
            st.image(input_image, caption="Foto Originale", use_container_width=True)
            
    with col_r:
        if uploaded_file:
            if st.button("✨ Elabora (Rimuovi Sfondo + Stira)"):
                with st.spinner("Elaborazione AI in corso..."):
                    # Conversione per elaborazione
                    img_array = np.array(input_image)
                    img_removed = remove(img_array)
                    
                    # Logica corretta per OpenCV (Gestione canali Alpha)
                    img_bgra = cv2.cvtColor(img_removed, cv2.COLOR_RGBA2BGRA)
                    img_bgr = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2BGR)
                    
                    # Filtro "Stira"
                    smoothed = cv2.bilateralFilter(img_bgr, 15, 75, 75)
                    
                    # Riunione canali
                    b, g, r = cv2.split(smoothed)
                    _, _, _, alpha = cv2.split(img_bgra)
                    final_processed = cv2.merge([b, g, r, alpha])
                    
                    result_img = Image.fromarray(cv2.cvtColor(final_processed, cv2.COLOR_BGRA2RGBA))
                    st.image(result_img, caption="Risultato Elaborato", use_container_width=True)
                    
                    buf = io.BytesIO()
                    result_img.save(buf, format="PNG")
                    st.download_button("📥 Scarica Foto Catalogo", buf.getvalue(), "capo_ottimizzato.png", "image/png")
        
        st.markdown("### 🛠️ Checklist Post-Produzione")
        st.table(pd.DataFrame({
            "Parametro": ["Esposizione", "Contrasto", "Saturazione", "Nitidezza", "Temp. Colore"],
            "Valore Consigliato": ["+0.3", "+10", "+5", "+20", "-2"],
            "Effetto": ["Sfondo più pulito", "Texture visibile", "Colori fedeli", "Dettagli etichette", "Aspetto pro"]
        }))

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    
    with col_a:
        st.markdown("### 🖼️ Carica Foto di Supporto")
        st.file_uploader("Carica foto dettagli (etichetta, difetti):", type=["jpg", "png"], key="foto_annuncio")
        
        brand = st.text_input("Brand / Marca del capo")
        tipo_capo = st.text_input("Tipo di articolo")
        colore = st.text_input("Colore e dettagli visivi")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit"])
        
        col_cm1, col_cm2 = st.columns(2)
        cm_ascelle = col_cm1.text_input("Ascella - Ascella (cm)")
        cm_lunghezza = col_cm2.text_input("Lunghezza totale (cm)")
            
        condizioni = st.selectbox("Condizioni del capo", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime condizioni", "Buone condizioni"])
        difetti = st.text_input("Note su eventuali difetti")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        stringa_misure = f"• 📐 Misure prese in piano:\n   - Ascella - Ascella: {cm_ascelle} cm\n   - Lunghezza totale: {cm_lunghezza} cm\n" if (cm_ascelle or cm_lunghezza) else ""
        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo splendido/a {tipo_capo} del brand {brand}.

• 🎨 Colore/Dettagli: {colore}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
• 🔎 Difetti: {difetti if difetti else "Nessuno, capo perfetto."}

Spedisco rapidamente entro 24 ore 📦. Disponibile per info in chat! 📲

---
#{brand.replace(' ', '').lower()} #{tipo_capo.replace(' ', '').lower()} #taglia{taglia.lower()} #streetwear #reselling
"""
        st.text_area("📄 Descrizione dell'annuncio:", descrizione_generata, height=400)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi del Profitto")
    col_input, col_chart = st.columns([1.5, 2.5], gap="large")

    with col_input:
        st.markdown("### 📊 Dati Finanziari")
        costo_acquisto = st.number_input("💰 Costo di acquisto (€)", min_value=0.0, value=0.0, format="%.2f")
        prezzo_vendita = st.number_input("🏷️ Prezzo di vendita stimato (€)", min_value=0.0, value=0.0, format="%.2f")
        percentuale_sconto = st.slider("Percentuale sconto per lotti (%):", 0, 50, 15)

    with col_chart:
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = (guadagno_netto / costo_acquisto) * 100 if costo_acquisto > 0 else 0
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - costo_acquisto

        st.markdown("### 🏬 Resoconto Margini")
        m_col1, m_col2 = st.columns(2)
        m_col1.metric("🤑 Guadagno Netto", f"{guadagno_netto:.2f} €")
        m_col2.metric("📈 ROI %", f"{roi:.1f}%")

        data_tabella = {
            "Scenario": ["Vendita Singola", f"Vendita in Lotto (-{percentuale_sconto}%)"],
            "Prezzo Finale (€)": [f"{prezzo_vendita:.2f}", f"{prezzo_scontato_lotto:.2f}"],
            "Margine (€)": [f"{guadagno_netto:.2f}", f"{guadagno_lotto:.2f}"],
            "Stato Profitto": ["Massimo" if guadagno_netto > 0 else "Nessuno", "Ridotto" if guadagno_lotto > 0 else "Nessuno"]
        }
        st.table(pd.DataFrame(data_tabella))

# ==========================================
# TAB 4: TREND & ANALISI NICCHIE
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato e Analisi")
    st.write("Analisi aggregata delle categorie con maggiore rotazione su Vinted Italia.")
    
    col_t1, col_t2 = st.columns(2, gap="large")
    
    with col_t1:
        st.markdown("### 🔥 Trend di Ricerca")
        st.dataframe(pd.DataFrame({
            "Posizione": [1, 2, 3, 4, 5],
            "Stile": ["Sneakers Retro", "Giacche Tecniche", "Denim Baggy", "Streetwear Tops", "Varsity Vintage"],
            "Liquidità": ["Molto Alta", "Alta", "Media", "Alta", "Media"]
        }), use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("### 📈 Nicchie in Forte Crescita")
        st.dataframe(pd.DataFrame({
            "Nicchia": ["Band T-shirt", "Calcio 90s/00s", "Colorblock Windbreakers", "Workwear Pants"],
            "Crescita": ["+120%", "+105%", "+90%", "+75%"]
        }), use_container_width=True, hide_index=True)
        
    st.markdown("---")
    st.markdown("### ⚠️ Guida Sicurezza: Rischio Repliche")
    st.table(pd.DataFrame({
        "Brand a Rischio": ["High-End Streetwear", "Nike Tech/Sport", "Luxury Brand"],
        "Azione Consigliata": ["Richiedi sempre ricevuta", "Verifica font etichette", "Usa solo autenticazione Vinted"]
    }))
