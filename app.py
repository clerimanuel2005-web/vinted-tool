import streamlit as st
import pandas as pd
import altair as alt
import os
import io
import logging
import re
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from fpdf import FPDF
import xlsxwriter

# ==============================================================================
# 1. SETUP AMBIENTE E LOGGING ENTERPRISE
# ==============================================================================
st.set_page_config(page_title="Vinted Pro Enterprise Suite", layout="wide", page_icon="🏢")

logging.basicConfig(
    filename='vinted_enterprise_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [MODULO:%(module)s] - LINE:%(lineno)d - %(message)s'
)

st.markdown("""
    <style>
    .stButton>button { border-radius: 6px; font-weight: bold; background-color: #09b1ba; color: white; }
    .stDownloadButton>button { background-color: #2c3e50; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #09b1ba; }
    .help-text { color: #7f8c8d; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. DATABASE ORM (SQLAlchemy)
# ==============================================================================
Base = declarative_base()
engine = create_engine('sqlite:///vinted_enterprise_master.db')
Session = sessionmaker(bind=engine)

class InventoryItem(Base):
    __tablename__ = 'inventory_master'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    brand = Column(String(100), nullable=False)
    tipo_capo = Column(String(100), nullable=False)
    taglia = Column(String(20))
    condizioni = Column(String(50))
    costo_acquisto = Column(Float, default=0.0)
    spese_extra = Column(Float, default=0.0)
    prezzo_vendita = Column(Float, default=0.0)
    commissioni_perc = Column(Float, default=0.0)
    profitto_netto = Column(Float, default=0.0)
    stato_articolo = Column(String(50), default="In Vendita")
    note = Column(String(255))

Base.metadata.create_all(engine)

# ==============================================================================
# 3. MODULO VALIDAZIONE DATI
# ==============================================================================
class DataValidator:
    @staticmethod
    def is_valid_price(price, cost, extra):
        if price <= 0: return False, "Il prezzo non può essere zero o negativo."
        if price < (cost + extra): return False, "Attenzione: Il prezzo genera perdita."
        return True, "Prezzo valido"

    @staticmethod
    def is_valid_brand(brand_str):
        if not brand_str or len(brand_str.strip()) < 2: return False, "Brand troppo corto."
        if not re.match(r'^[a-zA-Z0-9 &.-]+$', brand_str): return False, "Caratteri non validi."
        return True, "Brand valido"

    @staticmethod
    def calculate_roi(profit, total_cost):
        return round((profit / total_cost) * 100, 2) if total_cost > 0 else 100.0

# ==============================================================================
# 4. MODULO INTELLIGENZA ARTIFICIALE
# ==============================================================================
class AIEngine:
    @staticmethod
    def remove_background(image_file):
        try:
            input_img = Image.open(image_file).convert("RGBA")
            img_no_bg = remove(input_img)
            canvas = Image.new("RGBA", (2000, 2000), (255, 255, 255, 255))
            img_no_bg.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            offset = ((2000 - img_no_bg.width) // 2, (2000 - img_no_bg.height) // 2)
            canvas.paste(img_no_bg, offset, img_no_bg)
            return canvas.convert("RGB")
        except Exception as e:
            logging.error(f"Errore AI: {str(e)}")
            return None

    @staticmethod
    def enhance_image(image, sharpness=1.5, contrast=1.2):
        img = ImageEnhance.Sharpness(image).enhance(sharpness)
        return ImageEnhance.Contrast(img).enhance(contrast)

# ==============================================================================
# 5. GENERAZIONE DOCUMENTI
# ==============================================================================
class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 15, 'VINTED PRO SELLER - SCHEDA TECNICA', 0, 1, 'C')

    def generate_product_sheet(self, data_dict):
        self.add_page()
        self.set_font('Arial', '', 12)
        for key, value in data_dict.items():
            self.cell(50, 10, f"{key}:", border=1)
            self.cell(140, 10, str(value), border=1, ln=1)
        return self.output(dest='S').encode('latin-1')

class AdvancedExcelExport:
    @staticmethod
    def create_financial_report(dataframe):
        output = io.BytesIO()
        with xlsxwriter.Workbook(output, {'in_memory': True}) as workbook:
            worksheet = workbook.add_worksheet('Report')
            # Scrittura semplificata per brevità
            dataframe.to_excel(output, index=False)
        return output.getvalue()

# ==============================================================================
# 6. FUNZIONI UI
# ==============================================================================
def show_ai_studio():
    st.header("📸 AI Studio")
    upload = st.file_uploader("Carica Foto", type=["jpg", "png"])
    if upload and st.button("🚀 AVVIA ELABORAZIONE"):
        with st.spinner("Elaborazione in corso..."):
            res = AIEngine.remove_background(upload)
            if res:
                res = AIEngine.enhance_image(res)
                st.image(res)
                buf = io.BytesIO()
                res.save(buf, format="JPEG")
                st.download_button("📥 Scarica", buf.getvalue(), "asset.jpg")

def show_seo_generator():
    st.header("📝 Modulo SEO")
    with st.form("seo_form"):
        brand = st.text_input("Brand")
        tipo = st.text_input("Tipo")
        taglia = st.selectbox("Taglia", ["S", "M", "L", "XL"])
        if st.form_submit_button("Genera"):
            st.success("✅ Annuncio pronto")
            st.code(f"{tipo.capitalize()} {brand.upper()} - Tg {taglia}")

def show_finance_dashboard():
    st.header("💰 Hub Finanziario")
    with st.form("finance_form"):
        c1, c2 = st.columns(2)
        costo = c1.number_input("Costo", step=0.5)
        prezzo = c2.number_input("Prezzo", step=1.0)
        if st.form_submit_button("Salva"):
            profitto = prezzo - costo
            st.success(f"Profitto netto: € {profitto:.2f}") # CORRETTO

def show_inventory():
    st.header("📦 Magazzino")
    session = Session()
    df = pd.read_sql(session.query(InventoryItem).statement, session.bind)
    session.close()
    if not df.empty:
        st.data_editor(df, width=None) # CORRETTO: width='stretch' non necessario se None

def show_analytics():
    st.header("📈 Analisi")
    session = Session()
    df = pd.read_sql(session.query(InventoryItem).statement, session.bind)
    session.close()
    if not df.empty:
        st.metric("Totale Netto", f"€ {df['profitto_netto'].sum():.2f}") # CORRETTO
        chart = alt.Chart(df).mark_bar().encode(x='brand', y='sum(profitto_netto)')
        st.altair_chart(chart, use_container_width=True)

def main():
    st.sidebar.title("Navigazione")
    menu = {"AI Studio": show_ai_studio, "SEO": show_seo_generator, "Finanza": show_finance_dashboard, "Magazzino": show_inventory, "Analisi": show_analytics}
    scelta = st.sidebar.radio("Modulo", list(menu.keys()))
    menu[scelta]()

if __name__ == "__main__":
    main()
