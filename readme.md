# CloudHive  
...  
#### ¿cómo correr el proyecto en mi computadora?  

Se ha puesto a disposición una guía paso a paso para ejecutar el proyecto utilizando contenedores de Docker, para mantener un entorno aislado y controlado. Para contribuir al desarrollo del código, la guía también incluye instrucciones para activar un Dev Container, permitiéndole trabajar en un entorno seguro sin preocuparse por problemas de dependencias, versiones o fallos en la ejecución.  

A continuación, encontrará el enlace a la guía detallada:  

[django-dash.pdf](https://workdrive.zoho.com/file/uk2wdff11cb87c81c49f38052bfa50dffa14c)

#### otros comandos útiles:  
 
- **Crear otra app:** `docker-compose exec django-web python manage.py startapp __name_your_app__`  
- **Crear migraciones:** `docker-compose exec django-web python manage.py makemigrations`  
