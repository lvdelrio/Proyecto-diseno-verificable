from sqlalchemy import event
from sqlalchemy.orm import Session
from db.models.notas import Notas
from db.controller.notas_finales_controller import update_nota_final 

@event.listens_for(Notas, 'after_insert')
@event.listens_for(Notas, 'after_update')
@event.listens_for(Notas, 'after_delete')
def nota_changed(mapper, connection, target):
    db = Session(bind=connection)
    curso_id = target.evaluacion.categoria.seccion.curso_id
    update_nota_final(db, target.alumno_id, curso_id)
    db.close()
