import sqlite3

def guardar_en_sql(piso, empresa, vecino):
    conexion = sqlite3.connect("mi_primera_base.db")
    cursor = conexion.cursor()

    cursor.execute('''
        INSERT INTO paquetes  (piso, empresa, vecino)
        VALUES (?, ?, ?)
    ''', (piso, empresa, vecino))

    conexion.commit()
    conexion.close()

    print(f"¡Paquete para el piso {piso} guardado en SQLite!")

guardar_en_sql("1A", "Seur", "López")
guardar_en_sql("5C", "Correos", "Martínez")