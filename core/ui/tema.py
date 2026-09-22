"""Tema visual compartido para las calculadoras de HeyAlgb."""

FONDO_CALCULADORA = "#060606"
FONDO_TERMINAL = "#060606"
FONDO_PANEL = "#4d0000"
FONDO_ENCABEZADO = "#8f0000"
FONDO_BOTON = "#ffffff"
FONDO_TERMINO_INDEPENDIENTE = "#060606"
TEXTO_CLARO = "#ffffff"
TEXTO_OSCURO = "#000000"
ACENTO = "#fe0000"

def estilo_menu_desplegable():
    """Devuelve el estilo común de los menús desplegables de las calculadoras."""
    return {
        "corner_radius": 0,
        "border_width": 3,
        "border_color": TEXTO_OSCURO,
        "fg_color": FONDO_BOTON,
        "text_color": TEXTO_OSCURO,
        "button_color": FONDO_BOTON,
        "button_hover_color": "#e2e2e2",
        "dropdown_fg_color": "#1a1a1a",
        "dropdown_hover_color": ACENTO,
        "dropdown_text_color": TEXTO_CLARO,
    }

# --- NUEVAS FUNCIONES DE ESTILO AGREGADAS ---

def estilo_boton_principal():
    """Para botones de acción crítica como 'Calcular' o 'Evaluar Límite'."""
    return {
        "corner_radius": 0,
        "fg_color": ACENTO,
        "hover_color": "#b30000",
        "text_color": TEXTO_CLARO,
        "font": ("Impact", 15)  # Caótico y grueso
    }

def estilo_boton_secundario():
    """Para botones normales como 'Generar Red', 'Limpiar Valores', etc."""
    return {
        "corner_radius": 0,
        "fg_color": FONDO_BOTON,
        "hover_color": "#d0d2d0",
        "text_color": TEXTO_OSCURO,
        "font": ("Arial", 13, "bold")
    }

def estilo_panel_contenedor():
    """Para los CTkFrame principales, dándoles silueta y separándolos de la oscuridad."""
    return {
        "corner_radius": 0,
        "border_width": 2,
        "border_color": FONDO_PANEL,
        "fg_color": "#111111"  # Un gris extremadamente oscuro para dar relieve
    }

def estilo_consola_resultado():
    """Para las cajas CTkTextbox de respuesta."""
    return {
        "fg_color": FONDO_TERMINAL,
        "text_color": TEXTO_CLARO,
        "border_width": 1,
        "border_color": "#ffffff"  # Simula un recorte de papel blanco perimetral
    }

# --------------------------------------------

FUENTE_TITULO = "UltraCondensedSansSerif"
FUENTE_CONTROLES = "Democratica"
FUENTE_RESULTADOS = "Consolas"


def configurar_tema(ctk):
    """Configura el tema base de CustomTkinter para las vistas internas."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
