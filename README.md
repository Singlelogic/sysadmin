# sysadmin
Sysadmin is а simple blog application made on Django.<br>

**Main menu of the blog**<br>
<br>
<img width="1267" alt="blog" src="https://user-images.githubusercontent.com/44861438/84574938-90012700-adb2-11ea-9e05-e540e0e0ff69.png">
***
**Creating and editing a post**<br>

When creating and editing a post for the body of the post, the 'django-summernote' editor is used.
https://github.com/summernote/django-summernote
<img width="1280" alt="Снимок экрана 2020-06-13 в 20 23 39" src="https://user-images.githubusercontent.com/44861438/84575145-defb8c00-adb3-11ea-962c-3b0280a6f8e2.png">
***

**Setup**<br>
1. git clone https://github.com/Singlelogic/sysadmin.git
2. cd ./sysadmin
3. python3.8 -m venv ./venv
4. source ./venv/bin/activate
5. pip install -r requirements.txt
6. Database
The application uses the PostgreSQL database.<br>
Create the .env file in the application root using the SECRET_KEY environment variable (for example, SECRET_KEY = 'database_password'). Also set other settings for the database in the 'settings.py' file (NAME, USER...).<br>
Or replace with the default settings when using the SQLite database.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
7. python manage.py migrate
8. python manage.py runserver

