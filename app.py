import streamlit as st
import pandas as pd
import requests
import io
import base64
from PIL import Image, ImageFilter, ImageOps
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

        proporzione_capo = st.slider("Dimensione del livello nello sfondo:", 50, 90, 70, step=5)

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Elaborato")
        
        if foto_originale is not None:
            if st.button("✨ Genera Foto Catalogo", type="primary"):
                with st.spinner("Generazione dello sfondo e fusione dei livelli in corso..."):
                    try:
                        # 1. APERTURA IMMAGINE UTENTE
                        input_image = Image.open(foto_originale).convert("RGBA")
                        input_image = ImageOps.exif_transpose(input_image)
                        
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
                            
                            # 3. COMPOSIZIONE GRAFICA COMPATIBILE
                            dim_max = int(1080 * (proporzione_capo / 100))
                            input_image.thumbnail((dim_max, dim_max), Image.Resampling.LANCZOS)
                            
                            livello_composizione = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
                            pos_x = (1080 - input_image.width) // 2
                            pos_y = (1080 - input_image.height) // 2
                            
                            livello_composizione.paste(input_image, (pos_x, pos_y))
                            
                            # Fusione finale dei livelli
                            foto_finale = Image.alpha_composite(sfondo_ai, livello_composizione).convert("RGB")
                            
                            # Output a schermo
                            st.image(foto_finale, caption="Ecco la tua foto aggiornata", use_container_width=True)
                            
                            # Bottone di download
                            buffer = io.BytesIO()
                            foto_finale.save(buffer, format="JPEG", quality=95)
                            st.download_button(
                                label="📥 Scarica Foto Finita",
                                data=buffer.getvalue(),
                                file_name="vinted_studio_perfect.jpg",
                                mime="image/jpeg"
                            )
                            st.success("Immagine creata correttamente!")
                        else:
                            st.error("Il server AI degli sfondi è momentaneamente occupato. Riprova tra un istante.")
                            
                    except Exception as e:
                        st.error(f"Errore durante l'elaborazione dell'immagine: {e}")
        else:
            st.info("💡 Carica lo scatto originale a sinistra per iniziare.")


# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="", placeholder="Inserisci la marca...")
        tipo_capo = st.text_input("Tipo di articolo", value="", placeholder="Es. T-shirt, Felpa...")
        colore = st.text_input("Colore e dettagli visivi", value="", placeholder="Es. Bianco con stampa rossa...")
        
        st.markdown("### 📏 Taglia e Misure")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit"])
        
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1:
            cm_ascelle = st.text_input("Ascella - Ascella (cm)", value="", placeholder="Es. 54")
        with col_cm2:
            cm_lunghezza = st.text_input("Lunghezza totale (cm)", value="", placeholder="Es. 70")
            
        st.markdown("### 🎚️ Stato del capo")
        condizioni = st.selectbox("Condizioni del capo", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime condizioni", "Buone condizioni"])
        difetti = st.text_input("Note su eventuali difetti", value="", placeholder="Es. nessuno...")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia}" if tipo_capo or brand else ""
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti else "• 🔎 Difetti: Nessuno, capo perfetto."
        
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure prese in piano:\n"
            if cm_ascelle: stringa_misure += f"    - Ascella - Ascella: {cm_ascelle} cm\n"
            if cm_lunghezza: stringa_misure += f"    - Lunghezza totale: {cm_lunghezza} cm\n"

        brand_tag = brand.replace(' ', '').lower() if brand else "brand"
        tipo_tag = tipo_capo.replace(' ', '').lower() if tipo_capo else "capo"

        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo splendida {tipo_capo.lower() if tipo_capo else 'maglia'} originale del brand {brand.capitalize() if brand else '-'}. Il capo è stato trattato con cura, lavato e igienizzato.

• 🎨 Colore/Dettagli: {colore.capitalize() if colore else '-'}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedisco rapidamente entro 24 ore 📦. Disponibile per info in chat! 📲

---
# {brand_tag} #{tipo_tag} #taglia{taglia.lower()} #streetwear #reselling
"""
        st.text_input("📌 Titolo dell'annuncio:", titolo_generato)
        st.text_area("📄 Descrizione dell'annuncio:", descrizione_generata, height=320)


# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi del Profitto")
    col_input, col_chart = st.columns([1.5, 2.5], gap="large")

    with col_input:
        st.markdown("### 📊 Dati Finanziari dell'Articolo")
        costo_acquisto = st.number_input("💰 Costo di acquisto del capo (€)", min_value=0.0, value=0.0, format="%.2f")
        prezzo_vendita = st.number_input("🏷️ Prezzo di vendita stimato (€)", min_value=0.0, value=0.0, format="%.2f")
        percentuale_sconto = st.slider("Percentuale sconto impostata sui lotti (%):", 0, 50, 15)

    with col_chart:
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = (guadagno_netto / costo_acquisto) * 100 if costo_acquisto > 0 else 0
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - costo_acquisto

        st.markdown("### 🏬 Resoconto Margini Operativi")
        m_col1, m_col2 = st.columns(2)
        with m_col1: 
            st.metric(label="🤑 Guadagno Netto Singolo", value=f"{guadagno_netto:.2f} €")
        with m_col2: 
            st.metric(label="📈 ROI %", value=f"{roi:.1f}%")

        st.markdown("---")
        st.markdown("##### 📊 Tabella dei Margini Simulati")
        data_tabella = {
            "Scenario di Vendita": ["Vendita Singola Standard", f"Vendita in Lotto (Sconto {percentuale_sconto}%)"],
            "Prezzo Finale (€)": [f"{prezzo_vendita:.2f} €", f"{prezzo_scontato_lotto:.2f} €"],
            "Margine di Guadagno (€)": [f"{guadagno_netto:.2f} €", f"{guadagno_lotto:.2f} €"],
            "Stato Profitto": ["Massimo" if guadagno_netto > 0 else "Nessuno", "Ridotto" if guadagno_lotto > 0 else "Nessuno"]
        }
        st.table(pd.DataFrame(data_tabella))


# ==========================================
# TAB 4: TREND & RICERCA RAPIDA
# ==========================================
with tab4:
    st.header("📊 I Trend di Mercato Caldi & Analisi Nicchie")
    col_t1, col_t2 = st.columns(2, gap="medium")
    
    with col_t1:
        st.markdown("### 🔥 Trend di Ricerca Attuali (Italia)")
        tabelle_ricerca = pd.DataFrame({
            "Posizione": [1, 2, 3, 4, 5],
            "Categoria/Stile": ["Sneakers Hype Retro", "Giacche Gorpcore / Tecniche", "Denim Baggy & Skate", "Y2K Streetwear Tops", "Giacche Varsity Vintage"],
            "Volume di Ricerca": ["Alto (15k+)", "Alto (9k+)", "Medio (6k+)", "Medio (4k+)", "In Crescita (2k+)"]
        })
        st.dataframe(tabelle_ricerca, use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("### 📈 Nicchie in Forte Crescita")
        tabelle_nicchie = pd.DataFrame({
            "Posizione": [1, 2, 3, 4],
            "Tipologia Prodotto Vintage": ["T-shirt di Band Musicali Vintage", "Maglie da Calcio Anni '90/00", "Giacche a Vento Colorblock", "Workwear Pants Usurati"],
            "Tasso di Crescita": ["+120%", "+105%", "+90%", "+75%"]
        })
        st.dataframe(tabelle_nicchie, use_container_width=True, hide_index=True)
