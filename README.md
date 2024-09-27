# Instrucciones de Instalación

Para correr el backend en un contenedor de docker

    docker-compose up --build

La app funciona en conjunto con una extension de firefox para el bloqueo de tareas. Para instalar la extension temporalmente,
ir a

    about:debugging#/runtime/this-firefox
   
y cargar el manifest.json

# Modo de uso

## Pantalla Principal

![Imgur](https://imgur.com/PNw7Wyu.png)

Al iniciar la aplicación, se te presentará una lista de proyectos existentes. Desde aquí puedes:

    Ver detalles de un proyecto: Haz clic en el nombre del proyecto para ver las tareas asociadas.
    Agregar un nuevo proyecto: Completa el formulario de "Crear nuevo proyecto" en la parte inferior de la pantalla.



## Gestión de Proyectos
## Ver Detalles del Proyecto

![Imgur](https://imgur.com/HRo7aKG.png)

    Haz clic en el nombre de un proyecto para acceder a su vista de detalles.
    En esta vista, podrás ver:
        El nombre y la descripción del proyecto.
        El tiempo total estimado del proyecto.
        Una lista de tareas asociadas.

## Agregar Tareas

    Ve a la vista de detalles del proyecto.
    Completa el formulario "Agregar nueva tarea" y haz clic en "Agregar".
    La tarea se añadirá a la lista de tareas del proyecto.

## Editar o Eliminar Tareas

    Para editar una tarea, usa el formulario de edición junto a la tarea correspondiente y haz clic en "Editar".
    Para eliminar una tarea, haz clic en el botón "Eliminar" correspondiente.

## Establecer Intervalos de Concentración

![Imgur](https://imgur.com/y99oMFB.png)

    Ve a la vista de detalles del proyecto.
    Busca la sección "Iniciar un Intervalo de Concentración".
    Selecciona las tareas en las que deseas trabajar.
    Especifica los sitios web que deseas bloquear.
    Indica la duración del intervalo en minutos.
    Haz clic en "Iniciar Intervalo".


# Arquitectura de la Aplicación

## Modelo

Archivos: models/models.py

- **Proyecto**: Representa un proyecto con atributos como nombre, descripción y duración total.
- **Tarea**: Representa una tarea dentro de un proyecto, con atributos como nombre y duración estimada.
- **Intervalo**: Representa un período de concentración, que incluye las tareas seleccionadas y los sitios web a bloquear.


## Controladores

Archivos: api/routes.py

El controlador maneja la interacción entre el modelo y la vista. Recibe las solicitudes del usuario, procesa la lógica de negocio y determina qué vista se debe renderizar. Las funciones del controlador incluyen:

- **Gestión de Proyectos**: Funciones para crear, editar y eliminar proyectos.
- **Gestión de Tareas**: Funciones para agregar, editar y eliminar tareas dentro de un proyecto.
- **Manejo de Intervalos**: Funciones para iniciar intervalos de concentración y gestionar las tareas y sitios web seleccionados.

## Servicios

Archivos: services/proyect_service.py services/task_service.py services/interval_service.py

Se implementan servicios que encapsulan la lógica de negocio, permitiendo que los controladores se mantengan delgados y enfocados en la interacción con la vista. Por ejemplo, el servicio de proyecto se encarga de la creación, actualización y eliminación de proyectos y tareas.

## Base de Datos

La aplicación utiliza una base de datos relacional  para almacenar datos de manera estructurada. Se emplea como ORM SQLAlchemy.

## Contenerización

La aplicación se despliega utilizando Docker, lo que permite que todas las dependencias y configuraciones se encapsulen en contenedores.



