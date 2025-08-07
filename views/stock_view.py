import tkinter as tk
from tkinter import ttk, messagebox
import random

class StockView:
    def __init__(self, parent, controller=None):
        self.controller = controller
        self.frame = tk.Frame(parent, bg="#076397")
        self.setup_variables()
        self.create_widgets()
        
    def set_controller(self, controller):
        """Asignar controller después de la inicialización"""
        print(f"DEBUG: Asignando controller: {controller}")
        self.controller = controller
        print(f"DEBUG: Controller asignado correctamente: {self.controller}")
        
    def setup_variables(self):
        """Configurar variables del formulario"""
        self.item_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.brand_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.price2_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.iva_var = tk.StringVar(value="21%")
        self.qnt_to_add = tk.StringVar(value=1)
        self.iva_included_var = tk.StringVar(value="-")
        
        # Configurar traces DESPUÉS de crear las variables
        self.price_var.trace_add("write", self.update_price_preview)
        self.iva_var.trace_add("write", self.update_price_preview)
        
        # Lista de variables para fácil acceso
        self.form_vars = [
            self.item_id_var,
            self.name_var,
            self.brand_var,
            self.price_var,
            self.price2_var,
            self.quantity_var,
            self.iva_var,
        ]
    
    def create_widgets(self):
        """Crear todos los widgets de la vista"""
        self.create_buttons_frame()
        self.create_form_frame()
        self.create_tree_frame()
    
    def create_buttons_frame(self):
        """Crear frame para botones de stock"""
        manage_frame = tk.LabelFrame(self.frame, text='Opción', borderwidth=5)
        manage_frame.grid(row=0, column=0, sticky='w', padx=[10,20], pady=20, ipadx=[6])

        btnColor = "#FFFFFF"

        save_btn = tk.Button(manage_frame, text="GUARDAR", width=10, borderwidth=3, bg=btnColor, fg='black', 
                            command=lambda: self.controller.save_product())
        update_btn = tk.Button(manage_frame, text="ACTUALIZAR", width=10, borderwidth=3, bg=btnColor, fg='black', 
                              command=lambda: self.controller.update_product())
        select_btn = tk.Button(manage_frame, text="SELECCIONAR", width=10, borderwidth=3, bg=btnColor, fg='black', 
                              command=lambda: self.controller.select_product())
        delete_btn = tk.Button(manage_frame, text="BORRAR", width=10, borderwidth=3, bg=btnColor, fg='black', 
                              command=lambda: self.controller.delete_product())
        find_btn = tk.Button(manage_frame, text="BUSCAR", width=10, borderwidth=3, bg=btnColor, fg='black', 
                            command=lambda: self.controller.find_product())
        clear_btn = tk.Button(manage_frame, text="LIMPIAR", width=10, borderwidth=3, bg=btnColor, fg='black', 
                             command=self.clear_form)
        add_btn = tk.Button(manage_frame, text="AGREGAR", width=10, borderwidth=3, bg=btnColor, fg='black', 
                           command=lambda: self.controller.add_to_sales())

        save_btn.grid(row=0, column=0, padx=5, pady=5)
        update_btn.grid(row=0, column=1, padx=5, pady=5)
        select_btn.grid(row=0, column=2, padx=5, pady=5)
        delete_btn.grid(row=0, column=3, padx=5, pady=5)
        find_btn.grid(row=0, column=4, padx=5, pady=5)
        clear_btn.grid(row=0, column=5, padx=5, pady=5)
        add_btn.grid(row=0, column=6, padx=5, pady=5)
        

        self.qnt_to_add_entry = ttk.Entry(manage_frame, width=2, textvariable=self.qnt_to_add)
        self.qnt_to_add_entry.grid(row=0, column=7, padx=5, pady=5)

    def create_form_frame(self):
        """Crear frame para formulario de producto"""
        entries_frame = tk.LabelFrame(self.frame, text="Form", borderwidth=5)
        entries_frame.grid(row=1, column=0, sticky='w', padx=[10,200], pady=[0,20], ipadx=[6])

        # Botón generar ID
        generate_id_btn = tk.Button(entries_frame, text="GENERAR ID", borderwidth=3, bg="#FFFFFF", fg='black', 
                                   command=self.generate_random_id)
        generate_id_btn.grid(row=0, column=3, padx=5, pady=5)

        # Labels
        tk.Label(entries_frame, text='ID', anchor='e', width=10).grid(row=0, column=0, padx=10)
        tk.Label(entries_frame, text='NOMBRE', anchor='e', width=10).grid(row=1, column=0, padx=10)
        tk.Label(entries_frame, text='MARCA', anchor='e', width=10).grid(row=2, column=0, padx=10)
        tk.Label(entries_frame, text='P. COSTO', anchor='e', width=10).grid(row=3, column=0, padx=10)
        tk.Label(entries_frame, text='P. VENTA', anchor='e', width=10).grid(row=4, column=0, padx=10)
        tk.Label(entries_frame, text='CANTIDAD', anchor='e', width=10).grid(row=5, column=0, padx=10)

        tk.Label(entries_frame, text='IVA', anchor='e', width=2).grid(row=3, column=4)

        # Label para mostrar costo + IVA
        tk.Label(entries_frame, text="COSTO + IVA:", fg='black').grid(row=4, column=3, sticky='e', padx=5)
        self.iva_label = tk.Label(entries_frame, textvariable=self.iva_included_var, fg='black')
        self.iva_label.grid(row=4, column=4, sticky='w', padx=5)

        # Entries
        self.item_id_entry = tk.Entry(entries_frame, width=50, textvariable=self.item_id_var)
        self.name_entry = tk.Entry(entries_frame, width=50, textvariable=self.name_var)
        self.brand_entry = tk.Entry(entries_frame, width=50, textvariable=self.brand_var)
        self.price_entry = tk.Entry(entries_frame, width=50, textvariable=self.price_var)
        self.price2_entry = tk.Entry(entries_frame, width=50, textvariable=self.price2_var)
        self.quantity_entry = tk.Entry(entries_frame, width=50, textvariable=self.quantity_var)

        # Combobox para IVA
        iva = ['21%', '10.5%', '0%']
        self.iva_combo = ttk.Combobox(entries_frame, width=5, textvariable=self.iva_var, values=iva, state='readonly')
        self.iva_combo.grid(row=3, column=3, padx=5)

        # Grid layout para entries
        self.item_id_entry.grid(row=0, column=2, padx=5, pady=5)
        self.name_entry.grid(row=1, column=2, padx=5, pady=5)
        self.brand_entry.grid(row=2, column=2, padx=5, pady=5)
        self.price_entry.grid(row=3, column=2, padx=5, pady=5)
        self.price2_entry.grid(row=4, column=2, padx=5, pady=5)
        self.quantity_entry.grid(row=5, column=2, padx=5, pady=5)

    def create_tree_frame(self):
        """Crear frame para tabla de stock"""
        tree_frame = tk.Frame(self.frame)
        tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Treeview
        self.stock_tree = ttk.Treeview(tree_frame, show="headings", height=10)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.stock_tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.stock_tree.configure(yscrollcommand=scrollbar.set)

        self.stock_tree['columns'] = ('Item Id', "Name", "Brand", "Price", "Price2", "Quantity")
        self.stock_tree['displaycolumns'] = self.stock_tree['columns']
        self.stock_tree.column("Item Id", anchor=tk.W, width=80, stretch=False)
        self.stock_tree.column("Name", anchor=tk.W, width=350, stretch=False)   # Aumentado
        self.stock_tree.column("Brand", anchor=tk.W, width=180, stretch=False)
        self.stock_tree.column("Price", anchor=tk.W, width=100, stretch=False)
        self.stock_tree.column("Price2", anchor=tk.W, width=100, stretch=False)
        self.stock_tree.column("Quantity", anchor=tk.W, width=60, stretch=False)

        self.stock_tree.heading('Item Id', text='Código', anchor=tk.W)
        self.stock_tree.heading('Name', text='Descripción', anchor=tk.W)
        self.stock_tree.heading('Brand', text='Marca', anchor=tk.W)
        self.stock_tree.heading('Price', text='Precio Costo', anchor=tk.W)
        self.stock_tree.heading('Price2', text='Precio Venta', anchor=tk.W)
        self.stock_tree.heading('Quantity', text='Cantidad', anchor=tk.W)
        

        self.stock_tree.tag_configure('orow', background="#FFFFFF")
        self.stock_tree.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="nsew")

    def generate_random_id(self):
        """Generar ID aleatorio para producto"""
        numeric = '1234567890'
        item_id = ''
        for i in range(4):
            randno = random.randrange(0, len(numeric))
            item_id += numeric[randno]
        self.item_id_var.set(item_id)

    def get_form_data(self):
        """Obtener datos del formulario"""
        return {
            'id': self.item_id_var.get().strip(),
            'name': self.name_var.get().strip(),
            'brand': self.brand_var.get().strip(),
            'price': self.price_var.get().strip(),
            'price2': self.price2_var.get().strip(),
            'quantity': self.quantity_var.get().strip(),
            'iva': self.iva_var.get().strip()
        }

    def set_form_data(self, data):
        """Establecer datos en el formulario"""
        if len(data) >= 6:
            self.item_id_var.set(data[0])
            self.name_var.set(data[1])
            self.brand_var.set(data[2])
            self.price_var.set(data[3])
            self.price2_var.set(data[4])
            self.quantity_var.set(data[5])

    def clear_form(self):
        """Limpiar formulario"""
        for var in self.form_vars:
            if var == self.iva_var:
                var.set('21%')
            else:
                var.set('')
        # Resetear la preview del IVA
        self.iva_included_var.set('-')

    def get_selected_product(self):
        """Obtener producto seleccionado del tree"""
        try:
            selected_item = self.stock_tree.selection()[0]
            values = self.stock_tree.item(selected_item)['values']
            product_id = str(values[0]).zfill(4)
            
            return {
                'id': product_id,
                'name': values[1],
                'brand': values[2],
                'price': float(values[3]),
                'price2': float(values[4]),
                'quantity': int(values[5]),
            }
        except (IndexError, ValueError):
            return None

    def refresh_stock_table(self, products):
        """Refrescar tabla de stock con nuevos datos"""
        # Limpiar tabla actual
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        # Agregar productos
        for product in products:
            self.stock_tree.insert(parent='', index='end', iid=product[0], text="", 
                                  values=product, tag="orow")
        
        self.stock_tree.tag_configure('orow', background="white", foreground='black')

    def update_price_preview(self, *args):
        """Actualizar preview del costo + IVA"""
        try:
            # Obtener precio costo
            cost_str = self.price_var.get().strip()
            if not cost_str:
                self.iva_included_var.set("-")
                return
            
            cost = float(cost_str)
            
            # Obtener porcentaje de IVA
            iva_str = self.iva_var.get().strip()
            if iva_str == "21%":
                iva_multiplier = 1.21
            elif iva_str == "10.5%":
                iva_multiplier = 1.105
            elif iva_str == "0%":
                iva_multiplier = 1.0
            else:
                iva_multiplier = 1.21  # Default a 21%
            
            # Calcular costo con IVA
            cost_with_iva = round(cost * iva_multiplier, 2)
            
            # Mostrar resultado
            self.iva_included_var.set(f"${cost_with_iva:.2f}")
            
        except (ValueError, AttributeError) as e:
            self.iva_included_var.set("-")
            print(f"Error calculando IVA: {e}")

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