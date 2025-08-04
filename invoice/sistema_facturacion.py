# factura_pdf.py - Generador de PDF para facturas AFIP
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import qrcode
import io
import os

class FacturaPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configurar estilos personalizados"""
        # Estilo para el título
        self.styles.add(ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=10
        ))
        
        # Estilo para datos importantes
        self.styles.add(ParagraphStyle(
            'ImportantData',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=5
        ))
        
        # Estilo para el CAE (destacado)
        self.styles.add(ParagraphStyle(
            'CAEStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))

    def generar_qr_afip(self, datos_factura):
        """Generar código QR con formato AFIP"""
        # URL base de verificación de AFIP
        # En producción sería diferente, pero para testing usamos esta estructura
        qr_data = f"https://www.afip.gob.ar/fe/qr/?p="
        qr_data += f"cuit={datos_factura['cuit']}&"
        qr_data += f"pv={datos_factura['punto_venta']:04d}&"
        qr_data += f"comp={datos_factura['tipo_comprobante']:02d}&"
        qr_data += f"nro={datos_factura['numero_comprobante']:08d}&"
        qr_data += f"fecha={datos_factura['fecha']}&"
        qr_data += f"importe={datos_factura['importe_total']:.2f}"
        
        # Crear QR
        qr = qrcode.QRCode(version=1, box_size=3, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Convertir a imagen en memoria
        qr_img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return img_buffer

    def crear_encabezado_empresa(self, datos_empresa):
        """Crear encabezado con datos de la empresa"""
        data = [
            [datos_empresa.get('razon_social', 'TU EMPRESA S.A.'), '', 'FACTURA'],
            [f"CUIT: {datos_empresa.get('cuit', '20-44551555-9')}", '', 'B'],
            [datos_empresa.get('direccion', 'Dirección de tu empresa'), '', f"N° {datos_empresa.get('punto_venta', '0001'):04d}-{datos_empresa.get('numero', 1):08d}"],
            [f"{datos_empresa.get('localidad', 'Ciudad')}, {datos_empresa.get('provincia', 'Provincia')}", '', ''],
        ]
        
        table = Table(data, colWidths=[8*cm, 2*cm, 4*cm])
        table.setStyle(TableStyle([
            # Empresa (columna 1)
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            
            # Tipo de factura (columna 3)
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('FONTSIZE', (2, 0), (2, -1), 12),
            ('FONTNAME', (2, 0), (2, 2), 'Helvetica-Bold'),
            ('BOX', (2, 0), (2, 2), 2, colors.black),
            ('BACKGROUND', (2, 1), (2, 1), colors.lightgrey),
            
            # Líneas generales
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        return table

    def crear_datos_cliente(self, datos_cliente):
        """Crear sección de datos del cliente"""
        # Validaciones y formateo
        nombre = datos_cliente.get('nombre', 'CONSUMIDOR FINAL').upper()
        documento = datos_cliente.get('documento', '')
        direccion = datos_cliente.get('direccion', '')
        condicion_iva = datos_cliente.get('condicion_iva', 'Consumidor Final')
        
        # Formatear documento según el tipo
        if documento:
            if len(documento) == 11:  # CUIT
                documento = f"{documento[:2]}-{documento[2:10]}-{documento[10]}"
                doc_label = "CUIT"
            elif len(documento) == 8:  # DNI
                doc_label = "DNI"
            else:
                doc_label = "Documento"
            documento_texto = f"{doc_label}: {documento}"
        else:
            documento_texto = "Sin identificar"
        
        data = [
            ['DATOS DEL CLIENTE'],
            [f"Nombre/Razón Social: {nombre}"],
            [documento_texto],
            [f"Dirección: {direccion if direccion else 'Sin especificar'}"],
            [f"Condición IVA: {condicion_iva}"],
        ]
        
        table = Table(data, colWidths=[14*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        return table

    def crear_detalle_productos(self, productos):
        """Crear tabla de productos/servicios"""
        # Encabezado
        data = [['Cantidad', 'Descripción', 'Precio Unitario', 'Subtotal']]
        
        # Productos
        total_neto = 0
        for producto in productos:
            cantidad = producto.get('quantity', 1)
            descripcion = producto.get('name', 'Producto/Servicio')
            precio_unitario = producto.get('price', 0)
            subtotal = cantidad * precio_unitario
            total_neto += subtotal
            
            data.append([
                str(cantidad),
                descripcion,
                f"$ {precio_unitario:.2f}",
                f"$ {subtotal:.2f}"
            ])
        
        # Totales
        iva_21 = total_neto * 0.21
        total_final = total_neto + iva_21
        
        data.extend([
            ['', '', 'Subtotal:', f"$ {total_neto:.2f}"],
            ['', '', 'IVA 21%:', f"$ {iva_21:.2f}"],
            ['', '', 'TOTAL:', f"$ {total_final:.2f}"]
        ])
        
        table = Table(data, colWidths=[2*cm, 7*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Productos
            ('ALIGN', (0, 1), (0, -4), 'CENTER'),  # Cantidad
            ('ALIGN', (1, 1), (1, -4), 'LEFT'),    # Descripción
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Precios
            
            # Totales (últimas 3 filas)
            ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (2, -1), (-1, -1), colors.lightgrey),
            
            # Bordes
            ('GRID', (0, 0), (-1, -4), 0.5, colors.black),
            ('BOX', (2, -3), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        
        return table, total_final

    def crear_datos_fiscales(self, datos_factura):
        """Crear sección de datos fiscales (CAE, etc.)"""
        fecha_formateada = datetime.strptime(datos_factura['fecha'], '%Y%m%d').strftime('%d/%m/%Y')
        vto_cae_formateado = datetime.strptime(datos_factura['vencimiento_cae'], '%Y%m%d').strftime('%d/%m/%Y')
        
        data = [
            ['DATOS FISCALES'],
            [f"Fecha de Emisión: {fecha_formateada}"],
            [f"CAE: {datos_factura['cae']}"],
            [f"Vencimiento CAE: {vto_cae_formateado}"],
            [f"Comprobante Nº: {datos_factura['punto_venta']:04d}-{datos_factura['numero_comprobante']:08d}"],
        ]
        
        table = Table(data, colWidths=[10*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),  # CAE en negrita
            ('TEXTCOLOR', (0, 2), (0, 2), colors.red),       # CAE en rojo
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        
        return table

    def generar_factura_pdf(self, datos_factura, datos_empresa, datos_cliente, productos, filename=None):
        """Generar el PDF completo de la factura"""
        
        if filename is None:
            filename = f"factura_{datos_factura['punto_venta']:04d}_{datos_factura['numero_comprobante']:08d}.pdf"
        
        # Crear documento
        doc = SimpleDocTemplate(filename, pagesize=A4, 
                              rightMargin=2*cm, leftMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        story = []
        
        # 1. Encabezado con datos de empresa y tipo de factura
        story.append(self.crear_encabezado_empresa(datos_empresa))
        story.append(Spacer(1, 10*mm))
        
        # 2. Datos del cliente
        story.append(self.crear_datos_cliente(datos_cliente))
        story.append(Spacer(1, 10*mm))
        
        # 3. Detalle de productos
        tabla_productos, total = self.crear_detalle_productos(productos)
        story.append(tabla_productos)
        story.append(Spacer(1, 10*mm))
        
        # 4. Datos fiscales y CAE
        story.append(self.crear_datos_fiscales(datos_factura))
        story.append(Spacer(1, 10*mm))
        
        '''
        # 5. Código QR (opcional)
        try:
            qr_buffer = self.generar_qr_afip(datos_factura)
            
            # Crear tabla con QR y texto
            qr_data = [
                ['Código QR para verificación AFIP'],
                ['Escaneá para verificar la autenticidad']
            ]
            
            qr_table = Table(qr_data, colWidths=[6*cm])
            qr_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(qr_table)
            
        except Exception as e:
            print(f"Error generando QR: {e}")
            story.append(Paragraph("QR de verificación no disponible", self.styles['Normal']))
        
        '''
        
        # 6. Generar PDF
        doc.build(story)
        print(f"✅ Factura PDF generada: {filename}")
        return filename

# Función de ejemplo para usar el generador
def generar_factura_ejemplo():
    """Función de ejemplo mostrando cómo usar el generador"""
    
    generator = FacturaPDFGenerator()
    
    # Datos de la factura (los que recibes de AFIP)
    datos_factura = {
        'cae': '75319266109747',
        'vencimiento_cae': '20250809',
        'numero_comprobante': 1,
        'punto_venta': 1,
        'tipo_comprobante': 6,  # Factura B
        'fecha': '20250730',
        'cuit': '20445515559',
        'importe_total': 121.00
    }
    
    # Datos de tu empresa
    datos_empresa = {
        'razon_social': 'ELECTRICIDAD JUAN S.A.',
        'cuit': '20-44551555-9',
        'direccion': 'Av. Ejemplo 1234',
        'localidad': 'Chazón',
        'provincia': 'Córdoba',
        'punto_venta': 1,
        'numero': 1
    }
    
    # Datos del cliente
    datos_cliente = {
        'nombre': 'CONSUMIDOR FINAL',
        'documento': 'Sin identificar',
        'direccion': 'Sin especificar',
        'condicion_iva': 'Consumidor Final'
    }
    
    # Productos vendidos
    productos = [
        {
            'cantidad': 2,
            'descripcion': 'Cable eléctrico 2.5mm x metro',
            'precio_unitario': 25.00
        },
        {
            'cantidad': 1,
            'descripcion': 'Tomacorriente doble con toma a tierra',
            'precio_unitario': 50.00
        }
    ]
    
    # Generar PDF
    filename = generator.generar_factura_pdf(
        datos_factura, datos_empresa, datos_cliente, productos
    )
    
    return filename
