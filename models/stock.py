from db.database import db

class StockModel:
    def __init__(self):
        pass
    
    def get_all_products(self):
        """Obtener todos los productos del stock"""
        query = "SELECT id, name, brand, price, price2, quantity FROM stock ORDER BY name"
        return db.fetch_all(query)
    
    def get_product_by_id(self, product_id):
        """Obtener un producto por su ID"""
        query = "SELECT id, name, brand, price, price2, quantity FROM stock WHERE id = ?"
        return db.fetch_one(query, (product_id,))
    
    def add_product(self, product_data):
        """Agregar un nuevo producto"""
        query = """
            INSERT INTO stock (id, name, brand, price, price2, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            product_data['id'],
            product_data['name'],
            product_data['brand'],
            product_data['price'],
            product_data['price2'],
            product_data['quantity'],
        )
        return db.execute_query(query, params)
    
    def update_product(self, product_id, product_data):
        """Actualizar un producto existente"""
        query = """
            UPDATE stock 
            SET name = ?, brand = ?, price = ?, price2 = ?, quantity = ?
            WHERE id = ?
        """
        params = (
            product_data['name'],
            product_data['brand'],
            product_data['price'],
            product_data['price2'],
            product_data['quantity'],
            product_id
        )
        return db.execute_query(query, params)
    
    def delete_product(self, product_id):
        """Eliminar un producto"""
        query = "DELETE FROM stock WHERE id = ?"
        return db.execute_query(query, (product_id,))
    
    def update_quantity(self, product_id, new_quantity):
        """Actualizar solo la cantidad de un producto"""
        query = "UPDATE stock SET quantity = ? WHERE id = ?"
        return db.execute_query(query, (new_quantity, product_id))
    
    def reduce_quantity(self, product_id, quantity_to_reduce):
        """Reducir la cantidad de un producto (para ventas)"""
        # Primero obtener la cantidad actual
        current_product = self.get_product_by_id(product_id)
        if not current_product:
            raise ValueError(f"Producto {product_id} no encontrado")
        
        current_quantity = current_product[4]  # quantity está en el índice 4
        
        if current_quantity < quantity_to_reduce:
            raise ValueError(f"Stock insuficiente. Disponible: {current_quantity}, Solicitado: {quantity_to_reduce}")
        
        new_quantity = current_quantity - quantity_to_reduce
        return self.update_quantity(product_id, new_quantity)
    
    def search_products(self, search_term):
        """Buscar productos por nombre o ID"""
        query = """
            SELECT id, name, brand, price, price2, quantity 
            FROM stock 
            WHERE name LIKE ? OR id LIKE ?
            ORDER BY name
        """
        search_pattern = f"%{search_term}%"
        return db.fetch_all(query, (search_pattern, search_pattern))
    
    def get_products_by_category(self, category):
        """Obtener productos por categoría"""
        query = """
            SELECT id, name, price, price2, quantity, category 
            FROM stock 
            WHERE category = ?
            ORDER BY name
        """
        return db.fetch_all(query, (category,))
    
    def get_categories(self):
        """Obtener todas las categorías únicas"""
        query = "SELECT DISTINCT category FROM stock ORDER BY category"
        results = db.fetch_all(query)
        return [row[0] for row in results]
    
    def get_low_stock_products(self, threshold=5):
        """Obtener productos con stock bajo"""
        query = """
            SELECT id, name, price, price2, quantity, category 
            FROM stock 
            WHERE quantity <= ?
            ORDER BY quantity ASC
        """
        return db.fetch_all(query, (threshold,))