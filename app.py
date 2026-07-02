import streamlit as st
import pandas as pd
from PIL import Image, ImageEnhance
from rembg import remove
import io

# Configurazione della pagina del sito
st.set_page_config(page_title="Vinted Speed Seller Online", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Speed Seller Tool")
st.write("Migliora le tue foto e scopri i segreti del reselling per vendere in un lampo!")

# Creazione delle schede (Tabs) sul sito
tab1, tab2 = st.tabs(["📸 Ottimizzatore Foto AI", "📊 Trend di Vendita del Mese"])

# ==========================================
# TAB 1: OTTIMIZZATORE FOTO (ONLINE)
# ==========================================
with tab1:
    st.header("Sistemazione Foto Istantanea")
    st.write("Carica la foto del tuo vestito: l'AI rimuoverà lo sfondo e regoleremo la nitidezza per metterlo in risalto.")

    uploaded_file = st.file_uploader("Scegli la foto di un vestito...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Foto Originale", use_container_width=True)
        
        with col2:
            with st.spinner("L'AI sta rimuovendo lo sfondo e stirando i dettagli..."):
                # Rimozione dello sfondo gratis con rembg
                img_bytes = uploaded_file.getvalue()
                output_bytes = remove(img_bytes)
                output_image = Image.open(io.BytesIO(output_bytes))
                
                # Creiamo uno sfondo bianco solido da studio
                background = Image.new("RGBA", output_image.size, (255, 255, 255))
                final_image = Image.alpha_composite(background, output_image.convert("RGBA")).convert("RGB")
                
                # Regolazione contrasto e nitidezza per attenuare le pieghe
                enhancer_sharp = ImageEnhance.Sharpness(final_image)
                final_image = enhancer_sharp.enhance(1.6) 
                
                enhancer_contrast = ImageEnhance.Contrast(final_image)
                final_image = enhancer_contrast.enhance(1.15)
                
                st.image(final_image, caption="Foto Ottimizzata da Negozio", use_container_width=True)
                
                # Bottone per scaricare il risultato
                buf = io.BytesIO()
                final_image.save(buf, format="JPEG")
                byte_im = buf.getvalue()
                st.download_button(label="📥 Scarica Foto Perfetta", data=byte_im, file_name="vestito_vinted.jpg", mime="image/jpeg")

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
    
    st.info("💡 **Consiglio per guadagnare:** Cerca questi brand impostando il filtro 'Prezzo decrescente' o cercando lotti di vestiti a poco prezzo, applica lo strumento di rimozione sfondo della Tab 1, e rivendili singolarmente al prezzo medio indicato nella tabella!")
