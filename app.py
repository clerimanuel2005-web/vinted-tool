import streamlit as st
import pandas as pd
import requests
import io
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from rembg import remove, new_session

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# Inizializzazione sessioni in cache per ottimizzare prestazioni
if "session_standard" not in st.session_state:
    st.session_state.session_standard = new_session(model_name="u2net")
if "session_clothing" not in st.session_state:
    st.session_state.session_clothing = new_session(model_name="u2net_clothing")

st.title("🛍️ Vinted Power Seller Suite")
st.write("L'hub definitivo per ottimizzare le foto dei tuoi capi, calcolare i margini e scrivere annunci perfetti.")

# Creazione delle schede
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Manichino AI & Ultra HD", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend di Mercato"
])

# ==========================================
# TAB 1: RIMOZIONE SFONDO E COMPOSIZIONE
# ==========================================
with tab1:
    st.header("📸 Ottimizzazione Sfondo Fotografico via AI")
    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Trascina qui la foto:", type=["jpg", "jpeg", "png"])
        
        st.markdown("### ⚙️ Impostazioni Scontornamento")
        modalita_scontorno = st.selectbox(
            "Modalità di ritaglio:",
            ["Bordi Precisi (Specifico per Magliette Bianche/Chiare)", "Standard (Consigliato per capi scuri)"]
        )
        
        if "bg_seed" not in st.session_state: st.session_state.bg_seed = random.randint(1, 9999)
        cambia_variante = st.button("🔄 Cambia variante sfondo")
        if cambia_variante: st.session_state.bg_seed = random.randint(1, 9999)

        tipo_sfondo_scelto = st.selectbox("Scenario:", [
            "Gruccia in legno minimale su muro in cemento industriale",
            "Showroom di lusso (Sfondo vuoto con luci calde)",
            "Sfondo bianco puro e-commerce (Stile Amazon/Zalando)"
        ])
        proporzione_capo = st.slider("Dimensione capo (%):", 50, 90, 70)

    with col_foto2:
        if foto_originale:
            if st.button("✨ Genera Foto Catalogo HQ", type="primary"):
                with st.spinner("Elaborazione in corso..."):
                    try:
                        img_input = Image.open(foto_originale)
                        img_input = ImageOps.exif_transpose(img_input)
                        
                        # LOGICA CORRETTA PER RISOLVERE IL PROBLEMA DI **image_a1fac5.jpg**
                        if modalita_scontorno == "Bordi Precisi (Specifico per Magliette Bianche/Chiare)":
                            # Convertiamo in scala di grigi e contrasto alto per isolare la forma del capo
                            img_gray = img_input.convert("L")
                            img_contrast = ImageEnhance.Contrast(img_gray).enhance(3.0)
                            # Generiamo la maschera sulla versione contrastata
                            mask = remove(img_contrast, session=st.session_state.session_clothing, only_mask=True)
                            mask = mask.resize(img_input.size)
                            maglietta_isolata = img_input.convert("RGBA")
                            maglietta_isolata.putalpha(mask)
                        else:
                            maglietta_isolata = remove(img_input, session=st.session_state.session_standard).convert("RGBA")
                        
                        # Generazione Sfondo
                        prompt_mappa = {
                            "Gruccia in legno minimale su muro in cemento industriale": "Minimalist wooden clothes hanger on raw grey concrete wall, soft side lighting, no clothes",
                            "Showroom di lusso (Sfondo vuoto con luci calde)": "Empty luxury fashion boutique, warm cinematic lighting, no clothes",
                            "Sfondo bianco puro e-commerce (Stile Amazon/Zalando)": "Clean solid pure white studio background, professional e-commerce, no clothes"
                        }
                        url = f"https://image.pollinations.ai/p/{prompt_mappa[tipo_sfondo_scelto].replace(' ', '%20')}?width=1440&height=1440&nologo=true&seed={st.session_state.bg_seed}"
                        sfondo_reale = Image.open(io.BytesIO(requests.get(url).content)).convert("RGBA")
                        
                        # Composizione
                        dim = int(1440 * (proporzione_capo / 100))
                        maglietta_isolata.thumbnail((dim, dim), Image.Resampling.LANCZOS)
                        alpha = maglietta_isolata.getchannel('A')
                        ombra = Image.new("RGBA", maglietta_isolata.size, (0, 0, 0, 40))
                        ombra.putalpha(alpha)
                        ombra = ombra.filter(ImageFilter.GaussianBlur(20))
                        
                        telaio = Image.new("RGBA", (1440, 1440), (0,0,0,0))
                        pos = ((1440-maglietta_isolata.width)//2, (1440-maglietta_isolata.height)//2)
                        telaio.paste(ombra, (pos[0]-10, pos[1]+15))
                        telaio.paste(maglietta_isolata, pos, mask=maglietta_isolata)
                        
                        risultato = Image.alpha_composite(sfondo_reale, telaio).convert("RGB")
                        st.image(risultato, width=580)
                    except Exception as e: st.error(f"Errore: {e}")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    brand = st.text_input("Brand")
    tipo_capo = st.text_input("Tipo articolo")
    st.text_area("Descrizione generata", f"Vendo {tipo_capo} originale {brand}. In ottime condizioni.")

# ==========================================
# TAB 3: CALCOLATORE PREZZI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini")
    costo = st.number_input("Costo acquisto (€)", value=15.0)
    vendita = st.number_input("Prezzo vendita (€)", value=45.0)
    st.metric("Guadagno Netto", f"{vendita - costo:.2f} €")
    st.table(pd.DataFrame({"Scenario": ["Singolo", "Lotto"], "Profitto": [vendita-costo, (vendita*0.85)-costo]}))

# ==========================================
# TAB 4: TREND DI MERCATO
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato")
    df = pd.DataFrame({
        "Categoria": ["Streetwear", "Vintage", "Denim"],
        "Volume": ["Alto", "Medio", "Alto"]
    })
    st.dataframe(df, use_container_width=True)
