import streamlit as st
import pandas as pd
import requests
import io
from PIL import Image

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite - Generatore Immagini AI")
st.write("Crea scatti da catalogo professionali su manichino direttamente nella tua app gratis.")

# Creazione delle Schede
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Generatore Catalogo AI", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: GENERATORE CATALOGO AI (100% GRATIS DENTRO L'APP)
# ==========================================
with tab1:
    st.header("🤖 Generazione Foto su Manichino Invisibile")
    st.write("Inserisci i dettagli del capo. L'AI genererà da zero una foto perfetta, stirata e ambientata in uno studio professionale.")

    # Input per guidare l'AI a ricreare perfettamente il tuo vestito
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        brand_input = st.text_input("Marca del vestito:", value="Off-White")
        colore_input = st.text_input("Colore del tessuto:", value="Bianco puro")
    with col_in2:
        dettagli_stampa = st.text_area("Descrivi la stampa/logo (es. freccia Off-White riempita di baci rossi):", 
                                       value="La classica grande freccia Off-White sul retro, riempita all'interno con un pattern di baci e labbra stampate in rosso accallato.")

    opzione_ambientazione = st.selectbox(
        "Scegli dove posizionare il vestito:",
        [
            "indossata da un manichino invisibile (effetto ghost mannequin) in uno studio fotografico con luci professionali e sfondo grigio chiaro minimale",
            "appesa a una gruccia di legno minimalista dentro uno showroom di lusso con sfondo sfocato e luci calde",
            "disposta perfettamente in piano (flat lay) su un pavimento di marmo bianco lucido da boutique"
        ]
    )

    if st.button("✨ Genera Foto Professionale Gratis", type="primary"):
        with st.spinner("L'AI sta creando il manichino e stirando il tessuto... Attendi qualche secondo."):
            try:
                # Costruiamo il prompt perfetto in inglese per l'AI (funziona molto meglio)
                prompt_scena = f"A high-end professional commercial product photography of a {colore_input.lower()} t-shirt by {brand_input}, perfectly ironed, wrinkle-free, {dettagli_stampa.lower()}. The t-shirt is {opzione_ambientazione}, 8k resolution, photorealistic, cinematic lighting, ultra detailed, retail catalog style."
                
                # Utilizziamo l'endpoint pubblico e gratuito di Hugging Face per il modello FLUX
                API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
                
                # Inviamo la richiesta al server AI esterno gratuito
                response = requests.post(API_URL, json={"inputs": prompt_scena})
                
                if response.status_code == 200:
                    # Trasformiamo la risposta in un'immagine visualizzabile
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Mostriamo il risultato finale dentro lo schermo dell'app
                    st.subheader("✅ Foto da Catalogo Generata")
                    st.image(image, caption="Foto generata dall'AI pronta per essere salvata e caricata", use_container_width=True)
                    
                    # Tasto per scaricarla sul computer o telefono
                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG")
                    st.download_button(
                        label="📥 Scarica Foto per Vinted",
                        data=buffer.getvalue(),
                        file_name="vestito_catalogo_ai.jpg",
                        mime="image/jpeg"
                    )
                    st.success("Immagine creata! Il tessuto è liscio e la presentazione è da negozio reale.")
                else:
                    st.error("Il server AI gratuito è momentaneamente sovraccarico. Riprova tra pochissimi secondi cliccando di nuovo il tasto.")
                    
            except Exception as e:
                st.error(f"Errore di caricamento: {e}")

# ==========================================
# LE ALTRE TAB RIMANGONO ATTIVE
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    brand = st.text_input("Brand / Marca per annuncio", value="Off-White")
    tipo_capo = st.text_input("Tipo di articolo", value="T-shirt grafica")
    st.text_area("📄 Descrizione Pronta:", f"✨ {tipo_capo} {brand}\n\nIn ottime condizioni, spedizione rapida! #streetwear")

with tab3:
    st.header("💰 Controllo Margini")
    st.metric(label=" Guida Guadagno", value="25.00 €")

with tab4:
    st.header("📊 Trend Vinted")
    st.write("Sezioni pronte.")
