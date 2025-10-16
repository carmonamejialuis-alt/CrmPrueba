import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de página - VERSIÓN COMPATIBLE
st.set_page_config(
    page_title="Artistic CRM",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS SIMPLIFICADO - compatible con todos los navegadores
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .gold-text {
        color: #d4af37;
    }
    .alert-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .appointment-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .appointment-card.selected {
        border-color: #d4af37;
        background: #fff9e6;
    }
    .client-detail-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Datos de ejemplo (igual que antes)
SAMPLE_DATA = {
    "alerts": [
        {
            "id": 1,
            "type": "high",
            "icon": "URGENTE",
            "title": "Confirmación de Cita Urgente",
            "message": "Cliente 'Ana Torres' confirmó cita para mañana 10:00 AM",
            "time": "Hace 15 min",
            "action": "Preparar materiales"
        },
        {
            "id": 2,
            "type": "medium", 
            "icon": "PENDIENTE",
            "title": "Aprobación de Diseño Pendiente",
            "message": "Javier Luna espera aprobación del boceto final",
            "time": "Hace 2 horas",
            "action": "Revisar y enviar"
        },
        {
            "id": 3,
            "type": "low",
            "icon": "SEGUIMIENTO",
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

# Funciones de utilidad - VERSIÓN COMPATIBLE
def get_status_badge(status):
    colors = {
        "confirmed": ("CONFIRMADO", "#10b981"),
        "pending": ("PENDIENTE", "#f59e0b"), 
        "cancelled": ("CANCELADO", "#ef4444")
    }
    text, color = colors.get(status, ("DESCONOCIDO", "#6b7280"))
    return f"<span style='background-color: {color}; color: white; padding: 0.2rem 0.8rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;'>{text}</span>"

def get_alert_color(alert_type):
    colors = {
        "high": "#ef4444",
        "medium": "#f59e0b", 
        "low": "#3b82f6"
    }
    return colors.get(alert_type, "#6b7280")

# Header principal - SIN EMOJIS PROBLEMÁTICOS
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">Panel de <span class="gold-text">Artista</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; margin-bottom: 2rem;">Bienvenido, aquí tienes un resumen actualizado de tu día</p>', unsafe_allow_html=True)

with col2:
    today = datetime.now().strftime("%d %b %Y")
    st.metric("Hoy", today)
    st.metric("Citas Hoy", len(SAMPLE_DATA["appointments"]))

# Layout principal - PESTAÑAS SIMPLIFICADAS
tab1, tab2, tab3 = st.tabs(["DASHBOARD", "AGENDA", "CLIENTES"])

with tab1:
    col1, col2, col3 = st.columns([1, 2, 1.2])
    
    # Columna 1: Alertas - SIN EMOJIS COMPLEJOS
    with col1:
        st.subheader("Alertas Prioritarias")
        for alert in SAMPLE_DATA["alerts"]:
            color = get_alert_color(alert["type"])
            st.markdown(f"""
            <div class="alert-card" style="border-left-color: {color}">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <strong style="margin-right: 0.5rem; color: {color};">{alert['icon']}</strong>
                    <div>
                        <h4 style="margin: 0; color: #1f2937; font-weight: 600; font-size: 1rem;">{alert['title']}</h4>
                        <small style="color: #6b7280;">{alert['time']}</small>
                    </div>
                </div>
                <p style="margin: 0.5rem 0; color: #4b5563; font-size: 0.9rem;">{alert['message']}</p>
                <div style="background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 6px; text-align: center; font-size: 0.9rem;">
                    {alert['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Columna 2: Agenda - SIN EMOJIS PROBLEMÁTICOS
    with col2:
        st.subheader("Agenda de Hoy")
        
        selected_client = st.selectbox(
            "Seleccionar cliente:",
            options=[appointment["client"] for appointment in SAMPLE_DATA["appointments"]],
            key="client_selector"
        )
        
        for appointment in SAMPLE_DATA["appointments"]:
            is_selected = appointment["client"] == selected_client
            badge = get_status_badge(appointment["status"])
            
            st.markdown(f"""
            <div class="appointment-card {'selected' if is_selected else ''}">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <h3 style="margin: 0; color: #1f2937; font-size: 1.1rem;">{appointment['time']}</h3>
                    {badge}
                </div>
                <h4 style="margin: 0 0 0.5rem 0; color: #d4af37; font-size: 1rem;">{appointment['client']}</h4>
                <p style="margin: 0.2rem 0; color: #4b5563; font-size: 0.9rem;"><strong>Servicio:</strong> {appointment['service']}</p>
                <p style="margin: 0.2rem 0; color: #4b5563; font-size: 0.9rem;"><strong>Sesion:</strong> {appointment['session']}</p>
                <p style="margin: 0.2rem 0; color: #4b5563; font-size: 0.9rem;"><strong>Duracion:</strong> {appointment['duration']}</p>
                <p style="margin: 0.2rem 0; color: #4b5563; font-size: 0.9rem;"><strong>Precio:</strong> {appointment['price']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Columna 3: Detalles del cliente - TEXTO SIMPLE
    with col3:
        st.subheader("Ficha del Cliente")
        
        if selected_client and selected_client in SAMPLE_DATA["clients"]:
            client_data = SAMPLE_DATA["clients"][selected_client]
            
            st.markdown("""
            <div class="client-detail-card">
            """, unsafe_allow_html=True)
            
            st.write("**CONTACTO**")
            contact = client_data["contact"]
            st.write(f"Telefono: {contact['phone']}")
            st.write(f"Email: {contact['email']}")
            st.write(f"Instagram: {contact['instagram']}")
            
            st.write("**INFORMACION MEDICA**")
            medical = client_data["medical"]
            st.write(f"Alergias: {medical['allergies']}")
            st.write(f"Medicamentos: {medical['medications']}")
            st.write(f"Tipo de piel: {medical['skin_type']}")
            
            st.write("**PREFERENCIAS**")
            prefs = client_data["preferences"]
            st.write(f"Estilo: {prefs['style']}")
            st.write(f"Tolerancia al dolor: {prefs['pain_tolerance']}")
            st.write(f"Duracion de sesion: {prefs['session_length']}")
            
            st.write("**HISTORIAL**")
            history = client_data["history"]
            st.write(f"Sesiones completadas: {history['sessions_completed']}")
            st.write(f"Total gastado: {history['total_spent']}")
            st.write(f"Ultima visita: {history['last_visit']}")
            
            st.write("**NOTAS IMPORTANTES**")
            st.info(history['notes'])
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.button("Llamar", use_container_width=True)
            with col_btn2:
                st.button("Email", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Selecciona un cliente de la agenda para ver sus detalles")

with tab2:
    st.subheader("Agenda Completa")
    st.info("Vista de calendario completa - En desarrollo")

with tab3:
    st.subheader("Gestion de Clientes")
    st.info("Panel de gestion de clientes - En desarrollo")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6b7280;'>Artistic CRM v1.0 - Desarrollado para artistas tatuadores</div>", unsafe_allow_html=True)