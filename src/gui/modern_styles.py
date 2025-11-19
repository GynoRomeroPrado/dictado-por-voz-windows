"""
Estilos modernos para la aplicación Dictado por Voz
Incluye tema oscuro y claro con diseño minimalista y actual
"""

# Paleta de colores moderna
COLORS = {
    # Dark Theme
    'dark': {
        'primary': '#6366F1',      # Indigo vibrante
        'primary_hover': '#818CF8',
        'primary_pressed': '#4F46E5',
        'secondary': '#8B5CF6',     # Purple
        'success': '#10B981',       # Green
        'danger': '#EF4444',        # Red
        'warning': '#F59E0B',       # Amber
        'bg_primary': '#0F172A',    # Slate 900
        'bg_secondary': '#1E293B',  # Slate 800
        'bg_tertiary': '#334155',   # Slate 700
        'text_primary': '#F1F5F9',  # Slate 100
        'text_secondary': '#94A3B8', # Slate 400
        'border': '#334155',        # Slate 700
        'shadow': 'rgba(0, 0, 0, 0.3)',
    },
    # Light Theme
    'light': {
        'primary': '#6366F1',
        'primary_hover': '#818CF8',
        'primary_pressed': '#4F46E5',
        'secondary': '#8B5CF6',
        'success': '#10B981',
        'danger': '#EF4444',
        'warning': '#F59E0B',
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#F8FAFC',  # Slate 50
        'bg_tertiary': '#E2E8F0',   # Slate 200
        'text_primary': '#0F172A',  # Slate 900
        'text_secondary': '#64748B', # Slate 500
        'border': '#E2E8F0',        # Slate 200
        'shadow': 'rgba(0, 0, 0, 0.1)',
    }
}


def get_modern_stylesheet(theme='dark'):
    """
    Retorna el stylesheet completo para la aplicación

    Args:
        theme: 'dark' o 'light'
    """
    c = COLORS[theme]

    return f"""
    /* ===== GENERAL ===== */
    QWidget {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
        font-size: 13px;
        color: {c['text_primary']};
        background-color: {c['bg_primary']};
    }}

    /* ===== DIALOG ===== */
    QDialog {{
        background-color: {c['bg_primary']};
        border-radius: 12px;
    }}

    /* ===== BUTTONS ===== */
    QPushButton {{
        background-color: {c['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 13px;
        min-height: 36px;
    }}

    QPushButton:hover {{
        background-color: {c['primary_hover']};
    }}

    QPushButton:pressed {{
        background-color: {c['primary_pressed']};
    }}

    QPushButton:disabled {{
        background-color: {c['bg_tertiary']};
        color: {c['text_secondary']};
    }}

    QPushButton#secondary {{
        background-color: {c['bg_secondary']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
    }}

    QPushButton#secondary:hover {{
        background-color: {c['bg_tertiary']};
    }}

    QPushButton#danger {{
        background-color: {c['danger']};
    }}

    QPushButton#danger:hover {{
        background-color: #DC2626;
    }}

    /* ===== INPUT FIELDS ===== */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 8px 12px;
        color: {c['text_primary']};
        selection-background-color: {c['primary']};
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 2px solid {c['primary']};
        background-color: {c['bg_primary']};
    }}

    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: {c['bg_tertiary']};
        color: {c['text_secondary']};
    }}

    /* ===== COMBOBOX ===== */
    QComboBox {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 8px 12px;
        min-height: 36px;
        color: {c['text_primary']};
    }}

    QComboBox:hover {{
        border-color: {c['primary']};
    }}

    QComboBox::drop-down {{
        border: none;
        padding-right: 10px;
    }}

    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 6px solid {c['text_secondary']};
        margin-right: 8px;
    }}

    QComboBox QAbstractItemView {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 4px;
        selection-background-color: {c['primary']};
        selection-color: white;
        outline: none;
    }}

    QComboBox QAbstractItemView::item {{
        padding: 8px 12px;
        border-radius: 4px;
        min-height: 32px;
    }}

    QComboBox QAbstractItemView::item:hover {{
        background-color: {c['bg_tertiary']};
    }}

    /* ===== CHECKBOX ===== */
    QCheckBox {{
        spacing: 8px;
        color: {c['text_primary']};
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid {c['border']};
        background-color: {c['bg_secondary']};
    }}

    QCheckBox::indicator:hover {{
        border-color: {c['primary']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {c['primary']};
        border-color: {c['primary']};
        image: none;
    }}

    QCheckBox::indicator:checked::after {{
        content: "✓";
        color: white;
    }}

    /* ===== RADIO BUTTON ===== */
    QRadioButton {{
        spacing: 8px;
        color: {c['text_primary']};
    }}

    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: 2px solid {c['border']};
        background-color: {c['bg_secondary']};
    }}

    QRadioButton::indicator:hover {{
        border-color: {c['primary']};
    }}

    QRadioButton::indicator:checked {{
        border-color: {c['primary']};
        background-color: {c['bg_secondary']};
    }}

    QRadioButton::indicator:checked::after {{
        content: "";
        width: 10px;
        height: 10px;
        border-radius: 5px;
        background-color: {c['primary']};
    }}

    /* ===== GROUPBOX ===== */
    QGroupBox {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        margin-top: 12px;
        padding: 16px;
        font-weight: 600;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        background-color: {c['bg_primary']};
        color: {c['text_primary']};
        border-radius: 4px;
    }}

    /* ===== LABELS ===== */
    QLabel {{
        color: {c['text_primary']};
        background: transparent;
    }}

    QLabel#subtitle {{
        color: {c['text_secondary']};
        font-size: 12px;
    }}

    QLabel#title {{
        font-size: 18px;
        font-weight: 700;
        color: {c['text_primary']};
    }}

    /* ===== SCROLLBAR ===== */
    QScrollBar:vertical {{
        background-color: {c['bg_secondary']};
        width: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {c['bg_tertiary']};
        border-radius: 5px;
        min-height: 20px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {c['text_secondary']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background-color: {c['bg_secondary']};
        height: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {c['bg_tertiary']};
        border-radius: 5px;
        min-width: 20px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background-color: {c['text_secondary']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* ===== SLIDER ===== */
    QSlider::groove:horizontal {{
        background: {c['bg_tertiary']};
        height: 4px;
        border-radius: 2px;
    }}

    QSlider::handle:horizontal {{
        background: {c['primary']};
        width: 16px;
        height: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }}

    QSlider::handle:horizontal:hover {{
        background: {c['primary_hover']};
    }}

    /* ===== TAB WIDGET ===== */
    QTabWidget::pane {{
        border: 1px solid {c['border']};
        border-radius: 8px;
        background-color: {c['bg_secondary']};
        padding: 8px;
    }}

    QTabBar::tab {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 10px 20px;
        margin-right: 2px;
        color: {c['text_secondary']};
    }}

    QTabBar::tab:selected {{
        background-color: {c['bg_primary']};
        color: {c['text_primary']};
        font-weight: 600;
    }}

    QTabBar::tab:hover {{
        background-color: {c['bg_tertiary']};
    }}

    /* ===== TOOLTIP ===== */
    QToolTip {{
        background-color: {c['bg_tertiary']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 12px;
    }}

    /* ===== MENU ===== */
    QMenu {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 4px;
    }}

    QMenu::item {{
        padding: 8px 24px 8px 12px;
        border-radius: 4px;
        margin: 2px 4px;
    }}

    QMenu::item:selected {{
        background-color: {c['primary']};
        color: white;
    }}

    QMenu::separator {{
        height: 1px;
        background-color: {c['border']};
        margin: 4px 8px;
    }}

    /* ===== PROGRESS BAR ===== */
    QProgressBar {{
        background-color: {c['bg_tertiary']};
        border: none;
        border-radius: 6px;
        height: 8px;
        text-align: center;
    }}

    QProgressBar::chunk {{
        background-color: {c['primary']};
        border-radius: 6px;
    }}
    """


def get_recording_overlay_style(theme='dark'):
    """
    Estilo específico para la ventana flotante de grabación
    """
    c = COLORS[theme]

    return f"""
    QDialog {{
        background-color: {c['bg_secondary']};
        border: 2px solid {c['primary']};
        border-radius: 16px;
    }}

    QLabel#status {{
        color: {c['text_primary']};
        font-size: 14px;
        font-weight: 600;
    }}

    QLabel#subtitle {{
        color: {c['text_secondary']};
        font-size: 11px;
    }}
    """


# Iconos SVG como strings para usar sin archivos externos
ICONS = {
    'microphone': '''
        <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
        </svg>
    ''',
    'settings': '''
        <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>
        </svg>
    '''
}
