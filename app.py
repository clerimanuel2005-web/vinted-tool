import streamlit as st
import pandas as pd

# Configurazione della pagina del sito
st.set_page_config(page_title="Vinted Speed Seller Online", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Speed Seller Tool")
st.write("Il tuo braccio destro per vendere su Vinted al triplo della velocità!")

# Creazione delle schede (Tabs) sul sito
tab1, tab2 = st.tabs(["📸 Ottimizzatore Foto AI Gratis", "📊 Trend di Vendita del Mese"])

# ==========================================
# TAB 1: OTTIMIZZATORE FOTO 
# ==========================================
with tab1:
    st.header("Sistemazione Foto Istantanea")
    st.write("Per evitare rallentamenti e garantirti il risultato migliore senza pagare, usa i due step qui sotto:")
    
    st.markdown("""
    ### 1️⃣ Step 1: Rimuovi lo sfondo in 2 secondi
    Clicca sul link qui sotto per usare il tool AI numero uno al mondo. Trascina la foto del tuo vestito stropicciato e scarica la versione con lo sfondo bianco perfetto da studio:
    """)
    
    # Pulsante accattivante per andare a rimuovere lo sfondo gratis
    st.link_button("✨ Rimuovi Sfondo Gratis con AI", "https://www.photoroom.com/it/strumenti/rimuovere-sfondo-delle-foto", type="primary")
    
    st.markdown("""
    ---
    ### 2️⃣ Step 2: I trucchi per far sembrare il vestito come nuovo (Stirato)
    Quando ricarichi la foto pulita su Vinted, l'algoritmo premia la nitidezza. Segui queste regole d'oro direttamente nell'editor di Vinted:
    * **Luminosità al +15%:** Spariscono le ombre delle pieghe della maglietta stropicciata.
    * **Contrasto al +10%:** I colori sembrano vivi e il tessuto sembra appena uscito dal negozio.
    * **Nitidezza al massimo:** Mette in risalto le trame del brand, attirando subito i compratori.
    """)

# ==========================================
# TAB 2: ANALISI TREND & RESELLING
# ==========================================
with tab2:
    st.header("I Trend di Mercato su Vinted")
    st.write("Questa tabella mostra gli articoli, i brand e le nicchie più calde del mese, con i margini di guadagno stimati per il reselling.")

    # Dati strutturati sui trend attuali di Vinted per il reselling
    trend_data = [
        {"Categoria": "Streetwear", "Brand Più Cercati": "Nike, Adidas, Stüssy, Carhartt", "Prezzo Medio Vendita": "25€ - 60€", "Richiesta su Vinted": "🔥 Altissima", "Velocità di Vendita": "Meno di 48 ore"},
        {"Categoria": "Y2K / Vintage Anni 2000", "Brand Più Cercati": "Diesel, Von Dutch, Juicy Couture", "Prezzo Medio Vendita": "20€ - 50€", "Richiesta su Vinted": "🔥 Alta", "Velocità di Vendita": "1-3 giorni"},
        {"Categoria": "Giacche / Outerwear", "Brand Più Cercati": "The North Face, Patagonia, Arc'teryx", "Prezzo Medio Vendita": "50€ - 120€", "Richiesta su Vinted": "🔥 Alta", "Velocità di Vendita": "2-4 giorni"},
        {"Categoria": "Scarpe & Sneakers", "Brand Più Cercati": "Nike Jordan 1, Adidas Campus, New Balance 550", "Prezzo Medio Vendita": "40€ - 90€", "Richiesta su Vinted": "🔥 Altissima", "Velocità di Vendita": "Meno di 24 ore"},
        {"Categoria": "Accessori di Lusso (Fascia Media)", "Brand Più Cercati": "Michael Kors, Guess, Vivienne Westwood", "Prezzo Medio Vendita": "35€ - 80€", "Richiesta su Vinted": "Medium", "Velocità di Vendita": "3-5 giorni"},
        {"Categoria": "Denim / Jeans", "Brand Più Cercati": "Levi's (Modelli 501 / 550)", "Prezzo Medio Vendita": "15€ - 35€", "Richiesta su Vinted": "🔥 Alta", "Velocità di Vendita": "1-2 giorni"}
    ]
    
    df = pd.DataFrame(trend_data)
    
    # Mostra la tabella
    st.dataframe(df, use_container_width=True)
    
    st.info("💡 **Consiglio per guadagnare:** Cerca questi brand su Vinted impostando il filtro 'Prezzo decrescente' o cercando lotti di vestiti a poco prezzo, ripulisci la foto e rivendili singolarmente seguendo i prezzi della tabella!")
