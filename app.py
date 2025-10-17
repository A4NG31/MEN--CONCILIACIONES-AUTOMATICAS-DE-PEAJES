import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
import base64

# Configuración de página
st.set_page_config(
    page_title="GoPass - Menú de Concesiones", 
    page_icon="https://i.imgur.com/PgN46mi.jpeg", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Helper functions
# -----------------------------
def to_excel_bytes(df_dict):
    from openpyxl import Workbook
    import openpyxl
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, df in df_dict.items():
            sheet_name = str(name)[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()
    return output.getvalue()

def make_download_link(bytes_obj, filename, label="Descargar resultado"):
    b64 = base64.b64encode(bytes_obj).decode()
    href = f"data:application/octet-stream;base64,{b64}"
    return f"<a href='{href}' download='{filename}'>{label}</a>"

# -----------------------------
# CSS Styling Profesional
# -----------------------------
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stDecoration {display:none;}
    .stSidebar {display:none;}
    
    /* Fondo profesional con gradiente suave */
    .main .block-container {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 25%, #2d3748 50%, #1a202c 75%, #0f1419 100%);
        background-attachment: fixed;
        min-height: 100vh;
        padding: 2rem;
        max-width: 1400px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 25%, #2d3748 50%, #1a202c 75%, #0f1419 100%);
        background-attachment: fixed;
    }
    
    /* Header principal con verde GoPass */
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 2rem;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 25px;
        border: none;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 25s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    .company-logo {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 4px solid rgba(255,255,255,0.8);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .company-logo:hover {
        transform: scale(1.05);
    }
    
    .header-subtitle {
        color: #e2e8f0;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 0.5rem;
        opacity: 0.95;
        line-height: 1.5;
    }
    
    /* Títulos de secciones con verde profesional */
    .sub-header {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        padding: 1.2rem 2rem;
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        border-radius: 20px;
        border-left: 6px solid #34d399;
        text-align: center;
        box-shadow: 0 10px 25px rgba(4, 120, 87, 0.25);
        position: relative;
    }
    
    .sub-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #34d399, #10b981);
        border-radius: 0 0 20px 20px;
    }
    
    /* Matriz de concesiones 8x7 */
    .concessions-matrix {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(8, auto);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .concession-cell {
        background: linear-gradient(145deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 15px;
        padding: 1rem 0.8rem;
        box-shadow: 
            0 10px 15px -5px rgba(0, 0, 0, 0.1),
            0 5px 5px -5px rgba(0, 0, 0, 0.04);
        border: 2px solid #e2e8f0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 120px;
        min-height: 120px;
    }
    
    .concession-cell:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 15px 25px -8px rgba(0, 0, 0, 0.25),
            0 10px 10px -5px rgba(0, 0, 0, 0.1);
        border-color: #10b981;
    }
    
    .concession-cell::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981 0%, #059669 50%, #34d399 100%);
    }
    
    .concession-number {
        position: absolute;
        top: 8px;
        left: 8px;
        background: #10b981;
        color: white;
        border-radius: 50%;
        width: 25px;
        height: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .concession-title {
        font-size: 1rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0.8rem 0 0.5rem 0;
        line-height: 1.2;
        word-wrap: break-word;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    /* Botones profesionales con verde GoPass */
    .concession-btn {
        display: inline-block;
        width: 100%;
        padding: 0.5rem 0.8rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        text-decoration: none;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        cursor: pointer;
        box-shadow: 0 5px 10px rgba(16, 185, 129, 0.3);
        position: relative;
        overflow: hidden;
        margin-top: auto;
    }
    
    .concession-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .concession-btn:hover::before {
        left: 100%;
    }
    
    .concession-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(16, 185, 129, 0.4);
        text-decoration: none;
        color: #ffffff;
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    
    .concession-btn:active {
        transform: translateY(-1px);
    }
    
    /* Botón deshabilitado */
    .btn-disabled {
        background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
        box-shadow: 0 3px 8px rgba(160, 174, 192, 0.2);
        cursor: not-allowed;
    }
    
    .btn-disabled:hover {
        transform: none;
        background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
        box-shadow: 0 3px 8px rgba(160, 174, 192, 0.2);
    }
    
    /* Info boxes con verde profesional */
    .info-box {
        background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 2px solid #10b981;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.15);
        color: #064e3b;
    }
    
    .info-box h3 {
        color: #047857;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .info-box ul {
        color: #065f46;
        line-height: 1.6;
        font-size: 0.9rem;
    }
    
    .info-box strong {
        color: #064e3b;
        font-weight: 600;
    }
    
    /* Footer profesional */
    .footer {
        text-align: center;
        padding: 2rem 1.5rem;
        color: #e2e8f0;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border-radius: 20px;
        margin-top: 3rem;
        border: 2px solid #4a5568;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    
    .footer strong {
        color: #10b981;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .footer p {
        margin: 0.6rem 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Responsive mejorado */
    @media (max-width: 1200px) {
        .concessions-matrix {
            grid-template-columns: repeat(6, 1fr);
            grid-template-rows: repeat(8, auto);
        }
    }
    
    @media (max-width: 992px) {
        .concessions-matrix {
            grid-template-columns: repeat(5, 1fr);
            grid-template-rows: repeat(10, auto);
        }
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 2rem 1.5rem;
        }
        
        .concessions-matrix {
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(12, auto);
        }
        
        .concession-cell {
            height: 110px;
            min-height: 110px;
            padding: 0.8rem 0.6rem;
        }
        
        .concession-title {
            font-size: 0.9rem;
        }
        
        .company-logo {
            width: 80px;
            height: 80px;
        }
        
        .sub-header {
            font-size: 1.4rem;
            padding: 1rem 1.5rem;
        }
    }
    
    @media (max-width: 576px) {
        .concessions-matrix {
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(16, auto);
        }
        
        .concession-cell {
            height: 100px;
            min-height: 100px;
        }
        
        .concession-title {
            font-size: 0.85rem;
        }
        
        .concession-btn {
            font-size: 0.75rem;
            padding: 0.4rem 0.6rem;
        }
    }
    
    @media (max-width: 400px) {
        .concessions-matrix {
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(23, auto);
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header Principal con Logo
# -----------------------------
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <img src="https://i.imgur.com/PgN46mi.jpeg" class="company-logo">
        <h1>CONCESIONES DISPONIBLES</h1>
        <p class="header-subtitle">MATRIZ DE CONCESIONES VIALES - 8 FILAS × 7 COLUMNAS</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Lista de Concesiones
# -----------------------------
concesiones = [
    "ACCENORTE", "ALT. VIALES", "ALMA", "AUT. EL CAFE", "APP GICA", "AUT. DEL CARIBE", "AUT. RIO GRANDE",
    "AUT. RIO MAGDA", "ALCA. ENVIGADO", "AUT. NORDESTE", "AUTOVIA BTS", "AUT. NEIVA-GIRAR", "PANAMERICANA",
    "COVIANDINA", "COVIORIENTE", "COVIPACIFICO", "DEVIMAR", "DEVIMED", "DEVISAB", "FINDETER", "LA PINTADA",
    "PACIFICO TRES", "PEAJES NACIONALES", "PERI. DEL ORIENTE", "CONCESIÓN PISA", "RUTA AL MAR", "RUTA AL SUR",
    "RUTA COSTERA C-B", "RUTA DEL CACAO", "R. MAGDALENA S.M", "RUTA DEL VALLE", "SABA. DE OCCIDENTE",
    "RUTA PORTUARIA", "TUNEL ABURRA OR.", "U.V CAMINO DEL P.", "VIA 40 EXPRESS", "VIAL DE LOS LLANOS",
    "TRANSV. SISGA", "MONTES DE MARIA", "RIO PAMPLONITA", "UNION DEL SUR", "VIAS DEL NUS", "YUMA", "ICCU",
    "AUT. URABÁ", "AUT. MAGDA MEDIO"
]

# -----------------------------
# Sección de Concesiones en Matriz
# -----------------------------
st.markdown('<h2 class="sub-header">🛣️ MATRIZ DE CONCESIONES VIALES</h2>', unsafe_allow_html=True)

# Función JavaScript para redirección
st.markdown("""
<script>
function redirectToConcession(concessionName) {
    // Aquí puedes definir la URL específica para cada concesión
    // Por ahora, redirige a una página genérica con el nombre de la concesión
    window.open('https://ejemplo.com/concesiones/' + encodeURIComponent(concessionName), '_blank');
}
</script>
""", unsafe_allow_html=True)

# Crear matriz 8x7
st.markdown('<div class="concessions-matrix">', unsafe_allow_html=True)

for i, concesion in enumerate(concesiones, 1):
    st.markdown(f"""
    <div class="concession-cell">
        <div class="concession-number">{i}</div>
        <div class="concession-title">{concesion}</div>
        <button class="concession-btn" onclick="redirectToConcession('{concesion}')">
            Acceder
        </button>
    </div>
    """, unsafe_allow_html=True)

# Completar la matriz si hay menos de 56 elementos (8x7)
celdas_faltantes = 56 - len(concesiones)
for i in range(celdas_faltantes):
    st.markdown(f"""
    <div class="concession-cell" style="opacity: 0.3;">
        <div class="concession-number">{len(concesiones) + i + 1}</div>
        <div class="concession-title">Próximamente</div>
        <button class="concession-btn btn-disabled">
            Próximamente
        </button>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Información adicional
# -----------------------------
st.markdown("""
<div class="info-box">
    <h3>ℹ️ Información de la Matriz</h3>
    <ul>
        <li><strong>Estructura:</strong> Matriz de 8 filas × 7 columnas (56 celdas totales)</li>
        <li><strong>Concesiones Activas:</strong> 46 concesiones disponibles</li>
        <li><strong>Espacios Reservados:</strong> 10 celdas para futuras expansiones</li>
        <li><strong>Acceso Rápido:</strong> Cada celda proporciona acceso directo a la concesión correspondiente</li>
        <li><strong>Diseño Responsivo:</strong> Se adapta automáticamente a diferentes tamaños de pantalla</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Footer Profesional
# -----------------------------
st.markdown("""
<div class="footer">
    <p><strong>GoPass</strong> · Sistema Profesional de Gestión de Concesiones</p>
    <p>Plataforma centralizada para acceso a todas las concesiones viales disponibles</p>
    <p>Matriz organizada para navegación eficiente y rápida</p>
    <p>Desarrollado por Angel Torres</p>
    <p style="margin-top: 1.5rem; opacity: 0.8; font-size: 0.85rem;">© 2025 GoPass. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
