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
