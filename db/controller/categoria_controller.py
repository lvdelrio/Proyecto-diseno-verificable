from ..config import db
from ..models.categoria import Categoria

def crear_categoria(tipo_categoria, id_seccion, ponderacion, opcional):
    nueva_categoria = Categoria(
        tipo_categoria=tipo_categoria,
        id_seccion=id_seccion,
        ponderacion=ponderacion,
        opcional=opcional
    )
    db.session.add(nueva_categoria)
    db.session.commit()
    return nueva_categoria

def obtener_categoria(categoria_id):
    return Categoria.query.get(categoria_id)

def actualizar_categoria(categoria_id, **kwargs):
    categoria = Categoria.query.get(categoria_id)
    for key, value in kwargs.items():
        setattr(categoria, key, value)
    db.session.commit()
    return categoria

def eliminar_categoria(categoria_id):
    categoria = Categoria.query.get(categoria_id)
    db.session.delete(categoria)
    db.session.commit()
