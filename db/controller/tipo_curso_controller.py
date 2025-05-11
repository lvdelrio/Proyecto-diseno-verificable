from sqlalchemy.orm import Session
from ..models.tipo_curso import TipoCurso
from ..models.requisitos import CursoRequisito

def create_tipo_curso(db: Session, tipo_curso_code: str, description: str, credits: int, id: int = None):
    if id is not None:
        new_tipo_curso = TipoCurso(id=id, codigo=tipo_curso_code, descripcion=description, creditos=credits)
    else:
        new_tipo_curso= TipoCurso(codigo=tipo_curso_code, descripcion=description, creditos=credits)
    db.add(new_tipo_curso)
    db.commit()
    db.refresh(new_tipo_curso)
    return new_tipo_curso

def get_tipo_curso_by_id(db: Session, tipo_curso_id: int):
    return db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()

def get_all_tipo_cursos(db: Session):
    return db.query(TipoCurso).all()


def edit_tipo_curso_by_id(db: Session, tipo_curso_id: int, tipo_curso_code: str, description: str):
    tipo_curso = db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()
    if tipo_curso:
        tipo_curso.codigo = tipo_curso_code
        tipo_curso.descripcion = description
        db.commit()
        db.refresh(tipo_curso)
        return tipo_curso
    return None

def delete_tipo_curso_by_id(db: Session, tipo_curso_id: int):
    tipo_curso = db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()
    if tipo_curso:
        db.delete(tipo_curso)
        db.commit()
        return True
    return False

def add_requisito_tipo_curso(db: Session, tipo_curso_id: int):
    tipo_curso = db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()
    if tipo_curso:
        db.delete(tipo_curso)
        db.commit()
        return True
    return False


def enroll_tipo_curso_in_tipo_cursos(db: Session, tipo_curso_base_id: int, tipo_curso_id: int):
    if tipo_curso_base_id == tipo_curso_id:
        return False, "Un tipo de curso no puede ser requisito de sí mismo."

    existing = db.query(CursoRequisito).filter_by(
        tipo_curso_id=tipo_curso_base_id,
        curso_requisito_id=tipo_curso_id
    ).first()

    if existing:
        return False, "Este requisito ya está asignado."

    create_requisito(
        db,
        tipo_curso_id=tipo_curso_base_id,
        curso_requisito_id=tipo_curso_id
    )
    return True, "Requisito agregado exitosamente."

def create_tipo_cursos_from_json(db: Session, data: dict):
    cursos_json = data.get("cursos", [])
    tipos_curso_map = {}

    for curso_data in cursos_json:
        tipo_curso = create_tipo_curso(
            db=db,
            id=curso_data["id"],
            codigo=curso_data.get("codigo"),
            code=curso_data.get("codigo"),
            description=curso_data.get("descripcion"),
            credits=curso_data.get("creditos")
        )
        tipos_curso_map[curso_data["codigo"]] = tipo_curso

    for curso_data in cursos_json:
        for req_codigo in curso_data["requisitos"]:
            enroll_tipo_curso_in_tipo_cursos(
                tipo_curso_id=curso_data["id"],
                curso_requisito_id=tipos_curso_map[req_codigo].id
            )

def create_requisito(db: Session, tipo_curso_id: int, curso_requisito_id: int):
    nuevo_requisito = CursoRequisito(tipo_curso_id=tipo_curso_id, 
                                     curso_requisito_id=curso_requisito_id)
    db.add(nuevo_requisito)
    db.commit()
    db.refresh(nuevo_requisito)
    return nuevo_requisito
