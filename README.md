# 📦 Stock Management System

Sistema de gestión de stock, ventas, generación de presupuestos en PDF y facturación integrada con AFIP. Desarrollado en Python con interfaz gráfica Tkinter.

---

## 🖥️ Características

- Gestión de productos (stock, marcas, categorías)
- Panel de ventas con cálculo automático de subtotal y total
- Generación de presupuestos en PDF
- Facturación electrónica (AFIP) en entorno de homologación
- Base de datos SQLite persistente
- Interfaz gráfica amigable y organizada con pestañas

---

## 🛠️ Tecnologías utilizadas

- Python 3.10+
- Tkinter (GUI)
- SQLite3 (Base de datos local)
- ReportLab (PDFs)
- Zeep (para integración SOAP con AFIP)
- PyInstaller (para generar ejecutables)

---

## ⚙️ Instalación

### 1. Cloná el repositorio

```bash
git clone https://github.com/tuusuario/stock-management-system.git
cd stock-management-system
```

### 2. Creá y activá un entorno virtual (opcional pero recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalá las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutá la aplicación

```bash
python main.py
```

---

## 📄 Facturación con AFIP

El sistema permite generar comprobantes en entorno de prueba (homologación) usando el WS de AFIP.  
Para esto se requiere:

- Certificado digital asociado a CUIT
- TA (ticket de acceso)
- Clave fiscal con servicios habilitados
- Archivos `test_private.key`, `test_request.csr`, `test.crt`, `TA.xml`, etc.

**Importante:** Los archivos confidenciales no están incluidos en el repositorio. Se deben generar manualmente y ubicar en la carpeta `certs/`.

---

## 🧪 Compilar ejecutable (Windows)

Podés generar un `.exe` con PyInstaller:

```bash
pyinstaller --noconsole --onefile main.py
```

Para evitar que la base de datos se borre, asegurate de ubicarla en una ruta fuera del bundle generado.

---

## 🔐 .gitignore recomendado

```gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
*.spec
dist/
build/
venv/
certs/*.key
certs/*.csr
certs/*.crt
certs/TA.xml
presupuestos/
```

---

## 👨‍💻 Autor

Juan Cruz Reynoso
