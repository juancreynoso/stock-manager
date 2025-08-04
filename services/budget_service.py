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
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=1,  # Centrado
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='ClientInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10
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
        
        # Crear documento
        doc = SimpleDocTemplate(save_path, pagesize=A4)
        elements = []
        
        '''
        # Título principal
        title = Paragraph("PRESUPUESTO", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        '''
        
        # Información de la empresa (personalizable)
        company_info = self._get_company_info()
        elements.append(company_info)
        elements.append(Spacer(1, 30))
        
        # Información del presupuesto y cliente
        budget_info = self._create_budget_info_table(budget_data)
        elements.append(budget_info)
        elements.append(Spacer(1, 20))
        
        # Tabla de productos
        products_table = self._create_products_table(budget_data['items'])
        elements.append(products_table)
        elements.append(Spacer(1, 20))
        
        # Total
        total_table = self._create_total_table(budget_data['total'])
        elements.append(total_table)
        
        # Validez del presupuesto
        validity_days = budget_data.get('validity_days', 30)
        validity_text = f"<b>Validez del presupuesto:</b> {validity_days} días"
        validity = Paragraph(validity_text, self.styles['Normal'])
        elements.append(Spacer(1, 20))
        elements.append(validity)
        
        # Notas adicionales si existen
        if budget_data.get('notes'):
            elements.append(Spacer(1, 20))
            notes_title = Paragraph("<b>Observaciones:</b>", self.styles['Normal'])
            notes_content = Paragraph(budget_data['notes'], self.styles['Normal'])
            elements.append(notes_title)
            elements.append(notes_content)
        
        # Generar PDF
        doc.build(elements)
        return save_path
    
    def _get_company_info(self):
        """Información de la empresa - personalizable"""
        company_text = """
        <b>NESTOR PALACIOS ELECTRICIDAD E ILUMINACIÓN</b><br/>
        Dirección: Martín Gil 134<br/>
        Teléfono: +54 9 3584 37-2313<br/>
        Email: nestorpalacios@gmail.com<br/>
        CUIT: 20-12345678-9
        """
        return Paragraph(company_text, self.styles['CompanyInfo'])
    
    def _create_budget_info_table(self, budget_data):
        """Crear tabla con información del presupuesto y cliente"""
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        data = [
            ['Presupuesto N°:', budget_data['budget_number'], 'Fecha:', current_date],
            ['Cliente:', budget_data['client_name'], '', ''],
            ['Dirección:', budget_data.get('client_address', ''), '', ''],
            ['Teléfono:', budget_data.get('client_phone', ''), '', '']
        ]
        
        table = Table(data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # Primera columna en negrita
            ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),   # "Fecha:" en negrita
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        return table
    
    def _create_products_table(self, items):
        """Crear tabla de productos"""
        # Encabezados
        headers = ['Cant.', 'Descripción', 'Marca', 'Precio Unit.', 'Subtotal']
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
        
        # Crear tabla
        table = Table(data, colWidths=[1*inch, 2.5*inch, 1.5*inch, 1*inch, 1*inch])
        
        # Aplicar estilos
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Descripción alineada a la izquierda
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'), # Precios alineados a la derecha
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def _create_total_table(self, total):
        """Crear tabla con el total"""
        data = [['TOTAL:', f'${total:.2f}']]
        
        table = Table(data, colWidths=[5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table