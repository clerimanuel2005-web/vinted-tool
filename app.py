import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
from PIL import Image

# Configurazione globale e layout dell'applicazione (Modalità Wide)
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
st.sidebar.write("Crea un token gratuito 'Read' su huggingface.co per abilitare l'elaborazione dell'immagine reale.")
hf_token = st.sidebar.text_input("Hugging Face Token:", type="password", placeholder="hf_...")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Manichino & Sfondi AI (Hugging Face)", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO GHOST MANNEQUIN
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico AI: Ghost Mannequin")
    st.write("Invia la tua foto originale ai modelli di Hugging Face per stirare le pieghe del tessuto e montarla su un manichino.")

    col_foto1, col_foto2 = st.columns([1.3, 1.7], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica lo Scatto Originale")
        foto_originale = st.file_uploader("Trascina qui la foto del tuo capo:", type=["jpg", "jpeg", "png"])
        
        st.markdown("### 2️⃣ Dettagli della Stampa")
        marca_vestito = st.text_input("Marca del capo:")
        tipo_vestito = st.text_input("Tipo di articolo:")
        colore_tessuto = st.text_area("Descrizione dettagliata della grafica e colore:")
        
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
            help="Valori bassi mantengono il logo originale intatto e spianano solo le pieghe."
        )

    with col_foto2:
        st.markdown("### 4️⃣ Anteprima Catalogo Finale")
        if foto_originale is None:
            st.info("💡 Carica un file immagine a sinistra ed inserisci il Token Hugging Face per elaborare il tuo capo reale.")
        else:
            if not hf_token:
                st.warning("⚠️ Token di autenticazione mancante. Inserisci il tuo Hugging Face Token nella barra laterale sinistra.")
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
                                f"of the {marca_vestito}, {colore_tessuto}, professional studio lighting, neutral grey background."
                            )
                            
                            payload = {"inputs": prompt_str, "image": img_bytes, "strength": forza_stiro}
                            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                            
                            if response.status_code == 200:
                                image_res = Image.open(io.BytesIO(response.content))
                                st.image(image_res, caption="Capo elaborato", use_container_width=True)
                                buffer = io.BytesIO()
                                image_res.save(buffer, format="JPEG", quality=98)
                                st.download_button("📥 Scarica Foto Catalogo", data=buffer.getvalue(), file_name="vinted_ghost_mannequin.jpg", mime="image/jpeg")
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
        brand = st.text_input("Brand / Marca")
        tipo_capo = st.text_input("Tipo di articolo")
        colore = st.text_input("Colore e dettagli visivi")
        
        st.markdown("### 📏 Taglia e Misure")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit"])
        
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1: cm_ascelle = st.text_input("Ascella - Ascella (cm)")
        with col_cm2: cm_lunghezza = st.text_input("Lunghezza totale (cm)")
            
        st.markdown("### 🎚️ Stato del capo")
        condizioni = st.selectbox("Condizioni del capo", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime condizioni", "Buone condizioni"])
        difetti = st.text_input("Note su eventuali difetti")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia}" if tipo_capo or brand else ""
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti else "• 🔎 Difetti: Nessuno, capo perfetto."
        
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure prese in piano:\n"
            if cm_ascelle: stringa_misure += f"   - Ascella - Ascella: {cm_ascelle} cm\n"
            if cm_lunghezza: stringa_misure += f"   - Lunghezza totale: {cm_lunghezza} cm\n"

        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo {tipo_capo.lower() if tipo_capo else 'articolo'} originale del brand {brand.capitalize() if brand else '-'}. Il capo è stato trattato con cura.

• 🎨 Colore/Dettagli: {colore.capitalize() if colore else '-'}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedisco rapidamente entro 24 ore 📦.

---
#{brand.replace(' ', '').lower() if brand else 'brand'} #{tipo_capo.replace(' ', '').lower() if tipo_capo else 'capo'} #taglia{taglia.lower()}
"""
        st.text_input("📌 Titolo:", titolo_generato)
        st.text_area("📄 Descrizione:", descrizione_generata, height=320)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi del Profitto")
    col_input, col_chart = st.columns([1.5, 2.5], gap="large")

    with col_input:
        st.markdown("### 📊 Dati Finanziari")
        costo_acquisto = st.number_input("💰 Costo di acquisto (€)", min_value=0.0, format="%.2f")
        prezzo_vendita = st.number_input("🏷️ Prezzo di vendita stimato (€)", min_value=0.0, format="%.2f")
        percentuale_sconto = st.slider("Percentuale sconto lotti (%):", 0, 50, 15)

    with col_chart:
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = (guadagno_netto / costo_acquisto) * 100 if costo_acquisto > 0 else 0
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - costo_acquisto

        st.markdown("### 🏬 Resoconto Margini")
        m_col1, m_col2 = st.columns(2)
        with m_col1: st.metric("Guadagno Netto", f"{guadagno_netto:.2f} €")
        with m_col2: st.metric("ROI %", f"{roi:.1f}%")

        st.table(pd.DataFrame({
            "Scenario": ["Vendita Singola", f"Lotto (-{percentuale_sconto}%)"],
            "Prezzo": [f"{prezzo_vendita:.2f} €", f"{prezzo_scontato_lotto:.2f} €"],
            "Margine": [f"{guadagno_netto:.2f} €", f"{guadagno_lotto:.2f} €"]
        }))
        
        if prezzo_vendita > 0 and costo_acquisto > 0:
            df_chart = pd.DataFrame({'Componente': ['Costo', 'Margine'], 'Valore': [costo_acquisto, max(0.0, guadagno_netto)]})
            st.altair_chart(alt.Chart(df_chart).mark_arc(innerRadius=50).encode(theta='Valore', color='Componente'), use_container_width=True)

# ==========================================
# TAB 4: TREND & RICERCA
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato & Analisi")
    col_t1, col_t2 = st.columns(2, gap="large")
    
    with col_t1:
        st.markdown("### 🔥 Trend di Ricerca (Italia)")
        st.dataframe(pd.DataFrame({
            "Categoria": ["Sneakers Retro", "Giacche Tecniche", "Denim Baggy", "Streetwear Tops"],
            "Volume": ["Alto", "Alto", "Medio", "Medio"],
            "Liquidità": ["Molto Alta", "Alta", "Media", "Alta"]
        }), use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("### 📈 Nicchie in Crescita")
        st.dataframe(pd.DataFrame({
            "Tipologia": ["Band Tees", "Maglie Calcio", "Giacche Vento", "Workwear"],
            "Crescita": ["+120%", "+105%", "+90%", "+75%"],
            "Prezzo": ["35€-80€", "45€-120€", "30€-60€", "40€-70€"]
        }), use_container_width=True, hide_index=True)
