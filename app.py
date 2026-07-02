import streamlit as st
import pandas as pd
import altair as alt
import io
from PIL import Image
from rembg import remove
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Vinted Pro Suite", layout="wide")

# --- DATABASE ---
Base = declarative_base()
engine = create_engine('sqlite:///vinted_master.db')
Session = sessionmaker(bind=engine)

class InventoryItem(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String)
    tipo = Column(String)
    costo = Column(Float)
    prezzo = Column(Float)
    profitto = Column(Float)

Base.metadata.create_all(engine)

# --- MODULI ---

def show_ai_studio():
    st.header("📸 AI Studio")
    upload = st.file_uploader("Carica foto per rimuovere sfondo", type=["jpg", "png"])
    if upload:
        if st.button("Elabora"):
            img = Image.open(upload).convert("RGBA")
            img_no_bg = remove(img)
            st.image(img_no_bg, caption="Sfondo rimosso")

def show_seo():
    st.header("📝 Generatore SEO")
    with st.form("seo_form"):
        brand = st.text_input("Brand")
        tipo = st.text_input("Tipo")
        if st.form_submit_button("Genera"):
            st.code(f"✨ VENDO: {tipo.upper()} {brand.upper()} - Ottime condizioni #vinted #secondhand")

def show_finance():
    st.header("💰 Gestione Finanziaria")
    with st.form("fin_form"):
        brand = st.text_input("Brand")
        costo = st.number_input("Costo", step=0.50)
        prezzo = st.number_input("Prezzo", step=1.00)
        if st.form_submit_button("Salva"):
            profitto = prezzo - costo
            session = Session()
            item = InventoryItem(brand=brand, costo=costo, prezzo=prezzo, profitto=profitto)
            session.add(item)
            session.commit()
            session.close()
            st.success("Salvataggio avvenuto!")

def show_magazzino():
    st.header("📦 Magazzino")
    session = Session()
    df = pd.read_sql(session.query(InventoryItem).statement, session.bind)
    session.close()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.write("Magazzino vuoto.")

def show_analytics():
    st.header("📈 Analisi Profitti")
    session = Session()
    df = pd.read_sql(session.query(InventoryItem).statement, session.bind)
    session.close()
    if not df.empty:
        chart = alt.Chart(df).mark_bar().encode(x='brand', y='profitto')
        st.altair_chart(chart, use_container_width=True)

# --- MAIN ---
menu = {
    "📸 AI Studio": show_ai_studio,
    "📝 SEO": show_seo,
    "💰 Finanza": show_finance,
    "📦 Magazzino": show_magazzino,
    "📈 Analisi": show_analytics
}

scelta = st.sidebar.radio("Menu", list(menu.keys()))
menu[scelta]()
