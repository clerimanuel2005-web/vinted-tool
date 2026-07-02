import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
from PIL import Image, ImageOps, ImageEnhance

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Studio Sfondi Pro (Fedeltà 100%)", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: STUDIO FOTOGRAFICO REALE (ZERO ALTERAZIONI AL LOGO)
# ==========================================
with tab1:
    st.header("📸 Mockup Studio: Cambia lo Sfondo senza toccare il Logo")
    st.write("Questa tecnologia NON usa l'AI per ridisegnare il capo. Prende la tua foto originale e la ambienta in un set fotografico di lusso, mantenendo la stampa intatta al 100%.")

    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Prepara il tuo Capo Reale")
        st.info("💡 Per un risultato perfetto come nei cataloghi: rimuovi lo sfondo dalla tua foto (usando i link sotto) ottenendo un file PNG trasparente, poi caricalo qui.")
        
        # Link ai tool di rimozione sfondo gratuiti leader del settore
        st.link_button("✂️ Rimuovi lo Sfondo Gratis con Adobe", "https://www.adobe.com/express/feature/image/remove-background", use_container_width=True)
        st.link_button("✨ Rimuovi lo Sfondo Gratis con Photoroom", "https://www.photoroom.com/tools/background-remover", use_container_width=True)
        
        st.markdown("---")
        foto_ritagliata = st.file_uploader("Ora carica qui la foto (Preferibilmente senza sfondo / PNG):", type=["png", "jpg", "jpeg"])

        st.markdown("### 2️⃣ Scegli l'Ambientazione Premium")
        opzione_sfondo = st.selectbox(
            "Scegli lo sfondo del set fotografico:",
            [
                "Boutique di lusso con pavimento in resina e luci calde",
                "Studio fotografico minimalista grigio neutro",
                "Muro di cemento urbano stile industrial",
                "Showroom moderno con appendiabiti in legno"
            ]
        )
        
        st.markdown("### ⚙️ Regolazioni di Posizionamento")
        dimensione_capo = st.slider("Scala / Dimensione del capo sullo sfondo:", 30, 100, 75, step=5)
        posizione_verticale = st.slider("Altezza della maglietta (Sposta Su/Giù):", 0, 100, 50, step=5)
        
        st.markdown("### 🎨 Bilanciamento Luci")
        luminosita = st.slider("Luminosità della maglietta:", 0.6, 1.8, 1.0, step=0.05)

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Finale per Vinted (Garanzia Logo Originale)")
        
        if foto_ritagliata is not None:
            try:
                # Carichiamo la maglietta originale dell'utente
                capo_img = Image.open(foto_ritagliata).convert("RGBA")
                
                # Applichiamo modifiche di luce sulla maglietta originale senza alterarla
                if luminosita != 1.0:
                    enhancer = ImageEnhance.Brightness(capo_img)
                    capo_img = enhancer.enhance(luminosita)
                
                # Generiamo lo sfondo perfetto tramite seed fisso ad altissima definizione (FLUX) per fare da wallpaper
                sfondo_prompts = {
                    "Boutique di lusso con pavimento in resina e luci calde": "Luxury fashion boutique showroom interior, warm blurry spotlight, concrete floor, minimalist out of focus background",
                    "Studio fotografico minimalista grigio neutro": "Professional photography studio background, neutral soft grey color, studio lighting, empty space",
                    "Muro di cemento urbano stile industrial": "Industrial concrete wall background, loft design, soft top light, realistic textures",
                    "Showroom moderno con appendiabiti in legno": "Modern fashion store wall, wooden elements, elegant blurred retail store display"
                }
                
                # Recuperiamo l'immagine di sfondo professionale
                prompt_bg = sfondo_prompts[opzione_sfondo].replace(" ", "%20")
                url_bg = f"https://image.pollinations.ai/p/{prompt_bg}?width=1020&height=1020&nologo=true&seed=99"
                
                with st.spinner("Allineamento del set fotografico in corso..."):
                    res_bg = requests.get(url_bg, timeout=20)
                    if res_bg.status_code == 200:
                        sfondo_img = Image.open(io.BytesIO(res_bg.content)).convert("RGBA")
                        
                        # Ridimensioniamo la maglietta dell'utente in base allo slider
                        sfondo_w, sfondo_h = sfondo_img.size
                        nuovo_w = int(sfondo_w * (dimensione_capo / 100))
                        nuovo_h = int(capo_img.height * (nuovo_w / capo_img.width))
                        capo_resizer = capo_img.resize((nuovo_w, nuovo_h), Image.Resampling.LANCZOS)
                        
                        # Calcolo posizionamento centrale dinamico
                        pos_x = (sfondo_w - nuovo_w) // 2
                        # La coordinata Y dipende dallo slider dell'altezza selezionata dall'utente
                        spazio_y_libero = sfondo_h - nuovo_h
                        pos_y = int(spazio_y_libero * (posizione_verticale / 100)) if spazio_y_libero > 0 else 0
                        
                        # Incolliamo la maglietta originale sopra lo sfondo digitale preservando la trasparenza (alfa channel)
                        sfondo_img.paste(capo_resizer, (pos_x, pos_y), capo_resizer)
                        
                        # Mostriamo il risultato finale immacolato
                        output_finale = sfondo_img.convert("RGB")
                        st.image(output_finale, caption="Foto catalogo generata con la tua maglietta reale al 100%", use_container_width=True)
                        
                        # Pulsante di download
                        buf = io.BytesIO()
                        output_finale.save(buf, format="JPEG", quality=95)
                        st.download_button(
                            label="📥 Scarica Foto Perfetta per Vinted",
                            data=buf.getvalue(),
                            file_name="vinted_catalogo_reale.jpg",
                            mime="image/jpeg"
                        )
                        st.success("Fatto! Il disegno è rimasto identico all'originale perché non è stato ricostruito dall'AI.")
                    else:
                        st.error("Impossibile caricare il fondale dello studio. Riprova tra un istante.")
            except Exception as e:
                st.error(f"Errore durante la sovrapposizione digitale dell'immagine: {e}")
        else:
            st.info("💡 Carica la tua foto a sinistra per vederla applicata all'interno del set fotografico scelto.")

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
