[![Build Status](https://travis-ci.com/wadobo/decide.svg?branch=master)](https://travis-ci.com/wadobo/decide) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/6a6e89e141b14761a19288a6b28db474)](https://www.codacy.com/gh/decide-update-4-1/decide-update-4.1/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=decide-update-4-1/decide-update-4.1&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/6a6e89e141b14761a19288a6b28db474)](https://www.codacy.com/gh/decide-update-4-1/decide-update-4.1/dashboard?utm_source=github.com&utm_medium=referral&utm_content=decide-update-4-1/decide-update-4.1&utm_campaign=Badge_Coverage)

Single Juanymedio 1
=====================================

### 1. Resumen ejecutivo



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