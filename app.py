import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
from PIL import Image

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

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
# TAB 1: GENERATORE MANICHINO E SFONDI PROFESSIONAL
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico AI: Indossa su Modello o Manichino")
    st.write("Crea foto catalogo per i tuoi vestiti inserendo i dettagli del capo reale per vederlo indossato professionalmente.")

    col_foto1, col_foto2 = st.columns(2, gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Dettagli del Capo Reale")
        brand_capo = st.text_input("Marca del vestito da ricreare:", value="Off-White")
        tipo_prodotto = st.text_input("Tipo di vestito (es. t-shirt, felpa con cappuccio):", value="t-shirt a maniche corte")
        colore_tessuto = st.text_input("Colore del tessuto e dettagli:", value="bianco puro con grande logo a frecce rosse sul retro")
        
        st.markdown("### 2️⃣ Scegli il Supporto (Come vuoi esporlo?)")
        opzione_esposizione = st.selectbox(
            "Seleziona il tipo di presentazione:",
            [
                "Indossato su un manichino invisibile (Ghost Mannequin) da negozio, perfettamente stirato",
                "Indossato da un modello ragazzo streetwear in posa, focus sul brand",
                "Indossato da una modella ragazza streetwear in posa di fronte, stile catalogo",
                "Appeso a una gruccia di legno minimalista all'interno di una boutique"
            ]
        )
        
        st.markdown("### 3️⃣ Scegli l'Ambientazione (Sfondo)")
        stile_sfondo = st.selectbox(
            "Scegli lo sfondo:",
            [
                "Dentro uno showroom di lusso con pavimento in resina grigia e luci calde soffuse",
                "Strade urbane di Londra, sfondo di mattoni scuri industriali e stile underground sfocato",
                "Studio fotografico professionale, sfondo grigio chiaro minimale, illuminazione da studio pulita",
                "Muro di cemento minimalista grigio con luci spot dall'alto"
            ]
        )

    with col_foto2:
        st.markdown("### 4️⃣ Risultato Generato")
        
        # Costruiamo il pulsante di generazione
        if st.button("✨ Genera Foto Professionale Gratis", type="primary"):
            with st.spinner("L'AI sta creando il mockup sul manichino/modello... Attendi qualche secondo."):
                try:
                    # Costruzione del prompt fotografico perfetto in inglese per l'AI
                    prompt_ai = (
                        f"Professional studio product photography of a {brand_capo.lower()} {tipo_prodotto.lower()}, "
                        f"{colore_tessuto.lower()}, {opzione_esposizione.lower()}, {stile_sfondo.lower()}, "
                        f"high-end commercial look, lookbook style, 8k resolution, crisp details, hyperrealistic."
                    ).replace(" ", "%20") # Codifica gli spazi per l'URL
                    
                    # URL dell'API di Pollinations (stabile, ultra-veloce e senza chiavi a pagamento)
                    api_url = f"https://image.pollinations.ai/p/{prompt_ai}?width=1080&height=1080&nologo=true"
                    
                    # Scarichiamo l'immagine generata dal server esterno sicuro
                    response = requests.get(api_url, timeout=30)
                    
                    if response.status_code == 200:
                        image_res = Image.open(io.BytesIO(response.content))
                        st.image(image_res, caption="Anteprima Foto Catalogo per Vinted", use_container_width=True)
                        
                        # Preparazione del download per l'utente
                        buffer = io.BytesIO()
                        image_res.save(buffer, format="JPEG", quality=95)
                        st.download_button(
                            label="📥 Scarica Foto Pronta per Vinted",
                            data=buffer.getvalue(),
                            file_name="vinted_catalogo_pro.jpg",
                            mime="image/jpeg"
                        )
                        st.success("Immagine creata! Puoi caricarla come copertina del tuo annuncio.")
                    else:
                        st.error("Errore temporaneo nel caricamento del modello grafico. Riprova tra un attimo.")
                except Exception as e:
                    st.error(f"Errore di rete: {e}. Controlla la tua connessione.")
        else:
            st.info("💡 Scegli le opzioni a sinistra e clicca sul pulsante rosso per generare la foto perfetta del tuo capo sul manichino o sul modello.")

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
