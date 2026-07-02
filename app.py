import streamlit as st
import pandas as pd
import altair as alt
import io
from PIL import Image

# Configurazione Pagina
st.set_page_config(page_title="Vinted Pro Manager", layout="wide")

# --- GESTIONE DATABASE LOCALE (Session State) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=[
        "ID", "Prodotto", "Brand", "Costo (€)", "Prezzo Vendita (€)", "Stato"
    ])

def add_to_inventory(item, brand, cost, price):
    new_entry = pd.DataFrame([[len(st.session_state.inventory)+1, item, brand, cost, price, "In Vendita"]], 
                             columns=st.session_state.inventory.columns)
    st.session_state.inventory = pd.concat([st.session_state.inventory, new_entry], ignore_index=True)

# --- SIDEBAR: NAVIGAZIONE E STATISTICHE ---
st.sidebar.title("📈 Dashboard Venditore")
st.sidebar.metric("Articoli in inventario", len(st.session_state.inventory))
if not st.session_state.inventory.empty:
    st.sidebar.metric("Investimento Totale", f"{st.session_state.inventory['Costo (€)'].sum():.2f} €")

# --- INTERFACCIA PRINCIPALE ---
st.title("🛍️ Vinted Pro Seller Suite")

tab1, tab2, tab3 = st.tabs(["📋 Gestione Inventario", "📝 Generatore Annunci", "📊 Analisi & Trend"])

with tab1:
    st.header("Il tuo Magazzino")
    with st.expander("➕ Aggiungi nuovo articolo"):
        c1, c2, c3, c4 = st.columns(4)
        prod = c1.text_input("Prodotto")
        brand = c2.text_input("Brand")
        cost = c3.number_input("Costo Acquisto", min_value=0.0)
        price = c4.number_input("Prezzo Vendita", min_value=0.0)
        if st.button("Salva nel Magazzino"):
            add_to_inventory(prod, brand, cost, price)
            st.success("Articolo salvato!")
    
    st.dataframe(st.session_state.inventory, use_container_width=True)

with tab2:
    st.header("Generatore Annunci AI")
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        input_brand = st.text_input("Marca")
        input_tipo = st.text_input("Articolo")
        input_cond = st.selectbox("Condizioni", ["Nuovo", "Ottimo", "Buono"])
        input_taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL"])
        
    with col_r:
        if st.button("Genera Descrizione"):
            desc = f"""🇮🇹 Vendo {input_tipo} {input_brand} - {input_cond}
            
✨ Articolo in perfette condizioni, taglia {input_taglia}. 
Vendo per inutilizzo, spedizione ultra rapida in 24h. 📦

#vinted #vintage #reselling #{input_brand.lower()} #{input_tipo.lower()}"""
            st.text_area("Copia questo testo:", desc, height=200)

with tab3:
    st.header("Analisi Performance")
    if not st.session_state.inventory.empty:
        df = st.session_state.inventory
        df['Profitto'] = df['Prezzo Vendita (€)'] - df['Costo (€)']
        
        c_a, c_b = st.columns(2)
        with c_a:
            st.subheader("Profitti per Articolo")
            chart = alt.Chart(df).mark_bar().encode(
                x='Prodotto',
                y='Profitto',
                color=alt.condition(alt.datum.Profitto > 0, alt.value('green'), alt.value('red'))
            )
            st.altair_chart(chart, use_container_width=True)
        
        with c_b:
            st.write("Statistiche rapide:")
            st.write(f"Profitto medio atteso: {df['Profitto'].mean():.2f} €")
    else:
        st.info("Aggiungi articoli all'inventario per vedere le statistiche.")

st.markdown("---")
st.caption("Vinted Pro Suite - Gestisci il tuo business con intelligenza.")
