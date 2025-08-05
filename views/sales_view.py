import tkinter as tk
from tkinter import ttk, messagebox

class SalesView:
    def __init__(self, parent, controller=None):
        self.controller = controller
        self.frame = tk.Frame(parent, bg="#076397")
        self.setup_variables()
        self.create_widgets()
        
    def setup_variables(self):
        """Configurar variables de la vista"""
        self.customer_name_var = tk.StringVar()
        self.customer_doc_var = tk.StringVar()
        self.customer_iva_var = tk.StringVar(value="Consumidor Final")
        self.customer_address_var = tk.StringVar()
        self.total_var = tk.StringVar()
        self.total_var.set("Total: $0.00")
    
    def create_widgets(self):
        """Crear todos los widgets de la vista"""
        self.create_customer_frame()
        self.create_products_frame()
        self.create_buttons_frame()
        self.create_summary_frame()
    
    def create_customer_frame(self):
        """Crear frame para datos del cliente"""
        customer_frame = tk.Frame(self.frame)
        customer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Labels
        tk.Label(customer_frame, text="NOMBRE").grid(row=0, column=0, sticky="w")
        tk.Label(customer_frame, text="DNI o CUIT").grid(row=1, column=0, sticky="w")
        tk.Label(customer_frame, text="DIRECCIÓN").grid(row=2, column=0, sticky="w")
        tk.Label(customer_frame, text="CONDICIÓN IVA").grid(row=3, column=0, sticky="w")

        # Entries
        self.customer_name_entry = tk.Entry(customer_frame, textvariable=self.customer_name_var, width=40)
        self.customer_doc_entry = tk.Entry(customer_frame, textvariable=self.customer_doc_var, width=40)
        self.customer_address_entry = tk.Entry(customer_frame, textvariable=self.customer_address_var, width=40)

        iva_options = ["Consumidor Final", "Responsable Inscripto", "Exento", "Monotributista"]
        self.customer_iva_combo = ttk.Combobox(customer_frame, textvariable=self.customer_iva_var, 
                                               values=iva_options, width=37, state="readonly")

        # Grid
        self.customer_name_entry.grid(row=0, column=1, padx=(5, 0), pady=2)
        self.customer_doc_entry.grid(row=1, column=1, padx=(5, 0), pady=2)
        self.customer_address_entry.grid(row=2, column=1, padx=(5, 0), pady=2)
        self.customer_iva_combo.grid(row=3, column=1, padx=(5, 0), pady=2)
            
    def create_products_frame(self):
        """Crear frame para lista de productos"""
        # Crear el Treeview para productos
        self.sales_tree = ttk.Treeview(self.frame, show="headings", height=15)

        self.sales_tree['columns'] = ('Item Id', "Name", "Brand", "Price", "Quantity", "Subtotal")
        self.sales_tree.column("#0", width=0, stretch=tk.NO)
        self.sales_tree.column("Item Id", anchor=tk.W, width=80, stretch=False)
        self.sales_tree.column("Name", anchor=tk.W, width=450, stretch=False)
        self.sales_tree.column("Brand", anchor=tk.W, width=120, stretch=False)
        self.sales_tree.column("Price", anchor=tk.W, width=140, stretch=False)
        self.sales_tree.column("Quantity", anchor=tk.W, width=100, stretch=False)
        self.sales_tree.column("Subtotal", anchor=tk.W, width=120, stretch=False)

        self.sales_tree.heading('Item Id', text='Código', anchor=tk.W)
        self.sales_tree.heading('Name', text='Descripción', anchor=tk.W)
        self.sales_tree.heading('Brand', text='Marca', anchor=tk.W)
        self.sales_tree.heading('Price', text='Precio unitario', anchor=tk.W)
        self.sales_tree.heading('Quantity', text='Cantidad', anchor=tk.W)
        self.sales_tree.heading('Subtotal', text='Subtotal', anchor=tk.W)

        self.sales_tree.tag_configure('orow', background="#FFFFFF")
        self.sales_tree.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        

    def create_buttons_frame(self):
        """Crear frame para botones de acción"""
        manage_frame = tk.LabelFrame(self.frame, text='Opción', borderwidth=5)
        manage_frame.grid(row=1, column=0, sticky='w', padx=[10,200], pady=20, ipadx=[6])

        btnColor = "#FFFFFF"

        delete_btn = tk.Button(manage_frame, text="QUITAR ARTICULO", width=10, borderwidth=3, 
                              bg=btnColor, fg='black', command=lambda: self.controller.delete_item() if self.controller else None)
        clear_btn = tk.Button(manage_frame, text="BORRAR TODO", width=10, borderwidth=3, 
                             bg=btnColor, fg='black', command=lambda: self.controller.clear_all() if self.controller else None)
        budget_btn = tk.Button(manage_frame, text="PRESUPUESTO", width=10, borderwidth=3, 
                               bg=btnColor, fg='black', command=lambda: self.controller.generate_budget() if self.controller else None)
        invoice_btn = tk.Button(manage_frame, text="FACTURA", width=10, borderwidth=3, 
                               bg=btnColor, fg='black', command=lambda: self.controller.generate_invoice() if self.controller else None)

        delete_btn.grid(row=0, column=0, padx=5, pady=5)
        clear_btn.grid(row=0, column=1, padx=5, pady=5)
        budget_btn.grid(row=0, column=2, padx=5, pady=5)
        invoice_btn.grid(row=0, column=3, padx=5, pady=5)

    def create_summary_frame(self):
        """Crear frame para resumen/total"""
        summary_frame = tk.LabelFrame(self.frame, text='Total', borderwidth=5)
        summary_frame.grid(row=3, column=0, sticky='w', padx=[10,200], pady=20, ipadx=[6])

        total_label = tk.Label(summary_frame, textvariable=self.total_var, font=('Arial', 12, 'bold'))
        total_label.pack(padx=10, pady=5)
    
    def get_customer_data(self):
        """Obtener datos del cliente del formulario"""
        return {
            'name': self.customer_name_var.get().strip(),
            'document': self.customer_doc_var.get().strip(),
            'address': self.customer_address_var.get().strip(),
            'iva': self.customer_iva_var.get()
        }
    
    def get_selected_products(self):
        """Obtener productos seleccionados del tree"""
        products = []
        for child in self.sales_tree.get_children():
            values = self.sales_tree.item(child)["values"]
            products.append({
                'code': values[0],
                'name': values[1],
                'price': float(values[2]),
                'quantity': int(values[3]),
                'subtotal': float(values[4])
            })
        return products
    
    def clear_products(self):
        """Limpiar lista de productos"""
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        self.update_total()
    
    def delete_selected_product(self):
        """Eliminar producto seleccionado"""
        try:
            selected_item = self.sales_tree.selection()[0]
            self.sales_tree.delete(selected_item)
            self.update_total()
            return True
        except IndexError:
            return False
    
    def add_product_to_tree(self, product_data, quantity_to_add=1):
        """Agregar producto al tree de ventas"""
        # Verificar si el producto ya existe
        for child in self.sales_tree.get_children():
            values = self.sales_tree.item(child)['values']
            if values[0] == product_data['id']:
                # Producto ya existe, incrementar cantidad
                current_quantity = int(values[4])
                new_quantity = current_quantity + quantity_to_add  # Usar quantity_to_add en lugar de 1
                new_subtotal = product_data['price2'] * new_quantity
                self.sales_tree.item(child, values=(
                    product_data['id'],
                    product_data['name'],
                    product_data['brand'],
                    product_data['price2'],
                    new_quantity,
                    new_subtotal
                ))
                self.update_total()
                return
        
        # Producto nuevo, agregarlo
        new_subtotal = product_data['price2'] * quantity_to_add  # Calcular subtotal con quantity_to_add
        self.sales_tree.insert("", "end", values=(
            product_data['id'],
            product_data['name'],
            product_data['brand'],
            product_data['price2'],
            quantity_to_add,
            new_subtotal
        ))
        self.update_total()
    
    def update_total(self):
        """Actualizar el total mostrado"""
        total = 0.0
        for child in self.sales_tree.get_children():
            values = self.sales_tree.item(child)['values']
            total += float(values[5])
        
        self.total_var.set(f"Total: ${total:.2f}")
    
    def clear_customer_form(self):
        """Limpiar formulario del cliente"""
        self.customer_name_var.set("")
        self.customer_doc_var.set("")
        self.customer_address_var.set("")
        self.customer_iva_var.set("Consumidor Final")

    def _on_delete_item_click(self):
        return None
    
    def _on_clear_list_click(self):
        return None
    
    def _on_generate_invoice_click(self):
        return None
    
    def show_success(self, message):
        """Mostrar mensaje de éxito"""
        messagebox.showinfo("Éxito", message)
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        messagebox.showerror("Error", message)
    
    def show_warning(self, message):
        """Mostrar mensaje de advertencia"""
        messagebox.showwarning("Advertencia", message)
    
    def ask_confirmation(self, message):
        """Preguntar confirmación al usuario"""
        return messagebox.askquestion("Confirmación", message) == 'yes'