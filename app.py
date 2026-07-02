import streamlit as st
import pandas as pd
import requests
import io
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np
from rembg import remove

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
    st.write("Isola il tuo capo e posizionalo su manichini o grucce all'interno di scenari commerciali premium in Alta Definizione.")

    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto Reale")
        foto_originale = st.file_uploader("Trascina qui la foto della maglietta:", type=["jpg", "jpeg", "png"], key="vinted_uploader")
        
        if foto_originale:
            st.image(foto_originale, caption="Foto originale caricata", width=130)

        # SEZIONE WORKAROUND PER CAPI BIANCHI / SCOLORITI
        st.markdown("### ⚙️ Ottimizzazione AI Speciale")
        maglietta_bianca_fix = st.checkbox("👕 La maglietta bianca sparisce? Attiva correzione bordi", value=True, help="Forza l'AI a vedere il tessuto bianco se lo sfondo originale è chiaro.")

        st.markdown("### 2️⃣ Personalizza lo Scenario & Supporto")
        tipo_sfondo_scelto = st.selectbox(
            "Seleziona l'ambientazione desiderata:",
            [
                "Manichino invisibile in Showroom di lusso, luci calde",
                "Gruccia in legno minimale su muro in cemento industriale",
                "Manichino sartoriale in un negozio di Milano centro",
                "Stand appendiabiti in metallo, sfondo studio grigio catalogo",
                "Sfondo bianco puro e-commerce (Stile Amazon/Zalando)",
                "Boutique Streetwear moderna con luci al neon soft"
            ]
        )

        proporzione_capo = st.slider("Dimensione del livello nello sfondo:", 50, 90, 75)

    with col_foto2:
        st.markdown("### 3️⃣ Risultato Elaborato HD")
        
        if foto_originale is not None:
            if st.button("✨ Genera Foto Catalogo", type="primary"):
                with st.spinner("Scontornamento e rendering in Ultra HD (1440p) in corso..."):
                    try:
                        # 1. Caricamento immagine e correzione orientamento
                        img_input = Image.open(foto_originale)
                        img_input = ImageOps.exif_transpose(img_input)
                        
                        # 2. Rimozione sfondo con trucco del contrasto se attivato
                        if maglietta_bianca_fix:
                            img_contrasto = ImageEnhance.Contrast(img_input).enhance(2.8)
                            img_contrasto = ImageEnhance.Brightness(img_contrasto).enhance(0.7)
                            maschera_rembg = remove(img_contrasto).convert("RGBA")
                            
                            alpha_canale = maschera_rembg.getchannel('A')
                            maglietta_isolata = img_input.convert("RGBA")
                            maglietta_isolata.putalpha(alpha_canale)
                        else:
                            maglietta_isolata = remove(img_input).convert("RGBA")
                        
                        # 3. Mappatura dei prompt con risoluzione aumentata a 1440px
                        prompt_mappa = {
                            "Manichino invisibile in Showroom di lusso, luci calde": "A clothing item displayed on an invisible mannequin hanger inside a luxury fashion boutique store, warm cinematic lighting, blurry rich background, premium look, commercial product photography, 8k resolution, highly detailed",
                            "Gruccia in legno minimale su muro in cemento industriale": "An elegant minimalist wooden clothes hanger hanging against a raw grey concrete wall, soft side lighting, professional product photography, urban style, 8k resolution, crisp details",
                            "Manichino sartoriale in un negozio di Milano centro": "A high-end fashion boutique background in Milan, an elegant tailor mannequin stand torso holding clothes, warm soft boutique lighting, blurred background, 8k, sharp focus",
                            "Stand appendiabiti in metallo, sfondo studio grigio catalogo": "Professional e-commerce studio photography, a sleek metal clothing rack stand, neutral clean soft grey studio background, commercial lighting, ultra sharp",
                            "Sfondo bianco puro e-commerce (Stile Amazon/Zalando)": "Clean minimalist bright solid pure white studio background for e-commerce website catalog, sharp focus, seamless white backdrop, high resolution",
                            "Boutique Streetwear moderna con luci al neon soft": "Modern hypebeast streetwear clothing store interior, high-end display rack, soft purple and white neon ambient lights, blurred background, crisp 8k texturing"
                        }
                        
                        prompt_sfondo = prompt_mappa[tipo_sfondo_scelto].replace(" ", "%20")
                        sfondo_url = f"https://image.pollinations.ai/p/{prompt_sfondo}?width=1440&height=1440&nologo=true&model=flux&seed=102"
                        
                        response_sfondo = requests.get(sfondo_url, timeout=30)
                        
                        if response_sfondo.status_code == 200:
                            # Dimensione Ultra HD 1440x1440
                            sfondo_reale = Image.open(io.BytesIO(response_sfondo.content)).resize((1440, 1440)).convert("RGBA")
                            
                            # 4. Ridimensionamento proporzionale ad alta qualità (LANCZOS)
                            dim_max = int(1440 * (proporzione_capo / 100))
                            maglietta_isolata.thumbnail((dim_max, dim_max), Image.Resampling.LANCZOS)
                            
                            # 5. Generazione ombra morbida HD
                            alpha_ombra = maglietta_isolata.getchannel('A')
                            ombra = Image.new("RGBA", maglietta_isolata.size, (0, 0, 0, 50))
                            ombra.putalpha(alpha_ombra)
                            ombra = ombra.resize((maglietta_isolata.width + 20, maglietta_isolata.height + 20))
                            ombra = ombra.filter(ImageFilter.GaussianBlur(18))
                            
                            # 6. Composizione finale dei livelli
                            telaio_trasparente = Image.new("RGBA", (1440, 1440), (0, 0, 0, 0))
                            pos_x = (1440 - maglietta_isolata.width) // 2
                            pos_y = (1440 - maglietta_isolata.height) // 2
                            
                            telaio_trasparente.paste(ombra, (pos_x - 10, pos_y + 12))
                            telaio_trasparente.paste(maglietta_isolata, (pos_x, pos_y), mask=maglietta_isolata)
                            
                            immagine_pronta = Image.alpha_composite(sfondo_reale, telaio_trasparente).convert("RGB")
                            
                            # ✨ AGGIUNTA FILTRO NITIDEZZA HD PRO ✨
                            esaltatore_nitidezza = ImageEnhance.Sharpness(immagine_pronta)
                            immagine_pronta = esaltatore_nitidezza.enhance(1.3) # Aumenta la definizione dei bordi e dei loghi
                            
                            # Mostra il risultato forzando una larghezza fissa a schermo per non sgranarlo sul browser
                            st.image(immagine_pronta, caption="Anteprima Catalogo HD", width=620)
                            
                            # Bottone di download sicuro alla massima qualità
                            buffer = io.BytesIO()
                            immagine_pronta.save(buffer, format="JPEG", quality=100) # Qualità JPEG al 100% senza compressione
                            st.download_button(
                                label="📥 Scarica Immagine Ultra HQ (1440p)",
                                data=buffer.getvalue(),
                                file_name="vinted_ultra_hd.jpg",
                                mime="image/jpeg"
                            )
                        else:
                            st.error("Il server di generazione dello sfondo non ha risposto. Riprova tra un istante.")
                    except Exception as e:
                        st.error(f"Errore durante l'elaborazione: {e}.")
        else:
            st.info("💡 Carica un'immagine nella colonna di sinistra per iniziare la trasformazione.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="", placeholder="Es. Off-White, Nike...")
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
            if cm_lunghezza: stringa_misure += f"    - Lunghezza totale: {cm_lunghezza} cm\
