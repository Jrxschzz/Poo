import json

from Modelo.Excepciones import GestorDatosException


class gestorIncidencias:
    def __init__(self):
        self.incidencias = []

    def agregar_incidencia(self, incidencia):
        self.incidencias.append(incidencia)

    def obtener_incidencias(self):
        return self.incidencias

    def guardar_json(self, ruta):
        try:
            lista = []
            for inc in self.incidencias:
                datos = dict(inc.__dict__)
                datos['tipo'] = inc.__class__.__name__
                lista.append(datos)
            with open(ruta, 'w', encoding='utf-8') as archivo:
                json.dump(lista, archivo, ensure_ascii=False, indent=2)
        except OSError as error:
            raise GestorDatosException(f'No se pudo guardar el archivo JSON: {error}') from error

    def cargar_json(self, ruta, constructor_map=None):
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            self.incidencias = []
            return
        except (json.JSONDecodeError, OSError) as error:
            raise GestorDatosException(f'No se pudo leer el archivo JSON: {error}') from error

        self.incidencias = []
        for dato in datos:
            tipo = dato.pop('tipo', None)
            if constructor_map and tipo in constructor_map:
                constructor = constructor_map[tipo]
                try:
                    objeto = constructor(**dato)
                except TypeError:
                    objeto = constructor(dato.get('id'), dato.get('titulo'), dato.get('descripcion'), dato.get('fecha'), dato.get('afectados'))
                self.incidencias.append(objeto)
            else:
                from Modelo.Incidencia import Incidencia
                objeto = Incidencia(dato.get('id'), dato.get('titulo'), dato.get('descripcion'), dato.get('fecha'), dato.get('afectados'))
                self.incidencias.append(objeto)