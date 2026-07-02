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

# Configurazione Logging Professionale (scrive su file locale per sicurezza)
logging.basicConfig(
    filename='vinted_enterprise_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [MODULO:%(module)s] - LINE:%(lineno)d - %(message)s'
)

# Stili CSS globali per interfaccia industriale
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
    """Modello Dati per l'inventario aziendale Vinted"""
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
# 3. MODULO VALIDAZIONE DATI RIGOROSA
# ==============================================================================
class DataValidator:
    """Gestisce i controlli di sicurezza sui dati in input"""
    
    @staticmethod
    def is_valid_price(price, cost, extra):
        """Verifica che il prezzo non generi una perdita automatica."""
        if price <= 0:
            return False, "Il prezzo di vendita non può essere zero o negativo."
        if price < (cost + extra):
            return False, "Attenzione: Il prezzo è inferiore ai costi totali (Genera perdita)."
        return True, "Prezzo valido"

    @staticmethod
    def is_valid_brand(brand_str):
        """Pulisce il brand ed evita caratteri non consentiti."""
        if not brand_str or len(brand_str.strip()) < 2:
            return False, "Il nome del brand deve avere almeno 2 caratteri."
        if not re.match(r'^[a-zA-Z0-9 &.-]+$', brand_str):
            return False, "Il brand contiene caratteri speciali non validi."
        return True, "Brand valido"

    @staticmethod
    def calculate_roi(profit, total_cost):
        """Calcola il Ritorno sull'Investimento in percentuale"""
        if total_cost <= 0:
            return 100.0 # Se ricevuto in regalo, ROI è tecnicamente inf, settiamo 100% o custom
        return round((profit / total_cost) * 100, 2)

# ==============================================================================
# 4. MODULO INTELLIGENZA ARTIFICIALE (IMMAGINI)
# ==============================================================================
class AIEngine:
    """Motore di elaborazione immagini professionale"""
    
    @staticmethod
    def remove_background(image_file):
        """Rimuove lo sfondo e centra su canvas bianco 2000x2000"""
        try:
            input_img = Image.open(image_file).convert("RGBA")
            # AI Background Removal
            img_no_bg = remove(input_img)
            
            # Setup Canvas Professionale Vinted Standard
            canvas_size = (2000, 2000)
            canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 255))
            
            # Ridimensionamento conservando l'aspect ratio
            img_no_bg.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            
            # Centratura matematica
            offset_x = (canvas_size[0] - img_no_bg.width) // 2
            offset_y = (canvas_size[1] - img_no_bg.height) // 2
            
            canvas.paste(img_no_bg, (offset_x, offset_y), img_no_bg)
            logging.info("Elaborazione AI immagine completata con successo.")
            return canvas.convert("RGB")
        except Exception as e:
            logging.error(f"Errore critico in AIEngine.remove_background: {str(e)}")
            return None

    @staticmethod
    def enhance_image(image, sharpness=1.5, contrast=1.2):
        """Applica filtri fotografici professionali in catena"""
        try:
            img = ImageEnhance.Sharpness(image).enhance(sharpness)
            img = ImageEnhance.Contrast(img).enhance(contrast)
            return img
        except Exception as e:
            logging.error(f"Errore applicazione filtri: {str(e)}")
            return image

# ==============================================================================
# 5. MODULO GENERAZIONE DOCUMENTI (PDF & EXCEL)
# ==============================================================================
class ReportPDF(FPDF):
    """Generatore di Schede Tecniche Prodotto in PDF"""
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(9, 177, 186) # Colore brand
        self.cell(0, 15, 'VINTED PRO SELLER - SCHEDA TECNICA', 0, 1, 'C')
        self.line(10, 25, 200, 25)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()} - Documento generato automaticamente', 0, 0, 'C')

    def generate_product_sheet(self, data_dict):
        self.add_page()
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 0)
        
        # Inserimento dati strutturati
        for key, value in data_dict.items():
            self.set_font('Arial', 'B', 12)
            self.cell(50, 10, f"{key}:", border=1, fill=False)
            self.set_font('Arial', '', 12)
            self.cell(140, 10, str(value), border=1, ln=1)
            
        return self.output(dest='S').encode('latin-1')

class AdvancedExcelExport:
    """Generatore di reportistica finanziaria in Excel"""
    @staticmethod
    def create_financial_report(dataframe):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Inventario Finanziario')

        # Definizione Formati
        header_format = workbook.add_format({'bold': True, 'bg_color': '#2c3e50', 'font_color': 'white', 'border': 1})
        money_format = workbook.add_format({'num_format': '€ #,##0.00', 'border': 1})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1})
        standard_format = workbook.add_format({'border': 1})

        # Scrittura Intestazioni
        headers = dataframe.columns.tolist()
        for col_num, data in enumerate(headers):
            worksheet.write(0, col_num, data, header_format)
            worksheet.set_column(col_num, col_num, 15) # Larghezza colonne automatica

        # Scrittura Dati
        for row_num, row_data in enumerate(dataframe.values):
            for col_num, data in enumerate(row_data):
                if isinstance(data, float):
                    worksheet.write(row_num + 1, col_num, data, money_format)
                elif isinstance(data, pd.Timestamp) or isinstance(data, datetime):
                    worksheet.write_datetime(row_num + 1, col_num, data, date_format)
                else:
                    worksheet.write(row_num + 1, col_num, data, standard_format)

        # Aggiunta Somma Totale Profitti
        profit_col_index = headers.index('profitto_netto')
        end_row = len(dataframe)
        worksheet.write(end_row + 1, profit_col_index - 1, "Totale Netto:", header_format)
        worksheet.write_formula(end_row + 1, profit_col_index, f"=SUM({xlsxwriter.utility.xl_col_to_name(profit_col_index)}2:{xlsxwriter.utility.xl_col_to_name(profit_col_index)}{end_row + 1})", money_format)

        workbook.close()
        return output.getvalue()

# ==============================================================================
# 6. FUNZIONI DI INTERFACCIA E TAB
# ==============================================================================

def show_ai_studio():
    st.header("📸 AI Studio: Ghost Mannequin & Processing")
    st.markdown('<p class="help-text">Rimuovi lo sfondo e adatta l\'immagine agli standard visivi di Vinted per aumentare il CTR (Click-Through Rate).</p>', unsafe_allow_html=True)
    
    upload = st.file_uploader("Carica Fotografia Prodotto", type=["jpg", "png", "jpeg"], accept_multiple_files=False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Impostazioni Motore AI")
        apply_filters = st.checkbox("Applica Ottimizzazione Texture (Nitidezza/Contrasto)", value=True)
    
    if upload:
        if st.button("🚀 AVVIA ELABORAZIONE AI", use_container_width=True):
            with st.spinner("Il motore neurale sta segmentando l'immagine... attendere."):
                processed_img = AIEngine.remove_background(upload)
                
                if processed_img:
                    if apply_filters:
                        processed_img = AIEngine.enhance_image(processed_img)
                        
                    st.success("✅ Elaborazione completata con successo!")
                    
                    with col2:
                        st.image(processed_img, caption="Risultato Finale - Pure White 2000x2000")
                        
                        # Conversione per download
                        buf = io.BytesIO()
                        processed_img.save(buf, format="JPEG", quality=95)
                        st.download_button("📥 Esporta Asset per Vinted", buf.getvalue(), f"vinted_asset_{datetime.now().strftime('%H%M%S')}.jpg", mime="image/jpeg")
                else:
                    st.error("❌ Si è verificato un errore critico durante l'elaborazione dell'immagine.")

def show_seo_generator():
    st.header("📝 Modulo SEO & Generazione Contenuti")
    
    with st.form("seo_content_form"):
        st.subheader("Dati Base Articolo")
        c1, c2, c3 = st.columns(3)
        brand = c1.text_input("Nome Brand (Es. Nike, Carhartt)")
        tipo = c2.text_input("Tipologia (Es. Felpa, Jeans)")
        taglia = c3.selectbox("Taglia", ["XXS", "XS", "S", "M", "L", "XL", "XXL", "Unica"])
        
        c4, c5 = st.columns(2)
        condizioni = c4.selectbox("Condizioni", ["Nuovo con cartellino", "Ottimo stato", "Buono stato", "Usato"])
        colore = c5.text_input("Colore / Pattern dominante")
        
        dettagli = st.text_area("Note e dettagli per l'acquirente (difetti, vestibilità)")
        
        submit = st.form_submit_button("Genera Annuncio Ottimizzato")
        
        if submit:
            val_ok, msg = DataValidator.is_valid_brand(brand)
            if not val_ok:
                st.error(f"Errore Validazione: {msg}")
            elif not tipo:
                st.error("Errore: Inserire la tipologia di capo.")
            else:
                # Generazione Testo
                titolo = f"{tipo.capitalize()} {brand.upper()} - Tg {taglia}"
                descrizione = f"👕 {titolo}\n\n"
                descrizione += f"Vendo {tipo.lower()} originale {brand.capitalize()}.\n"
                descrizione += f"📏 Taglia: {taglia}\n"
                descrizione += f"🎨 Colore: {colore}\n"
                descrizione += f"✨ Condizioni: {condizioni}\n\n"
                if dettagli:
                    descrizione += f"📝 Note: {dettagli}\n\n"
                descrizione += f"📦 Spedizione rapida e sicura.\n"
                descrizione += f"#{brand.lower().replace(' ','')} #{tipo.lower().replace(' ','')} #vinted #vintage"
                
                st.success("✅ Annuncio generato!")
                st.code(descrizione, language="text")
                
                # Generazione PDF
                pdf_doc = ReportPDF()
                pdf_bytes = pdf_doc.generate_product_sheet({
                    "Titolo": titolo, "Brand": brand, "Categoria": tipo, 
                    "Taglia": taglia, "Condizione": condizioni, "Note": dettagli
                })
                st.download_button("📥 Scarica Scheda Tecnica (PDF)", pdf_bytes, f"Scheda_{brand}.pdf", mime="application/pdf")

def show_finance_dashboard():
    st.header("💰 Business Intelligence e Inserimento Dati")
    
    with st.form("financial_form"):
        st.subheader("Dati Finanziari Transazione")
        
        col1, col2 = st.columns(2)
        brand = col1.text_input("Brand Articolo")
        tipo = col2.text_input("Tipologia Articolo")
        
        c1, c2, c3, c4 = st.columns(4)
        costo_acq = c1.number_input("Costo Acquisto (€)", min_value=0.0, step=0.5)
        spese_extra = c2.number_input("Spese Extra/Pack (€)", min_value=0.0, step=0.5)
        comm_perc = c3.number_input("Commissioni Vinted (%)", min_value=0.0, max_value=30.0, step=1.0, value=5.0)
        prezzo_ven = c4.number_input("Prezzo di Vendita (€)", min_value=0.0, step=1.0)
        
        save_btn = st.form_submit_button("💾 Registra Transazione in Database")
        
        if save_btn:
            # 1. Validazione Testo
            v_brand, m_brand = DataValidator.is_valid_brand(brand)
            if not v_brand: st.error(m_brand); return
            if not tipo: st.error("Inserire tipologia"); return
            
            # 2. Validazione Numerica e Calcolo
            v_prezzo, m_prezzo = DataValidator.is_valid_price(prezzo_ven, costo_acq, spese_extra)
            if not v_prezzo: st.warning(m_prezzo) # Warning ma permette il salvataggio
            
            profitto = prezzo_ven - (prezzo_ven * (comm_perc/100)) - (costo_acq + spese_extra)
            roi = DataValidator.calculate_roi(profitto, costo_acq + spese_extra)
            
            # 3. Inserimento in DB (SQLAlchemy)
            try:
                session = Session()
                nuovo_item = InventoryItem(
                    brand=brand, tipo_capo=tipo, 
                    costo_acquisto=costo_acq, spese_extra=spese_extra, 
                    prezzo_vendita=prezzo_ven, commissioni_perc=comm_perc,
                    profitto_netto=profitto
                )
                session.add(nuovo_item)
                session.commit()
                session.close()
                logging.info(f"Registrata transazione DB: {brand} | Profitto: €{profitto}")
                
                st.success(f"✅ Transazione salvata con successo! Profitto Netto stimato: €{profitto:.2f} (ROI: {roi}%)")
                st.toast('Dati scritti in SQLite!', icon='💾')
            except Exception as e:
                logging.error(f"Database insertion failed: {str(e)}")
                st.error("Errore critico in scrittura database. Controllare log.")

def show_inventory():
    st.header("📦 Gestione Database Magazzino")
    
    session = Session()
    try:
        query = session.query(InventoryItem)
        df = pd.read_sql(query.statement, session.bind)
    except Exception as e:
        st.error("Errore lettura DB.")
        df = pd.DataFrame()
    finally:
        session.close()
        
    if df.empty:
        st.info("Il database magazzino è attualmente vuoto.")
        return
        
    # Tabella Interattiva Editabile
    st.markdown("### Stock Attuale")
    edited_df = st.data_editor(
        df, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "timestamp": st.column_config.DatetimeColumn("Data di Creazione", disabled=True, format="DD/MM/YYYY"),
            "costo_acquisto": st.column_config.NumberColumn("Costo", format="€ %.2f"),
            "prezzo_vendita": st.column_config.NumberColumn("Prezzo", format="€ %.2f"),
            "profitto_netto": st.column_config.NumberColumn("Netto", format="€ %.2f"),
            "stato_articolo": st.column_config.SelectboxColumn("Stato", options=["In Vendita", "Spedito", "Completato", "Reso"])
        }
    )
    
    # Esportazione EXCEL Avanzata
    st.markdown("### Export Dati Aziendali")
    excel_data = AdvancedExcelExport.create_financial_report(df)
    st.download_button(
        label="📊 Esporta Report Finanziario Completo (Excel)",
        data=excel_data,
        file_name=f"Vinted_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def show_analytics():
    st.header("📈 Dashboard Analitica Globale")
    
    session = Session()
    df = pd.read_sql(session.query(InventoryItem).statement, session.bind)
    session.close()
    
    if df.empty:
        st.warning("Dati insufficienti per generare grafici.")
        return
        
    # KPI Globali
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Totale Capi in DB", len(df))
    c2.metric("Profitto Netto Totale", f"€ {df['profitto_netto'].sum():.2f}")
    c3.metric("Spese Totali Sostenute", f"€ {(df['costo_acquisto'] + df['spese_extra']).sum():.2f}")
    
    try:
        roi_globale = (df['profitto_netto'].sum() / (df['costo_acquisto'].sum() + df['spese_extra'].sum())) * 100
    except ZeroDivisionError:
        roi_globale = 0
    c4.metric("ROI Globale Medio", f"{roi_globale:.1f} %")
    
    st.markdown("---")
    
    # Grafici Avanzati Altair
    st.subheader("Andamento Profitti per Brand")
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('brand:N', sort='-y', title="Brand"),
        y=alt.Y('sum(profitto_netto):Q', title="Profitto Totale (€)"),
        color=alt.Color('brand:N', legend=None),
        tooltip=['brand', 'sum(profitto_netto)']
    ).interactive()
    st.altair_chart(bar_chart, use_container_width=True)

def show_help_system():
    st.header("📖 Manuale Operativo Enterprise")
    st.markdown("""
    Benvenuto nella **Vinted Pro Enterprise Suite**.
    Questo strumento è progettato per scalare il tuo business di abbigliamento online.
    
    ### 1. Come usare l'AI Studio
    Carica un'immagine alla massima risoluzione possibile. Il sistema AI identificherà il capo, rimuoverà l'ambiente circostante e lo posizionerà matematicamente al centro di una tela bianca `2000x2000` pixel, lo standard aureo per gli e-commerce di moda.
    
    ### 2. Gestione Database
    Il sistema non perde mai i dati. Tutto è salvato in un database relazionale **SQLite** (`vinted_enterprise_master.db`). 
    Se chiudi l'applicazione, i tuoi inventari e le tue metriche finanziarie rimarranno intatti al riavvio.
    
    ### 3. Log di Sistema
    Per ragioni di audit aziendale, ogni transazione finanziaria, caricamento immagine ed eventuale errore software viene silenziosamente registrato nel file `vinted_enterprise_system.log`. In caso di anomalie, consulta questo file.
    
    ### 4. Esportazione Dati
    Puoi esportare:
    *   **Immagini** modificate per l'upload su Vinted (in JPG compresso per il web).
    *   **Fogli PDF** per archivio interno o da inserire nel pacco di spedizione.
    *   **Fogli Excel (XLSX)** formattati automaticamente con formule matematiche per il commercialista.
    """)

# ==============================================================================
# 7. MAIN ROUTER
# ==============================================================================
def main():
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Vinted_logo.png/600px-Vinted_logo.png", width=150)
    st.sidebar.markdown("### Master Navigation")
    
    opzioni_menu = {
        "📸 Motore AI Studio": show_ai_studio,
        "📝 Generatore SEO": show_seo_generator,
        "💰 Hub Finanziario": show_finance_dashboard,
        "📦 Magazzino Dati": show_inventory,
        "📈 Analisi & BI": show_analytics,
        "📖 Manuale & System": show_help_system
    }
    
    selezione = st.sidebar.radio("Seleziona Modulo Operativo", list(opzioni_menu.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.info("🟢 System: ONLINE\n\n🛡️ Database: SQLite3\n\n🧠 AI: Rembg Active")
    
    # Esecuzione del modulo selezionato
    opzioni_menu[selezione]()

if __name__ == "__main__":
    main()
