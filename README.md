APIzza
======

APIzza is a REST API organized in different modules, each one is a separate application and can be running in different servers.

## Backend modules

* **Key.api** API access using app-id and api-key
* **Auth.api** users
* **Data.api** data objetcs
* **File.api** file objects
* **Shared.api** shared utilities for all modules

## Angular module

* **js.api** Angular module API.services 

## Installation

1.Clone this project on your system

2.Install virtualenv and pip

3.Install pip requeriments on project virtualenv:

    $ cd <project folder> 
    $ source ENV/bin/activate
    $ pip install -r req.txt

4.Setup and run each module:

    $ python manage.py syncdb
    $ python manage.py runserver localhost:(port)


## License

You may use any APIzza project under the terms of the GNU General Public License (GPL) Version 3.

(c) 2013 Emilio Mariscal

Want to contribute? fork the project, write us to dev [at] voolks.com