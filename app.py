import streamlit as st
import pandas as pd
import altair as alt

# Configurazione globale e layout dell'applicazione (Modalità Wide)
st.set_page_config(
    page_title="Vinted Power Seller Suite",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Studio Fotografico (Manuale)", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO (Manuale Pro)
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico: Setup Professionale")
    st.write("Segui le linee guida per ottenere foto catalogo di alta qualità senza dipendere da AI esterne.")

    col_foto1, col_foto2 = st.columns([1.3, 1.7], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Check-list Attrezzatura")
        st.write("• **Sfondo:** Parete bianca o pannello di cartongesso grigio.")
        st.write("• **Luce:** Luce naturale (vicino a una finestra) o due Softbox LED.")
        st.write("• **Esposizione:** Gruccia in legno (non plastica) per capi appesi.")
        st.markdown("### 2️⃣ Parametri Fotocamera/Smartphone")
        st.write("• **ISO:** 100-200 (per evitare rumore).")
        st.write("• **Bianco:** Bilanciamento manuale su bianco neutro.")
        st.write("• **Inquadratura:** Livello occhi, centratura perfetta.")

    with col_foto2:
        st.markdown("### 3️⃣ Workflow Post-Produzione Consigliato")
        data_ritocco = {
            "Parametro": ["Esposizione", "Contrasto", "Saturazione", "Nitidezza", "Temp. Colore"],
            "Valore Consigliato": ["+0.3", "+10", "+5", "+20", "-2 (più freddo)"],
            "Effetto": ["Sfondo più pulito", "Texture visibile", "Colori fedeli", "Dettagli etichette", "Aspetto professionale"]
        }
        st.table(pd.DataFrame(data_ritocco))
        st.info("💡 Consiglio: Scatta sempre in formato quadrato (1:1) per evitare ritagli indesiderati su Vinted.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo", placeholder="Es. Nike, Carhartt...")
        tipo_capo = st.text_input("Tipo di articolo", placeholder="Es. Felpa, T-shirt...")
        colore = st.text_input("Colore e dettagli visivi", placeholder="Es. Bianco con stampa...")
        
        st.markdown("### 📏 Taglia e Misure")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit"])
        
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1:
            cm_ascelle = st.text_input("Ascella - Ascella (cm)")
        with col_cm2:
            cm_lunghezza = st.text_input("Lunghezza totale (cm)")
            
        st.markdown("### 🎚️ Stato del capo")
        condizioni = st.selectbox("Condizioni del capo", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime condizioni", "Buone condizioni"])
        difetti = st.text_input("Note su eventuali difetti", placeholder="Es. Nessuno...")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        stringa_misure = f"• 📐 Misure prese in piano:\n   - Ascella - Ascella: {cm_ascelle} cm\n   - Lunghezza totale: {cm_lunghezza} cm\n" if (cm_ascelle or cm_lunghezza) else ""
        
        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo splendido/a {tipo_capo} del brand {brand}. Articolo selezionato con cura, lavato e igienizzato.

• 🎨 Colore/Dettagli: {colore}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
• 🔎 Difetti: {difetti if difetti else "Nessuno, capo perfetto."}

Spedisco rapidamente entro 24 ore 📦. Disponibile per info in chat! 📲

---
#{brand.replace(' ', '').lower()} #{tipo_capo.replace(' ', '').lower()} #taglia{taglia.lower()} #streetwear #reselling
"""
        st.text_area("📄 Descrizione dell'annuncio:", descrizione_generata, height=320)

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
        tabelle_ricerca = pd.DataFrame({
            "Posizione": [1, 2, 3, 4, 5],
            "Stile": ["Sneakers Retro", "Giacche Tecniche", "Denim Baggy", "Streetwear Tops", "Varsity Vintage"],
            "Liquidità": ["Molto Alta", "Alta", "Media", "Alta", "Media"]
        })
        st.dataframe(tabelle_ricerca, use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("### 📈 Nicchie in Forte Crescita")
        tabelle_nicchie = pd.DataFrame({
            "Nicchia": ["Band T-shirt", "Calcio 90s/00s", "Colorblock Windbreakers", "Workwear Pants"],
            "Crescita": ["+120%", "+105%", "+90%", "+75%"]
        })
        st.dataframe(tabelle_nicchie, use_container_width=True, hide_index=True)
        
    st.markdown("---")
    st.markdown("### ⚠️ Guida Sicurezza: Rischio Repliche")
    tabelle_rischio = pd.DataFrame({
        "Brand a Rischio": ["High-End Streetwear", "Nike Tech/Sport", "Luxury Brand"],
        "Azione Consigliata": ["Richiedi sempre ricevuta", "Verifica font etichette", "Usa solo autenticazione Vinted"]
    })
    st.table(tabelle_rischio)
