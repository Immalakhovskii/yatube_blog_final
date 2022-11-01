# Blogging platform Yatube (Final) #

### Description ###

Yatube is a site that stores posts with text and image. Posts can be assigned to groups and commented, posts' authors can be followed. Anonymous has accesses to main posts feed, single post page with comments, page with all posts by author and page with all posts assgined to distinct group. Signed up and logged user can create new posts, edit own posts, comment own and other posts and follow other authors to have personilized posts feed. New groups can be created only in admin zone

### Technology Stack ###
Python 3.7 / Django 2.2.16 / HTML 5 / Pillow 8.3.1 / Faker 12.0.1

### Features ###
- Every page with multiple posts has pagination
- 20 posts on index page are cached via template
- CSRF-tokens used in templates
- HTTP responses 403, 404, 500 have custom pages 
- There is custom django-admin script for creating and populating database
- Django Debug Toolbar installed to the project (works with DEBUG = True set in settings.py) 

### Coverage with Unit Tests ###
Yatube applications about and posts covered with unit tests. Coverage report states that 98% of functionality of these apps tested. Tests' code with descriptions via docstrings can be seen at posts/tests and about/tests directories

### How to Start Yatube ###
```
# clone repository, create virtual enviroment and install dependencies
git clone https://github.com/Immalakhovskii/yatube_blog_final.git
cd yatube_blog_final/
python -m venv venv
python -m pip install -r requirements.txt

# activate virtual enviroment 
source venv/scripts/activate            # (Windows) 
source venv/bin/activate                # (macOS and Linux)

# execute custom script for static collection, migrations and 
# objects creation with Faker package
cd yatube/
python manage.py populate_database

# or prepare clean database and manually collect static
python manage.py collectstatic 
python manage.py migrate
python manage.py createsuperuser 

# start!
python manage.py runserver
```
Now Yatube available at http://127.0.0.1:8000/, admin zone at http://127.0.0.1:8000/admin/. If you used script for populating database there are 1 superuser, 3 regular users, 3 groups, 50 posts and 150 comments (there is random quantity of posts by each user, comments' authors and posts also assigned randomly). There are no images and follows, but why not create them:

```
# log in to the site and admin zone as Admin superuser
username: admin
password: youllneverguess

# or log to the site as one of regular users:
usernames: porter, ruiz, hayes
password: youllneverguess
```
To stop development server press **ctrl (command) + c**
- For sake of convenience for starting the project static/ folder excluded from .gitignore so it is inside repository. For the same reason SECRET_KEY is public

### Yatube as Web API ###
There is an almost exact Django REST Framework implementation of Yatube without any frontend. This project can be seen here: https://github.com/Immalakhovskii/yatube_blog_api  
