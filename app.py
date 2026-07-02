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
    "📸 Manichino & Sfondi AI Multi-Scelta", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: GENERATORE MULTI-OPZIONE AI
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico AI Avanzato: Scegli il tuo Risultato")
    st.write("Carica la foto reale del capo. L'AI elaborerà le varianti e potrai selezionare la foto professionale migliore da salvare.")

    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Carica lo scatto originale (es. la maglietta sul letto):", type=["jpg", "jpeg", "png"])
        
        if foto_originale:
            st.image(foto_originale, caption="Foto originale caricata con successo", width=150)

        st.markdown("### 2️⃣ Dettagli dell'Articolo")
        brand_capo = st.text_input("Marca del capo:", value="", placeholder="Es. Off-White, Nike, Jordan...")
        tipo_prodotto = st.text_input("Tipo di capo:", value="", placeholder="Es. t-shirt, felpa con cappuccio...")
        
        st.markdown("### ⚙️ Parametri di Controllo AI")
        conservazione = st.slider("Mantenimento Grafica Originale:", 0.60, 0.90, 0.80, step=0.05, 
                                  help="Valori alti costringono l'AI a non toccare il logo originale.")

    with col_foto2:
        st.markdown("### 3️⃣ Genera e Scegli la tua Variante Preferita")
        
        if foto_originale is not None:
            # Creiamo i 3 stili pronti per essere scelti dall'utente
            stili_disponibili = {
                "Opzione 1: Manichino Invisibile (Showroom)": {
                    "supporto": "placed on an invisible ghost mannequin, perfectly ironed, high-end look",
                    "sfondo": "inside a luxury fashion showroom boutique with soft ambient light, premium minimalism"
                },
                "Opzione 2: Modello Streetwear (Studio)": {
                    "supporto": "worn by a professional streetwear male model, lookbook catalog pose",
                    "sfondo": "clean photography studio background, neutral grey tone, cinematic lighting"
                },
                "Opzione 3: Appeso Urban Style (Strada)": {
                    "supporto": "hanging cleanly on a premium minimalist wooden hanger",
                    "sfondo": "industrial urban street background, blurred city architecture, London style"
                }
            }
            
            # Selezione della variante tramite tab interne o pulsanti dedicati
            scelta_variante = st.radio("Scegli quale configurazione AI vuoi generare/visualizzare:", list(stili_disponibili.keys()))
            
            if st.button("✨ Elabora Variante Selezionata con AI", type="primary"):
                with st.spinner("L'AI sta modellando il capo sul supporto scelto... Attendi qualche secondo."):
                    try:
                        # Codifica l'immagine in Base64 per passarla al motore grafico
                        bytes_data = foto_originale.getvalue()
                        base64_image = base64.b64encode(bytes_data).decode("utf-8")
                        data_url = f"data:image/jpeg;base64,{base64_image}"
                        
                        # Recupero dei dati dello stile scelto
                        stile_selezionato = stili_disponibili[scelta_variante]
                        
                        # Costruzione del prompt combinato strutturale
                        prompt_str = (
                            f"Commercial clean lookbook product photography of the exact {brand_capo.lower()} {tipo_prodotto.lower()} from the source image. "
                            f"{stile_selezionato['supporto']}. {stile_selezionato['sfondo']}. "
                            f"Keep the exact colors, logo shapes, text elements and red graphic pattern details identical to the source image. "
                            f"Photorealistic, 8k, highly detailed garment structure."
                        ).replace(" ", "%20")
                        
                        # Chiamata API Img2Img dedicata
                        api_url = f"https://image.pollinations.ai/p/{prompt_str}?width=1080&height=1080&nologo=true&seed=42"
                        payload = {"image": data_url, "strength": conservazione}
                        
                        response = requests.post(api_url, json=payload, timeout=40)
                        
                        if response.status_code == 200:
                            image_res = Image.open(io.BytesIO(response.content))
                            st.image(image_res, caption=f"Anteprima Risultato: {scelta_variante}", use_container_width=True)
                            
                            # Preparazione file per scaricarlo
                            buffer = io.BytesIO()
                            image_res.save(buffer, format="JPEG", quality=95)
                            st.download_button(
                                label="📥 Scarica questa foto per il tuo annuncio",
                                data=buffer.getvalue(),
                                file_name="vinted_mockup_scelto.jpg",
                                mime="image/jpeg"
                            )
                            st.success("Variante generata! Se non ti soddisfa, seleziona un'altra Opzione sopra e clicca di nuovo il pulsante.")
                        else:
                            st.error("Il server AI è momentaneamente saturo. Attendi 5 secondi e clicca di nuovo.")
                    except Exception as e:
                        st.error(f"Errore tecnico nella comunicazione AI: {e}")
        else:
            st.info("💡 Per iniziare a generare le opzioni grafiche su manichino o modello, trascina la tua foto originale nel riquadro di sinistra.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="", placeholder="Inserisci la marca...")
        tipo_capo = st.text_input("Tipo di articolo", value="", placeholder="Es. Felpa, T-shirt...")
        colore = st.text_input("Colore e dettagli visivi", value="", placeholder="Es. Bianco con grafica...")
        
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
        difetti = st.text_input("Note su eventuali difetti", value="", placeholder="Es. nessuno, oppure descrivi...")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia}" if tipo_capo or brand else ""
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti else "• 🔎 Difetti: Nessuno, capo perfetto."
        
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure prese in piano:\n"
            if cm_ascelle: stringa_misure += f"   - Ascella - Ascella: {cm_ascelle} cm\n"
            if cm_lunghezza: stringa_misure += f"   - Lunghezza totale: {cm_lunghezza} cm\n"

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
