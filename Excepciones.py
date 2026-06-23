class ValidacionException(Exception): #Aparece cuando faltan datos al tratar de añadirlo en el formulario
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
class GestorDatosException(Exception): #Aparece cuando no es capaz de leer o escribir los ficheros
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)