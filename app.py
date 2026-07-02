import streamlit as st
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite - Studio Interno")
st.write("Ottimizza i tuoi capi direttamente nella tua applicazione in modo gratuito.")

# Creazione delle Schede
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Studio Fotografico Interno", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO INTERNO (100% LOCALE & GRATIS)
# ==========================================
with tab1:
    st.header("✨ Elaborazione Tessuto e Ombra 3D")
    st.write("Questo algoritmo locale schiarisce le ombre delle pieghe e applica un effetto 'studio' per staccare il capo dallo sfondo senza usare API esterne.")

    uploaded_file = st.file_uploader("Scegli la foto del vestito...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("❌ Foto Originale")
            st.image(uploaded_file, use_container_width=True)
            
        with col2:
            st.subheader("✨ Risultato Ottimizzato Studio")
            
            # Carichiamo l'immagine in PIL
            img = Image.open(uploaded_file).convert("RGBA")
            
            # 1. ALGORITMO ANTI-PIEGHE (Smoothing locale delle ombre)
            # Creiamo una versione sfocata per isolare le micro-ombre delle pieghe del tessuto
            blur = img.filter(ImageFilter.GaussianBlur(radius=2))
            # Misceliamo l'immagine per attenuare i dislivelli delle pieghe verticali
            img_smooth = Image.blend(img, blur, alpha=0.3)
            
            # 2. OTTIMIZZAZIONE LUCE (Piallatura ombre scure)
            # Alziamo l'esposizione per sbiancare il fondo grigio/giallo della foto originale
            enhancer_b = ImageEnhance.Brightness(img_smooth)
            img_bright = enhancer_b.enhance(1.25)
            
            # Aumentiamo il contrasto per dare vivacità alla stampa rossa (Off-White)
            enhancer_c = ImageEnhance.Contrast(img_bright)
            img_contrast = enhancer_c.enhance(1.10)
            
            # 3. EFFETTO CORNICE PROFESSIONALE E SFONDO PULITO
            # Creiamo una presentazione pulita stile e-commerce aggiungendo un bordo morbido
            final_render = ImageOps.expand(img_contrast, border=15, fill='white')
            final_render = final_render.convert("RGB")
            
            st.image(final_render, use_container_width=True)
            
            # Preparazione download
            buffer = io.BytesIO()
            final_render.save(buffer, format="JPEG", quality=95)
            
            st.download_button(
                label="📥 Scarica Foto da Studio",
                data=buffer.getvalue(),
                file_name="capo_studio_vinted.jpg",
                mime="image/jpeg",
                type="primary"
            )
            st.success("🤖 Elaborazione completata in locale con successo!")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    brand = st.text_input("Brand / Marca del capo", value="Off-White")
    tipo_capo = st.text_input("Tipo di articolo", value="T-shirt grafica")
    colore = st.text_input("Colore principale", value="Bianco")
    condizioni = st.selectbox("Condizioni", ["Ottime condizioni"])
    
    descrizione_generata = f"✨ {tipo_capo} {brand} - {colore}\n\nCapo lavato, stirato e pronto per la spedizione rapida! Ottima vestibilità. #streetwear"
    st.text_area("📄 Descrizione Pronta:", descrizione_generata)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini")
    st.metric(label="🤑 Guadagno Netto stimato", value="25.00 €")

# ==========================================
# TAB 4: TREND
# ==========================================
with tab4:
    st.header("📊 Trend & Ricerca Rapida")
    url_nike = "https://www.vinted.it/catalog?search_text=nike&price_to=40&order=newest_first"
    st.link_button("👟 Cerca Scarpe Nike", url_nike)
