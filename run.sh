echo Running key.api ... ; \
cd key.api ; \

#source ENV/bin/activate ; \
python manage.py runserver localhost:7999 & \

echo Running auth.api ... ; \
cd ../auth.api ; \

#source ENV/bin/activate ; \
python manage.py runserver localhost:8000 & \

echo Running data.api ... ; \
cd ../data.api ; \

#source ENV/bin/activate ; \
python manage.py runserver localhost:8001 

echo Running file.api ... ; \
cd ../file.api ; \

#source ENV/bin/activate ; \
python manage.py runserver localhost:80012

