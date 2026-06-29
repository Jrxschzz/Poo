class ValidacionCargaException(Exception): #Aparece cuando faltan datos o son hay un error al cargar json
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
