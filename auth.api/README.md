Auth.API
========

Manages users authentication and sign up.


## Install and run

**1.Create the database**

    $ python manage.py syncdb

**2.Run the project:**

    $ python manage.py runserver localhost:8001

Now you can add an user:

    $ curl -H "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" http://localhost:8000/users/signup/?username=test&password=test

And authenticate it:

    $ curl -H "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" http://localhost:8000/users/login/?username=test&password=test


