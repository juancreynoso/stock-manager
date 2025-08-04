# config/settings.py - Configuración central de la aplicación

import os

# Configuración de la base de datos
DATABASE_CONFIG = {
    'db_path': 'db/stock.db',
    'backup_enabled': True,
    'backup_interval_hours': 24
}

# Configuración de la empresa
COMPANY_CONFIG = {
    'razon_social': 'ELECTRICIDAD NESTOR PALACIOS',
    'cuit': '20-44551555-9',
    'direccion': 'Ricardo Araujo 363',
    'localidad': 'Carnerillo',
    'provincia': 'Córdoba',
    'punto_venta': 1,
    'telefono': '',
    'email': ''
}

# Configuración AFIP
AFIP_CONFIG = {
    'testing_mode': True,  # Cambiar a False en producción
    'cert_path': 'arca/my_cert.crt',
    'key_path': 'arca/my_private.key',
    'cuit': '20445515559',
    'service_url_testing': 'https://wswhomo.afip.gov.ar/wsfev1/service.asmx',
    'service_url_production': 'https://servicios1.afip.gov.ar/wsfev1/service.asmx'
}

# Configuración de PDF
PDF_CONFIG = {
    'output_directory': 'facturas/',
    'template_logo': None,  # Ruta al logo si lo tienes
    'font_family': 'Helvetica',
    'page_margins': {
        'top': 2,
        'bottom': 2,
        'left': 2,
        'right': 2
    }
}

# Configuración de interfaz
UI_CONFIG = {
    'window_title': 'Sistema de Gestión - Electricidad Juan',
    'window_size': '1080x720',
    'theme_colors': {
        'primary': '#076397',
        'secondary': '#40C395',
        'accent': '#FFFFFF',
        'background': '#F5F5F5'
    },
    'categories': [
        'Iluminación',
        'Protección',
        'Tomas e Interruptores',
        'Cables',
        'Herramientas',
        'Otros'
    ]
}

# Configuración de validaciones
VALIDATION_CONFIG = {
    'product_id_length': 5,
    'max_product_name_length': 100,
    'max_customer_name_length': 100,
    'min_price': 0.01,
    'max_price': 999999.99,
    'low_stock_threshold': 5
}

# Configuración de facturación
INVOICE_CONFIG = {
    'tipo_comprobante': 6,  # Factura B
    'iva_rate': 0.21,  # 21%
    'auto_backup': True,
    'print_after_generate': False
}

def get_full_path(relative_path):
    """Obtener ruta completa desde el directorio raíz del proyecto"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

def ensure_directory_exists(directory):
    """Asegurar que un directorio existe"""
    full_path = get_full_path(directory)
    os.makedirs(full_path, exist_ok=True)
    return full_path

# Inicializar directorios necesarios
def initialize_directories():
    """Crear directorios necesarios si no existen"""
    directories = [
        'db',
        'facturas',
        'logs',
        'backups'
    ]
    
    for directory in directories:
        ensure_directory_exists(directory)