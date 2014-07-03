# Documentación

## ID de aplicación y API Key

Todas las consultas se hacen al dominio en el cual tengas instalada la API:

https://api.example.com/

Enviando una API Key (clave para usar la API) y un App Id (id de aplicación para usar la API)..

Se pueden enviar por GET como parámetros en la URL (VoolksApiKey, VoolksAppId) o en los headers HTTP X-Voolks-Api-Key, X-Voolks-App-Id

## Datos

### API de datos

https://api.example.com/classes/

### Crear objetos

### Request

Se envía un request POST con un objeto JSON que contiene la lista de llaves y valores a:

/classes/<clase del objeto>/

### JavaScript

$.ajax({
    url: "https://api.example.com/classes/Client/",
    headers: {
             "X-Voolks-Api-Key":<Api-Key>,
             "X-Voolks-App-Id":<App-Id>
    },                                        
    type: "POST",
    data: JSON.stringify({
            "name": "Juan Perez",
            "city": "Buenos Aires"
    }),
    success: function(r) {
                console.log(r);
            }
});

### Respuesta

La respuesta es un objeto JSON con el timestamp de creación y el id del objeto creado.

## Obtener objetos

### Request

Se envía un request GET a:

/classes/<clase del objeto>/<id del objeto>

### JavaScript

$.ajax({
    url: "https://api.example.com/classes/Client/53b566cafd625c5955d73b07/",
    headers: {
             "X-Voolks-Api-Key":<Api-Key>,
             "X-Voolks-App-Id":<App-Id>
    },                                        
    type: "GET",
    success: function(r) {
                console.log(r);
            }
});

### Respuesta

La respuesta es el objeto en formato JSON.

## Actualizar objetos

### Request

Se envía un request PUT a:

/classes/<clase del objeto>/<id del objeto>/

Con un objeto JSON que reemplazará al anterior.

### JavaScript

$.ajax({
    url: "https://api.example.com/classes/Client/53b566cafd625c5955d73b07/",
    headers: {
             "X-Voolks-Api-Key":<Api-Key>,
             "X-Voolks-App-Id":<App-Id>
    },                                        
    type: "PUT",
    data: JSON.stringify({
            "name": "Juan Perez",
            "city": "Córdoba"
    }),
    success: function(r) {
                console.log(r);
            }
});

### Respuesta

La respuesta es un objeto JSON con el timestamp de actualización (updatedAt)

## Borrar objetos

### Request

Se envía un request DELETE a:

/classes/<clase del objeto>/<id del objeto>/

### JavaScript

$.ajax({
    url: "https://api.example.com/classes/Client/53b566cafd625c5955d73b07/",
    headers: {
             "X-Voolks-Api-Key":<Api-Key>,
             "X-Voolks-App-Id":<App-Id>
    },                                        
    type: "DELETE"
});

Obtener todos los objetos de una clase

### Request

Para obtener todos los objetos de una clase, se envía un request GET a:

/classes/<clase del objeto>/

### JavaScript

$.ajax({
    url: "https://api.example.com/classes/Client/",
    headers: {
             "X-Voolks-Api-Key":<Api-Key>,
             "X-Voolks-App-Id":<App-Id>
    },                                        
    type: "GET",
    success: function(r) {
                console.log(r);
            }
});

### Respuesta

Un objeto JSON con el array de objetos del resultado.

## Filtrar objetos

### Request

Para realizar consultas con filtros, debe usarse el parámetro where en el request GET:

/classes/<clase del objeto>/

Ejemplos:

?where={“country”:”Argentina”}
?where={“customer”:”Starbucks”, “sent”: false}

### Respuesta

Un objeto JSON con el array de objetos del resultado.

### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/Client/?where={"name":"Juan Perez"}',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
});


## Operaciones

Al pasar el parámetro “where”, los queries son similares a los de MongoDB:

http://docs.mongodb.org/manual/tutorial/query-documents/

## Expresiones regulares

Ejemplo usando una expresión regular para traer todos los registros cuyo campo “name” empiece con “R” :
### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/app/?where={"name":{"$regex":"^R(.*)$"}}',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
});

## Projections

Para hacer projections, el parámetro where debe ser un array con la query y los campos a retornar:

### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/Client/?where=[{"name":"Juan Perez"},{"_id":1}]',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})

La respuesta será un array de objetos que contienen sólo los campos indicados.

## Limit

Para establecer límites a la consulta, hay que enviar el parámetro “limit” en el GET:

### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/Client/?limit=1&where=[{"name":"Juan Perez"},{"_id":1}]',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})



## Contar resultados

Para contar los resultados de una consulta, se agrega el siguiente parámetro a la URL del request:

count=true

Ejemplo: https://api.example.com/classes/app/?count=true

### Respuesta

La respuesta es un objeto que sólo contiene el número de objetos que coinciden con la consulta.

### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/Client/?count=true&where=[{"name":"Juan Perez"},{"_id":1}]',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})


## Autenticación

### API de usuarios

https://api.example.com/auth/

Registro de usuarios

Se realiza mediante el envío de un request POST (temporalmente un GET) a /users/signup/. 

### Data

Objeto con username, password 

### JavaScript

$.ajax({
    url: 'https://api.example.com/users/signup/?username=demo&password=abc321',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})

### Respuesta

La respuesta HTTP debe contener un status (ej: 201 Created).

El body de la respuesta es un objeto con fecha de creación, id y un token de sesión.

Login de usuarios

### Request

Se envía un request GET con usuario y password a /users/login/

### JavaScript

$.ajax({
    url: 'https://api.example.com/users/login/?username=demo&password=abc321',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})

### Respuesta

La respuesta es un objeto con todos los datos disponibles del usuario, menos el password. También incluye un token de sesión.

## Permisos de usuarios

Esta sección de la API hace referencia a un servicio experimental, un prototipo que posiblemente tenga cambios próximamente.

### 1. Obtener un id de usuario

Para restringir el acceso a datos, primero necesitamos un id de usuario, por ejemplo haciendo login:

### JavaScript

$.ajax({
    url: 'https://api.example.com/users/login/?username=demo&password=abc321',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})

### 2. Guardar un objeto 

Guardamos el objeto haciendo referencia al id de usuario:

### JavaScript

$.ajax({
    url: "https://api.example.com/classes/Client/",
    headers: {
             "X-Voolks-Api-Key":<Api-Key>,
             "X-Voolks-App-Id":<App-Id>
    },                                        
    type: "POST",
    data: JSON.stringify({
            "name": "Juan Perez",
            "city": "Buenos Aires", 
            "_mod": {5:"write"}
    }),
    success: function(r) {
                console.log(r);
            }
});

La línea clave es:

"_mod": {5:"write"}

En este ejemplo el número 5 es el id de usuario. El permiso puede ser de escritura (write) o sólo lectura (read).

### 3. Obtener objetos 

Ahora no vamos a tener éxito si intentamos obtener este objeto como hacíamos anteriormente:

### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/Client/53b56b91fd625c5b465dd7d1/',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>, 
           
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})

Para lograrlo necesitamos un id de sesión del usuario con permisos sobre ese objeto, que se envía como el header X-Voolks-Session-Id:

### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/Client/53b56b91fd625c5b465dd7d1/',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>, 
            "X-Voolks-Session-Id":"w4s8s4dcjedu9cl4tl1gupdt734a45j2"
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})

Lo mismo sucederá si queremos obtener todos los objetos:

### JavaScript

$.ajax({
    url: 'https://api.example.com/classes/Client/',
    headers: {
            "X-Voolks-Api-Key":<Api-Key>,
            "X-Voolks-App-Id":<App-Id>, 
            "X-Voolks-Session-Id":"w4s8s4dcjedu9cl4tl1gupdt734a45j2"
    },                                      
    type: "GET",
    success: function(r) {
        console.log(r);
    }
})

El resto de las operaciones CRUD funcionan de la misma forma, sólo se pueden modificar o eliminar objetos que estén protegidos por un permiso si se envía un session id válido.


