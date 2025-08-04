import tkinter as tk
from tkinter import ttk
from views.sales_view import SalesView
from views.stock_view import StockView
from controllers.sales_controller import SalesController
from controllers.stock_controller import StockController

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_tabs()
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title("Gestión de Stock y Ventas")
        self.root.geometry("1080x720")
        self.root.resizable(False, False)
        
    def create_tabs(self):
        """Crear pestañas y configurar MVC"""
        # Crear notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')
        
        # Crear vistas
        self.sales_view = SalesView(notebook)
        self.stock_view = StockView(notebook)
        
        # Crear controladores
        self.sales_controller = SalesController(self.sales_view, self.stock_view)
        self.stock_controller = StockController(self.stock_view, self.sales_view)
        
        # Conectar controladores con vistas
        self.sales_view.controller = self.sales_controller
        self.stock_view.controller = self.stock_controller
        
        
        # Establecer referencias cruzadas entre controladores
        self.sales_controller.set_stock_view(self.stock_view)
        self.stock_controller.set_sales_view(self.sales_view)
        
        # Agregar pestañas al notebook
        notebook.add(self.sales_view.frame, text="Venta")
        notebook.add(self.stock_view.frame, text="Administrar Stock")
        
        # Cargar datos iniciales
        self.load_initial_data()
    
    def load_initial_data(self):
        """Cargar datos iniciales"""
        try:
            # Refrescar tabla de stock
            self.stock_controller.refresh_stock_table()
        except Exception as e:
            print(f"Error cargando datos iniciales: {e}")
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()