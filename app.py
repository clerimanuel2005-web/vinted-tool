import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
from PIL import Image

# Configurazione globale
st.set_page_config(
    page_title="Vinted Power Seller Suite",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# PANNELLO LATERALE DI AUTENTICAZIONE API
# ==========================================
st.sidebar.markdown("### 🔑 Autenticazione AI")
st.sidebar.write("Crea un token gratuito 'Read' su huggingface.co.")
hf_token = st.sidebar.text_input("Hugging Face Token:", type="password", placeholder="hf_...")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Manichino & Sfondi AI", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO GHOST MANNEQUIN
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico AI: Ghost Mannequin")
    st.write("Invia la tua foto originale per stirare le pieghe del tessuto e montarla su un manichino invisibile.")

    col_foto1, col_foto2 = st.columns([1.3, 1.7], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica lo Scatto Originale")
        foto_originale = st.file_uploader("Trascina qui la foto del tuo capo:", type=["jpg", "jpeg", "png"])
        
        st.markdown("### 2️⃣ Dettagli del Capo")
        marca_vestito = st.text_input("Marca del capo:", value="")
        tipo_vestito = st.text_input("Tipo di articolo:", value="")
        colore_tessuto = st.text_area("Descrizione dettagliata (colore e stile):", value="")
        
        st.markdown("### 3️⃣ Regolazioni Algoritmo AI")
        opzione_manichino = st.selectbox(
            "Stile di esposizione:",
            [
                "Invisible ghost mannequin style, flat front view, perfectly straight shoulders",
                "Professional fashion lookbook studio mannequin display, clean and elegant"
            ]
        )
        
        forza_stiro = st.slider(
            "Intensità Stiratura / Fedeltà (Denoising):", 
            0.20, 0.60, 0.35, step=0.05,
            help="Valori bassi (0.30 - 0.35) mantengono i dettagli originali e spianano solo le pieghe."
        )

    with col_foto2:
        st.markdown("### 4️⃣ Anteprima Catalogo Finale")
        if foto_originale is None:
            st.info("💡 Carica un file immagine a sinistra ed inserisci il Token Hugging Face per elaborare il tuo capo.")
        else:
            if not hf_token:
                st.warning("⚠️ Token di autenticazione mancante.")
                st.image(foto_originale, caption="Anteprima scatto originale", use_container_width=True)
            else:
                if st.button("✨ Applica Manichino e Stira Tessuto", type="primary"):
                    with st.spinner("Connessione ai server di Inpainting in corso..."):
                        try:
                            img_bytes = foto_originale.getvalue()
                            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-refiner-1.0"
                            headers = {"Authorization": f"Bearer {hf_token}"}
                            
                            prompt_str = (
                                f"High-end commercial clothing photography, {opzione_manichino}, retail lookbook, "
                                f"fabric is perfectly ironed, 100% flat smooth texture, zero wrinkles, clean crisp details "
                                f"of the {marca_vestito}, {colore_tessuto}, professional studio lighting, "
                                f"neutral grey background."
                            )
                            
                            payload = {"inputs": prompt_str, "image": img_bytes, "strength": forza_stiro}
                            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                            
                            if response.status_code == 200:
                                image_res = Image.open(io.BytesIO(response.content))
                                st.image(image_res, caption="Capo elaborato", use_container_width=True)
                                buffer = io.BytesIO()
                                image_res.save(buffer, format="JPEG", quality=98)
                                st.download_button("📥 Scarica Foto Catalogo", data=buffer.getvalue(), file_name="vinted_ghost_mannequin.jpg", mime="image/jpeg")
                                st.success("Fatto!")
                            else:
                                st.error(f"Errore dal server AI (Codice {response.status_code}).")
                        except Exception as e:
                            st.error(f"Errore tecnico di rete: {e}")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo")
        tipo_capo = st.text_input("Tipo di articolo")
        colore = st.text_input("Colore e dettagli")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"])
        vestibilita = st.selectbox("Vestibilità", ["Regolare", "Oversize / Baggy", "Slim fit"])
        cm_ascelle = st.text_input("Ascella - Ascella (cm)")
        cm_lunghezza = st.text_input("Lunghezza totale (cm)")
        condizioni = st.selectbox("Condizioni del capo", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime condizioni", "Buone condizioni"])
        difetti = st.text_input("Note su eventuali difetti")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        stringa_misure = f"• 📐 Misure prese in piano:\n   - Ascella - Ascella: {cm_ascelle} cm\n   - Lunghezza totale: {cm_lunghezza} cm\n" if (cm_ascelle or cm_lunghezza) else ""
        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo splendida {tipo_capo} del brand {brand}.

• 🎨 Colore/Dettagli: {colore}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
• 🔎 Difetti: {difetti if difetti else "Nessuno, capo perfetto."}

Spedisco rapidamente 📦. Disponibile per info in chat! 📲

---
#{brand.replace(' ', '')} #{tipo_capo.replace(' ', '')} #taglia{taglia.lower()} #streetwear #reselling
"""
        st.text_area("📄 Copia il testo qui sotto:", descrizione_generata, height=350)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi del Profitto")
    col_input, col_chart = st.columns([1.5, 2.5], gap="large")

    with col_input:
        costo_acquisto = st.number_input("💰 Costo di acquisto del capo (€)", min_value=0.0, format="%.2f")
        prezzo_vendita = st.number_input("🏷️ Prezzo di vendita stimato (€)", min_value=0.0, format="%.2f")
        percentuale_sconto = st.slider("Percentuale sconto impostata sui lotti (%):", 0, 50, 15)

    with col_chart:
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = (guadagno_netto / costo_acquisto) * 100 if costo_acquisto > 0 else 0
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - costo_acquisto

        st.markdown("### 🏬 Resoconto")
        m_col1, m_col2 = st.columns(2)
        m_col1.metric("🤑 Guadagno Netto", f"{guadagno_netto:.2f} €")
        m_col2.metric("📈 ROI %", f"{roi:.1f}%")

        data_tabella = {
            "Scenario": ["Singolo", "Lotto"],
            "Prezzo": [f"{prezzo_vendita:.2f}€", f"{prezzo_scontato_lotto:.2f}€"],
            "Margine": [f"{guadagno_netto:.2f}€", f"{guadagno_lotto:.2f}€"]
        }
        st.table(pd.DataFrame(data_tabella))

# ==========================================
# TAB 4: TREND & RICERCA RAPIDA
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato & Analisi Nicchie")
    st.write("Consulta i dati di mercato per ottimizzare il tuo inventario.")
    col_t1, col_t2 = st.columns(2, gap="large")
    
    with col_t1:
        st.markdown("### 🔥 Trend di Ricerca")
        df_trend = pd.DataFrame({
            "Categoria": ["Sneakers Retro", "Giacche Tecniche", "Denim Baggy", "Streetwear Tops"],
            "Liquidità": ["Alta", "Alta", "Media", "Media"]
        })
        st.dataframe(df_trend, use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("### 📈 Nicchie in Crescita")
        df_nicchie = pd.DataFrame({
            "Tipologia": ["Vintage Band T-shirt", "Maglie Calcio 90s", "Workwear Pants"],
            "Tasso Crescita": ["+120%", "+105%", "+75%"]
        })
        st.dataframe(df_nicchie, use_container_width=True, hide_index=True)
