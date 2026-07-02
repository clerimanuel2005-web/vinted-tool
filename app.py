import streamlit as st
import pandas as pd
import altair as alt
import io
import logging
import re
from datetime import datetime
from PIL import Image, ImageEnhance
from rembg import remove
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from fpdf import FPDF
import xlsxwriter

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Vinted Pro Enterprise", layout="wide", page_icon="🏢")

# --- DATABASE SETUP ---
Base = declarative_base()
engine = create_engine('sqlite:///vinted_enterprise_master.db')
Session = sessionmaker(bind=engine)

class InventoryItem(Base):
    __tablename__ = 'inventory_master'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    brand = Column(String(100), nullable=False)
    tipo_capo = Column(String(100), nullable=False)
    costo_acquisto = Column(Float, default=0.0)
    prezzo_vendita = Column(Float, default=0.0)
    profitto_netto = Column(Float, default=0.0)

Base.metadata.create_all(engine)

# --- FUNZIONI AI ---
class AIEngine:
    @staticmethod
    def process_image(image_file):
        try:
            img = Image.open(image_file).convert("RGBA")
            img_no_bg = remove(img)
            canvas = Image.new("RGBA", (2000, 2000), (255, 255, 255, 255))
            img_no_bg.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            offset = ((2000 - img_no_bg.width) // 2, (2000 - img_no_bg.height) // 2)
            canvas.paste(img_no_bg, offset, img_no_bg)
            return canvas.convert("RGB")
        except Exception as e:
            st.error(f"Errore AI: {e}")
            return None

# --- MODULI UI ---
def show_ai_studio():
    st.header("📸 AI Studio")
    upload = st.file_uploader("Carica Foto", type=["jpg", "png"])
    if upload:
        if st.button("🚀 AVVIA ELABORAZIONE"):
            res = AIEngine.process_image(upload)
            if res:
                st.image(res, caption="Risultato")
                buf = io.BytesIO()
                res.save(buf, format="JPEG")
                st.download_button("📥 Scarica", buf.getvalue(), "vinted_asset.jpg")

def show_finance():
    st.header("💰 Hub Finanziario")
    with st.form("finance_form"):
        brand = st.text_input("Brand")
        costo = st.number_input("Costo Acquisto", step=0.5)
        prezzo = st.number_input("Prezzo Vendita", step=1.0)
        if st.form_submit_button("Salva Transazione"):
            netto = prezzo - costo
            session = Session()
            new_item = InventoryItem(brand=brand, costo_acquisto=costo, prezzo_vendita=prezzo, profitto_netto=netto, tipo_capo="N/A")
            session.add(new_item)
            session.commit()
            session.close()
            st.success(f"✅ Salvato! Profitto: €{netto:.2f}")

def show_inventory():
    st.header("📦 Magazzino")
    session = Session()
    df = pd.read_sql(session.query(InventoryItem).statement, session.bind)
    session.close()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nessun dato presente.")

def show_analytics():
    st.header("📈 Analisi")
    session = Session()
    df = pd.read_sql(session.query(InventoryItem).statement, session.bind)
    session.close()
    if not df.empty:
        st.metric("Totale Netto", f"€{df['profitto_netto'].sum():.2f}")
        chart = alt.Chart(df).mark_bar().encode(x='brand', y='sum(profitto_netto)')
        st.altair_chart(chart, use_container_width=True)

# --- MAIN ROUTER ---
def main():
    menu = {
        "📸 AI Studio": show_ai_studio,
        "💰 Finanza": show_finance,
        "📦 Magazzino": show_inventory,
        "📈 Analisi": show_analytics
    }
    scelta = st.sidebar.radio("Navigazione", list(menu.keys()))
    menu[scelta]()

if __name__ == "__main__":
    main()
