import streamlit as st
import pandas as pd
import requests
import io
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from rembg import remove, new_session

# 1. CONFIGURAZIONE DELLA PAGINA
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# Inizializzazione sessioni in cache
if "session_standard" not in st.session_state:
    st.session_state.session_standard = new_session(model_name="u2net")

# Titolo principale
st.title("🛍️ Vinted Power Seller Suite")
st.write("L'hub definitivo per ottimizzare le foto dei tuoi capi, calcolare i margini e scrivere annunci perfetti.")

# ==========================================
# CREAZIONE DELLE SCHEDE DI NAVIGAZIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Manichino AI & Ultra HD", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend di Mercato"
])

# ==========================================
# TAB 1: RIMOZIONE SFONDO E COMPOSIZIONE HD
# ==========================================
with tab1:
    st.header("📸 Ottimizzazione Sfondo Fotografico via AI")
    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Trascina qui la foto scattata:", type=["jpg", "jpeg", "png"], key="vinted_uploader")
        
        if foto_originale:
            st.image(foto_originale, caption="Foto originale caricata", width=140)

        st.markdown("### ⚙️ Impostazioni Scontornamento AI")
        modalita_scontorno = st.selectbox(
            "Modalità di ritaglio del capo:",
            ["Bordi Precisi (Specifico per Magliette Bianche/Chiare)", "Standard (AI)"]
        )
        
        if "bg_seed" not in st.session_state: st.session_state.bg_seed = random.randint(1, 9999)
        if st.button("🔄 Cambia variante sfondo"): st.session_state.bg_seed = random.randint(1, 9999)

        tipo_sfondo_scelto = st.selectbox("Scenario:", [
            "Gruccia in legno minimale su muro in cemento industriale",
            "Showroom di lusso (Sfondo vuoto con luci calde)",
            "Sfondo bianco puro e-commerce (Stile Amazon/Zalando)"
        ])
        proporzione_capo = st.slider("Dimensione del capo (%):", 50, 90, 70)

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Elaborato in Ultra HD")
        if foto_originale is not None:
            if st.button("✨ Genera Foto Catalogo HQ", type="primary"):
                with st.spinner("Isolamento tessuto e fusione in corso..."):
                    try:
                        img_input = Image.open(foto_originale).convert("RGBA")
                        
                        # LOGICA FIXLAB PER BIANCO SU BIANCO (Risolve il logo isolato)
                        if modalita_scontorno == "Bordi Precisi (Specifico per Magliette Bianche/Chiare)":
                            img_lab = img_input.convert("LAB")
                            l, a, b = img_lab.split()
                            # Soglia luminanza
                            mask = l.point(lambda i: 255 if i > 200 else 0)
                            mask = mask.filter(ImageFilter.MaxFilter(9))
                            mask = mask.filter(ImageFilter.GaussianBlur(2))
                            maglietta_isolata = img_input.copy()
                            maglietta_isolata.putalpha(mask)
                        else:
                            maglietta_isolata = remove(img_input, session=st.session_state.session_standard)

                        # Generazione Sfondo (Pollinations)
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
                        
                        # Ombra e posizionamento
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
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand", placeholder="Es. Off-White")
        tipo = st.text_input("Tipo", placeholder="Es. T-Shirt")
        colore = st.text_input("Colore")
        taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL"])
        condizioni = st.selectbox("Condizioni", ["Nuovo", "Ottimo", "Buono"])
    with col_b:
        st.subheader("📋 Testo Pronto")
        desc = f"Vendo {tipo} {brand}. Colore: {colore}. Taglia: {taglia}. Condizioni: {condizioni}."
        st.text_area("Copia questo:", desc, height=200)

# ==========================================
# TAB 3: CALCOLATORE PREZZI
# ==========================================
with tab3:
    st.header("💰 Calcolatore Margini")
    c = st.number_input("Costo (€)", value=15.0)
    v = st.number_input("Vendita (€)", value=45.0)
    
    data = pd.DataFrame({
        "Voce": ["Costo", "Vendita", "Profitto Netto"], 
        "Valore": [f"{c}€", f"{v}€", f"{v-c}€"]
    })
    st.table(data)

# ==========================================
# TAB 4: TREND DI MERCATO
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato")
    df = pd.DataFrame({
        "Categoria": ["Streetwear", "Vintage", "Denim"],
        "Trend": ["⬆️ Alta", "➡️ Stabile", "⬆️ Crescita"]
    })
    st.dataframe(df)

# ==========================================
# FOOTER / INFO
# ==========================================
st.markdown("---")
st.write("Suite sviluppata per massimizzare le vendite su Vinted.")
