# Making my own Wiki
Using Django

Steps I went through:
1) Get Base file ("django-admin startproject PROJECT_NAME" when from scratch) from CS50
2) pip3 install Django
3) python manage.py runserver
4) Look at http://127.0.0.1:8000/'s Wiki (only Home URL works but it indicates we should make a new page and 5 topics)
5) python manage.py startapp APP_NAME (encylopedia? and/or just wiki)
6) Create Page: Form (see Notes/3)
7) {% extends "tasks/layout.html" %} (change tasks)
8) Follow along with Lecture and make notes/copy the examplary code

9) Check in index.html to Create New Page
10) End up(9) in layout.html and copy Home code
11) https://cs50.harvard.edu/web/2020/projects/1/wiki/

12) If you want to allow for an HTML string to be outputted, you can do so with the safe filter (as by adding |safe after the variable name you’re substituting).
13) Follow Youtube for inspiration. Get pages overview lighting up

14) 