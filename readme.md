CloudHive  
...  
#### ¿cómo correr el proyecto en mi computadora?  

Se ha puesto a disposición una guía paso a paso para ejecutar el proyecto en producción utilizando Docker, y otra para para ejecutar el servidor de django en un servidor local.

A continuación, encontrará el enlace a la guía detallada:  

[manual to exec .pdf](https://uniminuto0-my.sharepoint.com/:b:/g/personal/juan_suarez-so_uniminuto_edu_co/Ee8j0Xh8C5lCs7LQtARElOABI0mAyYcN4HmdPV78EH61UQ?e=PYaiwV)

Posteriormente, debe ejecutar el comando: `docker-compose exec django-web python manage.py migrate` para activar todos los servicios de django.

![alt func](https://developer.mozilla.org/es/docs/Learn_web_development/Extensions/Server-side/Django/Home_page/basic-django.png)


#### otros comandos útiles:  
 
- **Crear otra app:** `docker-compose exec django-web python manage.py startapp __name_your_app__`  
- **Crear migraciones:** `docker-compose exec django-web python manage.py makemigrations`  
