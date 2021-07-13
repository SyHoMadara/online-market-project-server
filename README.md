Simple Online Market server
===========================

This is simple [Django](https://www.djangoproject.com/) project server to hase api with
my [android application](https://github.com/rbehzad/onlineMarket-project.git)

It contains these features:

**User**

1. Admin page that you can log in and creat or update database graphically.
1. Creat user and give it some permutations from supper user (you can do it from admin page)

**Database**

1. Product categories : you can also creat sub category.
1. Products : Contain pictures , rate , user information, etc.
1. Pictures : Hase two option that you can use it in a product, or you can also use it for user profile

Installation
------------
**Linux and Mac**

.First install python3 and pip3

```angular2html
    sudo apt install python3 python3-pip
```

For setup project you can run setup. You can also move directory everywhere that you want than run setup.

```angular2html
   ./setup.sh
```

**Windows**

At first, you should install [python3](https://www.python.org/downloads/)
and [add it to path](https://geek-university.com/python/add-python-to-the-windows-path/)
than run setup.cmd


Usage
-----
*In project folder*


**Creat supperuser** : 
```angular2html
    python manage.py createsuperuser
```

**Run server** :
```angular2html
    python manage.py runserver
```
Then go to you browser and type `127.0.0.1/admin` at url bar or click on [this](http://127.0.0.1:8000/admin)

remember don't close command line or kill process


**Creat normal user** : After login as supperuser you can click on User and add user or update a user 
