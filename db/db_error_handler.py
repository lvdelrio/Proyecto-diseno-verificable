from http import HTTPStatus
from flask import jsonify, request, flash, redirect
from sqlalchemy.exc import IntegrityError, DataError
from db.config import db

def setup_global_error_handler(app):
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        user_message = parse_database_error(str(error.orig))
        return handle_database_error(user_message, 'Error de validación')

    @app.errorhandler(DataError)
    def handle_data_error(error):
        user_message = parse_database_error(str(error.orig))
        return handle_database_error(user_message, 'Error de formato')

    @app.errorhandler(AttributeError)
    def handle_attribute_error(error):
        user_message = parse_reference_error(str(error))
        return handle_database_error(user_message, 'Error de referencia')

def handle_database_error(user_message, error_type):
    db.session.rollback()
    if is_json_request():
        return create_json_error_response(user_message, error_type)
    return create_web_error_response(user_message)

def is_json_request():
    return request.is_json or request.path.startswith('/api/')

def create_json_error_response(message, error_type):
    return jsonify({
        'error': error_type,
        'message': message,
        'status': HTTPStatus.BAD_REQUEST
    }), HTTPStatus.BAD_REQUEST

def create_web_error_response(message):
    flash(f'Error: {message}', 'error')
    return redirect(request.referrer or '/'), HTTPStatus.BAD_REQUEST

def parse_database_error(error_message):
    msg = error_message.lower()

    if 'foreign key constraint' in msg:
        if 'alumno' in msg:
            return 'El alumno especificado no existe en el sistema'
        elif 'profesor' in msg:
            return 'El profesor especificado no existe en el sistema'
        elif 'curso' in msg:
            return 'El curso especificado no existe en el sistema'
        elif 'seccion' in msg:
            return 'La sección especificada no existe en el sistema'
        elif 'instancia' in msg:
            return 'La instancia de curso especificada no existe en el sistema'
        else:
            return 'Una de las referencias proporcionadas no existe en el sistema'

    if 'cannot be null' in msg:
        return (
            'Faltan campos obligatorios. '
            'Verifique que todos los datos requeridos estén completos'
        )

    format_keywords = [
        'incorrect', 'invalid', 'data too long', 'out of range'
    ]
    if any(keyword in msg for keyword in format_keywords):
        return (
            'Los datos proporcionados tienen un formato incorrecto. '
            'Verifique los tipos de datos'
        )

    duplicate_keywords = ['duplicate', 'unique constraint']
    if any(keyword in msg for keyword in duplicate_keywords):
        return 'Ya existe un registro con estos datos. Verifique que no haya duplicados'

    if 'unknown column' in msg:
        return (
            'Error en la estructura de datos. '
            'Verifique las referencias y claves proporcionadas'
        )

    return (
        'Error en los datos proporcionados. '
        'Verifique la información e intente nuevamente'
    )

def parse_reference_error(error_message):
    if "'NoneType' object has no attribute 'seccion_id'" in error_message:
        return 'La sección especificada no existe. Verifique que la sección esté creada'

    if "'NoneType' object has no attribute 'id'" in error_message:
        return 'El registro que está intentando referenciar no existe. Verifique el ID'

    if "'NoneType' object has no attribute 'curso_id'" in error_message:
        return 'La instancia de curso especificada no existe. Verifique que el curso esté creado'

    if "'NoneType' object has no attribute 'alumno_id'" in error_message:
        return 'El alumno especificado no existe en el sistema'

    if "'NoneType' object has no attribute 'profesor_id'" in error_message:
        return 'El profesor especificado no existe en el sistema'

    if "'NoneType' object has no attribute" in error_message:
        return (
            'Uno de los registros que está intentando referenciar no existe. '
            'Verifique los datos proporcionados'
        )

    return (
        'Error en las referencias de datos. '
        'Verifique que todos los registros existan antes de crear relaciones'
    )
