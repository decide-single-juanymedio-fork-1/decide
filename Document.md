[![Build Status](https://travis-ci.com/wadobo/decide.svg?branch=master)](https://travis-ci.com/wadobo/decide) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/6a6e89e141b14761a19288a6b28db474)](https://www.codacy.com/gh/decide-update-4-1/decide-update-4.1/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=decide-update-4-1/decide-update-4.1&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/6a6e89e141b14761a19288a6b28db474)](https://www.codacy.com/gh/decide-update-4-1/decide-update-4.1/dashboard?utm_source=github.com&utm_medium=referral&utm_content=decide-update-4-1/decide-update-4.1&utm_campaign=Badge_Coverage)

Single Juanymedio 1
=====================================

### 1. Resumen ejecutivo
Nuestra labor en un principio consistía en desarrollar funcionalidades a los módulos `vote` y `store` al empezar siendo un Proyecto ‘Part’, pero con la decisión unánime de los integrantes de nuestro equipo de cambiar a ser un proyecto ‘Single’, hemos tocado múltiples módulos ya que no se tomó en cuenta el enfocarnos en alguno en específico, sino que se desarrollaron funcionalidades en base a los intereses que presentara cada miembro del equipo, asegurándose de que no se realizaran desarrollos en el mismo modulo al mismo tiempo o por lo menos avisar con antelación que se empezaría a trabajar en dicho modulo.

A continuación, se da un resumen de la implementación realizada utilizando los ‘issues’ creados en el repositorio del proyecto en GitHub para trabajar en ellos:

- **Issue #2 Feature – Doble check:**
  Implementación de un pop-up para confirmar la respuesta deseada en una votación.

- **Issue #5 Feature – Lenguaje ofensivo:**
  No permitir un lenguaje ofensivo en las votaciones, preguntas ni tampoco en las opciones.

- **Issue #8 Feature – Autenticación por email:**
  Añadir el campo email a `user` para que este sirva para hacer login.

- **Issue #10 Feature – Exportación de censo:**
  Implementar la posibilidad de exportar el censo.

- **Issue #11 Feature – Importación de censo desde Excel:**
  Implementar la posibilidad de importar el censo para las votaciones desde un archivo Excel.

- **Issue #14 Feature – Traducir la interfaz al español:**
  Traducción de la interfaz de `decide` al español.

- **Issue #15 Feature – Traducir la interfaz a otros idiomas:**
  Traducción de la interfaz de `decide` a otros idiomas (francés).

- **Issue #16 Feature – Formulario registro usuarios:**
  Documento HTML que incluya un formulario con capacidad de crear nuevos usuarios.

- **Issue #18 Feature – Mostrar información en tiempo real:**
  Implementación de estadísticas a las votaciones abiertas y cerradas (con tally aplicado).

- **Issue #21 Feature – Crear módulo de recuento:**
  Crear un módulo de recuento donde aplicar técnicas más específicas de recuento como el método D’Hondt. Esta implementación fue cambiada a estar directamente implementada en el modulo `voting` debido a los conflictos que se presentaban con Docker.

- **Issue #28 Feature – Agregar gráficas de resultados:**
  Mostrar gráficas de los resultados de las votaciones cerradas (con tally).

- **Issue #37 Feature – Añadir email al usuario y al registro de usuario:**
  Añadir el atributo email al usuario, así como la posibilidad de registrar un email a su cuenta.

- **Issue #39 Feature – Crear vista de login:**
  Añadir una vista de inicio a la aplicación en la que se muestre la marca del producto y le permita al usuario realizar distintas acciones como registrarse o iniciar sesión, así como los métodos necesarios para iniciar sesión.

- **Issue #41 Feature – Iniciar sesión con el correo electrónico:**
  Añadir la posibilidad al usuario de iniciar sesión con su correo electrónico en lugar de su nombre de usuario.

- **Issue #42 Feature – Permitir al admin iniciar sesión desde el inicio:**
  Permitir al administrador o cualquier otro usuario con permisos de superusuario iniciar sesión desde la página de inicio, sin necesidad de escribir la URL `/admin` en el navegador.

- **Issue #45 Feature – Notificar por email a usuarios de votación:**
  Notificación automática a usuarios pertenecientes al censo de una votación recién iniciada.

- **Issue #46 Feature – Página principal con información del usuario:**
  Añadir una página principal que le permita al usuario acceder a información personal, como las encuestas en las que ha participado o su perfil personal.

- **Issue #57 Feature – Notificación cuando el usuario es añadido a una nueva votación:**
  Añadir una notificación a la página principal cuando el usuario es añadido a una nueva votación. Desde esta nueva notificación se mandará al usuario a la votación.

- **Issue #59 Feature – Resetear votaciones:**
  Implementada acción de reset sobre las votaciones en la vista de admin, llevando a las votaciones seleccionadas a su estado inicial (como recién creada).

- **Issue #66 Feature – Modificar información del usuario:**
  Permitir al usuario modificar su información personal, como el nombre de usuario o el correo electrónico.

Como se puede observar con las funcionalidades implementadas, se le ha dado un enfoque de mejora en la accesibilidad de la aplicación facilitando tanto el manejo como la interacción sobre diferentes aspectos de `Decide`.



### 2. Descripción del sistema



### 3. Visión global del proceso de desarrollo



### 4. Entorno de desarrollo

Todos los miembros hemos empleado Ubuntu 23.04 como sistema operativo de nuestros ordenadores personales, los cuales a su vez hemos utilizado para realizar este proyecto. 

Para la gestión de versiones hemos empleado git y github, apuntando a nuestro repositorio el cual es un fork del repositorio de decide provisto por la asignatura. Mediante el empleo de python 3.10 (versión empleada para el desarrollo de nuestra aplicación de Decide) instalamos las herramientas de desarrollo de python "python3-dev" así como "python3-env" para poder crear el entorno virtual donde tendremos alojada nuestra aplicación. En nuestro entorno hemos instalado los mismos programas del documento "requirements.txt" cuyo contenido es:

Django==4.1
pycryptodome==3.15.0
djangorestframework==3.14.0
django-cors-headers==3.13.0
requests==2.28.1
django-filter==22.1
psycopg2==2.9.4
coverage==6.5.0
jsonnet==0.18.0
django-nose==1.4.6
django-rest-swagger==2.2.0
selenium==4.7.2
dj-database-url==2.1.0
pynose==1.4.8
whitenoise==6.5.0
gunicorn==21.2.0

Utilizamos PostgreSQL para la creación de la base de datos.

Todos los miembros hemos empleado Visual Studio Code como IDE para el desarrollo de la aplicación. Para el despliegue en Vagrant hemos empleado virtualBox. En docker hemos empleado la version 2.3.3 al igual que en las prácticas. Con respecto a workflow, mantuvimos la misma configuración que ya existía en decide.

### 5. Ejercicio de propuesta de cambio

Propondremos para el cambio el acceso por certificación digital.

Será necesario crear una issue en nuestro repositorio de github. Esta issue puede emplear uno de los dos templates que hemos incorporado al repositorio, en este caso usaremos el de Feat. Nombraremos la issue como "Feat - Acceso certificado". Otorgaremos una prioridad que variará entre "Critical", "High", "Medium" y "Low", así como una breve descripción. Como complemento se le añadirán las distintas labels disponibles y se le asignará la issue a un miembro del equipo y a una rama.

La rama creada será nombrada como la issue pero se eliminiarán los espacios innecesarios y los que no puedan ser eliminados se reemplazarán por "_" quedando la rama como "Feat-Acceso_Certificado".

El miembro que llevará a cabo la tarea se traerá esta rama a su máquina y trabajará en ella. 

Los commits seguirán la estructura de conventional commits, y estos deberán contener avances completos, ya sea el código del incremento, sus tests correspondientes o ambos.

Tras realizar todo el código necesario y hacer su debido commit, el miembro con el issue asignado pedirá la pull request desde github. La rama será comparada (y en un futuro mergeada) a la rama "develop", siendo esta la rama que recibe todos los incrementos testeados y aceptados.

Otro miembro del equipo, normalmente aquel que esté disponible lo antes posible, bajará a su equipo la rama que solicitó el pull request y comprobará el correcto funcionamiento del código. Tras un resultado positivo, aprobará la pull request y esta rama será mergeada con la rama develop.

La issue abierta será cerrada tanto en el apartado "issues" del repositorio como en el tablero kanbam del apartado "projects" del repositorio.

### 6. Conclusiones y trabajo futuro

Durante el trascurso de este proyecto hemos atravesado distintas dificultades, la más notoria fue la transformación de proyecto part a proyecto single. Este cambio conllevo una pequeña reestructuración del trabajo pendiente por realizar.

Tras repartir el trabajo, decidimos mantener la estructura GitFlow, puesto que estabamos familiarizados con ella y temíamos desarrollar el código frente a develop por posibles errores durante la realización del código.

Pese a haber acordado unos milestones, el desarrollo de los incrementos no fue realizado por igual entre los distintos miembros del equipo, lo cual llevo a un breve lapso de pesimismo de cara a la entrega. Tras un proceso de comunicación, retomamos el proyecto y conseguimos tenerlo listo para la entrega.

Este proyecto nos ha formado en uno de los aspectos técnicos más importantes de lo que será nuestro futuro laboral.
