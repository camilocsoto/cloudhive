# CloudHive  
...  
#### ¿cómo correr el proyecto en mi computadora?  

Se ha puesto a disposición una guía paso a paso para ejecutar el proyecto en su computadora local utilizando contenedores de Docker, para mantener un entorno aislado y controlado. Si desea contribuir al desarrollo del código, la guía también incluye instrucciones para activar un Dev Container, permitiéndole trabajar en un entorno seguro sin preocuparse por problemas de dependencias, versiones o fallos en la ejecución.  

A continuación, encontrará el enlace a la guía detallada:  

[django-dash.pdf](https://workdrive.zohoexternal.com/external/b0466ef3ef8f091597c3331cd3b62c01d2fe6c3f6af10b9253bf662fe4cb703e)

#### otros comandos útiles:  
 
- **Crear otra app:** `docker-compose exec django-web python manage.py startapp __name_your_app__`  
- **Crear migraciones:** `docker-compose exec django-web python manage.py makemigrations`  