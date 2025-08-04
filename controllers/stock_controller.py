from models.stock import StockModel
from tkinter import messagebox

class StockController:
    def __init__(self, view, sales_view=None, stock_view=None):
        self.view = view
        self.sales_view = sales_view  # Referencia a la vista de ventas
        self.stock_model = StockModel()
        self.stock_view = stock_view
    
    def set_sales_view(self, sales_view):
        """Establecer referencia a la vista de ventas"""
        self.sales_view = sales_view
    
    def save_product(self):
        """Guardar nuevo producto"""
        try:
            # Obtener datos del formulario
            form_data = self.view.get_form_data()
            
            # Validaciones
            if not self._validate_form_data(form_data):
                return
            
            if not self._validate_product_id(form_data['id']):
                self.view.show_warning("Código del producto inválido. Debe tener 4 dígitos.")
                return
            
            # Convertir tipos
            product_data = {
                'id': form_data['id'],
                'name': form_data['name'],
                'brand': form_data['brand'],
                'price': float(form_data['price']),
                'price2': float(form_data['price2']),
                'quantity': int(form_data['quantity']),
            }

            if form_data['iva'] == "21%":
                product_data['price'] *= 1.21
            else:
                product_data['price'] *= 1.105
            
            # Guardar en base de datos
            self.stock_model.add_product(product_data)
            
            # Refrescar tabla
            self.refresh_stock_table()
            
            # Limpiar formulario
            self.view.clear_form()
            
            self.view.show_success("Producto guardado correctamente")
            
        except ValueError as e:
            self.view.show_error(f"Error en los datos: {str(e)}")
        except Exception as e:
            self.view.show_error(f"Error al guardar producto: {str(e)}")
    
    def update_product(self):
        """Actualizar producto existente"""
        try:
            # Obtener producto seleccionado
            selected_product = self.view.get_selected_product()
            if not selected_product:
                self.view.show_warning("Por favor seleccione una fila con datos")
                return
            
            # Obtener datos del formulario
            form_data = self.view.get_form_data()
            
            # Validaciones
            if not self._validate_form_data(form_data):
                return
            
            # Verificar que no se cambie el ID
            if int(selected_product['id']) != int(form_data['id']):
                self.view.show_warning("No se puede cambiar el código del producto")
                return
            
            # Convertir tipos
            product_data = {
                'name': form_data['name'],
                'brand': form_data['brand'],
                'price': float(form_data['price']),
                'price2': float(form_data['price2']),
                'quantity': int(form_data['quantity']),
            }
            
            # Actualizar en base de datos
            self.stock_model.update_product(form_data['id'], product_data)
            
            # Refrescar tabla
            self.refresh_stock_table()
            
            # Limpiar formulario
            self.view.clear_form()
            
            self.view.show_success("Producto actualizado correctamente")
            
        except ValueError as e:
            self.view.show_error(f"Error en los datos: {str(e)}")
        except Exception as e:
            self.view.show_error(f"Error al actualizar producto: {str(e)}")
    
    def select_product(self):
        """Seleccionar producto y cargar en formulario"""
        try:
            selected_product = self.view.get_selected_product()
            if not selected_product:
                self.view.show_warning("Por favor seleccione una fila")
                return
            
            # Cargar datos en el formulario
            data = [
                selected_product['id'],
                selected_product['name'],
                selected_product['brand'],
                str(selected_product['price']),
                str(selected_product['price2']),
                str(selected_product['quantity'])
            ]
            
            self.view.set_form_data(data)
            
        except Exception as e:
            self.view.show_error(f"Error al seleccionar producto: {str(e)}")
    
    def delete_product(self):
        """Eliminar producto seleccionado"""
        try:
            selected_product = self.view.get_selected_product()
            if not selected_product:
                self.view.show_warning("Por favor seleccione una fila")
                return
            
            if not self.view.ask_confirmation("¿Eliminar el producto seleccionado?"):
                return
            
            # Eliminar de base de datos
            self.stock_model.delete_product(selected_product['id'])
            
            # Refrescar tabla
            self.refresh_stock_table()
            
            self.view.show_success("Producto eliminado correctamente")
            
        except Exception as e:
            self.view.show_error(f"Error al eliminar producto: {str(e)}")
    
    def find_product(self):
        """Buscar producto por ID o nombre"""
        try:
            form_data = self.view.get_form_data()
            item_id = form_data['id']
            name = form_data['name']
            
            if not (item_id or name):
                self.view.show_warning("Ingrese ID o nombre para buscar")
                return
            
            # Buscar en base de datos
            results = self.stock_model.search_products(item_id or name)
            
            if results:
                # Cargar primer resultado en formulario
                self.view.set_form_data(results[0])
            else:
                self.view.show_warning("No se encontraron productos")
                
        except Exception as e:
            self.view.show_error(f"Error al buscar producto: {str(e)}")
    
    def add_to_sales(self):
        """Agregar producto seleccionado a las ventas"""
        try:
            # Obtener la cantidad del Entry usando self.view en lugar de self.stock_view
            quantity_str = self.view.qnt_to_add.get()
            
            # Validar que sea un número válido
            if not quantity_str or quantity_str.strip() == "":
                quantity_to_add = 1  # Valor por defecto si está vacío
            else:
                quantity_to_add = int(quantity_str)
                if quantity_to_add <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
            
            # Obtener los datos del producto seleccionado
            product_data = self.view.get_selected_product()
            
            if product_data:
                # Llamar a add_product_to_tree con la cantidad especificada
                self.sales_view.add_product_to_tree(product_data, quantity_to_add)

                messagebox.showinfo("", f"Se han agregado {quantity_to_add} unidades del articulo {product_data['name']}")
                
                # Opcional: resetear el Entry después de agregar
                self.view.qnt_to_add.set("1")
            else:
                # Manejar caso donde no hay producto seleccionado
                messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Cantidad inválida: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def refresh_stock_table(self):
        """Refrescar tabla de stock"""
        try:
            products = self.stock_model.get_all_products()
            self.view.refresh_stock_table(products)
        except Exception as e:
            self.view.show_error(f"Error al refrescar tabla: {str(e)}")
    
    def _validate_form_data(self, form_data):
        """Validar datos del formulario"""
        required_fields = ['id', 'name', 'brand', 'price', 'price2', 'quantity']
        
        for field in required_fields:
            if not form_data[field]:
                self.view.show_warning("Por favor complete todos los campos")
                return False
        
        # Validar tipos numéricos
        try:
            float(form_data['price'])
            float(form_data['price2'])
            int(form_data['quantity'])
        except ValueError:
            self.view.show_warning("Los precios y cantidad deben ser números válidos")
            return False
        
        return True
    
    def _validate_product_id(self, product_id):
        """Validar formato del ID del producto"""
        if len(product_id) != 4:
            return False
        
        # Verificar que todos sean dígitos
        return product_id.isdigit()