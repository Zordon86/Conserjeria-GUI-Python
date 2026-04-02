class Paquete:
    def __init__(self, piso_recibido, empresa_recibida, vecino_recibido):
        self.piso = piso_recibido
        self.empresa = empresa_recibida
        self.vecino = vecino_recibido
    def a_diccionario(self):
        return{"piso":self.piso,"empresa":self.empresa, "vecino":self.vecino}