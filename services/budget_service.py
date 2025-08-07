from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

class BudgetService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configurar estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,  # Reducido de 18
            spaceAfter=15,  # Reducido de 30
            alignment=1,  # Centrado
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=9,  # Reducido de 10
            alignment=1,  # Centrado
            spaceAfter=10  # Reducido de 20
        ))
        
        self.styles.add(ParagraphStyle(
            name='ClientInfo',
            parent=self.styles['Normal'],
            fontSize=9,  # Reducido de 10
            spaceAfter=5  # Reducido de 10
        ))
    
    def generate_budget(self, budget_data, save_path=None):
        """
        Generar presupuesto en PDF
        
        Args:
            budget_data (dict): Datos del presupuesto con estructura:
            {
                'budget_number': str,
                'client_name': str,
                'client_address': str,
                'client_phone': str,
                'items': [
                    {
                        'quantity': int,
                        'description': str,
                        'brand': str,
                        'unit_price': float,
                        'subtotal': float
                    }
                ],
                'total': float,
                'validity_days': int (opcional, default 30),
                'notes': str (opcional)
            }
            save_path (str): Ruta donde guardar el archivo
        """
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"presupuesto_{budget_data['budget_number']}_{timestamp}.pdf"
            save_path = os.path.join("presupuestos", filename)
            
            # Crear directorio si no existe
            os.makedirs("presupuestos", exist_ok=True)
        
        # Crear documento con márgenes reducidos
        doc = SimpleDocTemplate(
            save_path, 
            pagesize=A4,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            leftMargin=0.5*inch, 
            rightMargin=0.5*inch
        )
        elements = []
        
        # Información de la empresa (personalizable)
        company_info = self._get_company_info()
        elements.append(company_info)
        elements.append(Spacer(1, 15))
        
        # Información del presupuesto y cliente
        budget_info = self._create_budget_info_table(budget_data)
        elements.append(budget_info)
        elements.append(Spacer(1, 10))
        
        # Tabla de productos
        products_table = self._create_products_table(budget_data['items'])
        elements.append(products_table)
        elements.append(Spacer(1, 10))
        
        # Total
        total_table = self._create_total_table(budget_data['total'])
        elements.append(total_table)
        
        # Validez del presupuesto y notas en la misma línea si es posible
        validity_days = budget_data.get('validity_days', 1)
        elements.append(Spacer(1, 10))
        
        # Crear tabla para validez y notas en una sola línea
        footer_info = self._create_footer_info(validity_days, budget_data.get('notes'))
        elements.append(footer_info)
        
        # Generar PDF
        doc.build(elements)
        return save_path
    
    def _get_company_info(self):
        """Información de la empresa - personalizable"""
        company_text = """
        <b>NESTOR PALACIOS ELECTRICIDAD E ILUMINACIÓN</b><br/>
        Martín Gil 142 | Tel: +54 9 3584 37-2313 | nestorpalacios032017@gmail.com | CUIT: 20-25582386-9
        """
        return Paragraph(company_text, self.styles['CompanyInfo'])
    
    def _create_budget_info_table(self, budget_data):
        """Crear tabla con información del presupuesto y cliente"""
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Información en formato más limpio y legible
        data = [
            ['Presupuesto N°:', budget_data['budget_number'], '', 'Fecha:', current_date],
            ['', '', '', '', ''],  # Fila vacía como separador
            ['Cliente:', budget_data['client_name'], '', '', ''],
            ['Documento:', budget_data['client_doc'], '', '', ''],
            ['Dirección:', budget_data.get('client_address', ''), '', '', '']
        ]
        
        table = Table(data, colWidths=[1.2*inch, 2.5*inch, 0.3*inch, 0.8*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (3, 0), (3, 0), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            
            # Si querés una fila específica más compacta (por ejemplo, fila 1):
            ('FONTSIZE', (0, 1), (-1, 1), 4),
            ('TOPPADDING', (0, 1), (-1, 1), 0),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 0),
        ]))

        return table
    
    def _create_products_table(self, items):
        """Crear tabla de productos"""
        # Encabezados
        headers = ['Cant.', 'Descripción', 'Marca', 'P. Unit.', 'Subtotal']
        data = [headers]
        
        # Agregar productos
        for item in items:
            row = [
                str(item['quantity']),
                item['description'],
                item['brand'],
                f"${item['unit_price']:.2f}",
                f"${item['subtotal']:.2f}"
            ]
            data.append(row)
        
        # Crear tabla con anchos optimizados
        table = Table(data, colWidths=[0.5*inch, 3.2*inch, 1.3*inch, 0.8*inch, 0.9*inch])
        
        # Aplicar estilos más compactos
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Reducido
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Reducido de 9
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes más finos
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Padding reducido
            ('LEFTPADDING', (0, 0), (-1, -1), 3),  # Reducido
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),  # Reducido
            ('TOPPADDING', (0, 0), (-1, -1), 3),  # Reducido
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Reducido
        ]))
        
        return table
    
    def _create_total_table(self, total):
        """Crear tabla con el total"""
        data = [['TOTAL:', f'${total:.2f}']]
        
        table = Table(data, colWidths=[5.5*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),  # Reducido de 12
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.black),  # Borde más fino
            ('LEFTPADDING', (0, 0), (-1, -1), 4),  # Reducido
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),  # Reducido
            ('TOPPADDING', (0, 0), (-1, -1), 4),  # Reducido
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Reducido
        ]))
        
        return table
    
    def _create_footer_info(self, validity_days, notes):
        """Crear información del pie de página compacta"""
        validity_text = Paragraph(f"<b>Validez del presupuesto:</b> {validity_days} días")
        
        if notes:
            # Si hay notas, crear una tabla de dos columnas
            data = [[validity_text, Paragraph(f"<b>Observaciones:</b> {notes}")]]
            table = Table(data, colWidths=[2*inch, 4.7*inch])
        else:
            # Si no hay notas, solo mostrar validez
            data = [[validity_text]]
            table = Table(data, colWidths=[6.7*inch])
        
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),  # Tamaño pequeño
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        return table