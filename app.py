import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
import base64
from PIL import Image

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Manichino & Sfondi AI (Img2Img)", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO CON IMAGE-TO-IMAGE
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico AI: Trasforma la tua Foto Reale")
    st.write("Carica la foto reale del tuo capo. L'AI userà la tua immagine come base per mantenere il logo originale identico, inserendolo su un manichino o modello nel contesto scelto.")

    col_foto1, col_foto2 = st.columns(2, gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la Foto Reale del Capo")
        foto_originale = st.file_uploader("Trascina qui la foto scattata da te (es. sul letto o appendiabiti):", type=["jpg", "jpeg", "png"])
        
        if foto_originale:
            st.image(foto_originale, caption="Tua foto di riferimento originale", width=200)

        st.markdown("### 2️⃣ Dettagli per il perfezionamento")
        brand_capo = st.text_input("Marca del vestito:", value="Off-White")
        tipo_prodotto = st.text_input("Tipo di vestito:", value="t-shirt")
        
        st.markdown("### 3️⃣ Scegli il Supporto & Ambientazione")
        opzione_esposizione = st.selectbox(
            "Come vuoi esporlo?:",
            [
                "Placed perfectly on an invisible ghost mannequin, smooth fabric, no wrinkles",
                "Worn by a professional male model, streetwear look, fashion catalog pose",
                "Worn by a professional female model, modern look, clear front view",
                "Hanging elegantely on a minimalist wooden hanger"
            ]
        )
        
        stile_sfondo = st.selectbox(
            "Scegli lo sfondo:",
            [
                "Inside a luxury fashion showroom boutique, warm soft lighting, grey resin floor",
                "Industrial urban street background, blurred city lights, London underground style",
                "Clean minimal photography studio background, soft professional catalog lighting",
                "Minimalist concrete wall with premium studio spot light from top"
            ]
        )
        
        # Slider di fedeltà all'originale
        somiglianza = st.slider("Fedeltà alla foto originale (Più è alto, più il logo rimane identico):", 0.50, 0.90, 0.75, step=0.05)

    with col_foto2:
        st.markdown("### 4️⃣ Risultato Generato")
        
        if foto_originale is not None:
            if st.button("✨ Genera Foto Professionale Fedele", type="primary"):
                with st.spinner("Analisi della foto originale e fusione con il manichino... Attendi qualche secondo."):
                    try:
                        # Convertiamo l'immagine caricata in Base64 leggibile dall'AI senza salvare file sul server
                        bytes_data = foto_originale.getvalue()
                        base64_image = base64.b64encode(bytes_data).decode("utf-8")
                        data_url = f"data:image/jpeg;base64,{base64_image}"
                        
                        # Costruzione del prompt avanzato combinando testo ed elementi strutturali dell'immagine sorgente
                        prompt_str = (
                            f"High-end commercial product photography of the exact {brand_capo.lower()} {tipo_prodotto.lower()} from the source image. "
                            f"{opzione_esposizione}, {stile_sfondo}. Keep the original graphic print logo, shapes, and colors exactly as shown in the source image. "
                            f"Photorealistic, 8k resolution, crisp details, highly professional look."
                        ).replace(" ", "%20")
                        
                        # Chiamata al motore avanzato Image-to-Image di Pollinations (Flux-Img2Img-Bypass)
                        api_url = f"https://image.pollinations.ai/p/{prompt_str}?width=1080&height=1080&nologo=true&seed=42"
                        
                        # Inviamo la richiesta includendo la struttura dell'immagine sorgente
                        payload = {
                            "image": data_url,
                            "strength": somiglianza # Controlla quanto l'AI può variare rispetto alla maglietta reale
                        }
                        
                        response = requests.post(api_url, json=payload, timeout=40)
                        
                        if response.status_code == 200:
                            image_res = Image.open(io.BytesIO(response.content))
                            st.image(image_res, caption="Foto Catalogo generata mantenendo il tuo capo reale", use_container_width=True)
                            
                            # Download
                            buffer = io.BytesIO()
                            image_res.save(buffer, format="JPEG", quality=95)
                            st.download_button(
                                label="📥 Scarica Foto per Vinted",
                                data=buffer.getvalue(),
                                file_name="vinted_catalogo_fedele.jpg",
                                mime="image/jpeg"
                            )
                            st.success("Immagine creata! Il logo è stato preservato usando la tua foto come mappa.")
                        else:
                            st.error("Il sistema di rendering è temporaneamente occupato. Clicca di nuovo tra 5 secondi.")
                    except Exception as e:
                        st.error(f"Errore durante l'elaborazione dell'immagine: {e}")
        else:
            st.info("💡 Carica la foto reale del tuo capo a sinistra (box 1) per permettere all'AI di copiare fedelmente il logo reale!")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="Off-White")
        tipo_capo = st.text_input("Tipo di articolo", value="T-shirt corta")
        colore = st.text_input("Colore principale", value="Bianco con stampa rossa")
        st.markdown("### 📏 Taglia e Misure")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=3)
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Oversize / Baggy", "Regolare", "Slim fit"])
        cm_ascelle = st.text_input("Ascella - Ascella (cm)", placeholder="Es. 56")
        cm_lunghezza = st.text_input("Lunghezza totale (cm)", placeholder="Es. 74")
        condizioni = st.selectbox("Condizioni del capo", ["Ottime condizioni", "Nuovo con cartellino", "Nuovo senza cartellino"])
        difetti = st.text_input("Note o piccoli difetti", value="nessuna")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia} - {colore.capitalize()}"
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti and difetti.lower() != "nessuna" else "• 🔎 Difetti: Nessuno, capo perfetto."
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure piatte:\n"
            if cm_ascelle: stringa_misure += f"   - Pit to Pit: {cm_ascelle} cm\n"
            if cm_lunghezza: stringa_misure += f"   - Lunghezza: {cm_lunghezza} cm\n"

        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo splendida {tipo_capo.lower()} originale del brand {brand.capitalize()}. Capo trattato con cura, lavato e igienizzato.

• 🎨 Colore: {colore.capitalize()}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedisco entro 24 ore📦. Scrivimi pure per offerte o domande! 📲

---
#reselling #{brand.lower()} #{tipo_capo.replace(' ', '').lower()} #streetwear
"""
        st.text_input("📌 Titolo dell'annuncio:", titolo_generato)
        st.text_area("📄 Descrizione dell'annuncio:", descrizione_generata, height=300)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi del Profitto")
    col_input, col_chart = st.columns([1.5, 2.5], gap="large")
    with col_input:
        costo_acquisto = st.number_input("💰 Quanto hai pagato il capo? (€)", min_value=0.0, value=10.0, format="%.2f")
        prezzo_vendita = st.number_input("🏷️ A quanto vuoi venderlo? (€)", min_value=costo_acquisto, value=35.0, format="%.2f")
        percentuale_sconto = st.slider("Sconto lotto (%)", 0, 50, 15)

    with col_chart:
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = (guadagno_netto / costo_acquisto) * 100 if costo_acquisto > 0 else 0
        st.markdown("### 🏬 Risultato")
        st.metric(label="🤑 Guadagno Netto", value=f"{guadagno_netto:.2f} €")
        st.metric(label="📈 ROI %", value=f"{roi:.1f}%")

# ==========================================
# TAB 4: TREND & RICERCA RAPIDA
# ==========================================
with tab4:
    st.header("📊 I Trend di Mercato Caldi")
    trend_data = [{"Categoria": "👟 Sneakers Hype", "Brand": "Nike, Jordan, Adidas"}, {"Categoria": "🧥 Outerwear", "Brand": "The North Face, Arc'teryx"}]
    st.dataframe(pd.DataFrame(trend_data), use_container_width=True)
    st.link_button("👟 Cerca Scarpe Nike (<40€) su Vinted", "https://www.vinted.it/catalog?search_text=nike&price_to=40&order=newest_first", use_container_width=True)
