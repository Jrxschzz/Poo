import sys
import os
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Control.Control import gestorIncidencias
from Modelo.Incidencia import Incidencia
from Modelo.IncidenciaMalware import IncidenciaMalware
from Modelo.IncidenciaPhishing import IncidenciaPhishing
from Modelo.IncidenciaFuerzaBruta import IncidenciaFuerzaBruta
from Modelo.IncidenciaAccesoNoAutorizado import IncidenciaAccesoNoAutorizado
from Modelo.IncidenciaFugaDeDatos import IncidenciaFugaDeDatos
from Modelo.Excepciones import ValidacionException, GestorDatosException


st.set_page_config(page_title='Gestor simple', layout='wide')

ruta_json = os.path.join(os.path.dirname(__file__), '..', 'incidencias.json')

clases_incidentes = [
    ('Phishing', IncidenciaPhishing),
    ('Malware', IncidenciaMalware),
    ('FuerzaBruta', IncidenciaFuerzaBruta),
    ('FugaDeDatos', IncidenciaFugaDeDatos),
    ('AccesoNoAutorizado', IncidenciaAccesoNoAutorizado),
]

if 'gestor' not in st.session_state:
    gestor_inicial = gestorIncidencias()
    gestor_inicial.cargar_json(ruta_json, constructor_map={nombre: clase for nombre, clase in clases_incidentes})
    st.session_state['gestor'] = gestor_inicial
gestor = st.session_state['gestor']

st.title('Gestor de Incidencias')
st.caption('Registra y gestiona incidencias de ciberseguridad.')

tab_formulario, tab_resultados = st.tabs(['Formulario', 'Resultados'])

with tab_formulario:
    st.subheader('Registrar incidencia')
    with st.form('form_registro'):
        columna_izquierda, columna_derecha = st.columns(2)
        with columna_izquierda:
            tipo_incidente = st.selectbox('Tipo de incidencia', [nombre for nombre, _ in clases_incidentes])
            identificador = st.text_input('ID')
            titulo = st.text_input('Título')
        with columna_derecha:
            descripcion = st.text_area('Descripción')
            fecha = st.date_input('Fecha')
            valor_extra = None
            if tipo_incidente == 'Malware':
                valor_extra = st.text_input('Tipo de malware')
            elif tipo_incidente == 'Phishing':
                valor_extra = st.text_input('URL sospechosa')
            elif tipo_incidente == 'FuerzaBruta':
                valor_extra = st.number_input('Número de intentos', min_value=0, value=0)
            elif tipo_incidente == 'FugaDeDatos':
                valor_extra = st.text_input('Tipo de dato filtrado')
            elif tipo_incidente == 'AccesoNoAutorizado':
                valor_extra = st.text_input('Método de acceso')

        enviado = st.form_submit_button('Agregar incidencia')

    if enviado:
        try:
            if not identificador or not str(identificador).strip():
                raise ValidacionException('El campo ID es obligatorio.')
            if not titulo or not str(titulo).strip():
                raise ValidacionException('El campo título es obligatorio.')
            if not descripcion or not str(descripcion).strip():
                raise ValidacionException('El campo descripción es obligatorio.')
            if fecha is None:
                raise ValidacionException('Debes seleccionar una fecha.')

            if tipo_incidente in {'Malware', 'Phishing', 'FugaDeDatos', 'AccesoNoAutorizado'}:
                if not valor_extra or not str(valor_extra).strip():
                    raise ValidacionException('Falta información específica para este tipo de incidencia.')
            if tipo_incidente == 'FuerzaBruta' and (valor_extra is None or int(valor_extra) < 0):
                raise ValidacionException('El número de intentos no puede ser negativo.')

            if tipo_incidente == 'Malware':
                incidencia = IncidenciaMalware(identificador, titulo, descripcion, fecha, [], valor_extra or '')
            elif tipo_incidente == 'Phishing':
                incidencia = IncidenciaPhishing(identificador, titulo, descripcion, fecha, [], valor_extra or '')
            elif tipo_incidente == 'FuerzaBruta':
                incidencia = IncidenciaFuerzaBruta(identificador, titulo, descripcion, fecha, [], valor_extra or 0)
            elif tipo_incidente == 'FugaDeDatos':
                incidencia = IncidenciaFugaDeDatos(identificador, titulo, descripcion, fecha, [], valor_extra or '')
            elif tipo_incidente == 'AccesoNoAutorizado':
                incidencia = IncidenciaAccesoNoAutorizado(identificador, titulo, descripcion, fecha, [], valor_extra or '')
            else:
                incidencia = Incidencia(identificador, titulo, descripcion, fecha, [])

            incidencia.tipo = tipo_incidente
            try:
                incidencia.limpieza_datos()
            except Exception as error:
                raise ValidacionException('Los datos de la incidencia no son válidos.') from error

            try:
                if hasattr(incidencia, 'calcular_riesgo'):
                    incidencia.calcular_riesgo()
            except Exception as error:
                raise ValidacionException('No se pudo calcular el riesgo.') from error

            gestor.agregar_incidencia(incidencia)
            gestor.guardar_json(ruta_json)
            st.success('Incidencia añadida y guardada en incidencias.json')
        except ValidacionException as error:
            st.error(str(error))
        except GestorDatosException as error:
            st.error(str(error))

with tab_resultados:
    st.subheader('Incidencias registradas')
    datos_incidentes = [incidencia.__dict__ for incidencia in gestor.obtener_incidencias()]
    if datos_incidentes:
        tabla = pd.DataFrame(datos_incidentes)
        tipos_disponibles = sorted(set(tabla.get('tipo', [])))
        riesgos_disponibles = sorted(set(tabla.get('riesgo', [])))
        columna_filtro_tipo, columna_filtro_riesgo = st.columns(2)
        with columna_filtro_tipo:
            filtro_tipo = st.selectbox('Filtrar por tipo', ['Todos'] + tipos_disponibles)
        with columna_filtro_riesgo:
            filtro_riesgo = st.selectbox('Filtrar por riesgo', ['Todos'] + riesgos_disponibles)

        tabla_filtrada = tabla.copy()
        if 'recomendaciones' not in tabla_filtrada.columns:
            def obtener_recomendacion(fila):
                objeto_incidente = None
                for incidente in gestor.obtener_incidencias():
                    if str(getattr(incidente, 'id', '')) == str(fila.get('id', '')):
                        objeto_incidente = incidente
                        break
                if objeto_incidente and hasattr(objeto_incidente, 'recomendaciones'):
                    try:
                        return objeto_incidente.recomendaciones()
                    except Exception:
                        return ''
                return ''
            tabla_filtrada['recomendaciones'] = tabla_filtrada.apply(obtener_recomendacion, axis=1)
        if filtro_tipo != 'Todos':
            tabla_filtrada = tabla_filtrada[tabla_filtrada['tipo'] == filtro_tipo]
        if filtro_riesgo != 'Todos':
            tabla_filtrada = tabla_filtrada[tabla_filtrada['riesgo'] == filtro_riesgo]

        st.metric('Total', len(tabla_filtrada))
        st.metric('Riesgos altos o críticos', int((tabla_filtrada['riesgo'].astype(str).str.upper().isin(['ALTO', 'CRÍTICO'])).sum()))

        for _, fila in tabla_filtrada.iterrows():
            with st.expander(f"{fila['titulo']} — {fila['tipo']} ({fila['riesgo']})"):
                st.write(f"**ID:** {fila.get('id', '')}")
                st.write(f"**Fecha:** {fila.get('fecha', '')}")
                st.write(f"**Descripción:** {fila.get('descripcion', '')}")
                if fila.get('recomendaciones'):
                    st.write(f"**Recomendación:** {fila['recomendaciones']}")

        st.subheader('Estadísticas')
        columna_estadistica_tipo, columna_estadistica_riesgo = st.columns(2)
        with columna_estadistica_tipo:
            st.write('Por tipo:')
            st.bar_chart(tabla['tipo'].value_counts())
        with columna_estadistica_riesgo:
            st.write('Por riesgo:')
            st.bar_chart(tabla['riesgo'].value_counts())
    else:
        st.info('No hay incidencias registradas')




