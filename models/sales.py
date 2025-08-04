from db.database import db
from datetime import datetime

class SalesModel:
    def __init__(self):
        pass
    
    def create_invoice(self, invoice_data, items_data):
        """Crear una nueva factura con sus items"""
        try:
            # Insertar la factura
            invoice_query = """
                INSERT INTO facturas (
                    numero_factura, fecha_emision, cae, fecha_vencimiento_cae,
                    cliente_nombre, cliente_cuit, cliente_domicilio, cliente_condicion_iva,
                    subtotal, iva, total, estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            invoice_params = (
                invoice_data['numero_factura'],
                invoice_data['fecha_emision'],
                invoice_data.get('cae'),
                invoice_data.get('fecha_vencimiento_cae'),
                invoice_data['cliente_nombre'],
                invoice_data.get('cliente_cuit'),
                invoice_data.get('cliente_domicilio'),
                invoice_data.get('cliente_condicion_iva', 'Consumidor Final'),
                invoice_data['subtotal'],
                invoice_data['iva'],
                invoice_data['total'],
                invoice_data.get('estado', 'autorizada')
            )
            
            # Ejecutar inserción de factura
            invoice_id = db.execute_query(invoice_query, invoice_params)
            
            # Insertar los items de la factura
            for item in items_data:
                self.add_invoice_item(invoice_id, item)
            
            return invoice_id
            
        except Exception as e:
            raise Exception(f"Error al crear factura: {str(e)}")
    
    def add_invoice_item(self, invoice_id, item_data):
        """Agregar un item a una factura"""
        query = """
            INSERT INTO factura_items (
                factura_id, producto_id, producto_nombre, 
                cantidad, precio_unitario, subtotal
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        
        params = (
            invoice_id,
            item_data['producto_id'],
            item_data['producto_nombre'],
            item_data['cantidad'],
            item_data['precio_unitario'],
            item_data['subtotal']
        )
        
        return db.execute_query(query, params)
    
    def get_invoice_by_id(self, invoice_id):
        """Obtener una factura por ID"""
        query = """
            SELECT id, numero_factura, fecha_emision, cae, fecha_vencimiento_cae,
                   cliente_nombre, cliente_cuit, cliente_domicilio, cliente_condicion_iva,
                   subtotal, iva, total, estado
            FROM facturas 
            WHERE id = ?
        """
        return db.fetch_one(query, (invoice_id,))
    
    def get_invoice_items(self, invoice_id):
        """Obtener los items de una factura"""
        query = """
            SELECT id, factura_id, producto_id, producto_nombre,
                   cantidad, precio_unitario, subtotal
            FROM factura_items 
            WHERE factura_id = ?
        """
        return db.fetch_all(query, (invoice_id,))
    
    def get_all_invoices(self, limit=100):
        """Obtener todas las facturas (limitadas)"""
        query = """
            SELECT id, numero_factura, fecha_emision, cliente_nombre, total, estado
            FROM facturas 
            ORDER BY fecha_emision DESC, id DESC
            LIMIT ?
        """
        return db.fetch_all(query, (limit,))
    
    def update_invoice_cae(self, invoice_id, cae, fecha_vencimiento_cae):
        """Actualizar el CAE de una factura"""
        query = """
            UPDATE facturas 
            SET cae = ?, fecha_vencimiento_cae = ?, estado = 'autorizada'
            WHERE id = ?
        """
        return db.execute_query(query, (cae, fecha_vencimiento_cae, invoice_id))
    
    def get_next_invoice_number(self):
        """Obtener el próximo número de factura"""
        query = "SELECT MAX(CAST(SUBSTR(numero_factura, -8) AS INTEGER)) FROM facturas"
        result = db.fetch_one(query)
        
        if result[0] is None:
            return "0001-00000001"
        else:
            next_number = result[0] + 1
            return f"0001-{next_number:08d}"
    
    def search_invoices(self, search_term):
        """Buscar facturas por número o cliente"""
        query = """
            SELECT id, numero_factura, fecha_emision, cliente_nombre, total, estado
            FROM facturas 
            WHERE numero_factura LIKE ? OR cliente_nombre LIKE ?
            ORDER BY fecha_emision DESC
        """
        search_pattern = f"%{search_term}%"
        return db.fetch_all(query, (search_pattern, search_pattern))
    
    def get_invoices_by_date_range(self, start_date, end_date):
        """Obtener facturas en un rango de fechas"""
        query = """
            SELECT id, numero_factura, fecha_emision, cliente_nombre, total, estado
            FROM facturas 
            WHERE fecha_emision BETWEEN ? AND ?
            ORDER BY fecha_emision DESC
        """
        return db.fetch_all(query, (start_date, end_date))
    
    def get_sales_summary(self, start_date=None, end_date=None):
        """Obtener resumen de ventas"""
        if start_date and end_date:
            query = """
                SELECT 
                    COUNT(*) as total_facturas,
                    SUM(total) as total_ventas,
                    AVG(total) as promedio_venta
                FROM facturas 
                WHERE fecha_emision BETWEEN ? AND ? AND estado = 'autorizada'
            """
            return db.fetch_one(query, (start_date, end_date))
        else:
            query = """
                SELECT 
                    COUNT(*) as total_facturas,
                    SUM(total) as total_ventas,
                    AVG(total) as promedio_venta
                FROM facturas 
                WHERE estado = 'autorizada'
            """
            return db.fetch_one(query)