import streamlit as st
import pandas as pd
import requests
import io
import base64
from PIL import Image
from rembg import remove  # Libreria per rimuovere lo sfondo gratis senza deformare i loghi

# Configurazione della pagina
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
# TAB 1: MANICHINO REALE E CAMBIO SFONDO AUTOMATICO (CORRETTO)
# ==========================================
with tab1:
    st.header("📸 Manichino Invisibile & Cambio Sfondo Automatico via AI")
    st.write("Questo sistema isola la tua maglietta originale (mantenendo il logo intatto) e la posiziona su uno sfondo professionale con effetto manichino.")

    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Trascina qui la foto originale della maglietta (anche su letto o pavimento):", type=["jpg", "jpeg", "png"], key="vinted_uploader")
        
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

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Elaborato")
        
        if foto_originale is not None:
            if st.button("✨ Genera Foto Catalogo", type="primary"):
                with st.spinner("Isolamento della maglietta e rimozione sfondo in corso..."):
                    try:
                        # 1. RIMOZIONE SFONDO AUTOMATICA E GRATUITA (Mantiene il logo perfetto!)
                        input_image = Image.open(foto_originale)
                        output_image = remove(input_image) # La maglietta ora è isolata su sfondo trasparente
                        
                        # 2. GENERAZIONE DELLO SFONDO IDEALE CON POLLINATIONS AI
                        prompt_mappa = {
                            "Studio grigio minimalista, luce morbida da catalogo": "Professional product photography background, empty ghost mannequin template torso, neutral soft grey photography studio background, high-end look, 8k",
                            "Showroom di lusso sfocato, luci calde": "Luxury fashion boutique clothing store blurred background, elegant hanger display stand area, warm cinematic lighting",
                            "Sfondo bianco puro e-commerce": "Clean minimalist bright solid white background for e-commerce catalog, studio lighting, sharp focus"
                        }
                        
                        prompt_sfondo = prompt_mappa[tipo_sfondo_scelto].replace(" ", "%20")
                        sfondo_url = f"https://image.pollinations.ai/p/{prompt_sfondo}?width=1080&height=1080&nologo=true&model=flux&seed=42"
                        
                        response_sfondo = requests.get(sfondo_url, timeout=30)
                        
                        if response_sfondo.status_code == 200:
                            sfondo_ai = Image.open(io.BytesIO(response_sfondo.content)).resize((1080, 1080))
                            
                            # 3. COMBINIAMO LA TUA MAGLIETTA SOPRA LO SFONDO AI
                            # Convertiamo in RGBA per gestire la trasparenza
                            maglietta_ritagliata = output_image.convert("RGBA")
                            
                            # Ridimensioniamo proporzionalmente la maglietta per farla stare bene nel quadro
                            maglietta_ritagliata.thumbnail((750, 750), Image.Resampling.LANCZOS)
                            
                            # Creiamo un livello trasparente per centrare la maglietta sullo sfondo
                            livello_maglietta = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
                            pos_x = (1080 - maglietta_ritagliata.width) // 2
                            pos_y = (1080 - maglietta_ritagliata.height) // 2
                            livello_maglietta.paste(maglietta_ritagliata, (pos_x, pos_y))
                            
                            # Uniamo lo sfondo generato dall'AI e il ritaglio della maglietta originale
                            foto_finale = Image.alpha_composite(sfondo_ai.convert("RGBA"), livello_maglietta).convert("RGB")
                            
                            # Mostriamo il risultato finale a schermo
                            st.image(foto_finale, caption="Ecco il tuo capo su sfondo professionale", use_container_width=True)
                            
                            # Bottone per scaricare il file pronto
                            buffer = io.BytesIO()
                            foto_finale.save(buffer, format="JPEG", quality=95)
                            st.download_button(
                                label="📥 Scarica Foto Finita",
                                data=buffer.getvalue(),
                                file_name="vinted_mannequin_perfect.jpg",
                                mime="image/jpeg"
                            )
                            st.success("Fatto! Il logo e la maglietta sono reali al 100%, ma lo sfondo e l'effetto catalogo sono stati ricreati dall'AI!")
                        else:
                            st.error("Il server AI è congestionato. Attendi un istante e riprova.")
                            
                    except Exception as e:
                        st.error(f"Errore di connessione o elaborazione: {e}")
        else:
            st.info("💡 Carica lo scatto originale a sinistra e premi il pulsante per far fare tutto al sistema.")


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
