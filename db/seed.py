import sqlite3

# Ruta a tu base de datos
DB_PATH = "stock.db"

productos = [
    ("1001", "LÁMPARA LED 9W E27", "PHILIPS", 400.0, 650.0, 150),
    ("1002", "LÁMPARA LED 12W E27", "OSRAM", 480.0, 800.0, 100),
    ("1003", "TUBO LED 18W 120CM", "GENÉRICO", 900.0, 1300.0, 80),
    ("1004", "PORTALÁMPARAS PLÁSTICO", "SICA", 150.0, 250.0, 300),
    ("1005", "TECLA SENCILLA MODENA", "JELUZ", 180.0, 280.0, 500),
    ("1006", "LLAVE TERMOMAGNÉTICA 16A", "SICA", 950.0, 1400.0, 60),
    ("1007", "CABLE 2.5MM ROLLO X 100M", "INDELPLAS", 10500.0, 14500.0, 20),
    ("1008", "CAJA OCTOGONAL METÁLICA", "GENÉRICO", 300.0, 500.0, 200),
    ("1009", "FOCO DICROICA LED 7W GU10", "PHILIPS", 550.0, 950.0, 120),
    ("1010", "ARTEFACTO PLAFÓN REDONDO LED 18W", "SICA", 1800.0, 2500.0, 40),
    ("1011", "VARILLA ROSCADA 1M", "GENÉRICO", 200.0, 350.0, 100),
    ("1012", "CINTA AISLADORA NEGRA", "3M", 180.0, 290.0, 300),
    ("1013", "TOMACORRIENTE DOBLE MODENA", "JELUZ", 700.0, 1100.0, 150),
    ("1014", "INTERRUPTOR DOBLE MODENA", "JELUZ", 680.0, 1050.0, 120),
    ("1015", "LLAVE TERMOMAGNÉTICA 25A", "SICA", 1100.0, 1600.0, 50),
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for prod in productos:
        cursor.execute("""
            INSERT INTO stock (id, name, brand, price, price2, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, prod)

    conn.commit()
    conn.close()
    print("✔ Productos insertados correctamente.")

if __name__ == "__main__":
    seed()
