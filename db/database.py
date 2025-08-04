import sqlite3
import os

class Database:
    def __init__(self, db_path="db/stock.db"):
        self.db_path = db_path
        self.ensure_db_exists()
        self.create_tables()
    
    def ensure_db_exists(self):
        """Asegurar que el directorio de la base de datos existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """Crear todas las tablas necesarias"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de stock (existente)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    price REAL NOT NULL,
                    price2 REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )
            ''')
            
            # Tabla de facturas (nueva)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS facturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_factura TEXT NOT NULL,
                    fecha_emision TEXT NOT NULL,
                    cae TEXT,
                    fecha_vencimiento_cae TEXT,
                    cliente_nombre TEXT NOT NULL,
                    cliente_cuit TEXT,
                    cliente_domicilio TEXT,
                    cliente_condicion_iva TEXT DEFAULT 'Consumidor Final',
                    subtotal REAL NOT NULL,
                    iva REAL NOT NULL,
                    total REAL NOT NULL,
                    estado TEXT DEFAULT 'autorizada'
                )
            ''')
            
            # Tabla de items de factura (nueva)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS factura_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factura_id INTEGER,
                    producto_id TEXT,
                    producto_nombre TEXT,
                    producto_marca TEXT,
                    cantidad INTEGER,
                    precio_unitario REAL,
                    subtotal REAL,
                    FOREIGN KEY(factura_id) REFERENCES facturas(id),
                    FOREIGN KEY(producto_id) REFERENCES stock(id)
                )
            ''')
            
            conn.commit()
    
    def execute_query(self, query, params=None):
        """Ejecutar una consulta que no devuelve resultados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
    
    def fetch_all(self, query, params=None):
        """Ejecutar una consulta que devuelve múltiples resultados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        """Ejecutar una consulta que devuelve un resultado"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()

# Instancia global de la base de datos
db = Database()