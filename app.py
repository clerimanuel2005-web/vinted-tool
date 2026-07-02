import os
import sys
import subprocess

# ==========================================
# SISTEMA DI AUTO-RIPARAZIONE ALL'AVVIO
# ==========================================
# Se i server di Streamlit Cloud hanno problemi di cache, questo blocco forza l'installazione
try:
    from PIL import Image, ImageImageFilter, ImageOps
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageImageFilter, ImageOps

try:
    from rembg import remove
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rembg"])
    from rembg import remove

import streamlit as st
import pandas as pd
import requests
import io
import base64
import numpy as np

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
# TAB 1: MANICHINO INVISIBILE E ADATTAMENTO SFONDO
# ==========================================
with tab1:
    st.header("📸 Manichino Invisible & Cambio Sfondo Automatico via AI")
    st.write("Isola la tua maglietta mantenendo il logo originale intatto al 100%, posizionandola su uno sfondo professionale da e-commerce.")

    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Trascina qui la foto originale della maglietta (anche su letto o pavimento):", type=["jpg", "jpeg", "png"], key="vinted_uploader")
        
        if foto_originale:
            st.image(foto_originale, caption="Foto originale caricata", width=150)

        st.markdown("### 2️⃣ Personalizza l'Ambiente")
        tipo_sfondo_scelto = st.selectbox(
            "Seleziona lo sfondo dello studio fotografico:",
            [
                "Studio grigio minimalista, luce morbida da catalogo",
                "Showroom di lusso sfocato, luci calde",
                "Sfondo bianco puro e-commerce"
            ]
        )

        proporzione_capo = st.slider("Dimensione della maglietta nello sfondo:", 50, 90, 70, step=5, help="Regola quanto deve apparire grande la maglietta rispetto al riquadro finale.")

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Elaborato")
        
        if foto_originale is not None:
            if st.button("✨ Genera Foto Catalogo", type="primary"):
                with st.spinner("Isolamento della maglietta e fusione dello sfondo in corso..."):
                    try:
                        # 1. RIMOZIONE SFONDO AUTOMATICA
                        input_image = Image.open(foto_originale)
                        # Corregge l'orientamento se la foto viene da uno smartphone
                        input_image = ImageOps.exif_transpose(input_image)
                        
                        maglietta_senza_sfondo = remove(input_image).convert("RGBA")
                        
                        # 2. GENERAZIONE DELLO SFONDO CON POLLINATIONS AI
                        prompt_mappa = {
                            "Studio grigio minimalista, luce morbida da catalogo": "Professional product photography background, elegant empty showroom studio, neutral soft grey background, commercial catalog lighting, 8k, photorealistic",
                            "Showroom di lusso sfocato, luci calde": "Luxury fashion boutique clothing store interior blurred background, elegant display stand area, warm cinematic lighting, fashion lookbook",
                            "Sfondo bianco puro e-commerce": "Clean minimalist bright solid white studio background for e-commerce catalog, studio soft lighting, sharp focus"
                        }
                        
                        prompt_sfondo = prompt_mappa[tipo_sfondo_scelto].replace(" ", "%20")
                        sfondo_url = f"https://image.pollinations.ai/p/{prompt_sfondo}?width=1080&height=1080&nologo=true&model=flux&seed=42"
                        
                        response_sfondo = requests.get(sfondo_url, timeout=30)
                        
                        if response_sfondo.status_code == 200:
                            sfondo_ai = Image.open(io.BytesIO(response_sfondo.content)).resize((1080, 1080)).convert("RGBA")
                            
                            # 3. ADATTAMENTO E FUSIONE LIVELLI
                            dim_max = int(1080 * (proporzione_capo / 100))
                            maglietta_senza_sfondo.thumbnail((dim_max, dim_max), Image.Resampling.LANCZOS)
                            
                            # Creazione di un'ombra morbida realistica sotto il capo
                            alpha = maglietta_senza_sfondo.getchannel('A')
                            shadow = Image.new("RGBA", maglietta_senza_sfondo.size, (0, 0, 0, 80))
                            shadow.putalpha(alpha)
                            shadow = shadow.resize((maglietta_senza_sfondo.width + 10, maglietta_senza_sfondo.height + 10))
                            shadow = shadow.filter(ImageImageFilter.GaussianBlur(15))
                            
                            # Composizione finale
                            livello_composizione = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
                            pos_x = (1080 - maglietta_senza_sfondo.width) // 2
                            pos_y = (1080 - maglietta_senza_sfondo.height) // 2
                            
                            livello_composizione.paste(shadow, (pos_x - 5, pos_y + 10))
                            livello_composizione.paste(maglietta_senza_sfondo, (pos_x, pos_y), mask=maglietta_senza_sfondo)
                            
                            foto_finale = Image.alpha_composite(sfondo_ai, livello_composizione).convert("RGB")
                            
                            # Output a schermo
                            st.image(foto_finale, caption="Ecco il tuo capo elaborato sul nuovo sfondo", use_container_width=True)
                            
                            # Bottone di download
                            buffer = io.BytesIO()
                            foto_finale.save(buffer, format="JPEG", quality=95)
                            st.download_button(
                                label="📥 Scarica Foto Finita",
                                data=buffer.getvalue(),
                                file_name="vinted_studio_perfect.jpg",
                                mime="image/jpeg"
                            )
                            st.success("Fatto! Sfondo applicato correttamente senza deformare l'immagine.")
                        else:
                            st.error("Il server AI degli sfondi è momentaneamente occupato. Riprova tra un istante.")
                            
                    except Exception as e:
                        st.error(f"Errore durante l'elaborazione dell'immagine: {e}")
        else:
            st.info("💡 Carica lo scatto originale a sinistra per iniziare.")


# ==========================================
# TAB 2
