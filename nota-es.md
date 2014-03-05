# Voölks API

 _Powered by APIzza https://github.com/emi420/APIzza_ 

 La API de Voölks consiste de una serie de webservices para ser reutilizados por las distintas aplicaciones que desarrollamos.


### Id de aplicación y API key

Todas las consultas deben llevar los headers X-Voolks-App-Id y X-Voolks-Api-Key con el id de aplicación y una key para usar la API, provista por el administrador.

Pueden administrarse las aplicaciones desde el admin:

http://auth.voolks.com/admin/

## Datos (data.api)

** http://data.voolks.com **

Para trabajar con los objetos hay que usar el nombre de clase al que pertenece:

* http://data.voolks.com/classes/product/
* http://data.voolks.com/classes/contact/
* ...

### Crear

Usando el método POST:

    $ curl http://data.voolks.com/classes/product/ -X POST -d '{"title": "1kg de naranjas", "price": 4.5}' -H "X-Voolks-App-Id: 1" -H "X-Voolks-Api-Key: 1234"

Al crear el objeto, la API devuelve un id único que lo identifica.

### Obtener

Puede usarse su id:

    curl 'http://data.voolks.com/classes/product/531503e9820c491ec8c272f7/'

U obtener todos:

    curl 'http://data.voolks.com/classes/product/' 
      
### Actualizar

Mediante el método PUT:

    curl 'http://data.voolks.com/classes/product/' -X PUT -d '{"title": "1kg de naranjas", "price": 5.25}'

### Filtrar

Usando el filtro where, que acepta los comandos de MongoDB ($gt, $lt, $regex, etc)
	
	curl 'http://data.voolks.com/classes/product/?where=\{"price":\{"$gt":3.5\}\}'

### Borrar

Usando el método DELETE:

    curl 'http://data.voolks.com/classes/product/' -X DELETE 


## Usuarios (auth.api)

** http://auth.voolks.com **
    
### Registrar

	curl 'http://auth.voolks.com/users/signup/?username=test&password=12345'

### Autenticar

	curl 'http://auth.voolks.com/users/login/?username=test&password=12345'


## Datos con permisos

### Guardar un objeto con permisos sólo para un usuario

Usando el id de usuario, que podemos obtener en el login:

	curl 'http://data.voolks.com/classes/note/' -X POST -d '{\"note":"My secret note", "_mod": \{"2":"write"\}\}'" 

Usando el parámetro especial *_mod* indicamos el id de usuario y los permisos.

Ejemplos:

* _mod: {"2", "read"} *Solo lectura*
* _mod: {"2", "write"} *Esctitura y lectura*

### Obtener 

Usando el sessionid que nos da el login podemos hacer cualquier tipo de consulta incluyendo a los objetos para los cuales tengamos permisos.

    curl 'http://data.voolks.com/classes/product/ -H "X-Voolks-Session-Id: 2xak6pr6n3mfsiqaks4lxtckpnxsy30"'