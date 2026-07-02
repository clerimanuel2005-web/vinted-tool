import streamlit as st
import pandas as pd
import altair as alt
import os
import io
import logging
from datetime import datetime
from PIL import Image, ImageEnhance
from rembg import remove
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from fpdf import FPDF

# ==============================================================================
# 1. SETUP AMBIENTE, DB E LOGGING
# ==============================================================================
logging.basicConfig(filename='vinted_pro.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

Base = declarative_base()
engine = create_engine('sqlite:///vinted_pro.db')
Session = sessionmaker(bind=engine)

class Prodotto(Base):
    __tablename__ = 'prodotti'
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default=datetime.utcnow)
    brand = Column(String)
    tipo = Column(String)
    prezzo_vendita = Column(Float)
    costo_base = Column(Float)
    profitto = Column(Float)

Base.metadata.create_all(engine)

# ==============================================================================
# 2. MOTORI AI E FUNZIONI DI UTILITÀ
# ==============================================================================
def genera_pdf(brand, tipo, prezzo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"SCHEDA PRODOTTO PROFESSIONALE", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Brand: {brand}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo: {tipo}", ln=True)
    pdf.cell(200, 10, txt=f"Prezzo Vendita: {prezzo} Euro", ln=True)
    return pdf.output(dest='S').encode('latin-1')

def elabora_foto_industriale(img_file):
    input_img = Image.open(img_file)
    # Rimozione sfondo tramite AI
    img_no_bg = remove(input_img)
    # Creazione background bianco professionale
    canvas = Image.new("RGBA", (2000, 2000), (255, 255, 255, 255))
    resized_img = img_no_bg.resize((1500, 1500))
    canvas.paste(resized_img, (250, 250), resized_img)
    return canvas.convert("RGB")

# ==============================================================================
# 3. INTERFACCIA GRAFICA (FRONTEND)
# ==============================================================================
st.set_page_config(page_title="Vinted Pro Enterprise", layout="wide", page_icon="🛍️")

st.title("🛍️ Vinted Pro Suite - Enterprise Edition")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📸 AI Studio", "📝 Annunci SEO", "💰 Finanza", "📦 Inventario"])

with tab1:
    st.header("📸 AI Studio: Background Removal")
    uploaded = st.file_uploader("Carica foto capo (alta risoluzione)")
    if uploaded and st.button("✨ Avvia AI Processing"):
        with st.spinner("L'AI sta analizzando la sagoma..."):
            res = elabora_foto_industriale(uploaded)
            st.image(res, caption="Prodotto pronto per Vinted")
            buf = io.BytesIO()
            res.save(buf, format="JPEG")
            st.download_button("📥 Scarica Foto Pro (JPG)", buf.getvalue(), "prodotto_finale.jpg")

with tab2:
    st.header("📝 Generatore Annunci & Documentazione")
    colA, colB = st.columns(2)
    brand = colA.text_input("Brand")
    tipo = colB.text_input("Tipo")
    if st.button("Genera Scheda PDF"):
        pdf_data = genera_pdf(brand, tipo, "0.00")
        st.download_button("📥 Scarica PDF Tecnico", pdf_data, "scheda_prodotto.pdf")

with tab3:
    st.header("💰 Gestione Finanziaria Industriale")
    c1, c2 = st.columns(2)
    prezzo = c1.number_input("Prezzo Vendita (€)", 0.0)
    costo = c2.number_input("Costo Acquisto (€)", 0.0)
    
    if st.button("💾 Registra Transazione"):
        session = Session()
        new_p = Prodotto(brand=brand, tipo=tipo, prezzo_vendita=prezzo, 
                         costo_base=costo, profitto=(prezzo-costo))
        session.add(new_p)
        session.commit()
        session.close()
        logging.info(f"Salvataggio eseguito: {brand} | Profitto: {prezzo-costo}")
        st.success("Transazione salvata e loggata nel sistema.")

with tab4:
    st.header("📦 Inventario Enterprise (SQL Database)")
    session = Session()
    df = pd.read_sql(session.query(Prodotto).statement, session.bind)
    st.dataframe(df, use_container_width=True)
    
    if st.button("📊 Esporta Report CSV"):
        df.to_csv("report_finale.csv", index=False)
        st.info("File 'report_finale.csv' generato nella cartella locale.")
    session.close()

# Footer di sistema
st.sidebar.markdown("---")
st.sidebar.write("🟢 **Stato Sistema:** Online")
st.sidebar.write("💾 **Database:** SQLite Attivo")
st.sidebar.write("⚙️ **Log:** `vinted_pro.log` attivo")
