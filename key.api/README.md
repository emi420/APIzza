Key.api
=======

Manages app authentication and permissions for each module.

## Setup and run

1.Create the database:

    $ python manage.py syncdb

2.Run the project:

    $ python manage.py runserver localhost:7999

Now you can add an app from the admin (http://localhost:7999/admin/) and then run:

    $ curl -H "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" http://localhost:7999/check_key/

For testing the API key.

3.You need to configure the KEYS_API_URL on shared.api/decorators.py.
