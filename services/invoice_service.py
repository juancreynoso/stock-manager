from datetime import datetime
from models.sales import SalesModel
from models.stock import StockModel
from services.afip_service import AFIPService
from invoice.sistema_facturacion import FacturaPDFGenerator

class InvoiceService:
    def __init__(self):
        self.sales_model = SalesModel()
        self.stock_model = StockModel()
        self.afip_service = AFIPService()
        self.pdf_generator = FacturaPDFGenerator()
    
    def create_invoice(self, customer_data, products_data):
        """
        Crear una factura completa:
        1. Validar datos
        2. Obtener CAE de AFIP
        3. Guardar en base de datos
        4. Generar PDF
        5. Actualizar stock
        """
        try:
            # 1. Validar datos
            self._validate_invoice_data(customer_data, products_data)
            
            # 2. Calcular totales
            totals = self._calculate_totals(products_data)
            
            # 3. Obtener siguiente número de factura
            numero_factura = self.afip_service.obtener_siguiente_numero_comprobante()
            
            # 4. Preparar datos para AFIP
            afip_data = self._prepare_afip_data(customer_data, totals, numero_factura)
            
            # 5. Obtener CAE de AFIP
            cae_response = self.afip_service.obtener_cae(afip_data)
            
            if cae_response['resultado'] != 'A':
                raise Exception(f"AFIP rechazó la factura: {cae_response.get('errores', 'Error desconocido')}")
            
            # 6. Preparar datos de la factura para BD
            invoice_data = {
                'numero_factura': numero_factura,
                'fecha_emision': datetime.now().strftime('%Y-%m-%d'),
                'cae': cae_response['cae'],
                'fecha_vencimiento_cae': cae_response['fecha_vencimiento_cae'],
                'cliente_nombre': customer_data['nombre'],
                'cliente_cuit': customer_data.get('documento', ''),
                'cliente_domicilio': customer_data.get('direccion', ''),
                'cliente_condicion_iva': customer_data.get('condicion_iva', 'Consumidor Final'),
                'subtotal': totals['subtotal'],
                'iva': totals['iva'],
                'total': totals['total'],
                'estado': 'autorizada'
            }
            
            # 7. Preparar items para BD
            items_data = []
            for product in products_data:
                items_data.append({
                    'producto_id': product['code'],
                    'producto_nombre': product['name'],
                    'cantidad': product['quantity'],
                    'precio_unitario': product['price'],
                    'subtotal': product['subtotal']
                })
            
            # 8. Guardar en base de datos
            invoice_id = self.sales_model.create_invoice(invoice_data, items_data)
            
            # 9. Actualizar stock
            for product in products_data:
                self.stock_model.reduce_quantity(product['code'], product['quantity'])
            
            # 10. Generar PDF
            pdf_filename = self._generate_pdf(invoice_data, customer_data, products_data, cae_response)
            
            return {
                'success': True,
                'invoice_id': invoice_id,
                'numero_factura': numero_factura,
                'cae': cae_response['cae'],
                'pdf_filename': pdf_filename,
                'total': totals['total']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _validate_invoice_data(self, customer_data, products_data):
        """Validar datos de la factura"""
        # Validar cliente
        if not customer_data.get('nombre', '').strip():
            raise ValueError("El nombre del cliente es obligatorio")
        
        # Validar CUIT si se proporciona
        cuit = customer_data.get('documento', '')
        if cuit and not self.afip_service.validar_cuit(cuit):
            raise ValueError("El CUIT/DNI proporcionado no es válido")
        
        # Validar productos
        if not products_data:
            raise ValueError("Debe agregar al menos un producto")
        
        for product in products_data:
            if product['quantity'] <= 0:
                raise ValueError(f"La cantidad del producto {product['name']} debe ser mayor a 0")
            
            if product['price'] <= 0:
                raise ValueError(f"El precio del producto {product['name']} debe ser mayor a 0")
    
    def _calculate_totals(self, products_data):
        """Calcular totales de la factura"""
        subtotal = sum(product['subtotal'] for product in products_data)
        iva = subtotal * 0.21  # IVA 21%
        total = subtotal + iva
        
        return {
            'subtotal': round(subtotal, 2),
            'iva': round(iva, 2),
            'total': round(total, 2)
        }
    
    def _prepare_afip_data(self, customer_data, totals, numero_factura):
        """Preparar datos para enviar a AFIP"""
        # Extraer número del formato "0001-00000001"
        parts = numero_factura.split('-')
        punto_venta = int(parts[0])
        numero_comprobante = int(parts[1])
        
        return {
            'punto_venta': punto_venta,
            'numero_comprobante': numero_comprobante,
            'tipo_comprobante': 6,  # Factura B
            'fecha': datetime.now().strftime('%Y%m%d'),
            'cuit': '20445515559',  # Tu CUIT
            'importe_total': totals['total'],
            'cliente_documento_tipo': 99 if not customer_data.get('documento') else 80,  # 99=Sin identificar, 80=CUIT
            'cliente_documento_numero': customer_data.get('documento', '0'),
            'importe_neto': totals['subtotal'],
            'importe_iva': totals['iva']
        }
    
    def _generate_pdf(self, invoice_data, customer_data, products_data, cae_response):
        """Generar PDF de la factura"""
        # Datos de la empresa (deberías moverlos a config)
        datos_empresa = {
            'razon_social': 'ELECTRICIDAD JUAN S.A.',
            'cuit': '20-44551555-9',
            'direccion': 'Ricardo Araujo 363',
            'localidad': 'Carnerillo',
            'provincia': 'Córdoba',
            'punto_venta': 1,
            'numero': int(invoice_data['numero_factura'].split('-')[1])
        }
        
        # Datos de la factura para PDF
        datos_factura = {
            'cae': cae_response['cae'],
            'vencimiento_cae': cae_response['fecha_vencimiento_cae'],
            'numero_comprobante': int(invoice_data['numero_factura'].split('-')[1]),
            'punto_venta': int(invoice_data['numero_factura'].split('-')[0]),
            'tipo_comprobante': 6,
            'fecha': datetime.now().strftime('%Y%m%d'),
            'cuit': '20445515559',
            'importe_total': invoice_data['total']
        }
        
        # Generar PDF
        filename = self.pdf_generator.generar_factura_pdf(
            datos_factura, datos_empresa, customer_data, products_data
        )
        
        return filename
    
    def get_invoice_details(self, invoice_id):
        """Obtener detalles completos de una factura"""
        invoice = self.sales_model.get_invoice_by_id(invoice_id)
        if not invoice:
            return None
            
        items = self.sales_model.get_invoice_items(invoice_id)
        
        return {
            'invoice': invoice,
            'items': items
        }
    
    def search_invoices(self, search_term):
        """Buscar facturas"""
        return self.sales_model.search_invoices(search_term)