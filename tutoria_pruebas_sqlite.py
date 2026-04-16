import sqlite3

# 1. Conectarnos a la base de datos (Si el archivo no existe, Python lo crea mágicamente)
conexion = sqlite3.connect("mi_primera_base.db")

# 2. Crear un "cursor" (Es como el ratón/puntero que ejecuta nuestras órdenes SQL)
cursor = conexion.cursor()

# 3. Escribir nuestra primera orden SQL: Crear una tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS paquetes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        piso TEXT NOT NULL,
        empresa TEXT NOT NULL,
        vecino TEXT NOT NULL
    )
''')

piso_falso = "4B"
empresa_falsa ="Amazon"
vecino_falso ="Garcia"

cursor.execute('''
 INSERT INTO paquetes(piso, empresa, vecino)
 VALUES (?, ?, ?)
''', (piso_falso, empresa_falsa, vecino_falso))

conexion.commit()
print("¡Paquete insertado en la base de datos!\n")

# 3. READ (Leer la base de datos para comprobar)
# El asterisco (*) significa "tráeme TODAS las columnas"
cursor.execute('SELECT * FROM paquetes')


lista_de_resultados = cursor.fetchall()

print(" Contenido actual de la Base de Datos:")
for fila in lista_de_resultados:
    print(fila)
# Cierre de seguridad    
conexion.close()