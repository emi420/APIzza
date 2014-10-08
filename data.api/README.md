Data.api
========

Manages data objects.

## Install and run

1.Install and run Mongo DB

* http://docs.mongodb.org/manual/installation/

2.Run the project:

    $ python manage.py runserver localhost:8001

Now you can test it, creating an object:

    $ curl -X POST -H "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" -d '{"title": "Red mate"}' http://localhost:8001/classes/Product/

And retrieving it:

    $ curl "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" http://localhost:8001/classes/Product/

