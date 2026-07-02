import streamlit as st
import pandas as pd
import requests
import io
from PIL import Image, ImageFilter, ImageOps
import numpy as np
from rembg import remove

# Configurazione obbligatoria della pagina Streamlit
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Manichino & Stiratura Avanzata AI", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: INTEGRAZIONE SFONDO E ADATTAMENTO ARTICOLO
# ==========================================
with tab1:
    st.header("📸 Ottimizzazione Sfondo Fotografico via AI")
    st.write("Posiziona la foto del tuo capo di abbigliamento su uno sfondo professionale da e-commerce generato dall'intelligenza artificiale.")

    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Trascina qui la foto della maglietta:", type=["jpg", "jpeg", "png"], key="vinted_uploader")
        
        if foto_originale:
            st.image(foto_originale, caption="Foto originale caricata", width=130)

        st.markdown("### 2️⃣ Personalizza l'Ambiente")
        tipo_sfondo_scelto = st.selectbox(
            "Seleziona lo sfondo dello studio fotografico:",
            [
                "Studio grigio minimalist, luce morbida da catalogo",
                "Showroom di lusso sfocato, luci calde",
                "Sfondo bianco puro e-commerce"
            ]
        )

        proporzione_capo = st.slider("Dimensione del livello nello sfondo:", 50, 90, 70)

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Elaborato")
        
        if foto_originale is not None:
            if st.button("✨ Genera Foto Catalogo", type="primary"):
                with st.spinner("Scontornamento dell'articolo e fusione con lo sfondo AI in corso..."):
                    try:
                        # 1. Caricamento immagine e correzione orientamento EXIF
                        img_input = Image.open(foto_originale)
                        img_input = ImageOps.exif_transpose(img_input)
                        
                        # 2. Rimozione sfondo originale (Scontornamento automatico pulito)
                        maglietta_isolata = remove(img_input).convert("RGBA")
                        
                        # 3. Mappatura prompt per lo sfondo generativo
                        prompt_mappa = {
                            "Studio grigio minimalist, luce morbida da catalogo": "Professional product photography background, elegant empty showroom studio, neutral soft grey background, commercial catalog lighting, 8k, photorealistic",
                            "Showroom di lusso sfocato, luci calde": "Luxury fashion boutique clothing store interior blurred background, elegant display stand area, warm cinematic lighting, fashion lookbook",
                            "Sfondo bianco puro e-commerce": "Clean minimalist bright solid white studio background for e-commerce catalog, studio soft lighting, sharp focus"
                        }
                        
                        prompt_sfondo = prompt_mappa[tipo_sfondo_scelto].replace(" ", "%20")
                        sfondo_url = f"https://image.pollinations.ai/p/{prompt_sfondo}?width=1080&height=1080&nologo=true&model=flux&seed=45"
                        
                        response_sfondo = requests.get(sfondo_url, timeout=30)
                        
                        if response_sfondo.status_code == 200:
                            sfondo_reale = Image.open(io.BytesIO(response_sfondo.content)).resize((1080, 1080)).convert("RGBA")
                            
                            # 4. Ridimensionamento proporzionale dell'articolo scontornato
                            dim_max = int(1080 * (proporzione_capo / 100))
                            maglietta_isolata.thumbnail((dim_max, dim_max), Image.Resampling.LANCZOS)
                            
                            # 5. Generazione ombra artificiale per dare profondità sul manichino virtuale
                            alpha_canale = maglietta_isolata.getchannel('A')
                            ombra = Image.new("RGBA", maglietta_isolata.size, (0, 0, 0, 65))
                            ombra.putalpha(alpha_canale)
                            ombra = ombra.resize((maglietta_isolata.width + 12, maglietta_isolata.height + 12))
                            ombra = ombra.filter(ImageFilter.GaussianBlur(12))
                            
                            # 6. Composizione finale a livelli (Sfondo + Ombra + Capo)
                            telaio_trasparente = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
                            pos_x = (1080 - maglietta_isolata.width) // 2
                            pos_y = (1080 - maglietta_isolata.height) // 2
                            
                            telaio_trasparente.paste(ombra, (pos_x - 6, pos_y + 8))
                            telaio_trasparente.paste(maglietta_isolata, (pos_x, pos_y), mask=maglietta_isolata)
                            
                            immagine_pronta = Image.alpha_composite(sfondo_reale, telaio_trasparente).convert("RGB")
                            
                            # Mostra il risultato a schermo
                            st.image(immagine_pronta, caption="Foto finale ottimizzata per la vendita", use_container_width=True)
                            
                            # Download button
                            buffer = io.BytesIO()
                            immagine_pronta.save(buffer, format="JPEG", quality=98)
                            st.download_button(
                                label="📥 Scarica Immagine HQ
