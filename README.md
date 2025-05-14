# Inicio del Proyecto

Este proyecto se ejecuta usando **Docker** y **Docker Compose**. Asegúrate de tener ambos instalados en tu máquina.

## Iniciar el proyecto localmente

Primero abrir la aplicacion de docker,
Luego la raíz del proyecto, ejecutar:

```bash
docker-compose up --build
```
Una vez ejecutando dejar que se inicie la base de datos, se deberia demorar 1 o 2 minutos

Para vincular profesores, almunos y evaluaciones a una seccion, primero hay que crear la seccion, lo cual implica crear la instancia de curso lo cual implica crear el tipo de curso

Los requisitos se ven en la pestaña de tipo de curso y para ver los profesores y estudiantes de una seccion hya que entrar a una seccion de un curso,
las evaluaciones de una seccion se pueden ver desde el curso mismo

El delete funciona en cascada lo cual implica que borrar un tipo de curso borraria todas las instancias de curso, secciones, evaluaciones y vinculos con profesores y estudiantes relacionadas entre ellas en cadena.

En caso de querer hacer un seed ir a 
```
http://127.0.0.1:5000/testing
```
considerar que ejecutar esto mas de una vez generaria todos los datos por segunda vez, implicando duplicados

# Carga de Datos vía JSON

Este sistema permite cargar datos en la base de datos a través de archivos JSON, utilizando botones habilitados en la interfaz web. Es **muy importante seguir el orden de carga indicado**, ya que existen relaciones entre las entidades que dependen unas de otras.

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
**Importante:** Si los archivos no se cargan en el orden indicado, pueden producirse errores por referencias faltantes entre entidades.

