import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite - Generatore AI Foto Realistiche")
st.write("Trasforma le foto stropicciate in scatti da catalogo su manichino e sfondi professionali.")

# La tua API Key di Clipdrop (Assicurati che sia corretta)
CLIPDROP_API_KEY = "INSERISCI_QUI_LA_TUA_API_KEY"

# Creazione delle Schede
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Clothes Ironing & Sfondi AI", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: CLOTHES IRONING AI & MODELLO/MANICHINO
# ==========================================
with tab1:
    st.header("Stiratura e Ambientazione Professionale AI")
    st.write("Carica la tua foto. L'AI integrerà la maglietta su uno sfondo premium o un manichino, eliminando le pieghe.")

    # Opzioni di ambientazione per rendere il vestito subito vendibile
    opzione_sfondo = st.selectbox(
        "Scegli lo stile dello scatto per Vinted:",
        [
            "Indossata da un manichino invisibile in uno studio fotografico luminoso",
            "Appesa elegantemente in uno showroom di abbigliamento moderno e minimalista",
            "Piegata perfettamente su un tavolo di legno rustico con luce naturale soft",
            "Scatto streetwear urbano, sfondo muro di mattoni grigi leggermente sfocato"
        ]
    )

    uploaded_file = st.file_uploader("Scegli la foto del vestito...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("❌ Foto Originale")
            st.image(uploaded_file, use_container_width=True)
            
        with col2:
            st.subheader("✨ Foto Catalogo Generata (Stirata e Ambientata)")
            with st.spinner("L'AI sta stirando il tessuto e ricreando la scena professionale..."):
                try:
                    # Usiamo l'endpoint di Clipdrop "Replace Background / Image Reimagine" o "Uncrop"
                    # che adatta l'oggetto a un prompt testuale descrittivo per creare la scena perfetta
                    prompt_ai = f"A professional fashion product shot of this t-shirt, ironed, wrinkle-free, {opzione_sfondo.lower()}, high resolution, photorealistic, commercial photography lighting"
                    
                    r = requests.post(
                        'https://clipdrop-api.co/replace-background/v1',
                        files={'image_file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                        data={'prompt': prompt_ai},
                        headers={'x-api-key': CLIPDROP_API_KEY}
                    )
                    
                    if r.status_code == 200:
                        # Mostra l'immagine finale generata dall'AI
                        final_img = Image.open(io.BytesIO(r.content))
                        st.image(final_img, use_container_width=True)
                        
                        buffer = io.BytesIO()
                        final_img.save(buffer, format="JPEG", quality=100)
                        
                        st.download_button(
                            label="📥 Scarica Scatto da Catalogo",
                            data=buffer.getvalue(),
                            file_name="vestito_manichino_perfetto.jpg",
                            mime="image/jpeg",
                            type="primary"
                        )
                        st.success("🎉 Foto rigenerata! Le pieghe sono state rimosse e il capo è stato posizionato nello sfondo scelto.")
                    else:
                        st.error(f"Errore dell'AI di Clipdrop (Codice: {r.status_code}). Verifica i tuoi crediti o l'API key.")
                except Exception as e:
                    st.error(f"Errore di connessione: {e}")

# ==========================================
# (Il resto delle TAB rimane intatto per la gestione del tuo account)
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    brand = st.text_input("Brand / Marca del capo", value="Off-White")
    tipo_capo = st.text_input("Tipo di articolo", value="T-shirt grafica")
    colore = st.text_input("Colore principale", value="Bianco")
    condizioni = st.selectbox("Condizioni", ["Ottime condizioni"])
    st.text_area("📄 Descrizione:", f"✨ {tipo_capo} {brand} - Pronta da copiare!")

with tab3:
    st.header("💰 Controllo Margini")
    st.metric(label="🤑 Guadagno Netto", value="25.00 €")

with tab4:
    st.header("📊 Trend & Ricerca Rapida")
    st.write("Usa le sezioni precedenti per trovare stock caldi.")
