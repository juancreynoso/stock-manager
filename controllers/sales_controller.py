from services.invoice_service import InvoiceService
from services.budget_service import BudgetService
from tkinter import messagebox, simpledialog
import random

class SalesController:
    def __init__(self, view, stock_view=None):
        self.view = view
        self.stock_view = stock_view  # Referencia a la vista de stock
        self.invoice_service = InvoiceService()
        self.budget_service = BudgetService()
    
    def set_stock_view(self, stock_view):
        """Establecer referencia a la vista de stock"""
        self.stock_view = stock_view
    
    def delete_item(self):
        """Eliminar item seleccionado de la lista de ventas"""
        if not self.view.ask_confirmation("¿Quitar artículo?"):
            return
            
        if self.view.delete_selected_product():
            self.view.update_total()
        else:
            self.view.show_warning("Seleccione el artículo que desea quitar.")
    
    def clear_all(self):
        """Limpiar toda la lista de ventas"""
        self.view.clear_products()
    
    def generate_invoice(self):
        """Generar factura completa"""
        try:
            # Obtener datos del cliente
            customer_data = self.view.get_customer_data()
            
            # Obtener productos
            products_data = self.view.get_selected_products()
            
            # Validaciones básicas
            if not products_data:
                self.view.show_warning("No hay artículos para facturar.")
                return
            
            if not customer_data['nombre']:
                self.view.show_error("El nombre del cliente es obligatorio")
                return
            
            # Mostrar confirmación con resumen
            total = sum(product['subtotal'] for product in products_data)
            confirmation_msg = f"¿Generar factura por ${total:.2f} para {customer_data['nombre']}?"
            
            if not self.view.ask_confirmation(confirmation_msg):
                return
            
            # Generar factura
            result = self.invoice_service.create_invoice(customer_data, products_data)
            
            if result['success']:
                # Éxito
                success_msg = f"Factura {result['numero_factura']} generada correctamente\n"
                success_msg += f"CAE: {result['cae']}\n"
                success_msg += f"Total: ${result['total']:.2f}\n"
                success_msg += f"PDF: {result['pdf_filename']}"
                
                self.view.show_success(success_msg)
                
                # Limpiar formularios
                self.view.clear_products()
                self.view.clear_customer_form()
                
                # Refrescar stock si hay referencia
                if self.stock_view and hasattr(self.stock_view, 'controller'):
                    self.stock_view.controller.refresh_stock_table()
                
            else:
                # Error
                self.view.show_error(f"Error al generar factura:\n{result['error']}")
                
        except Exception as e:
            self.view.show_error(f"Error inesperado: {str(e)}")
    
    def add_product_from_stock(self, product_data):
        """Agregar producto desde el stock a la lista de ventas"""
        try:
            # Verificar stock disponible
            if product_data['quantity'] <= 0:
                self.view.show_warning(f"El producto {product_data['name']} no tiene stock disponible.")
                return False
            
            # Verificar si el producto ya está en la lista
            current_products = self.view.get_selected_products()
            for product in current_products:
                if product['code'] == product_data['id']:
                    current_quantity = product['quantity']
                    if current_quantity + 1 > product_data['quantity']:
                        self.view.show_warning(f"Stock insuficiente. Solo hay {product_data['quantity']} unidades disponibles.")
                        return False
            
            # Agregar producto a la vista
            self.view.add_product_to_tree(product_data)
            return True
            
        except Exception as e:
            self.view.show_error(f"Error al agregar producto: {str(e)}")
            return False
    
    def generate_budget(self):
        """Generar presupuesto con los productos en el tree"""
        try:
            # Verificar que hay productos en el tree
            items = self.view.sales_tree.get_children()
            if not items:
                messagebox.showwarning("Advertencia", "No hay productos para generar el presupuesto")
                return
            
            # Recuperar datos del cliente del formulario
            client_data = self.view.get_customer_data()
            
            if not client_data['name']:
                messagebox.showwarning("Advertencia", "Debe ingresar el nombre del cliente")
                return

            if not client_data:
                messagebox.showwarning("Advertencia", "No hay datos del cliente")
                return
            
            extra_data = self._get_client_data_for_budget()

            # Recopilar productos del tree
            products = []
            total = 0
            
            for item_id in items:
                values = self.view.sales_tree.item(item_id)['values']
                product = {
                    'quantity': int(values[4]),
                    'description': values[1],  # nombre del producto
                    'brand': values[2],  # obtener marca por ID
                    'unit_price': float(values[3]),
                    'subtotal': float(values[5])
                }
                products.append(product)
                total += product['subtotal']
            
            # Generar número de presupuesto
            budget_number = self._generate_budget_number()

            
            # Preparar datos del presupuesto
            budget_data = {
                'budget_number': budget_number,
                'client_name': client_data['name'],
                'client_address': client_data.get('address', ''),
                'client_doc': client_data.get('document', ''),
                'client_phone': client_data.get('phone', ''),
                'items': products,
                'total': total,
                'validity_days': extra_data.get('validity_days', 1),
                'notes': extra_data.get('notes', '')
            }
            
            # Generar presupuesto
            pdf_path = self.budget_service.generate_budget(budget_data)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Presupuesto generado correctamente:\n{pdf_path}")
            
            # Opcional: abrir el PDF automáticamente
            self._open_pdf(pdf_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar presupuesto: {str(e)}")

    def _get_client_data_for_budget(self):
        """Solicitar datos del cliente para el presupuesto"""
        try:
            
            '''
            # Datos básicos (obligatorios)
            client_name = simpledialog.askstring("Cliente", "Nombre del cliente:")
            if not client_name:
                return None
            
            # Datos opcionales
            client_address = simpledialog.askstring("Cliente", "Dirección (opcional):") or ""
            client_phone = simpledialog.askstring("Cliente", "Teléfono (opcional):") or ""
            
            '''
            
            # Validez del presupuesto
            validity_str = simpledialog.askstring("Presupuesto", "Validez en días (por defecto: 1):") or "1"
            try:
                validity_days = int(validity_str)
            except ValueError:
                validity_days = 1
            
            # Notas adicionales
            notes = simpledialog.askstring("Presupuesto", "Observaciones (opcional):") or ""
            
            return {
                '''
                    'name': client_name,
                    'address': client_address,
                    'phone': client_phone,
                '''
                'validity_days': validity_days,
                'notes': notes
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener datos del cliente: {str(e)}")
            return None

    def _get_product_brand(self, product_id):
        """Obtener marca del producto por ID"""
        try:
            # Si tienes acceso al stock_view, puedes buscar la marca
            if self.stock_view and hasattr(self.stock_view, 'stock_model'):
                product = self.stock_view.stock_model.get_product_by_id(product_id)
                if product:
                    return product.get('brand', 'N/A')
            
            # Si no tienes acceso, retornar valor por defecto
            return 'N/A'
            
        except Exception:
            return 'N/A'

    def _generate_budget_number(self):
        """Generar número de presupuesto único"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d")
        random_num = random.randint(1000, 9999)
        return f"PPTO-{timestamp}-{random_num}"

    def _open_pdf(self, pdf_path):
        """Abrir PDF automáticamente"""
        try:
            import os
            import platform
            
            if platform.system() == 'Darwin':  # macOS
                os.system(f'open "{pdf_path}"')
            elif platform.system() == 'Windows':  # Windows
                os.system(f'start "" "{pdf_path}"')
            else:  # Linux
                os.system(f'xdg-open "{pdf_path}"')
                
        except Exception as e:
            print(f"No se pudo abrir el PDF automáticamente: {e}")