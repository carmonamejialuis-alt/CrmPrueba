import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import json

# Configuración de página
st.set_page_config(
    page_title="Artistic CRM",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para mejor apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .main-subheader {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .gold-text {
        color: #d4af37;
    }
    .alert-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .alert-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }
    .appointment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .appointment-card.selected {
        border-color: #d4af37;
        background: linear-gradient(135deg, #fff9e6 0%, #fff3cc 100%);
        transform: scale(1.02);
    }
    .client-detail-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .status-badge {
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Datos de ejemplo mejor estructurados
SAMPLE_DATA = {
    "alerts": [
        {
            "id": 1,
            "type": "high",
            "icon": "🔥",
            "title": "Confirmación de Cita Urgente",
            "message": "Cliente 'Ana Torres' confirmó cita para mañana 10:00 AM",
            "time": "Hace 15 min",
            "action": "Preparar materiales"
        },
        {
            "id": 2,
            "type": "medium", 
            "icon": "📋",
            "title": "Aprobación de Diseño Pendiente",
            "message": "Javier Luna espera aprobación del boceto final",
            "time": "Hace 2 horas",
            "action": "Revisar y enviar"
        },
        {
            "id": 3,
            "type": "low",
            "icon": "💌",
            "title": "Seguimiento Post-Cita",
            "message": "Enviar cuidados post-tatuaje a Sofia Beltrán",
            "time": "Ayer",
            "action": "Enviar email"
        }
    ],
    "appointments": [
        {
            "id": 1,
            "time": "10:00 AM",
            "client": "Carlos Rivas",
            "service": "Realismo - Manga completa",
            "session": "Sesión 3 de 4",
            "duration": "3 horas",
            "status": "confirmed",
            "price": "$450.000"
        },
        {
            "id": 2, 
            "time": "02:00 PM",
            "client": "Lucia Fernandez",
            "service": "Acuarela - Colibrí en antebrazo",
            "session": "Sesión única",
            "duration": "2 horas", 
            "status": "confirmed",
            "price": "$300.000"
        },
        {
            "id": 3,
            "time": "05:00 PM", 
            "client": "Miguel Angel",
            "service": "Consulta - Diseño espalda completa",
            "session": "Consulta inicial",
            "duration": "1 hora",
            "status": "pending",
            "price": "$0"
        }
    ],
    "clients": {
        "Carlos Rivas": {
            "contact": {
                "phone": "+57 300 123 4567",
                "email": "carlos.r@email.com",
                "instagram": "@carlos.tattoo"
            },
            "medical": {
                "allergies": "Alergia leve al látex",
                "medications": "Ninguna",
                "skin_type": "Mixta"
            },
            "preferences": {
                "style": "Realismo negro/gris",
                "pain_tolerance": "Alta",
                "session_length": "3-4 horas máximo"
            },
            "history": {
                "sessions_completed": 2,
                "total_spent": "$900.000",
                "last_visit": "2024-01-15",
                "notes": "Cliente puntual y tranquilo. Prefiere música rock durante sesiones."
            }
        },
        "Lucia Fernandez": {
            "contact": {
                "phone": "+57 310 987 6543", 
                "email": "lucia.f@email.com",
                "instagram": "@lucia.ink"
            },
            "medical": {
                "allergies": "Ninguna",
                "medications": "Anticonceptivos",
                "skin_type": "Sensible"
            },
            "preferences": {
                "style": "Acuarela color",
                "pain_tolerance": "Media", 
                "session_length": "2 horas máximo"
            },
            "history": {
                "sessions_completed": 0,
                "total_spent": "$0",
                "last_visit": "Primera vez",
                "notes": "Nerviosa por primer tatuaje. Explicar proceso detalladamente."
            }
        },
        "Miguel Angel": {
            "contact": {
                "phone": "+57 320 555 1122",
                "email": "miguel.a@email.com", 
                "instagram": "@miguel.art"
            },
            "medical": {
                "allergies": "Ninguna",
                "medications": "Ninguna",
                "skin_type": "Normal"
            },
            "preferences": {
                "style": "Mitología japonesa",
                "pain_tolerance": "Desconocida",
                "session_length": "Por determinar"
            },
            "history": {
                "sessions_completed": 0,
                "total_spent": "$0", 
                "last_visit": "Primera consulta",
                "notes": "Referido por Ana Torres. Trae diseños propios para revisar."
            }
        }
    }
}

# Funciones de utilidad
def get_status_badge(status):
    colors = {
        "confirmed": ("✅ Confirmado", "#10b981"),
        "pending": ("⏳ Pendiente", "#f59e0b"), 
        "cancelled": ("❌ Cancelado", "#ef4444")
    }
    text, color = colors.get(status, ("📝 Desconocido", "#6b7280"))
    return f"<span style='background-color: {color}; color: white; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;'>{text}</span>"

def get_alert_color(alert_type):
    colors = {
        "high": "#ef4444",
        "medium": "#f59e0b", 
        "low": "#3b82f6"
    }
    return colors.get(alert_type, "#6b7280")

# Header principal
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">Panel de <span class="gold-text">Artista</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subheader">Bienvenido, aquí tienes un resumen actualizado de tu día</p>', unsafe_allow_html=True)



# Layout principal
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📅 Agenda Completa", "👥 Gestión de Clientes"])

with tab1:
    
    
    # primera  fila: Contenido principal
    col1, col2, col3 = st.columns([1, 2, 1.2])
    
    # Columna 1: Alertas
    with col1:
        st.subheader("🔔 Alertas Prioritarias")
        for alert in SAMPLE_DATA["alerts"]:
            color = get_alert_color(alert["type"])
            st.markdown(f"""
            <div class="alert-card" style="border-left-color: {color}">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">{alert['icon']}</span>
                    <div>
                        <h4 style="margin: 0; color: #1f2937; font-weight: 600;">{alert['title']}</h4>
                        <small style="color: #6b7280;">{alert['time']}</small>
                    </div>
                </div>
                <p style="margin: 0.5rem 0; color: #4b5563;">{alert['message']}</p>
                <button style="background: {color}; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem;">
                    {alert['action']}
                </button>
            </div>
            """, unsafe_allow_html=True)
    
    # Columna 2: Agenda del día
    with col2:
        st.subheader("📅 Agenda de Hoy")
        
        # Selector de cliente
        selected_client = st.selectbox(
            "Seleccionar cliente:",
            options=[appointment["client"] for appointment in SAMPLE_DATA["appointments"]],
            key="client_selector"
        )
        
        # Mostrar citas
        for appointment in SAMPLE_DATA["appointments"]:
            is_selected = appointment["client"] == selected_client
            badge = get_status_badge(appointment["status"])
            
            st.markdown(f"""
            <div class="appointment-card {'selected' if is_selected else ''}">
                <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                    <h3 style="margin: 0; color: #1f2937; font-size: 1.3rem;">🕒 {appointment['time']}</h3>
                    {badge}
                </div>
                <h4 style="margin: 0 0 0.5rem 0; color: #d4af37; font-size: 1.1rem;">{appointment['client']}</h4>
                <p style="margin: 0.25rem 0; color: #4b5563;"><strong>Servicio:</strong> {appointment['service']}</p>
                <p style="margin: 0.25rem 0; color: #4b5563;"><strong>Sesión:</strong> {appointment['session']}</p>
                <p style="margin: 0.25rem 0; color: #4b5563;"><strong>Duración:</strong> {appointment['duration']}</p>
                <p style="margin: 0.25rem 0; color: #4b5563;"><strong>Precio:</strong> {appointment['price']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Columna 3: Detalles del cliente seleccionado
    with col3:
        st.subheader("👤 Ficha del Cliente")
        
        if selected_client and selected_client in SAMPLE_DATA["clients"]:
            client_data = SAMPLE_DATA["clients"][selected_client]
            
            st.markdown("""
            <div class="client-detail-card">
            """, unsafe_allow_html=True)
            
            # Información de contacto
            st.write("### 📞 Contacto")
            contact = client_data["contact"]
            st.write(f"**Teléfono:** {contact['phone']}")
            st.write(f"**Email:** {contact['email']}")
            st.write(f"**Instagram:** {contact['instagram']}")
            
            # Información médica
            st.write("### 🏥 Información Médica")
            medical = client_data["medical"]
            st.write(f"**Alergias:** {medical['allergies']}")
            st.write(f"**Medicamentos:** {medical['medications']}")
            st.write(f"**Tipo de piel:** {medical['skin_type']}")
            
            # Preferencias
            st.write("### 💫 Preferencias")
            prefs = client_data["preferences"]
            st.write(f"**Estilo:** {prefs['style']}")
            st.write(f"**Tolerancia al dolor:** {prefs['pain_tolerance']}")
            st.write(f"**Duración de sesión:** {prefs['session_length']}")
            
            # Historial
            st.write("### 📊 Historial")
            history = client_data["history"]
            st.write(f"**Sesiones completadas:** {history['sessions_completed']}")
            st.write(f"**Total gastado:** {history['total_spent']}")
            st.write(f"**Última visita:** {history['last_visit']}")
            
            # Notas importantes
            st.write("### 📝 Notas Importantes")
            st.info(history['notes'])
            
            # Botones de acción
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.button("📞 Llamar", use_container_width=True)
            with col_btn2:
                st.button("✉️ Email", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# Pestañas adicionales (puedes expandir estas)
with tab2:
    st.subheader("Agenda Completa")
    # Aquí puedes agregar un calendario interactivo
    st.info("📅 Vista de calendario completa - En desarrollo")

with tab3:
    st.subheader("Gestión de Clientes")
    # Aquí puedes agregar CRUD de clientes
    st.info("👥 Panel de gestión de clientes - En desarrollo")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6b7280;'>Artistic CRM v1.0 · Desarrollado para artistas tatuadores</div>", unsafe_allow_html=True)