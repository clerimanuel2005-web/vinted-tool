import streamlit as st
import pandas as pd
import requests
import io
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from rembg import remove, new_session

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# Inizializzazione sessioni
if "session_standard" not in st.session_state:
    st.session_state.session_standard = new_session(model_name="u2net")

st.title("🛍️ Vinted Power Seller Suite")
st.write("L'hub definitivo per ottimizzare le foto dei tuoi capi.")

tab1, tab2, tab3, tab4 = st.tabs(["📸 Manichino AI", "📝 Generatore Descrizioni", "💰 Calcolatore Prezzi", "📊 Trend di Mercato"])

# ==========================================
# TAB 1: RIMOZIONE SFONDO (CON FIX LAB)
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        foto_originale = st.file_uploader("Carica foto:", type=["jpg", "jpeg", "png"])
        modalita = st.selectbox("Modalità:", ["Bordi Precisi (Per capi bianchi)", "Standard (AI)"])
        sfondo = st.selectbox("Scenario:", ["Gruccia (Cemento)", "Showroom Lusso", "Bianco E-commerce"])
        proporzione = st.slider("Dimensione:", 50, 90, 70)
        
    with col2:
        if foto_originale:
            if st.button("✨ Genera Foto"):
                with st.spinner("Elaborazione..."):
                    img_input = Image.open(foto_originale).convert("RGBA")
                    
                    # LOGICA DI FIX PER IL BIANCO SU BIANCO
                    if modalita == "Bordi Precisi (Per capi bianchi)":
                        # Convertiamo in LAB per isolare la luminosità (canale L)
                        img_lab = img_input.convert("LAB")
                        l, a, b = img_lab.split()
                        # Threshold: tutto ciò che è molto chiaro diventa bianco nella maschera
                        # Abbassa il valore 200 se non prende abbastanza capo, alzalo se prende troppo sfondo
                        mask = l.point(lambda i: 255 if i > 200 else 0)
                        # Riempimento buchi (logo)
                        mask = mask.filter(ImageFilter.MaxFilter(9))
                        mask = mask.filter(ImageFilter.GaussianBlur(2))
                        maglietta_isolata = img_input.copy()
                        maglietta_isolata.putalpha(mask)
                    else:
                        maglietta_isolata = remove(img_input, session=st.session_state.session_standard)

                    # Composizione sfondo
                    url = f"https://image.pollinations.ai/p/empty%20background?width=1440&height=1440&nologo=true&seed={random.randint(1,999)}"
                    sfondo_img = Image.open(io.BytesIO(requests.get(url).content)).convert("RGBA")
                    
                    dim = int(1440 * (proporzione / 100))
                    maglietta_isolata.thumbnail((dim, dim))
                    
                    telaio = Image.new("RGBA", (1440, 1440), (0,0,0,0))
                    pos = ((1440-maglietta_isolata.width)//2, (1440-maglietta_isolata.height)//2)
                    telaio.paste(maglietta_isolata, pos, mask=maglietta_isolata)
                    
                    risultato = Image.alpha_composite(sfondo_img, telaio).convert("RGB")
                    st.image(risultato, width=500)

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI
# ==========================================
with tab2:
    brand = st.text_input("Brand")
    tipo = st.text_input("Tipo")
    st.text_area("Descrizione", f"Vendo {tipo} originale {brand}. Ottime condizioni.")

# ==========================================
# TAB 3: CALCOLATORE PREZZI
# ==========================================
with tab3:
    costo = st.number_input("Costo", value=15.0)
    vendita = st.number_input("Vendita", value=45.0)
    st.table(pd.DataFrame({
        "Voce": ["Costo", "Vendita", "Profitto"], 
        "Valore": [f"{costo}€", f"{vendita}€", f"{vendita-costo}€"]
    }))

# ==========================================
# TAB 4: TREND
# ==========================================
with tab4:
    st.dataframe(pd.DataFrame({
        "Categoria": ["Streetwear", "Vintage"],
        "Trend": ["⬆️ Alta", "➡️ Stabile"]
    }), use_container_width=True)
