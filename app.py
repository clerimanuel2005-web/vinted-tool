import streamlit as st
import pandas as pd

# Configurazione della pagina del sito
st.set_page_config(page_title="Vinted Speed Seller Online", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Speed Seller Tool")
st.write("Il tuo braccio destro per vendere su Vinted al triplo della velocità senza uscire da questa pagina!")

# Creazione delle schede (Tabs) sul sito
tab1, tab2 = st.tabs(["📸 Ottimizzatore Foto AI Diretto", "📊 Trend di Vendita del Mese"])

# ==========================================
# TAB 1: OTTIMIZZATORE FOTO INTERNO
# ==========================================
with tab1:
    st.header("Sistemazione Foto Istantanea")
    st.write("Trascina la foto del tuo vestito qui sotto: l'AI isolerà il prodotto inserendolo in uno sfondo perfetto da studio.")
    
    # Integrazione diretta del tool AI dentro la pagina tramite iframe HTML
    # Usiamo l'interfaccia ottimizzata di Photoroom integrata nel sito
    st.components.v1.html(
        """
        <iframe 
            src="https://www.photoroom.com/it/strumenti/rimuovere-sfondo-delle-foto" 
            width="100%" 
            height="650" 
            style="border:none; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);"
            allow="picture-in-picture"
            allowfullscreen>
        </iframe>
        """,
        height=660,
    )
    
    st.markdown("""
    ---
    ### 💡 Il Trucco del Venditore: Come simulare la stiratura
    Dopo aver ripulito lo sfondo nel box qui sopra e aver salvato la foto, caricala su Vinted e usa queste regolazioni rapide per camuffare le pieghe:
    * **Aumenta la Luminosità (+15%):** Rende lo sfondo ultra-bianco e "pialla" le ombre scure generate dalle pieghe del tessuto stropicciato.
    * **Aumenta il Contrasto (+10%):** Ravviva i colori sbiaditi, facendo sembrare il capo come nuovo.
    """)

# ==========================================
# TAB 2: ANALISI TREND & RESELLING
# ==========================================
with tab2:
    st.header("I Trend di Mercato su Vinted")
    st.write("Questa tabella mostra gli articoli, i brand e le nicchie più calde del mese, con i margini di guadagno stimati per il reselling.")

    trend_data = [
        {"Categoria": "Streetwear", "Brand Più Cercati": "Nike, Adidas, Stüssy, Carhartt", "Prezzo Medio Vendita": "25€ - 60€", "Richiesta su Vinted": "🔥 Altissima", "Velocità di Vendita": "Meno di 48 ore"},
        {"Categoria": "Y2K / Vintage Anni 2000", "Brand Più Cercati": "Diesel, Von Dutch, Juicy Couture", "Prezzo Medio Vendita": "20€ - 50€", "Richiesta su Vinted": "🔥 Alta", "Velocità di Vendita": "1-3 giorni"},
        {"Categoria": "Giacche / Outerwear", "Brand Più Cercati": "The North Face, Patagonia, Arc'teryx", "Prezzo Medio Vendita": "50€ - 120€", "Richiesta su Vinted": "🔥 Alta", "Velocità di Vendita": "2-4 giorni"},
        {"Categoria": "Scarpe & Sneakers", "Brand Più Cercati": "Nike Jordan 1, Adidas Campus, New Balance 550", "Prezzo Medio Vendita": "40€ - 90€", "Richiesta su Vinted": "🔥 Altissima", "Velocità di Vendita": "Meno di 24 ore"},
        {"Categoria": "Accessori di Lusso (Fascia Media)", "Brand Più Cercati": "Michael Kors, Guess, Vivienne Westwood", "Prezzo Medio Vendita": "35€ - 80€", "Richiesta su Vinted": "Medium", "Velocità di Vendita": "3-5 giorni"},
        {"Categoria": "Denim / Jeans", "Brand Più Cercati": "Levi's (Modelli 501 / 550)", "Prezzo Medio Vendita": "15€ - 35€", "Richiesta su Vinted": "🔥 Alta", "Velocità di Vendita": "1-2 giorni"}
    ]
    
    df = pd.DataFrame(trend_data)
    st.dataframe(df, use_container_width=True)
    
    st.info("💡 **Consiglio per guadagnare:** Cerca questi brand su Vinted impostando il filtro 'Prezzo decrescente' o cercando lotti di vestiti a poco prezzo, ripulisci la foto con il nostro tool nella Tab 1, e rivendili singolarmente seguendo i prezzi della tabella!")
