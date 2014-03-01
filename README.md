APIzza
======

An API, tasty like a pizza (?)

## Installation

1.Clone this project on your system

2.Install virtualenv and pip in your system.

3.Install pip requeriments on each project virtualenv:

    $ cd <project folder> 
    $ source ENV/bin/activate
    $ pip install -r req.txt
    $ deactivate

## Setup & run

### Key.API

1.Open the key.api folder

    $ cd key.api

2.Activate virtualenv

    $ source ENV/bin/activate

3.Create the database:

    $ python manage.py syncdb

4.Run the project:

    $ python manage.py runserver localhost:7999

Now you can add an app from the admin (http://localhost:7999/admin/) and then run:

    $ curl -H "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" http://localhost:7999/check_key/

For testing the API.

### Auth.API

1.Open the auth.api folder

    $ cd auth.api

2.Activate virtualenv

    $ source ENV/bin/activate

3.Create the database:

    $ python manage.py syncdb

4.Run the project:

    $ python manage.py runserver localhost:8000

Now you can add an user from the admin (http://localhost:8000/admin/") and the run:

    $ curl -H "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" http://localhost:8000/users/login/?username=test&password=test

For testing the API.

### Data.API

1.Install Mongo DB 

http://docs.mongodb.org/manual/installation/

2.Open the data.api folder

    $ cd data.api

3.Activate virtualenv

    $ source ENV/bin/activate

4.Run Mongo DB server:

    $ mongod

5.Run the project:

    $ python manage.py runserver localhost:8001

Now you can test it, creating a product:

    $ curl -X POST -H "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" -d "{'title': 'Red mate'}" http://localhost:8001/classes/product

And retrieving it:

    $ curl "X-Voolks-App-Id:1" -H "X-Voolks-Api-Key: 1234" http://localhost:8001/classes/product/53120df93c4588417a49d562

## License

You may use any APIzza project under the terms of the GNU General Public License (GPL) Version 3.

(c) 2013 Emilio Mariscal