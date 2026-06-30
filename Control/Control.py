import json
import os
from Modelo.Excepciones import ValidacionCargaException


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
                datos = inc.pasar_diccionario()
                datos['tipo'] = inc.__class__.__name__
                lista.append(datos)
            with open(ruta, 'w', encoding='utf-8') as archivo:
                json.dump(lista, archivo, ensure_ascii=False, indent=2)
        except OSError as error:
            raise ValidacionCargaException(f'No se pudo guardar el archivo JSON: {error}') from error
        
    def cargar_json(self, ruta, constructor_map=None):
        if not os.path.exists(ruta):
            self.incidencias = []
            return

        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except (json.JSONDecodeError, OSError) as error:
            raise ValidacionCargaException(f'No se pudo leer el archivo JSON: {error}') from error

        self.incidencias = []
        for dato in datos:
            tipo = dato.pop('tipo', None)
            if constructor_map and tipo in constructor_map:
                constructor = constructor_map[tipo]
                dato_cargado = dato.copy()

                if tipo == 'IncidenciaPhishing':
                    dato_cargado.setdefault('url_sospechosa', '')
                elif tipo == 'IncidenciaMalware':
                    dato_cargado.setdefault('tipo_malware', '')
                elif tipo == 'IncidenciaFuerzaBruta':
                    dato_cargado.setdefault('num_intentos', 0)
                elif tipo == 'IncidenciaFugaDeDatos':
                    dato_cargado.setdefault('tipo_dato', '')
                elif tipo == 'IncidenciaAccesoNoAutorizado':
                    dato_cargado.setdefault('metodo_acceso', '')

                try:
                    objeto = constructor(**dato_cargado)
                    self.incidencias.append(objeto)
                except Exception as error:
                    raise ValidacionCargaException(f'Error al reconstruir la incidencia de tipo {tipo}: {error}')