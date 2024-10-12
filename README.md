# expense-tracker

## setting up the project

```sh
# install python and pip using Homebrew
brew install python

# install virtualenv using pip
python3 -m pip install virtualenv

# make a main directory
mkdir directory_name
cd directory_name

# create a new virtual environment
virtualenv env

# activate virtual environment (macOS)
source env/bin/activate

# add .gitignore and requirements.txt
touch .gitignore
touch requirements.txt

# install Django in the virtual environment
pip install django
pip install python-dotenv

# check if Django is installed
django-admin --version
#
pip install -r requirements.txt
# create a new Django project (corrected command)
django-admin startproject project_name

# go to the project directory
cd project_name

# create an app inside the project
django-admin startapp appname
# or
python manage.py startapp appname

# start the development server
python manage.py runserver


```

After creating a remote repository, initialize it and connect to remote repository.

```sh
echo "# expense-tracker" >> README.md
git init
git add README.md
git commit -m "first commit"
# rename the current branch to main, if same name exist, overwrite it.
git branch -M main
# origin is the default name for the remote repository that we cloned from or that we have set up
git remote add origin https://github.com/Lotfullah21/expense-tracker.git
# set an upstream tracking, main on local corresponds to main on remote
git push -u origin main
```

Now, add the `app name` to `manage.py` file in at `settings.py`.

```py
INSTALLED_APPS = [
    'tracer',
    ... ]
```

## gitignore

If you only want to ignore SQLite files within a specific app, you can specify the path more explicitly. For example, if you only want to ignore `myapp/database.sqlite3`

`*.sqlite3`: Meaning: This pattern matches any file with the .sqlite3 extension in the current directory only. It does not traverse into subdirectories.

`Matches`: db.sqlite3 (in the root or any specific directory).
`Does Not Match`: subfolder/db.sqlite3 (inside a subdirectory).

`\*\*/_.sqlite3`: This pattern matches any file with the .sqlite3 extension in the current directory and any subdirectory at any level.

`Matches`:
db.sqlite3 (in the root directory),
app1/db.sqlite3 (in the app1 subdirectory),
app2/subfolder/db.sqlite3 (in a nested subdirectory).

## How to connect postgresql to django?

[postgres](https://www.postgresql.org/download/)
[pg-admin](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v8.11/macos/)
[How-to-connect](https://www.geeksforgeeks.org/how-to-use-postgresql-database-in-django/)

pg-admin to view the tables inside the database.

`pip install psycopg2-binary`

Add the following code to the boilerplate code in `settings.py`

```sh
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': ‘<database_name>’,
       'USER': '<database_username>',
       'PASSWORD': '<password>',
       'HOST': '<database_hostname_or_ip>',
       'PORT': '<database_port>',
   }
}
```

```sh
python manage.py runserver
```

### include

`include()` is a function used in urls.py to reference other URL configurations. It's particularly useful when your project has multiple apps or a large set of URLs.

### Purpose of include()

Instead of defining all URLs for all apps in the main project's urls.py, we can split each app’s URLs into its own urls.py file. Then, in the main project's urls.py, we use include() to point to each app's URL configuration.

1. Project level `urls.py`

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses.urls')),
]

```

2. App level `urls.py`

```py
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),
]

```

## Django Static and Media File Settings

Add the following code in `settings.py`

```py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIR = [
    os.path.join(BASE_DIR, "public/static")
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "public/media")
```

Add the following snippet in `urs.py`, it helps us to serve the files during dev mode correctly.

```py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
```

`BASE_DIR` is a commonly used variable that represents the absolute path to the root directory of our Django project

`/home/yourusername/Documents/my_django_project/static/css/style.css`

- **`STATIC_URL`**:
  - The URL path to static files.
- **`STATIC_ROOT`**:
  - The directory where all static files are collected when you run `collectstatic`.
- **`STATICFILES_DIRS`**:
  - The directories where Django looks for additional static files, apart from the ones in each app's `static/` folder.
- **`MEDIA_URL`**:
  - The URL path to user-uploaded files.
- **`MEDIA_ROOT`**:
  - The directory where those user-uploaded files are stored.
