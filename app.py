import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
from PIL import Image, ImageOps

# Configurazione globale della pagina in modalità Wide (schermo intero)
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# Intestazione principale dell'applicazione
st.title("🛍️ Vinted Power Seller Suite")
st.write("Gestisci, ottimizza e scala il tuo business di reselling su Vinted.")

# ==========================================
# CREAZIONE DELLE 4 SCHEDE DI GESTIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Ottimizzatore Foto", 
    "📝 Generatore Descrizioni AI", 
    "💰 Calcolatore Prezzi & Lotti", 
    "📊 Trend & Ricerca Rapida"
])

# ==========================================
# TAB 1: OTTIMIZZATORE FOTO (LEGGERO E SICURO)
# ==========================================
with tab1:
    st.header("📸 Studio Fotografico & Anteprima Sfondi")
    st.write("Carica la foto del tuo capo per ottimizzarla, ritagliarla visivamente o prepararla per i migliori siti di rimozione sfondo automatici.")

    col_foto1, col_foto2 = st.columns(2, gap="large")
    
    with col_foto1:
        st.markdown("### 1️⃣ Carica il tuo capo")
        uploaded_file = st.file_uploader("Trascina o seleziona la foto del tuo vestito", type=["jpg", "jpeg", "png"])
        
        st.markdown("### 🛠️ Strumenti di Rimozione Rapida Esterni")
        st.info("💡 Se vuoi rimuovere lo sfondo a livello professionale in 1 secondo senza rallentare questa app, usa questi fantastici strumenti gratuiti:")
        st.link_button("✂️ Rimuovi Sfondo con Adobe Express (Gratis)", "https://www.adobe.com/express/feature/image/remove-background", use_container_width=True)
        st.link_button("✨ Rimuovi Sfondo con Photoroom Web", "https://www.photoroom.com/tools/background-remover", use_container_width=True)

    with col_foto2:
        st.markdown("### 2️⃣ Anteprima e Regolazioni")
        if uploaded_file is not None:
            try:
                # Carica l'immagine in modo sicuro
                img = Image.open(uploaded_file)
                
                # Controlli di editing base (luminosità / specchio) per migliorare lo scatto originale
                st.write("📐 **Migliora lo scatto per Vinted:**")
                ruota = st.checkbox("Capovolgi/Specchia l'immagine horizontalmente")
                
                if ruota:
                    img = ImageOps.mirror(img)
                
                st.image(img, caption="Foto ottimizzata pronta per il caricamento", use_container_width=True)
                
                # Bottone di salvataggio locale della foto modificata
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=95)
                st.download_button(
                    label="📥 Scarica Foto Ottimizzata",
                    data=buffer.getvalue(),
                    file_name="capo_ottimizzato_vinted.jpg",
                    mime="image/jpeg"
                )
            except Exception as e:
                st.error(f"Errore nel caricamento dell'immagine: {e}")
        else:
            st.info("👋 Carica un file a sinistra per visualizzare l'editor e le opzioni di ottimizzazione.")

# ==========================================
# TAB 2: GENERATORE DESCRIZIONI AI
# ==========================================
with tab2:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    st.write("Compila i campi velocemente per generare una descrizione magnetica e formattata che attira i compratori su Vinted.")

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        brand = st.text_input("Brand / Marca del capo", value="Off-White")
        tipo_capo = st.text_input("Tipo di articolo", value="T-shirt corta")
        colore = st.text_input("Colore principale", value="Bianco con stampa rossa")
        
        st.markdown("### 📏 Taglia e Misure")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"], index=3)
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Oversize / Baggy", "Regolare (True to size)", "Slim fit / Stretto"])
        
        col_cm1, col_cm2 = st.columns(2)
        with col_cm1:
            cm_ascelle = st.text_input("Ascella - Ascella (cm)", placeholder="Es. 56")
        with col_cm2:
            cm_lunghezza = st.text_input("Lunghezza totale (cm)", placeholder="Es. 74")
            
        st.markdown("### 🎚️ Stato del capo")
        condizioni = st.selectbox("Condizioni del capo", ["Ottime condizioni (indossato pochissimo)", "Nuovo con cartellino", "Nuovo senza cartellino", "Buone condizioni"])
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
Vendo splendida {tipo_capo.lower()} originale del brand {brand.capitalize()}. Il capo è stato trattato con massima cura, lavato, igienizzato e pronto da indossare.

• 🎨 Colore: {colore.capitalize()}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
{stringa_misure}• 💎 Condizioni: {condizioni}
{nota_difetti}

Spedisco velocemente entro 24 ore dal pagamento 📦. Scrivimi pure in privato per qualsiasi domanda o foto extra! 📲

---
Tag per algoritmo:
#{brand.lower()} #{tipo_capo.replace(' ', '').lower()} #{colore.split()[0].lower()} #taglia{taglia.lower()} #vintedvintage #streetwear #reselling
"""
        st.text_input("📌 Titolo dell'annuncio:", titolo_generato)
        st.text_area("📄 Descrizione dell'annuncio (Copia e Incolla su Vinted):", descrizione_generata, height=350)

# ==========================================
# TAB 3: CALCOLATORE PREZZI & LOTTI
# ==========================================
with tab3:
    st.header("💰 Controllo Margini e Analisi del Profitto")
    st.write("Questa dashboard analizza la struttura dei costi e dei guadagni per darti una visione finanziaria chiara del tuo business.")

    col_input, col_chart = st.columns([1.5, 2.5], gap="large")

    with col_input:
        st.markdown("### 📊 Controlli del Capo")
        costo_acquisto = st.number_input("💰 Quanto hai pagato il capo? (€)", min_value=0.0, value=10.0, format="%.2f")
        prezzo_vendita = st.number_input("🏷️ A quanto vuoi venderlo su Vinted? (€)", min_value=costo_acquisto, value=35.0, format="%.2f")
        st.markdown("### 🏬 Simulatore Pacchetti")
        percentuale_sconto = st.slider("Se un utente crea un lotto, che sconto vuoi applicare? (%)", 0, 50, 15)

    with col_chart:
        guadagno_netto = prezzo_vendita - costo_acquisto
        roi = (guadagno_netto / costo_acquisto) * 100 if costo_acquisto > 0 else 0
        prezzo_scontato_lotto = prezzo_vendita * (1 - (percentuale_sconto / 100))
        guadagno_lotto = prezzo_scontato_lotto - costo_acquisto

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
        data_fin = pd.DataFrame({
            'Category': ['Costo di Acquisto', 'Guadagno Netto'], 
            'Value': [costo_acquisto, guadagno_netto]
        })

        base = alt.Chart(data_fin).encode(theta=alt.Theta("Value", stack=True))
        donut = base.mark_arc(innerRadius=50, outerRadius=90).encode(
            color=alt.Color("Category", scale=alt.Scale(range=['#FFD700', '#228B22']), legend=alt.Legend(orient="bottom"))
        ).properties(width='container', height=200)
        
        st.altair_chart(donut, use_container_width=True)

# ==========================================
# TAB 4: TREND & RICERCA RAPIDA
# ==========================================
with tab4:
    st.header("📊 I Trend di Mercato Caldi & Ricerca Automatica")
    st.write("Analizza la nicchia più redditizia del momento, poi usa i link rapidi per cercare stock ed errori di prezzo su Vinted.")

    trend_data = [
        {"Categoria": "👟 Sneakers Hype", "Brand Più Cercati": "Nike TN, Jordan 4, Adidas Campus", "Prezzo d'acquisto target": "< 40€", "Velocità di Vendita": "⚡ Istantanea"},
        {"Categoria": "🧥 Gorpcore & Outerwear", "Brand Più Cercati": "The North Face, Arc'teryx, Carhartt WIP", "Prezzo d'acquisto target": "< 50€", "Velocità di Vendita": "🔥 Molto Alta"},
        {"Categoria": "👖 Denim Premium & Baggy", "Brand Più Cercati": "Levi's 501 / 550, Polar Skate Big Boy", "Prezzo d'acquisto target": "< 15€", "Velocità di Vendita": "✅ Alta"}
    ]
    
    st.dataframe(pd.DataFrame(trend_data), use_container_width=True)
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.link_button("👟 Cerca Scarpe Nike (<40€) su Vinted", "https://www.vinted.it/catalog?search_text=nike&price_to=40&order=newest_first", use_container_width=True)
    with col_btn2:
        st.link_button("🛍️ Cerca Stüssy (Ultimi Arrivi) su Vinted", "https://www.vinted.it/catalog?search_text=stussy&order=newest_first", use_container_width=True)
