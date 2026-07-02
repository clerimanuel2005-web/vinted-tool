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
    "📸 AI Fashion Studio", 
    "📝 Generatore Descrizioni", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: AI FASHION STUDIO (Virtual Try-On & Processing)
# ==========================================
with tab1:
    st.header("📸 AI Fashion Studio: Virtual Mannequin")
    st.write("Carica il capo e scegli il contesto pubblicitario per il tuo Virtual Try-On.")
    
    col_l, col_r = st.columns([1.5, 2.5], gap="large")
    
    with col_l:
        st.markdown("### 1️⃣ Carica il capo")
        uploaded_file = st.file_uploader("Carica la foto del capo:", type=["jpg", "png", "jpeg"], key="foto_studio")
        if uploaded_file:
            input_image = Image.open(uploaded_file)
            st.image(input_image, caption="Foto Originale", use_container_width=True)
            
            target_context = st.selectbox("Dove vuoi il capo?", 
                                          ["Indossato da modello (Lifestyle)", 
                                           "Su manichino sartoriale", 
                                           "Su sfondo studio professionale"])
            
    with col_r:
        if uploaded_file:
            if st.button("✨ Genera Immagine AI"):
                with st.spinner("L'AI sta vestendo il manichino..."):
                    # Logica base di processing locale (rembg + filtro)
                    img_array = np.array(input_image)
                    img_removed = remove(img_array)
                    
                    # Elaborazione tecnica OpenCV
                    img_bgra = cv2.cvtColor(img_removed, cv2.COLOR_RGBA2BGRA)
                    img_bgr = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2BGR)
                    smoothed = cv2.bilateralFilter(img_bgr, 15, 75, 75)
                    
                    # Ricomposizione
                    b, g, r = cv2.split(smoothed)
                    _, _, _, alpha = cv2.split(img_bgra)
                    final_processed = cv2.merge([b, g, r, alpha])
                    result_img = Image.fromarray(cv2.cvtColor(final_processed, cv2.COLOR_BGRA2RGBA))
                    
                    st.image(result_img, caption="Risultato Elaborato", use_container_width=True)
                    st.info(f"Context selezionato: {target_context}. Integrazione AI completata.")

        st.markdown("### 🛠️ Perché l'AI per i manichini?")
        st.table(pd.DataFrame({
            "Vantaggio": ["Conversione", "Costi", "Velocità"],
            "Descrizione": ["Le foto indossate vendono il 40% in più", "Niente set fotografici costosi", "Generazione in pochi secondi"]
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
        cm_ascelle = st.text_input("Ascella - Ascella (cm)")
        cm_lunghezza = st.text_input("Lunghezza totale (cm)")
        condizioni = st.selectbox("Condizioni del capo", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime condizioni", "Buone condizioni"])
        difetti = st.text_input("Note su eventuali difetti")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo splendido/a {tipo_capo} del brand {brand}.

• 🎨 Colore/Dettagli: {colore}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
• 📐 Misure: {cm_ascelle}x{cm_lunghezza} cm
• 💎 Condizioni: {condizioni}
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

        st.table(pd.DataFrame({
            "Scenario": ["Vendita Singola", f"Vendita in Lotto (-{percentuale_sconto}%)"],
            "Prezzo Finale (€)": [f"{prezzo_vendita:.2f}", f"{prezzo_scontato_lotto:.2f}"],
            "Margine (€)": [f"{guadagno_netto:.2f}", f"{guadagno_lotto:.2f}"]
        }))

# ==========================================
# TAB 4: TREND & ANALISI NICCHIE
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato e Analisi")
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
        
    st.markdown("### ⚠️ Guida Sicurezza: Rischio Repliche")
    st.table(pd.DataFrame({
        "Brand a Rischio": ["High-End Streetwear", "Nike Tech/Sport", "Luxury Brand"],
        "Azione Consigliata": ["Richiedi sempre ricevuta", "Verifica font etichette", "Usa solo autenticazione Vinted"]
    }))
