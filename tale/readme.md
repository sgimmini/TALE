### Setting up

Using the TALE Project virtual environment only django should be necessary to install  
```
$ pip install Django==4.2.7  
```
Then you can run the server by   
```
$ python manage.py runserver  
````

It could be that you need to migrate. For this run 
```
$ python manage.py makemigrations  
$ python manage.py migrate 
```