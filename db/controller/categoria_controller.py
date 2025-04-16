from ..config import db
from ..models.categoria import Categoria

def create_categoria(tipo_categoria, seccion, ponderacion, tipo_ponderacion):
    nueva_categoria = Categoria(
        tipo_categoria=tipo_categoria,
        id_seccion=seccion.id,
        ponderacion=ponderacion, 
        tipo_ponderacion=tipo_ponderacion
    )
    db.session.add(nueva_categoria)
    db.session.commit()
    return nueva_categoria

def get_categoria(categoria_id):
    return Categoria.query.get(categoria_id)

def edit_categoria(categoria_id, **kwargs):
    categoria = Categoria.query.get(categoria_id)
    for key, value in kwargs.items():
        setattr(categoria, key, value)
    db.session.commit()
    return categoria

def delete_categoria(categoria_id):
    categoria = Categoria.query.get(categoria_id)
    db.session.delete(categoria)
    db.session.commit()
    return

def get_last_categoria_by_seccion( seccion_id ):
    return Categoria.query(Categoria).filter(Categoria.id_seccion == seccion_id).order_by(Categoria.id.desc()).first()

def validacion_categoria(categoria, seccion_id):
    if get_last_categoria_by_seccion(seccion_id).tipo_categoria == categoria.tipo_categoria:
        return False
    return True