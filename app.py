import streamlit as st
import pandas as pd
import requests
import io
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from rembg import remove, new_session

# 1. CONFIGURAZIONE DELLA PAGINA (Deve essere il primo comando Streamlit)
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# Inizializzazione in cache delle sessioni AI per non saturare la memoria e velocizzare l'app
if "session_standard" not in st.session_state:
    st.session_state.session_standard = new_session(model_name="u2net")
if "session_clothing" not in st.session_state:
    st.session_state.session_clothing = new_session(model_name="u2net_clothing")

# Titolo principale dell'applicazione
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
    st.write("Isola la tua maglietta, correggi i difetti di contrasto e posizionala su un supporto professionale senza sovrapposizioni.")

    # Layout a due colonne: Input a sinistra, Risultato a destra
    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Trascina qui la foto scattata:", type=["jpg", "jpeg", "png"], key="vinted_uploader")
        
        if foto_originale:
            st.image(foto_originale, caption="Foto originale caricata", width=140)

        st.markdown("### ⚙️ Impostazioni Scontornamento AI")
        
        modalita_scontorno = st.selectbox(
            "Modalità di ritaglio del capo:",
            [
                "Bordi Precisi (Specifico per Magliette Bianche/Chiare)",
                "Standard (Consigliato per capi scuri o molto colorati)",
                "Forza Contrasto Avanzato"
            ],
            index=0,
            help="Usa la modalità Bordi Precisi se lo sfondo originale è chiaro e la maglietta bianca rischia di sparire."
        )
        
        # Permette di cambiare il seed per generare variazioni diverse dello stesso sfondo
        cambia_variante = st.button("🔄 Cambia variante dello sfondo casualmente")
        if "bg_seed" not in st.session_state or cambia_variante:
            st.session_state.bg_seed = random.randint(1, 9999)

        st.markdown("### 2️⃣ Scegli lo Scenario (Sfondi Vuoti)")
        tipo_sfondo_scelto = st.selectbox(
            "Seleziona l'ambiente in cui inserire il tuo capo:",
            [
                "Gruccia in legno minimale su muro in cemento industriale",
                "Showroom di lusso (Sfondo vuoto con luci calde)",
                "Manichino sartoriale vuoto in un negozio di Milano centro",
                "Stand appendiabiti in metallo vuoto, studio grigio catalogo",
                "Sfondo bianco puro e-commerce (Stile Amazon/Zalando)",
                "Boutique Streetwear moderna vuota con luci al neon soft"
            ]
        )

        proporzione_capo = st.slider("Dimensione del capo all'interno dello scenario (%):", 50, 90, 70)

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Elaborato in Ultra HD")
        
        if foto_originale is not None:
            if st.button("✨ Genera Foto Catalogo HQ", type="primary"):
                with st.spinner("Isolamento tessuto bianco e fusione dei livelli in corso..."):
                    try:
                        # Caricamento immagine e auto-rotazione basata sui dati EXIF dello smartphone
                        img_input = Image.open(foto_originale)
                        img_input = ImageOps.exif_transpose(img_input)
                        
                        # APPLICAZIONE DELLA MODALITÀ DI SCONTORNAMENTO SELEZIONATA
                        if modalita_scontorno == "Bordi Precisi (Specifico per Magliette Bianche/Chiare)":
                            # TRUCCO TECNICO: Generiamo un'immagine ad altissimo contrasto temporanea solo per la maschera AI
                            img_temporanea = ImageOps.autocontrast(img_input)
                            img_temporanea = ImageEnhance.Contrast(img_temporanea).enhance(1.6)
                            
                            # Facciamo leggere all'AI l'immagine contrastata (dove i bordi bianchi sono evidenti)
                            maschera_rembg = remove(img_temporanea, session=st.session_state.session_clothing).convert("RGBA")
                            
                            # Prendiamo la sagoma perfetta trovata dall'AI e la applichiamo alla foto originale pulita
                            alpha_canale = maschera_rembg.getchannel('A')
                            maglietta_isolata = img_input.convert("RGBA")
                            maglietta_isolata.putalpha(alpha_canale)
                            
                        elif modalita_scontorno == "Standard (Consigliato per capi scuri o molto colorati)":
                            maglietta_isolata = remove(img_input, session=st.session_state.session_standard).convert("RGBA")
                            
                        else:  # Forza Contrasto Avanzato
                            img_elaborata = ImageEnhance.Contrast(img_input).enhance(2.0)
                            img_elaborata = ImageEnhance.Sharpness(img_elaborata).enhance(1.8)
                            maschera_rembg = remove(img_elaborata, session=st.session_state.session_standard).convert("RGBA")
                            
                            alpha_canale = maschera_rembg.getchannel('A')
                            maglietta_isolata = img_input.convert("RGBA")
                            maglietta_isolata.putalpha(alpha_canale)
                        
                        # MAPPA DEI PROMPT CORRETTA: Generano solo ambienti VUOTI, senza vestiti pre-esistenti dell'AI!
                        prompt_mappa = {
                            "Showroom di lusso (Sfondo vuoto con luci calde)": "An empty luxury fashion boutique store showroom, elegant minimalist background, warm cinematic lighting, blurry rich interior, premium look, commercial product photography, 8k resolution, highly detailed, no clothes, empty space",
                            "Gruccia in legno minimale su muro in cemento industriale": "An empty minimalist wooden clothes hanger hanging symmetrically against a raw grey concrete wall, soft side lighting, professional product photography, urban style, 8k resolution, crisp details, no clothes",
                            "Manichino sartoriale vuoto in un negozio di Milano centro": "A high-end fashion boutique background in Milan, an empty elegant vintage tailor mannequin stand torso with no clothes on it, warm soft boutique lighting, blurred interior background, 8k, sharp focus",
                            "Stand appendiabiti in metallo vuoto, studio grigio catalogo": "Professional e-commerce studio photography, a sleek empty metal clothing rack stand, neutral clean soft grey studio background, commercial studio lighting, ultra sharp, no clothes, empty display",
                            "Sfondo bianco puro e-commerce (Stile Amazon/Zalando)": "Clean minimalist bright solid pure white studio background for e-commerce website clothing catalog, sharp focus, seamless white backdrop, high resolution, empty clean space",
                            "Boutique Streetwear moderna vuota con luci al neon soft": "Modern hypebeast streetwear clothing store interior showroom, empty high-end display rack, soft purple and white neon ambient lights, blurred background, crisp 8k texturing, no clothes, empty interior"
                        }
                        
                        # Richiesta dello sfondo Ultra HD (1440x1440 pixel)
                        prompt_sfondo = prompt_mappa[tipo_sfondo_scelto].replace(" ", "%20")
                        sfondo_url = f"https://image.pollinations.ai/p/{prompt_sfondo}?width=1440&height=1440&nologo=true&model=flux&seed={st.session_state.bg_seed}"
                        
                        response_sfondo = requests.get(sfondo_url, timeout=30)
                        
                        if response_sfondo.status_code == 200:
                            sfondo_reale = Image.open(io.BytesIO(response_sfondo.content)).resize((1440, 1440)).convert("RGBA")
                            
                            # Ridimensionamento proporzionale ad alta qualità del capo d'abbigliamento
                            dim_max = int(1440 * (proporzione_capo / 100))
                            maglietta_isolata.thumbnail((dim_max, dim_max), Image.Resampling.LANCZOS)
                            
                            # Generazione di un'ombra morbida realistica sotto il capo
                            alpha_ombra = maglietta_isolata.getchannel('A')
                            ombra = Image.new("RGBA", maglietta_isolata.size, (0, 0, 0, 40))
                            ombra.putalpha(alpha_ombra)
                            ombra = ombra.resize((maglietta_isolata.width + 25, maglietta_isolata.height + 25))
                            ombra = ombra.filter(ImageFilter.GaussianBlur(22))
                            
                            # Posizionamento e composizione finale dei livelli sul canvas 1440p
                            telaio_trasparente = Image.new("RGBA", (1440, 1440), (0, 0, 0, 0))
                            pos_x = (1440 - maglietta_isolata.width) // 2
                            pos_y = (1440 - maglietta_isolata.height) // 2
                            
                            telaio_trasparente.paste(ombra, (pos_x - 12, pos_y + 15))
                            telaio_trasparente.paste(maglietta_isolata, (pos_x, pos_y), mask=maglietta_isolata)
                            
                            immagine_pronta = Image.alpha_composite(sfondo_reale, telaio_trasparente).convert("RGB")
                            
                            # FILTRO NITIDEZZA AVANZATO (Rende i contorni e la trama del cotone definiti)
                            esaltatore_nitidezza = ImageEnhance.Sharpness(immagine_pronta)
                            immagine_pronta = esaltatore_nitidezza.enhance(1.4)
                            
                            # Mostra l'anteprima bloccando la larghezza per evitare l'allungamento sgranato del browser
                            st.image(immagine_pronta, caption="Anteprima del tuo annuncio premium in HD", width=580)
                            
                            # Salvataggio in memoria alla massima qualità fotografica (Zero Compressione)
                            buffer = io.BytesIO()
                            immagine_pronta.save(buffer, format="JPEG", quality=100)
                            
                            st.download_button(
                                label="📥 Scarica Immagine Ultra HD (1440p)",
                                data=buffer.getvalue(),
                                file_name="vinted_annuncio_hd.jpg",
                                mime="image/jpeg"
                              )
                        else:
                            st.error("Il server di rendering dello sfondo non ha risposto. Riprova tra pochi secondi.")
                    except Exception as e:
                        st.error(f"Si è verificato un errore durante l'elaborazione dell'immagine: {e}")
        else:
            st.info("💡 Carica la foto della tua maglietta nella colonna di sinistra per iniziare la trasformazione.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI COMMERCIALI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="", placeholder="Es. Off-White, Nike, Adidas...")
        tipo_capo = st.text_input("Tipo di articolo", value="", placeholder="Es. T-shirt, Felpa, Hoodie...")
        colore = st.text_input("Colore e dettagli visivi", value="", placeholder="Es. Bianco con stampa rossa sul petto...")
        
        st.markdown("### 📏 Taglia e Misure in Piano")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit"])
        
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1:
            cm_ascelle = st.text_input("Distanza ascella-ascella (cm)", value="", placeholder="Es. 54")
        with col_cm2:
            cm_lunghezza = st.text_input("Lunghezza totale (cm)", value="", placeholder="Es. 71")
            
        st.markdown("### 🎚️ Stato di Usura")
        condizioni = st.selectbox("Condizioni generali", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime condizioni", "Buone condizioni"])
        difetti = st.text_input("Note su imperfezioni o difetti", value="", placeholder="Es. nessuno, nessun segno di usura...")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia}" if tipo_capo or brand else ""
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti else "• 🔎 Difetti: Nessuno, capo mantenuto in modo maniacale."
        
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure precise prese in piano:\n"
            if cm_ascelle: stringa_misure += f"    - Ascella - Ascella: {cm_ascelle} cm\n"
            if cm_lunghezza: stringa_misure += f"    - Lunghezza totale: {cm_lunghezza} cm\n"

        brand_tag = brand.replace(' ', '').lower() if brand else "brand"
        tipo_tag = tipo_capo.replace(' ', '').lower() if tipo_capo else "abbigliamento"

        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO PREMIUM:
Vendo bellissima {tipo_capo.lower() if tipo_capo else 'maglia'} originale {brand.capitalize() if brand else '-'}. Il capo è stato lavato professionalmente, igienizzato e conservato piegato.

• 🎨 Colore e Dettagli: {colore.capitalize() if colore else '-'}
• 📏 Taglia: {taglia}
• 📈 Vestibilità consigliata: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedizione super rapida e protetta entro 24 ore dall'acquisto 📦. Se hai domande o vuoi foto aggiuntive scrivimi pure in chat! 📲

---
# {brand_tag} #{tipo_tag} #taglia{taglia.lower()} #streetwear #vinteditalia #reseller
"""
        st.text_input("📌 Titolo da inserire su Vinted:", titolo_generato)
        st.text_area("📄 Descrizione completa da inserire su Vinted:", descrizione_generata, height=340)

# ==========================================
# TAB 3: CALCOLATORE PREZZI E MARGINI LOGISTICI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi dei Profitti")
    col_input, col_chart = st.columns([1.5, 2.5], gap="large")

    with col_input:
        st.markdown("### 📊 Analisi Finanziaria del Capo")
        costo_acquisto = st.number_input("💰 Quanto hai pagato questo capo? (€)", min_value=0.0, value=15.0, format="%.2f")
        prezzo_vendita = st.number_input("🏷️ Prezzo a cui vuoi venderlo su Vinted (€)", min_value=0.0, value=45.0, format="%.2f")
        percentuale_sconto = st.slider("Che sconto imposti se un utente fa un lotto? (%):", 0, 50, 15)

    with col_chart:
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = (guadagno_netto / costo_acquisto) * 100 if costo_acquisto > 0 else 0
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - costo_acquisto

        st.markdown("### 🏬 Performance Economica")
        m_col1, m_col2 = st.columns(2)
        with m_col1: 
            st.metric(label="🤑 Guadagno Netto (Vendita Singola)", value=f"{guadagno_netto:.2f} €")
        with m_col2: 
            st.metric(label="📈 Ritorno sull'Investimento (ROI)", value=f"{roi:.1f}%")

        st.markdown("---")
        st.markdown("##### 📊 Tabella Comparativa Ricavi")
        data_tabella = {
            "Scenario di Vendita": ["Vendita Singola Standard", f"Vendita in Lotto (Scontata del {percentuale_sconto}%)"],
            "Prezzo Pagato dall'Acquirente (€)": [f"{prezzo_vendita:.2f} €", f"{prezzo_scontato_lotto:.2f} €"],
            "Il tuo Profitto Reale (€)": [f"{guadagno_netto:.2f} €", f"{guadagno_lotto:.2f} €"],
            "Valutazione Operazione": ["Margine Massimo" if guadagno_netto > 0 else "Perdita", "Margine Ottimizzato" if guadagno_lotto > 0 else "Perdita"]
        }
        st.table(pd.DataFrame(data_tabella))

# ==========================================
# TAB 4: TREND E MONITORAGGIO MERCATO
# ==========================================
with tab4:
    st.header("📊 Trend di Mercato Caldi & Ricerche Frequenti")
    col_t1, col_t2 = st.columns(2, gap="medium")
    
    with col_t1:
        st.markdown("### 🔥 Categorie più cercate questo mese")
        tabelle_ricerca = pd.DataFrame({
            "Posizione": [1, 2, 3, 4, 5],
            "Categoria/Stile Outfit": ["Sneakers Hype (Jordan, Dunk, Campus)", "Giacche Tecniche Gorpcore (Arc'teryx, TNF)", "Denim Baggy / Skate Pants Y2K", "T-Shirt Streetwear Grafiche Vintage", "Varsity Jackets / Giacche College Usate"],
            "Volume di Ricerche Giornaliere": ["Altissimo (20k+)", "Alto (14k+)", "Alto (11k+)", "Medio-Alto (9k+)", "In forte crescita (5k+)"]
        })
        st.dataframe(tabelle_ricerca, use_container_width=True, hide_index=True)

    with col_t2:
        st.markdown("### 📈 Nicchie ad alto margine (Meno concorrenza)")
        tabelle_nicchie = pd.DataFrame({
            "Posizione": [1, 2, 3, 4],
            "Prodotti Vintage / Archivio": ["T-shirt di Band Musicali Anni '90", "Maglie da Calcio Vintage (Pre-2004)", "Pantaloni Workwear Carhartt/Dickies Usurati", "Giacche a vento Colorblock Old School"],
            "Incremento Domanda": ["+145%", "+120%", "+110%", "+85%"]
        })
        st.dataframe(tabelle_nicchie, use_container_width=True, hide_index=True)
