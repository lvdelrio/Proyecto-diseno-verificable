SCHEMAS = {
    'alumnos': {
        'main_key': 'alumnos',
        'required': ['id', 'nombre', 'correo', 'anio_ingreso'],
        'types': {'id': int, 'nombre': str, 'correo': str, 'anio_ingreso': int}
    },
    'notas': {
        'main_key': 'notas',
        'required': ['alumno_id', 'topico_id', 'instancia', 'nota'],
        'types': {'alumno_id': int, 'topico_id': int, 'instancia': int, 'nota': (int, float)}
    },
    'tipo_cursos': {
        'main_key': 'cursos',
        'required': ['id', 'codigo', 'descripcion', 'creditos', 'requisitos'],
        'types': {'id': int, 'codigo': str, 'descripcion': str, 'creditos': int, 'requisitos': list}
    },
    'secciones': {
        'main_key': 'secciones',
        'required': ['id', 'instancia_curso'],
        'types': {'id': int, 'instancia_curso': int, 'profesor_id': int, 'evaluacion': dict}
    },
    'profesores': {
        'main_key': 'profesores',
        'required': ['id', 'nombre', 'correo'],
        'types': {'id': int, 'nombre': str, 'correo': str}
    },
    'salas': {
        'main_key': 'salas',
        'required': ['id', 'nombre', 'capacidad'],
        'types': {'id': int, 'nombre': str, 'capacidad': int}
    },
    'alumnos_seccion': {
        'main_key': 'alumnos_seccion',
        'required': ['seccion_id', 'alumno_id'],
        'types': {'seccion_id': int, 'alumno_id': int}
    },
    'cursos': {
        'main_key': 'instancias',
        'required': ['id', 'curso_id'],
        'types': {'id': int, 'curso_id': int}
    }
}
