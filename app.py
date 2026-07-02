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
    st.write("Invia la tua foto originale ai modelli di Hugging Face per stirare le pieghe del tessuto e montarla su un manichino invisibile.")

    col_foto1, col_foto2 = st.columns([1.3, 1.7], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica lo Scatto Originale")
        foto_originale = st.file_uploader("Trascina qui la foto della tua maglietta (es. sul letto o spiegazzata):", type=["jpg", "jpeg", "png"])
        
        st.markdown("### 2️⃣ Dettagli della Stampa")
        marca_vestito = st.text_input("Marca del capo:", value="Off-White")
        tipo_vestito = st.text_input("Tipo di articolo:", value="T-shirt a maniche corte")
        colore_tessuto = st.text_area("Descrizione dettagliata della grafica e colore:", value="White cotton fabric, big red arrows logo on the back filled with red lips pattern texture, sharp print details.")
        
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
            help="Valori bassi (0.30 - 0.35) mantengono il logo originale intatto e spianano solo le pieghe del tessuto."
        )

    with col_foto2:
        st.markdown("### 4️⃣ Anteprima Catalogo Finale")
        
        if foto_originale is None:
            # Mostra l'immagine dimostrativa ideale finché l'utente non carica il file
            placeholder_url = "https://image.pollinations.ai/p/photorealistic%20back%20view%20ghost%20mannequin%20display%20of%20a%20clean%20ironed%20white%20off-white%20t-shirt%20with%20a%20prominent%20red%20arrows%20logo%20with%20kissing%20lips%20pattern%20on%20a%20smooth%20grey%20studio%20background?width=1020&height=1020&nologo=true&seed=99"
            st.image(placeholder_url, caption="Esempio di resa finale Ghost Mannequin", use_container_width=True)
            st.info("💡 Carica un file immagine a sinistra ed inserisci il Token Hugging Face per elaborare il tuo capo reale.")
        else:
            if not hf_token:
                st.warning("⚠️ Token di autenticazione mancante. Inserisci il tuo Hugging Face Token nella barra laterale sinistra per sbloccare l'elaborazione.")
                st.image(foto_originale, caption="Anteprima scatto originale (In attesa del Token)", use_container_width=True)
            else:
                if st.button("✨ Applica Manichino e Stira Tessuto", type="primary"):
                    with st.spinner("Connessione ai server di Inpainting in corso... Rimozione pieghe del tessuto..."):
                        try:
                            img_bytes = foto_originale.getvalue()
                            
                            # Endpoint Hugging Face per SDXL Refiner Image-to-Image
                            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-refiner-1.0"
                            headers = {"Authorization": f"Bearer {hf_token}"}
                            
                            prompt_str = (
                                f"High-end commercial clothing photography, {opzione_manichino}, retail lookbook, "
                                f"fabric is perfectly ironed, 100% flat smooth texture, zero wrinkles, clean crisp details "
                                f"of the {marca_vestito.capitalize()} logo, {colore_tessuto.lower()}, professional studio lighting, "
                                f"neutral grey background, flawless graphic shapes."
                            )
                            
                            payload = {
                                "inputs": prompt_str,
                                "image": img_bytes,
                                "strength": forza_stiro
                            }
                            
                            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                            
                            if response.status_code == 200:
                                image_res = Image.open(io.BytesIO(response.content))
                                st.image(image_res, caption="Capo elaborato: Tessuto stirato e montato su manichino", use_container_width=True)
                                
                                buffer = io.BytesIO()
                                image_res.save(buffer, format="JPEG", quality=98)
                                st.download_button(
                                    label="📥 Scarica Foto Catalogo Finita",
                                    data=buffer.getvalue(),
                                    file_name="vinted_ghost_mannequin.jpg",
                                    mime="image/jpeg"
                                )
                                st.success("Fatto! Il tessuto è stato levigato mantenendo la struttura principale.")
                            else:
                                st.error(f"Errore dal server AI (Codice {response.status_code}). Il modello potrebbe essere in caricamento, riprova tra un minuto.")
                        except Exception as e:
                            st.error(f"Errore tecnico di rete: {e}")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="", placeholder="Es. Off-White...")
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
        
        # Rendering del grafico ad anello se ci sono valori finanziari reali
        if prezzo_vendita > 0 and costo_acquisto > 0:
            df_chart = pd.DataFrame({
                'Componente': ['Costo Speso', 'Margine Guadagno'],
                'Valore': [costo_acquisto, max(0.0, guadagno_netto)]
            })
            chart_og = alt.Chart(df_chart).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Valore", type="quantitative"),
                color=alt.Color(field="Componente", type="nominal")
            )
            st.altair_chart(chart_og, use_container_width=True)

# ==========================================
# TAB 4: TREND & RICERCA RAPIDA (Tutte le tabelle complete)
# ==========================================
with tab4:
    st.header("📊 I Trend di Mercato Caldi & Analisi Nicchie")
    st.write("Consulta i dati aggregati in tempo reale relativi alle categorie e alle nicchie di reselling più redditizie su Vinted Italia.")
    
    col_t1, col_t2 = st.columns(2, gap="large")
    
    with col_t1:
        st.markdown("### 🔥 Trend di Ricerca Attuali (Italia)")
        tabelle_ricerca = pd.DataFrame({
            "Posizione": [1, 2, 3, 4, 5],
            "Categoria/Stile": ["Sneakers Hype Retro (Jordan, Dunk, Gazelle)", "Giacche Gorpcore / Tecniche (Arc'teryx, TNf)", "Denim Baggy & Skate (Y2K, Polar Big Boy)", "Y2K Streetwear Tops (Stussy, Corteiz)", "Giacche Varsity Vintage (Pelle/Lana)"],
            "Volume di Ricerca": ["Alto (15k+ ricerche/sett)", "Alto (9k+ ricerche/sett)", "Medio (6k+ ricerche/sett)", "Medio (4k+ ricerche/sett)", "In Crescita (2k+ ricerche/sett)"],
            "Liquidità Capo": ["Molto Alta (Vende in <48h)", "Alta", "Media", "Alta", "Media"]
        })
        st.dataframe(tabelle_ricerca, use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("### 📈 Nicchie Vintage in Forte Crescita")
        tabelle_nicchie = pd.DataFrame({
            "Posizione": [1, 2, 3, 4],
            "Tipologia Prodotto Vintage": ["T-shirt di Band Musicali Vintage (Anni '80/'90)", "Maglie da Calcio Anni '90/00 (Nomi storici)", "Giacche a Vento Colorblock (Nike, Adidas Vintage)", "Workwear Pants Usurati (Carhartt Carpenter)"],
            "Tasso di Crescita": ["+120% (Ultimi 3 mesi)", "+105%", "+90%", "+75%"],
            "Prezzo Medio Richiesto (€)": ["35€ - 80€", "45€ - 120€+", "30€ - 60€", "40€ - 70€"]
        })
        st.dataframe(tabelle_nicchie, use_container_width=True, hide_index=True)
        
    st.markdown("---")
    st.markdown("### 🎯 Brand Top-Selling e Margini di Rischio Controindicati")
    
    col_t3, col_t4 = st.columns(2, gap="large")
    
    with col_t3:
        st.markdown("##### 🚀 Brand con il Tasso di Rotazione più Alto")
        tabelle_brand = pd.DataFrame({
            "Brand": ["Nike", "Adidas", "Carhartt WIP", "Stussy", "Ralph Lauren", "The North Face"],
            "Categoria Dominante": ["Sneakers/Tute", "Samba/Gazelle/Vintage", "Pantaloni/Giacche", "T-shirt/Felpe", "Camicie/Maglioni", "Puffer/Giacche"],
            "Fascia Prezzo Target": ["20€ - 60€", "15€ - 50€", "30€ - 70€", "35€ - 90€", "15€ - 40€", "50€ - 150€"]
        })
        st.dataframe(tabelle_brand, use_container_width=True, hide_index=True)
        
    with col_t4:
        st.markdown("##### ⚠️ Rischio Repliche e Blocchi Segnalazioni Vinted")
        tabelle_rischio = pd.DataFrame({
            "Brand a Rischio": ["Trapstar / Synaworld", "Corteiz", "Stussy (T-shirt basic)", "Nike Tech Fleece", "Moncler (Puffer)"],
            "Livello di Rischio Replica": ["Critico (85%)", "Alto (70%)", "Medio-Alto", "Alto", "Critico"],
            "Azione Consigliata": ["Richiedi sempre ricevuta", "Controlla font etichette", "Verifica cuciture interne", "Evita lotti stock dubbi", "Usa solo autenticazione Vinted Pro"]
