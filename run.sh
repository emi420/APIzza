source ENV/bin/activate ;

cd key.api ; \
python manage.py runserver localhost:7999 & \
echo "key.api started on localhost:7999" ; \

cd ../auth.api ; \
python manage.py runserver localhost:8000 & \
echo "auth.api started on localhost:8000" ; \

cd ../data.api ; \
python manage.py runserver localhost:8001 & \
echo "data.api started on localhost:8001" ; \

cd ../file.api ; \
python manage.py runserver localhost:7998 & \
echo "file.api started on localhost:7998" ; \


