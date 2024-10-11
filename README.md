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
