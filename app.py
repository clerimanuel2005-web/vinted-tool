import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
from PIL import Image

# Configurazione globale della pagina
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Generatore Catalogo AI", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: GENERATORE CATALOGO AI (100% GRATIS)
# ==========================================
with tab1:
    st.header("🤖 Studio Fotografico AI Gratuito")
    st.write("Inserisci i dettagli del capo per generare una foto perfetta, stirata e ambientata senza bisogno di chiavi a pagamento.")

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        brand_input = st.text_input("Marca del vestito da ricreare:", value="Off-White")
        colore_input = st.text_input("Colore del tessuto:", value="Bianco puro")
    with col_in2:
        dettagli_stampa = st.text_area("Descrivi la stampa/logo sul vestito:", 
                                       value="La classica grande freccia Off-White sul retro, riempita all'interno con un pattern di baci e labbra stampate in rosso.")

    opzione_ambientazione = st.selectbox(
        "Scegli dove posizionare e ambientare il vestito:",
        [
            "indossata da un manichino invisibile (effetto ghost mannequin) in uno studio fotografico con luci professionali e sfondo grigio chiaro minimale",
            "appesa a una gruccia di legno minimalista dentro uno showroom di lusso con sfondo sfocato e luci calde",
            "disposta perfettamente in piano (flat lay) su un pavimento di marmo bianco lucido da boutique"
        ]
    )

    if st.button("✨ Genera Foto Professionale Gratis", type="primary"):
        with st.spinner("L'AI sta creando il manichino e stirando il tessuto... Attendi qualche secondo."):
            try:
                # Prompt per guidare il modello FLUX
                prompt_scena = f"A high-end professional commercial product photography of a {colore_input.lower()} t-shirt by {brand_input}, perfectly ironed, wrinkle-free, {dettagli_stampa.lower()}. The t-shirt is {opzione_ambientazione}, 8k resolution, photorealistic, cinematic lighting, ultra detailed, retail catalog style."
                
                # API Endpoint pubblico di Hugging Face (Modello FLUX)
                API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
                response = requests.post(API_URL, json={"inputs": prompt_scena}, timeout=60)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    
                    st.subheader("✅ Foto da Catalogo Generata")
                    st.image(image, caption="Foto generata senza pieghe pronta per Vinted", use_container_width=True)
                    
                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG")
                    st.download_button(
                        label="📥 Scarica Foto per Vinted",
                        data=buffer.getvalue(),
                        file_name="vestito_catalogo_ai.jpg",
                        mime="image/jpeg"
                    )
                    st.success("Immagine creata con successo in modo gratuito!")
                else:
                    st.error("I server di generazione gratuiti sono momentaneamente carichi. Attendi 5 secondi e riclicca il pulsante.")
            except Exception as e:
                st.error(f"Errore di generazione: {e}")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI (POTENZIATO)
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    st.write("Compila i campi velocemente per generare una descrizione magnetica che attira i compratori.")

    col_a, col_b = st.columns(2)
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="Puma")
        tipo_capo = st.text_input("Tipo di articolo", value="Felpa con cappuccio")
        colore = st.text_input("Colore principale", value="Bianco con scritte nere")
        
        st.markdown("### 📏 Taglia e Misure")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        with col_t2:
            vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare (True to size)", "Oversize / Baggy", "Slim fit / Stretto"])
        
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1:
            cm_ascelle = st.text_input("Ascella - Ascella (cm)", placeholder="Es. 54")
        with col_cm2:
            cm_lunghezza = st.text_input("Lunghezza totale (cm)", placeholder="Es. 70")
        
        st.markdown("### 🎚️ Stato del capo")
        condizioni = st.selectbox("Condizioni del capo", [
            "Ottime condizioni (indossato pochissimo, nessun difetto)",
            "Nuovo con cartellino", 
            "Nuovo senza cartellino", 
            "Buone condizioni (normali segni di usura)",
            "Soddisfacente (presenta piccoli difetti specificati)"
        ])
        difetti = st.text_input("Note o piccoli difetti (opzionale)", value="nessuna")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        
        titolo_generato = f"✨ {tipo_capo.capitalize()} {brand.upper()} - Taglia {taglia} - {colore.capitalize()}"
        nota_difetti = f"• 🔎 Difetti: {difetti.capitalize()}" if difetti and difetti.lower() != "nessuna" else "• 🔎 Difetti: Nessuno, capo perfetto."
        
        stringa_misure = ""
        if cm_ascelle or cm_lunghezza:
            stringa_misure = "• 📐 Misure piatte:\n"
            if cm_ascelle:
                stringa_misure += f"   - Pit to Pit (Ascella-Ascella): {cm_ascelle} cm\n"
            if cm_lunghezza:
                stringa_misure += f"   - Lunghezza totale: {cm_lunghezza} cm\n"

        descrizione_generata = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo bellissima {tipo_capo.lower()} originale del brand {brand.capitalize()}. Il capo è stato trattato con massima cura, lavato e igienizzato.

• 🎨 Colore: {colore.capitalize()}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedisco velocemente entro 24 ore dal pagamento 📦. Se hai domande o vuoi fare un'offerta (sensata), scrivimi pure in privato! 📲

---
Tag per algoritmo:
#{brand.lower()} #{tipo_capo.replace(' ', '').lower()} #{colore.split()[0].lower()} #taglia{taglia.lower()} #vintedvintage #streetwear #reselling
"""
        st.text_input("📌 Titolo dell'annuncio:", titolo_generato)
        st.text_area("📄 Descrizione dell'annuncio (Copia e Incolla su Vinted):", descrizione_generata, height=400)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI (PROFESSIONALE)
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi del Profitto")
    st.write("Questa dashboard analizza la struttura dei costi e dei guadagni per darti una visione finanziaria chiara del tuo business.")

    # Layout a due colonne principali
    col_input, col_chart = st.columns([1.5, 2.5], gap="large")

    with col_input:
        st.markdown("### 📊 Controlli del Capo")
        
        costo_acquisto = st.number_input(
            "💰 Quanto hai pagato il capo? (€)", 
            min_value=0.0, 
            value=10.0, 
            step=1.0, 
            format="%.2f"
        )
        
        prezzo_vendita = st.number_input(
            "🏷️ A quanto vuoi venderlo su Vinted? (€)", 
            min_value=costo_acquisto, 
            value=35.0, 
            step=1.0, 
            format="%.2f"
        )

        st.markdown("### 🏬 Simulatore Pacchetti")
        percentuale_sconto = st.slider("Se un utente crea un lotto, che sconto vuoi applicare? (%)", 0, 50, 15)

    with col_chart:
        # Calcoli Finanziari
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = 0.0
        if costo_acquisto > 0:
            roi = (guadagno_netto / costo_acquisto) * 100
        
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - costo_acquisto

        # Visualizzazione Metriche KPI
        st.markdown("### 🏬 Analisi Finanziaria Istantanea")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="🤑 Guadagno Netto", value=f"{guadagno_netto:.2f} €")
        with m_col2:
            st.metric(label="📈 ROI %", value=f"{roi:.1f}%")
        with m_col3:
            st.metric(label="🔄 Moltiplicatore", value=f"x{roi/100:.2f}")

        st.markdown("---")
        st.write(f"📉 **Se venduto in un lotto con lo sconto del {percentuale_sconto}%:**")
        st.write(f"• Prezzo finale al compratore: **{prezzo_scontato_lotto:.2f} €**")
        st.write(f"• Tuo guadagno pulito sul pezzo: **{guadagno_lotto:.2f} €**")
        st.markdown("---")
        
        st.subheader("🥧 Struttura del Guadagno (Donut Chart)")
        
        # DataFrame per il grafico
        data_fin = pd.DataFrame({
            'Category': ['Costo di Acquisto', 'Guadagno Netto'],
            'Value': [costo_acquisto, guadagno_netto]
        })

        # Costruzione del grafico ad anello con Altair
        base = alt.Chart(data_fin).encode(theta=alt.Theta("Value", stack=True))

        donut = base.mark_arc(innerRadius=50, outerRadius=90).encode(
            color=alt.Color(
                "Category", 
                title=None, 
                scale=alt.Scale(range=['#FFD700', '#228B22']), 
                legend=alt.Legend(orient="bottom", titleFontSize=13, labelFontSize=12)
            ),
            order=alt.Order("Value", sort="descending"),
            tooltip=["Category", alt.Tooltip("Value", format=".2f")]
        ).properties(
            width='container',
            height=220
        )
        
        text = base.mark_text(radius=110, fontSize=13).encode(
            text=alt.Text("Value", format=".2f"),
            order=alt.Order("Value", sort="descending"),
            color=alt.value("white")
        )

        st.altair_chart(donut + text, use_container_width=True)

# ==========================================
# TAB 4: TREND & RICERCA RAPIDA
# ==========================================
with tab4:
    st.header("📊 I Trend di Mercato Caldi & Ricerca Automatica")
    st.write("Analizza la nicchia più redditizia del momento, poi clicca sul pulsante per cercarla direttamente su Vinted in un clic.")

    trend_data = [
        {"Categoria": "👟 Sneakers Hype", "Brand Più Cercati": "Nike TN, Jordan 4, Adidas Campus, New Balance 2002R", "Prezzo d'acquisto target": "< 40€", "Prezzo Vendita Medio": "70€ - 130€", "Velocità di Vendita": "⚡ Istantanea (Meno di 24 ore)"},
        {"Categoria": "🧥 Gorpcore & Outerwear", "Brand Più Cercati": "The North Face (Nuptse), Arc'teryx, Patagonia, Carhartt WIP", "Prezzo d'acquisto target": "< 50€", "Prezzo Vendita Medio": "90€ - 160€", "Velocità di Vendita": "🔥 Molto Alta (1-2 giorni)"},
        {"Categoria": "🛍️ Streetwear & Vetrate Grafiche", "Brand Più Cercati": "Stüssy, Corteiz, Supreme, Travis Scott Merch", "Prezzo d'acquisto target": "< 20€", "Prezzo Vendita Medio": "45€ - 80€", "Velocità di Vendita": "🔥 Molto Alta (24-48 ore)"},
        {"Categoria": "👖 Denim Premium & Baggy", "Brand Più Cercati": "Levi's 501 / 550, Polar Skate Big Boy, Carhartt Double Knee", "Prezzo d'acquisto target": "< 15€", "Prezzo Vendita Medio": "35€ - 70€", "Velocità di Vendita": "✅ Alta (2-3 giorni)"},
        {"Categoria": "🧢 Accessori & Vintage Y2K", "Brand Più Cercati": "Oakley Sunglasses, Diesel, Von Dutch, Ed Hardy", "Prezzo d'acquisto target": "< 10€", "Prezzo Vendita Medio": "25€ - 55€", "Velocità di Vendita": "✅ Media (3-4 giorni)"}
    ]
    
    df = pd.DataFrame(trend_data)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔍 Azioni Veloci: Cerca Stock ed Errori di Prezzo su Vinted")

    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        url_nike = "https://www.vinted.it/catalog?search_text=nike&price_to=40&order=newest_first"
        st.link_button("👟 Cerca Scarpe Nike (<40€)", url_nike, use_container_width=True)

    with col_btn2:
        url_stussy = "https://www.vinted.it/catalog?search_text=stussy&order=newest_first"
        st.link_button("🛍️ Cerca Stüssy (Ultimi Arrivi)", url_stussy, use_container_width=True)

    with col_btn3:
        url_tnf = "https://www.vinted.it/catalog?search_text=the+north+face+giacca&order=newest_first"
        st.link_button("🧥 Cerca Giacche TNF", url_tnf, use_container_width=True)

    with col_btn4:
        url_levis = "https://www.vinted.it/catalog?search_text=levis+501&price_to=20&order=newest_first"
        st.link_button("👖 Cerca Levi's 501 (<20€)", url_levis, use_container_width=True)
