REM delete migration files
del authors\migrations\0*.py 
del authors\migrations\*.pyc
del books\migrations\0*.py 
del books\migrations\*.pyc
del customers\migrations\0*.py 
del customers\migrations\*.pyc
del publishers\migrations\0*.py 
del publishers\migrations\*.pyc
del rentals\migrations\0*.py 
del rentals\migrations\*.pyc

del "db.sqlite3"

python manage.py makemigrations
python manage.py migrate

REM create super user
echo "from users.models import CustomUser; CustomUser.objects.create_superuser('ajmvfr', 'ajmvfr@gmail.com', '!a1s2d3f4')" | python manage.py shell

python manage.py generate_dummy_data
