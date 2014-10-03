source ENV/bin/activate ;

cd key.api ; \
python manage.py runserver 192.168.0.13:7999 & \
echo "key.api started on 192.168.0.13:7999" ; \

cd ../auth.api ; \
python manage.py runserver 192.168.0.13:8000 & \
echo "auth.api started on 192.168.0.13:8000" ; \

cd ../data.api ; \
python manage.py runserver 192.168.0.13:8001 & \
echo "data.api started on 192.168.0.13:8001" ; \

cd ../file.api ; \
python manage.py runserver 192.168.0.13:7998
#echo "file.api started on 192.168.0.13:7998" ; \


