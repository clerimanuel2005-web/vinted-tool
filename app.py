import streamlit as st
import pandas as pd
import requests
import io
from PIL import Image

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Generatore Catalogo AI", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: GENERATORE CATALOGO AI
# ==========================================
with tab1:
    st.header("🤖 Generazione Foto su Manichino Invisibile")
    st.write("Inserisci i dettagli del capo per generare da zero una foto perfetta, stirata e ambientata.")

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        brand_input = st.text_input("Marca del vestito:", value="Off-White")
        colore_input = st.text_input("Colore del tessuto:", value="Bianco puro")
    with col_in2:
        dettagli_stampa = st.text_area("Descrivi la stampa/logo:", 
                                       value="La classica grande freccia Off-White sul retro, riempita all'interno con un pattern di baci e labbra stampate in rosso.")

    opzione_ambientazione = st.selectbox(
        "Scegli dove posizionare il vestito:",
        [
            "indossata da un manichino invisibile (effetto ghost mannequin) in uno studio fotografico con luci professionali e sfondo grigio chiaro minimale",
            "appesa a una gruccia di legno minimalista dentro uno showroom di lusso con sfondo sfocato e luci calde",
            "disposta perfettamente in piano (flat lay) su un pavimento di marmo bianco lucido da boutique"
        ]
    )

    if st.button("✨ Genera Foto Professionale Gratis", type="primary"):
        with st.spinner("L'AI sta creando il manichino..."):
            try:
                prompt_scena = f"A high-end professional commercial product photography of a {colore_input.lower()} t-shirt by {brand_input}, perfectly ironed, wrinkle-free, {dettagli_stampa.lower()}. The t-shirt is {opzione_ambientazione}, 8k resolution, photorealistic, cinematic lighting, ultra detailed, retail catalog style."
                API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
                response = requests.post(API_URL, json={"inputs": prompt_scena})
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, use_container_width=True)
                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG")
                    st.download_button(label="📥 Scarica Foto per Vinted", data=buffer.getvalue(), file_name="vestito_ai.jpg", mime="image/jpeg")
                else:
                    st.error("Il server gratuito è occupato, riprova tra un attimo!")
            except Exception as e:
                st.error(f"Errore: {e}")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI (POTENZIATO CON TAGLIA E MISURE!)
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    st.write("Compila i dettagli specifici del capo per generare testo e tag pronti da copiare.")

    col_a, col_b = st.columns(2)
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="Puma")
        tipo_capo = st.text_input("Tipo di articolo", value="Felpa con cappuccio")
        colore = st.text_input("Colore principale", value="Bianco con scritte nere")
        
        # NUOVI CAMPI INPUT PER LA TAGLIA E VESTIBILITÀ
        st.markdown("### 📏 Taglia e Vestibilità")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            taglia = st.selectbox("Taglia ufficiale sull'etichetta", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        with col_t2:
            vestibilita = st.selectbox("Come veste il capo? (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit / Stretto"])
        
        # MISURE IN CENTIMETRI (Opzionali)
        st.markdown("📐 **Misure precise in cm (Consigliato per vendere subito):**")
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1:
            cm_ascelle = st.text_input("Ascella - Ascella (cm)", placeholder="Es. 55")
        with col_cm2:
            cm_lunghezza = st.text_input("Lunghezza totale (cm)", placeholder="Es. 68")

        st.markdown("### 🎚️ Stato del capo")
        condizioni = st.selectbox("Condizioni del capo", [
            "Ottime condizioni (indossato pochissimo, nessun difetto)", 
            "Nuovo con cartellino", 
            "Nuovo senza cartellino", 
            "Buone condizioni (normali segni di usura)",
            "Soddisfacente (presenta piccoli difetti specificati)"
        ])
        difetti = st.text_input("Note o piccoli difetti (opzionale)", value="nessuna")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        
        # Logica di costruzione dinamica di titolo e testo
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia} - {colore.capitalize()}"
        
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti.lower() != "nessuna" else "• 🔎 Difetti: Nessuno, capo in perfetto stato."
        
        # Blocco misure in cm inserito solo se l'utente compila i campi
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure piatte:\n"
            if cm_ascelle:
                stringa_misure += f"   - Pit to Pit (Ascella-Ascella): {cm_ascelle} cm\n"
            if cm_lunghezza:
                stringa_misure += f"   - Lunghezza totale: {cm_lunghezza} cm\n"

        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo bellissima {tipo_capo.lower()} originale del brand {brand.capitalize()}. Il capo è stato lavato, igienizzato e conservato con cura.

• 🎨 Colore: {colore.capitalize()}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedisco velocemente entro 24 ore lavorative ben imballato 📦. Se hai domande, vuoi foto dei dettagli o desideri fare un'offerta sensata, scrivimi pure in chat! 📲

---
Tag per ottimizzare l'algoritmo di ricerca Vinted:
#{brand.lower()} #{tipo_capo.replace(' ', '').lower()} #{colore.split()[0].lower()} #taglia{taglia.lower()} #vintedvintage #streetwear #reselling #y2k
"""
        st.text_input("📌 Titolo dell'annuncio (Clicca due volte per copiare):", titolo_generato)
        st.text_area("📄 Descrizione dell'annuncio (Copia e Incolla su Vinted):", descrizione_generata, height=440)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Sconti sui Lotti")
    prezzo_acquisto = st.number_input("Quanto hai pagato il capo? (€)", min_value=0.0, value=10.0)
    prezzo_vendita = st.number_input("A quanto vuoi venderlo su Vinted? (€)", min_value=0.0, value=35.0)
    ricavo_netto = prezzo_vendita - prezzo_acquisto
    st.metric(label="🤑 Guadagno Netto Singolo", value=f"{ricavo_netto:.2f} €")

# ==========================================
# TAB 4: TREND
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato")
    st.write("Nicchie ad alta rotazione aggiornate.")
    url_nike = "https://www.vinted.it/catalog?search_text=nike&price_to=40&order=newest_first"
    st.link_button("👟 Cerca Stock Nike su Vinted", url_nike)
