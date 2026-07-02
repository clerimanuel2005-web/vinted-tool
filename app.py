import streamlit as st
import pandas as pd
import requests
import io
from PIL import Image

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# Creazione delle 4 Schede di Gestione
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
    st.header("🤖 Studio Fotografico AI Gratuito")
    st.write("Inserisci i dettagli del capo per generare una foto perfetta e senza pieghe.")

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        brand_input = st.text_input("Marca del vestito da ricreare:", value="Off-White")
        colore_input = st.text_input("Colore del tessuto:", value="Bianco puro")
    with col_in2:
        dettagli_stampa = st.text_area("Descrivi la stampa/logo sul vestito:", 
                                       value="La classica grande freccia Off-White sul retro, riempita all'interno con un pattern di baci e labbra stampate in rosso.")

    opzione_ambientazione = st.selectbox(
        "Scegli dove posizionare e ambientare il vestito:",
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
                response = requests.post(API_URL, json={"inputs": prompt_scena}, timeout=60)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.subheader("✅ Foto da Catalogo Generata")
                    st.image(image, use_container_width=True)
                    
                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG")
                    st.download_button(
                        label="📥 Scarica Foto per Vinted",
                        data=buffer.getvalue(),
                        file_name="vestito_catalogo_ai.jpg",
                        mime="image/jpeg"
                    )
                    st.success("Immagine creata con successo!")
                else:
                    st.error("Il server gratuito è momentaneamente occupato. Attendi 5 secondi e clicca di nuovo.")
            except Exception as e:
                st.error(f"Errore di generazione: {e}")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    st.write("Compila i campi per generare titolo e descrizione pronti.")

    col_a, col_b = st.columns(2)
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="Puma")
        tipo_capo = st.text_input("Tipo di articolo", value="Felpa con cappuccio")
        colore = st.text_input("Colore principale", value="Bianco con scritte nere")
        
        st.markdown("### 📏 Taglia e Misure")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        with col_t2:
            vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit / Stretto"])
        
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1:
            cm_ascelle = st.text_input("Ascella - Ascella (cm)", placeholder="Es. 54")
        with col_cm2:
            cm_lunghezza = st.text_input("Lunghezza totale (cm)", placeholder="Es. 70")
        
        st.markdown("### 🎚️ Stato del capo")
        condizioni = st.selectbox("Condizioni del capo", [
            "Ottime condizioni (indossato pochissimo, nessun difetto)",
            "Nuovo con cartellino", 
            "Nuovo senza cartellino", 
            "Buone condizioni (normali segni di usura)"
        ])
        difetti = st.text_input("Note o piccoli difetti (opzionale)", value="nessuna")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia} - {colore.capitalize()}"
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti and difetti.lower() != "nessuna" else "• 🔎 Difetti: Nessuno, capo perfetto."
        
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure piatte:\n"
            if cm_ascelle:
                stringa_misure += f"   - Pit to Pit (Ascella-Ascella): {cm_ascelle} cm\n"
            if cm_lunghezza:
                stringa_misure += f"   - Lunghezza totale: {cm_lunghezza} cm\n"

        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo bellissima {tipo_capo.lower()} originale del brand {brand.capitalize()}. Il capo è lavato e igienizzato.

• 🎨 Colore: {colore.capitalize()}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedisco velocemente entro 24 ore 📦. Scrivimi pure in privato per info! 📲

---
Tag:
#{brand.lower()} #{tipo_capo.replace(' ', '').lower()} #{taglia.lower()} #streetwear #reselling
"""
        st.text_input("📌 Titolo dell'annuncio:", titolo_generato)
        st.text_area("📄 Descrizione dell'annuncio:", descrizione_generata, height=350)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini")
    prezzo_acquisto = st.number_input("Quanto hai pagato il capo? (€)", min_value=0.0, value=10.0)
    prezzo_vendita = st.number_input("A quanto vuoi venderlo? (€)", min_value=0.0, value=35.0)
    ricavo_netto = prezzo_vendita - prezzo_acquisto
    st.metric(label="🤑 Guadagno Netto Singolo", value=f"{ricavo_netto:.2f} €")

# ==========================================
# TAB 4: TREND & RICERCA RAPIDA
# ==========================================
with tab4:
    st.header("📊 Trend & Ricerca")
    url_nike = "https://www.vinted.it/catalog?search_text=nike&price_to=40&order=newest_first"
    st.link_button("👟 Cerca Scarpe Nike (<40€) su Vinted", url_nike, use_container_width=True)
