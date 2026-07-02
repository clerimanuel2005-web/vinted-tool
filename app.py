import streamlit as st
import pandas as pd
import requests
from PIL import Image, ImageEnhance
import io

# Configurazione della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# Inserisci qui la tua chiave API presa da Clipdrop
CLIPDROP_API_KEY = "INSERISCI_QUI_LA_TUA_API_KEY"

# Creazione delle 4 Schede di Gestione
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Clothes Ironing AI", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend del Mese"
])

# ==========================================
# TAB 1: CLOTHES IRONING AI
# ==========================================
with tab1:
    st.header("Studio di Stiratura e Sfondo Digitale")
    uploaded_file = st.file_uploader("Scegli la foto del vestito...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("❌ Foto Originale")
            st.image(uploaded_file, use_container_width=True)
            
        with col2:
            st.subheader("✨ Risultato Professionale")
            with st.spinner("Elaborazione in corso..."):
                try:
                    r = requests.post(
                        'https://clipdrop-api.co/remove-background/v1',
                        files={'image_file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                        headers={'x-api-key': CLIPDROP_API_KEY}
                    )
                    if r.status_code == 200:
                        img_no_bg = Image.open(io.BytesIO(r.content))
                        white_bg = Image.new("RGBA", img_no_bg.size, (255, 255, 255, 255))
                        white_bg.paste(img_no_bg, (0, 0), img_no_bg)
                        final_img = white_bg.convert("RGB")
                        
                        enhancer = ImageEnhance.Brightness(final_img)
                        final_img = enhancer.enhance(1.15)
                        
                        st.image(final_img, use_container_width=True)
                        
                        buffer = io.BytesIO()
                        final_img.save(buffer, format="JPEG", quality=100)
                        
                        st.download_button(
                            label="📥 Scarica Foto Perfetta",
                            data=buffer.getvalue(),
                            file_name="vestito_vinted_ok.jpg",
                            mime="image/jpeg",
                            type="primary"
                        )
                        st.success("🎉 Foto ottimizzata!")
                    else:
                        st.error("Configura l'API Key di Clipdrop per sbloccare il tool.")
                except Exception as e:
                    st.error(f"Errore: {e}")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI (NUOVO!)
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    st.write("Compila i campi velocemente per generare una descrizione magnetica che attira i compratori e scala l'algoritmo di ricerca.")

    col_a, col_b = st.columns(2)
    with col_a:
        brand = st.text_input("Brand / Marca del capo", placeholder="Es. Off-White, Nike, Levi's")
        tipo_capo = st.text_input("Tipo di articolo", placeholder="Es. T-shirt grafica, Jeans 501, Felpa con cappuccio")
        colore = st.text_input("Colore principale", placeholder="Es. Bianco, Nero, Vintage Wash")
        
        condizioni = st.selectbox("Condizioni del capo", [
            "Nuovo con cartellino", 
            "Nuovo senza cartellino", 
            "Ottime condizioni (indossato pochissimo, nessun difetto)", 
            "Buone condizioni (normali segni di usura)",
            "Soddisfacente (presenta piccoli difetti specificati)"
        ])
        
        difetti = st.text_input("Note o piccoli difetti (opzionale)", placeholder="Es. Nessun difetto, micro-segno sulla manica")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        
        # Generatore di testo logico
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - {colore.capitalize()}"
        
        nota_difetti = f"• 🔎 Difetti: {difects}" if difetti else "• 🔎 Difetti: Nessuno, capo perfetto."
        
        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo bellissima {tipo_capo.lower()} originale del brand {brand.capitalize()}.

• 🎨 Colore: {colore.capitalize()}
• 📈 Condizioni: {condizioni}
{nota_difetti}
• 📏 Taglia: (Verificare misure in DM se necessario)

Spedisco velocemente entro 24 ore dal pagamento 📦. Se hai domande o vuoi fare un'offerta (sensata), scrivimi pure in privato! 📲

---
Tag per algoritmo:
#{brand.lower()} #{tipo_capo.replace(' ', '').lower()} #{colore.lower()} #vintedvintage #streetwear #reselling
"""
        st.text_input("📌 Titolo dell'annuncio:", titolo_generato)
        st.text_area("📄 Descrizione dell'annuncio (Copia e Incolla su Vinted):", descrizione_generata, height=320)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI (NUOVO!)
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Sconti sui Lotti")
    st.write("Calcola quanto guadagni davvero al netto dei tuoi costi ed imposta una strategia per i lotti di acquirenti multipli.")

    col_x, col_y = st.columns(2)
    with col_x:
        prezzo_acquisto = st.number_input("Quanto hai pagato il capo? (€)", min_value=0.0, value=10.0, step=1.0)
        prezzo_vendita = st.number_input("A quanto vuoi venderlo su Vinted? (€)", min_value=0.0, value=35.0, step=1.0)
        
        st.markdown("### 🏬 Simulatore Sconto Pacchetti")
        percentuale_sconto = st.slider("Se un utente crea un lotto, che sconto vuoi applicare? (%)", 0, 50, 15)

    with col_y:
        st.subheader("📊 Resoconto Finanziario")
        
        # Calcoli matematici semplici per il reselling
        ricavo_netto = prezzo_vendita - prezzo_acquisto
        roi = (ricavo_netto / prezzo_acquisto) * 100 if prezzo_acquisto > 0 else 0
        
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - prezzo_acquisto

        # Box metriche visive
        st.metric(label="🤑 Guadagno Netto Singolo", value=f"{ricavo_netto:.2s} €", delta=f"ROI: {roi:.1f}%")
        
        st.markdown("---")
        st.write(f"📉 **Se venduto in un lotto con lo sconto del {percentuale_sconto}%:**")
        st.write(f"• Prezzo finale al compratore: **{prezzo_scontato_lotto:.2f} €**")
        st.write(f"• Tuo guadagno pulito sul pezzo: **{guadagno_lotto:.2f} €**")
        
        if guadagno_lotto <= 0:
            st.error("⚠️ Attenzione: Con questo sconto lotto vai in perdita o guadagni 0€!")
        else:
            st.success("✅ Margine di guadagno sicuro.")

# ==========================================
# TAB 4: TREND
# ==========================================
with tab4:
    st.header("I Trend di Mercato su Vinted")
    trend_data = [
        {"Categoria": "Streetwear", "Brand Più Cercati": "Nike, Adidas, Stüssy", "Prezzo Medio Vendita": "25€ - 60€", "Richiesta": "🔥 Altissima"}
    ]
    st.dataframe(pd.DataFrame(trend_data), use_container_width=True)
