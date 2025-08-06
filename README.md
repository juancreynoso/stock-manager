# Stock Management System

Stock management, sales, PDF quote generation, and invoicing system integrated with AFIP. Developed in Python with a Tkinter graphical interface.

---

## Features

- Product management (stock, brands, categories)
- Sales panel with automatic subtotal and total calculation
- PDF quote generation
- Electronic invoicing (AFIP) in test environment (homologation)
- Persistent SQLite database
- User-friendly graphical interface organized with tabs

---

## Technologies

- Python 3.10+
- Tkinter (GUI)
- SQLite3 (local database)
- ReportLab (PDFs)
- Zeep (for SOAP integration with AFIP)
- PyInstaller (to generate executables)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/juancreynoso/stock-manager.git
cd stock-manager
```

### 2. Create and activate a virtual enviroment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependences

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

---

## Invoicing with AFIP

You’ll need the following:
- Digital certificate associated with your CUIT
- TA (access ticket)
- Fiscal key with necessary services enabled
- Files `test_private.key`, `test_request.csr`, `test.crt`, `TA.xml`, etc.

**Important:** Confidential files are not included in the repository. You must generate them manually and place them in the `certs/` folder.

---

## Build excecutable (Windows)

You can generate an `.exe` file using PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "db/stock.db;db" main.py
```

---

## Autor

Juan Cruz Reynoso
