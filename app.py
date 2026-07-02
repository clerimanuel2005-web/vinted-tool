import streamlit as st
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Vinted Pro Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Pro Seller Suite")
st.write("Strumento completo per copywriter, gestione margini e monitoraggio trend.")

tab1, tab2, tab3 = st.tabs(["📝 Generatore Annunci", "💰 Calcolo Margini", "📊 Trend & Link Vinted"])

# --- TAB 1: GENERATORE DESCRIZIONI ---
with tab1:
    st.header("📝 Scrittura Automatica Annunci Vinted")
    col_a, col_b = st.columns(2, gap="large")
    
    with col_a:
        brand = st.text_input("Brand / Marca del capo")
        tipo_capo = st.text_input("Tipo di articolo")
        colore = st.text_input("Colore e dettagli visivi")
        taglia = st.selectbox("Taglia ufficiale", ["XS", "S", "M", "L", "XL", "XXL"])
        vestibilita = st.selectbox("Vestibilità (Fit)", ["Regolare", "Oversize / Baggy", "Slim fit"])
        condizioni = st.selectbox("Condizioni", ["Nuovo con cartellino", "Nuovo senza cartellino", "Ottime", "Buone"])
        difetti = st.text_input("Note difetti (lascia vuoto se perfetto)")

    with col_b:
        st.subheader("📋 Testo Pronto da Copiare")
        descrizione = f"""🇮🇹 DESCRIZIONE ARTICOLO:
Vendo {tipo_capo} del brand {brand}.

• 🎨 Colore: {colore}
• 📏 Taglia: {taglia}
• 📈 Vestibilità: {vestibilita}
• 💎 Condizioni: {condizioni}
• 🔎 Difetti: {difetti if difetti else "Nessuno, capo perfetto."}

Spedisco rapidamente entro 24 ore 📦. Scrivimi pure per info o ulteriori foto! 📲

---
#{brand.replace(' ', '').lower()} #{tipo_capo.replace(' ', '').lower()} #taglia{taglia.lower()} #streetwear #reselling
"""
        st.text_area("Copia questo testo per Vinted:", descrizione, height=350)

# --- TAB 2: CALCOLO MARGINI ---
with tab3:
    pass # Spostato sotto per logica

with tab2:
    st.header("💰 Gestione Finanziaria e Margini")
    c1, c2 = st.columns(2)
    costo = c1.number_input("Costo di acquisto (€)", min_value=0.0, value=0.0, format="%.2f")
    prezzo = c2.number_input("Prezzo di vendita (€)", min_value=0.0, value=0.0, format="%.2f")
    sconto = st.slider("Sconto lotti (%)", 0, 50, 15)
    
    if prezzo > 0:
        guadagno = prezzo - costo
        roi = (guadagno / costo) * 100 if costo > 0 else 0
        
        st.markdown("### 📊 Analisi Profitto")
        st.table(pd.DataFrame({
            "Metrica": ["Ricavo Lordo", "Costo", "Margine Netto", "ROI %"],
            "Valore": [f"{prezzo:.2f} €", f"{costo:.2f} €", f"{guadagno:.2f} €", f"{roi:.1f}%"]
        }))
        
        st.markdown("### 📉 Simulazione Sconto Lotti")
        st.table(pd.DataFrame({
            "Scenario": ["Vendita Singola", f"Vendita in Lotto (-{sconto}%)"],
            "Prezzo Finale": [f"{prezzo:.2f} €", f"{prezzo*(1-sconto/100):.2f} €"],
            "Margine": [f"{guadagno:.2f} €", f"{prezzo*(1-sconto/100)-costo:.2f} €"]
        }))

# --- TAB 3: TREND E LINK VINTED ---
with tab3:
    st.header("🔥 Market Intelligence e Ricerca Vinted")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("### 🚀 Link Rapidi alle Occasioni")
        st.markdown("- [👟 Sneakers Nuovo - Prezzo Crescente](https://www.vinted.it/catalog?order=price_asc&status[]=6&catalog[]=1084)")
        st.markdown("- [👕 Streetwear in Tendenza](https://www.vinted.it/catalog?order=newest_first&brand_id[]=1355&brand_id[]=96)")
        st.markdown("- [💰 Capi Lusso sotto i 50€](https://www.vinted.it/catalog?order=price_asc&price_to=50)")
        st.markdown("- [📦 Cerca 'Stock' o 'Lotto'](https://www.vinted.it/catalog?search_text=lotto)")

    with col_t2:
        st.markdown("### 📊 Analisi Categorie")
        st.dataframe(pd.DataFrame({
            "Categoria": ["Streetwear", "Vintage Sport", "Workwear"],
            "Liquidità": ["Alta", "Alta", "Media"],
            "Trend": ["Crescente", "Stabile", "Stabile"]
        }), use_container_width=True)

    st.markdown("### 🛡️ Guida Sicurezza (Prevenzione Truffe)")
    st.table(pd.DataFrame({
        "Brand a Rischio": ["High-End", "Sportivo", "Lusso"],
        "Azione Consigliata": ["Richiedi sempre ricevuta", "Verifica etichette interne", "Usa autenticazione Vinted"]
    }))
