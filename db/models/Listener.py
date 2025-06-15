from sqlalchemy import event
from sqlalchemy.orm import Session
from db.models.notas import Notas
from db.controller.notas_finales_controller import update_nota_final
from db.controller.evaluacion_controller import get_evaluacion_by_id

@event.listens_for(Notas, 'after_insert')
@event.listens_for(Notas, 'after_update')
@event.listens_for(Notas, 'after_delete')
# Los argumentos mapper, connection y target son necesarios para el evento de SQLAlchemy.
# a pesar que no se usan directamente en la función, son parte del evento.
def handle_nota_change(mapper, connection, target):
    db = Session(bind=connection)
    evaluacion = get_evaluacion_by_id(db, target.evaluacion_id)
    curso_id = evaluacion.categoria.seccion.curso_id
    update_nota_final(db, target.alumno_id, curso_id)
    db.close()
