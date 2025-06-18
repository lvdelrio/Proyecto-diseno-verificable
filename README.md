# Inicio del Proyecto

Este proyecto se ejecuta usando **Docker** y **Docker Compose**. Asegúrate de tener ambos instalados en tu máquina.

## Iniciar el proyecto localmente

Primero, abre la aplicación de Docker.
Luego, en la raíz del proyecto, ejecuta:

```bash
docker-compose up --build
```
Una vez ejecutado, deja que se inicie la base de datos. Esto debería tardar entre 1 y 2 minutos.

Para vincular profesores, alumnos y evaluaciones a una sección, primero hay que crear la sección, lo cual implica crear la instancia de curso, lo que a su vez implica crear el tipo de curso.

Los requisitos se visualizan en la pestaña de Tipo de Curso. Para ver los profesores y estudiantes de una sección, hay que entrar a una sección específica dentro de un curso.
Las evaluaciones de una sección se deben visualizar dentro de la seccion a la que pertenecen.

El borrado funciona en cascada, lo que implica que eliminar un Tipo de Curso borrará todas las instancias de curso, secciones, evaluaciones y vínculos con profesores y estudiantes relacionados en cadena.

## Testing (Entrega 3)
Para ejecuntar los unit tests se debe tener el proyecto corriendo utilizando el comando especificado arriba y en una segunda consola se debe ejecutar:
```
docker-compose exec app pytest tests/ -v
```

## Testing (No para parte de la entrega 3)
El testing implementado no es para producción e incluye los archivos `test.py` y `seeds.py`, que tienen rutas respectivas en `app.py`.

En caso de querer hacer un *seed* de las tablas `Tipo_curso`, `Curso`, `Seccion`, `Profesor`, `Alumno`, `ProfesorSeccion`, `AlumnoSeccion`, puedes ejecutar la siguiente ruta:
```
http://127.0.0.1:5000/testing
```
⚠️ Considera que ejecutar esto más de una vez generará datos duplicados.

Si deseas borrar todos los datos de la base de datos (los datos son generados con la librería Faker), usa:
```
http://127.0.0.1:5000/reset_db?confirm=true
```
Ten en cuenta que esto elimina todos los datos, pero no reinicia la base de datos, por lo tanto, los IDs continuarán desde el último valor existente para cada tabla correspondiente.

Para generar el horario, utiliza la siguiente ruta:
```
http://127.0.0.1:5000/crear_horario
```
Esto crea un archivo `.csv` en la carpeta `exports`, ubicada en paralelo a las demás carpetas del proyecto. El archivo tendrá como nombre la fecha de creación.
En caso de que algunas secciones no se puedan ubicar en el horario debido a las restricciones definidas en el enunciado, estas se desplegarán por consola.

## Generacion de reportes
La generacion de reportes esta disponible en cada vista correspondiente a cada reporte, es decir (para acceder a los reportes hay que abrir la carpeta reports dentro del proyecto y el nombre del csv corresponde al tipo de reporte):
### Reporte Notas de una instancia de topico:
```
http://127.0.0.1:5000/evaluaciones/<id_evaluacion>/edit?seccion_id=<id_seccion>
```
A esto se llega ingresando a Gestion de cursos, editar curso, pestaña secciones, editar seccion, pestaña evaluaciones, opciones de evaluaciones, editar evaluacion.

### Reporte Notas finales de una Sección:
```
http://127.0.0.1:5000/seccion/<id_seccion>
```
A esto se llega ingresando a Gestion de cursos, editar curso, pestaña secciones, editar seccion.

### Reporte Notas finales de Cursos de un Alumno:
```
http://127.0.0.1:5000/alumno/<id_alumno>
```
A esto se llega ingresando a Gestion de alumnos, editar alumno.

# Carga de Datos vía JSON

Este sistema permite cargar datos en la base de datos a través de archivos JSON, utilizando botones habilitados en la interfaz web.
**Es muy importante seguir el orden de carga indicado**, ya que existen relaciones entre las entidades que dependen unas de otras.

## Orden de carga recomendado

Los archivos JSON deben cargarse en el siguiente orden:

1. `Alumno`
2. `Profesores`
3. `Cursos`
4. `Instancia de Curso`
5. `Instancia de Curso con Secciones`
6. `Alumnos por Sección`
7. `Notas de Alumnos`
8. `Salas de Clase`

## Cómo subir archivos JSON

Cada sección de la plataforma cuenta con un botón verde ubicado en la **esquina superior derecha** que permite subir un archivo JSON correspondiente a esa entidad.

### 1. Alumno
- Ir a la pestaña **Alumnos**.
- Hacer clic en el botón verde **"Subir JSON"**.
- Seleccionar el archivo correspondiente.

### 2. Profesores
- Ir a la pestaña **Profesores** desde la pantalla inicial.
- Hacer clic en **"Subir JSON"** y seleccionar el archivo.

### 3. Cursos
- Ir a la pestaña **Cursos** desde la pantalla inicial.
- Hacer clic en **"Subir JSON"**.

### 4. Instancia de Curso
- Ir a la pestaña **Instancia de Curso**.
- Hacer clic en **"Subir JSON"**.

### 5. Secciones del Curso
- Una vez creada la instancia del curso, acceder a la subpestaña **Secciones**.
- Ahí podrá crear o subir un JSON con las secciones relacionadas.
- Este proceso también generará automáticamente las **categorías** y **evaluaciones** correspondientes.

### 6. Alumnos por Sección
- Desde la vista de una **Instancia de Curso**, ir a la subpestaña **Estudiantes**.
- Hacer clic en el botón verde y subir el JSON con los alumnos asignados a las secciones respectivas.

### 7. Notas de Alumnos
- Ir a la pestaña **Notas** desde la pantalla principal.
- Hacer clic en **"Subir JSON"** para cargar las notas correspondientes.

### 8. Salas de Clase
- Desde la pestaña inicial, ir a la sección **Salas**.
- Usar el botón verde **"Subir JSON"** para cargar los datos de salas.

---
⚠️**Importante:** Si los archivos no se cargan en el orden indicado, pueden producirse errores por referencias faltantes entre entidades.

