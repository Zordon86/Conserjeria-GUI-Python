import json
import tkinter as tk 
from tkinter import messagebox
from modelos_conserjeria_V2 import Paquete

estanteria = []
historial_entregados = []

#Función para ver el historial de entregas 
def ver_historial():
    
    texto_salida = f"\nActualmente hay {len(historial_entregados)}\n"

    for paquete in historial_entregados:
        texto_salida +=f"\n Piso: {paquete.piso}"

    messagebox.showinfo("Consulta entregados", texto_salida)

def historial_entregados_json():
    estanteria_traducida = []
    
    for paquete in historial_entregados:
        estanteria_traducida.append(paquete.a_diccionario())

    with open("historial_general.json", "w") as archivo:
        texto_traducido = json.dumps(estanteria_traducida, indent=4)
        archivo.write(texto_traducido)

#Función para poder leer el contenido de las listas
def lectura_json():
    try:
        
        with open("registro_diario.json","r") as archivo:#Apertura para leer el registro_diario
            datos_del_disco = json.load(archivo)#Creamos variable de datos del disco que está cargando la lista de diccionarios de json con el .load desde la variable archivo

            for ficha in datos_del_disco:#For de los datos del disco que es la variable para poder volcar la información de resgitro_diario
                piso_almacenado = ficha ["piso"]#Variable para pasar los recorrido y meterla dentro de datos_paquete
                empresa_almacenada = ficha["empresa"]
                vecino_almacenado = ficha["vecino"]

                datos_paquete = Paquete(piso_almacenado,empresa_almacenada,vecino_almacenado)#Cada uno de los datos que se ha ido almacenando con el for ficha in datos_del_disco
                estanteria.append(datos_paquete)#Añadir a estantería la variable con todos los objetos    

    except FileNotFoundError:
        print("No hay nada en registro_diario.json")
    #Aquí es exactemente como con registro_diario pero ahora vamos a leer el historial_general
    try:
        with open("historial_general.json", "r") as archivo:
            datos_del_historial = json.load(archivo)
        for ficha in datos_del_historial:
            piso_historial = ficha["piso"]
            empresa_historial = ficha["empresa"]
            vecino_historial = ficha["vecino"]

            datos_a_almacenar_historial = Paquete(piso_historial,empresa_historial,vecino_historial)
            historial_entregados.append(datos_a_almacenar_historial)
    except FileNotFoundError:
        print("No hay nada dentro del historia_general.json")

#Función para traducir de objeto a texto y registrar en el registro
def traduccion_y_escritura_json():
    estanteria_traducida =[]

    for paquete in estanteria:#for con variable creada para estantería en Paquete recorriendo
        estanteria_traducida.append(paquete.a_diccionario())#todo el contenido recorrido pasa a estanteria traducida/transformada de objeto a texto con el return devuelve lo que antes era objeto como string para pasar a json.dumps

    with open ("registro_diario.json", "w") as archivo:#Abrimos el registro_diario, escribimos con W, como archivo
        texto_json = json.dumps(estanteria_traducida, indent=4)#Creamos variable texto_json para traducirlo el json.dumps es para volcar strings, decimos la variable que tiene los argumentos y marcamos el espaciado con indent creo recordar.
        archivo.write(texto_json)#La variable volcada de texto_json lo que hará es escribrir en registro_diario, llamada por archivo
#Función para entregar el paquete al piso, añadiendo al historial de entregados, quitando del registrados
def entregar_paquete():

    piso_a_buscar = entrada_recogida.get().upper().strip()

    paquete_encontrado = None

    for paquete in estanteria:
        if paquete.piso == piso_a_buscar:
            paquete_encontrado = paquete
            break 
    
    if paquete_encontrado != None:
        historial_entregados.append(paquete_encontrado)
        historial_entregados_json()
        estanteria.remove(paquete_encontrado)
        
        print(f"Se ha eliminado {paquete_encontrado.piso}")
        messagebox.showinfo("Entrega",f"Paquete del piso {piso_a_buscar} entregado con éxito.")

        entrada_recogida.delete(0,tk.END)

        traduccion_y_escritura_json()
        
    else:
        messagebox.showerror("Error", f"No hay ningún paquete para el piso {piso_a_buscar}.")
    
    print("Botón de entregar pulsado")
#Función consulta el listado e registros
def ver_inventario():

    # 1. Empezamos a construir nuestro mensaje de registrados
    texto_final = f"Actualmente hay {len(estanteria)} paquetes en la estantería.\n\nPisos pendientes:\n"
    
    # 2. El bucle "bola de nieve" que añade pisos al texto
    for registro in estanteria:
        # Fíjate en el += (Esto suma el nuevo piso al texto que ya existía)
        texto_final += f"Piso: {registro.piso} ({registro.empresa})\n" 
        
    # 3. Lanzamos el pop-up pasando solo 2 cosas: Título y nuestro texto gigante
    messagebox.showinfo("Inventario Actual", texto_final)

def leer_piso():

    piso_escrito = entrada_piso.get().upper().strip()#Estoy haciendo una función con una variable la cual lo que esté dentro de la etiqueta a la hora de usar la función lo asigne a esa variable
    empresa_escrita = entrada_empresa.get().upper().strip()
    vecino_escrito = entrada_vecino.get().upper().strip()
    
    

    nuevo_paquete = Paquete(piso_escrito, empresa_escrita,vecino_escrito)# Variable que absorbe los parametros/objetos para la clase Paquete
    estanteria.append(nuevo_paquete)#Añadir a la lista estantería los objetos asignados a un espacio
    
    traduccion_y_escritura_json()

    print(f"¡Objeto creado en memoria! Pertenece al piso {nuevo_paquete.piso}")
    # Creamos un pop-up de información. El primer texto es el título de la ventanita, el segundo es el mensaje.
    mensaje = f"Paquete para el piso: {piso_escrito}\nEmpresa: {empresa_escrita}\nVecino: {vecino_escrito}"
    messagebox.showinfo("¡Paquete Registrado!", mensaje)

    entrada_piso.delete(0, tk.END)
    entrada_empresa.delete(0,tk.END)
    entrada_vecino.delete(0, tk.END)


# 1. Crear la ventana principal (la carrocería)

lectura_json()#Uso la función de lectura para actualizar las listas 
ventana = tk.Tk()

# 2. Configurar los detalles visuales
ventana.title("Conserjería v3.0")
ventana.geometry("275x600") # Ancho x Alto en píxeles
ventana.configure(bg="#f0f0f0") # Un color de fondo gris clarito

etiqueta_bienvenida =tk.Label(ventana, text="Bienvenido a la Conserjería") #Etiqueta del título central
etiqueta_bienvenida.pack(pady=20) #Margen superior e inferior

label_piso =tk.Label(ventana, text="Piso del vecino:", bg="#f0f0f0")#Etiqueta del título central
label_piso.pack(pady=5)

entrada_piso =tk.Entry(ventana, width=30)
entrada_piso.pack(pady=5)

label_empresa = tk.Label(ventana, text="Empresa repartidora:", bg="#f0f0f0")
label_empresa.pack(pady=5)

entrada_empresa =tk.Entry(ventana, width=30)
entrada_empresa.pack(pady=5)

label_vecino = tk.Label(ventana, text="Nombre de vecino/a:", bg="#f0f0f0")
label_vecino.pack(pady=5)

entrada_vecino = tk.Entry(ventana, width=30)
entrada_vecino.pack(pady=5)

boton_registrar = tk.Button(ventana, text="Registrar Paquete", command=leer_piso)
boton_registrar.pack(pady=15)

boton_consulta_registrados = tk.Button(ventana, text="Consulta de registrados", command=ver_inventario)
boton_consulta_registrados.pack(pady=15)

etiqueta_entregas =tk.Label(ventana, text="---ZONA DE ENTREGAS---")
etiqueta_entregas.pack(pady=20)

label_entrega = tk.Label(ventana, text="Piso que recoge:", bg="#08947d")
label_entrega.pack(pady=5)

entrada_recogida = tk.Entry(ventana, width=20)
entrada_recogida.pack(pady=5)

boton_entregar = tk.Button(ventana, text="Entregar Paquete", command=entregar_paquete)
boton_entregar.pack(pady=15)

boton_consulta_entregados =tk.Button(ventana, text="Consulta de entregados", command=ver_historial)
boton_consulta_entregados.pack(pady=15)

# 3. Arrancar el motor gráfico (El bucle infinito)

ventana.mainloop()