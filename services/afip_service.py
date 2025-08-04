import sys
import os

# Agregar el directorio arca al path para importar los módulos AFIP
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'arca'))

class AFIPService:
    def __init__(self):
        self.is_testing = True  # Cambiar a False en producción
        
    def obtener_cae(self, datos_factura):
        """
        Obtener CAE de AFIP para una factura
        Por ahora devuelve datos de testing, después integrarás con wsfe.py
        """
        try:
            if self.is_testing:
                # Datos de prueba para testing
                return {
                    'cae': '75319266109747',
                    'fecha_vencimiento_cae': '20250809',
                    'resultado': 'A',  # A = Aprobado
                    'observaciones': [],
                    'errores': []
                }
            else:
                # Aquí integrarías con tu wsfe.py real
                # from arca.wsfe import obtener_cae_real
                # return obtener_cae_real(datos_factura)
                pass
                
        except Exception as e:
            return {
                'cae': None,
                'fecha_vencimiento_cae': None,
                'resultado': 'R',  # R = Rechazado
                'observaciones': [],
                'errores': [str(e)]
            }
    
    def validar_cuit(self, cuit):
        """Validar formato de CUIT"""
        if not cuit:
            return True  # CUIT opcional para Consumidor Final
            
        # Limpiar guiones y espacios
        cuit_limpio = cuit.replace('-', '').replace(' ', '')
        
        # Debe tener 11 dígitos
        if len(cuit_limpio) != 11 or not cuit_limpio.isdigit():
            return False
            
        # Validación del dígito verificador (algoritmo CUIT)
        multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        suma = sum(int(cuit_limpio[i]) * multiplicadores[i] for i in range(10))
        resto = suma % 11
        
        if resto < 2:
            digito_verificador = resto
        else:
            digito_verificador = 11 - resto
            
        return int(cuit_limpio[10]) == digito_verificador
    
    def formatear_cuit(self, cuit):
        """Formatear CUIT con guiones"""
        if not cuit:
            return ''
            
        cuit_limpio = cuit.replace('-', '').replace(' ', '')
        if len(cuit_limpio) == 11:
            return f"{cuit_limpio[:2]}-{cuit_limpio[2:10]}-{cuit_limpio[10]}"
        return cuit
    
    def obtener_siguiente_numero_comprobante(self, punto_venta=1, tipo_comprobante=6):
        """
        Obtener el siguiente número de comprobante disponible
        En producción esto consultaría a AFIP
        """
        try:
            if self.is_testing:
                # Para testing, usar un número secuencial simple
                from models.sales import SalesModel
                sales_model = SalesModel()
                return sales_model.get_next_invoice_number()
            else:
                # Aquí consultarías a AFIP el último número usado
                # from arca.wsfe import obtener_ultimo_comprobante
                # return obtener_ultimo_comprobante(punto_venta, tipo_comprobante) + 1
                pass
                
        except Exception as e:
            print(f"Error obteniendo siguiente número: {e}")
            return "0001-00000001"