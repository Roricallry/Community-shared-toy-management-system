usage

Community_toy_sharing_system/settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'toy_sharing',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

find this, set database for yourself.



run(Init)

```bash
python manage.py makemigrations
python manage.py migrate
```



run

```bash
python manage.py runserver 
```



open the web127.0.0.1:8000, register an account

（set admin）

in the table: user_customuser

set the value: type   , set 1

then, you can add the infomation for toys in web.