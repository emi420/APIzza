
# Voölks API

## Basic usage

For use this API, you will need an App Id and an API Key.

Ask for an App-Id/Api-Key pair to dev[at]voolks.com

This basic authentication method can be performed using headers:

	$.ajax({
	    url: "https://api.voolks.com/classes/Client/",
	    headers: {
	         "X-Voolks-Api-Key":"1234",
	         "X-Voolks-App-Id":"demo",
	         
	    }
	    ...

Or GET parameters:

	$.ajax({
	    url: "https://api.voolks.com/classes/Client/?VoolksAppId=demo&VoolksApiKey=1234"
	    ...

## Data

https://api.voolks.com/classes/

### Create

Send a POST request to:

/classes/\<class name>/

	$.ajax({
	    url: "https://api.voolks.com/classes/Client/",
	    headers: {
	        "X-Voolks-Api-Key":"1234",
	        "X-Voolks-App-Id":"demo",
	        "Content-Type": "application/json"
	    },                                        
	    type: "POST",
	    data: {
	       "name": "Juan Perez",
	       "city": "Buenos Aires"
	    },
	    success: function(r) {
	        console.log(r);
	    }
	});

### Get

To obtain one item, send a GET request to:

/classes/\<class name>/\<id>

	$.ajax({
	    url: "https://api.voolks.com/classes/Client/53b566cafd625c5955d73b07/",
	    headers: {
            "X-Voolks-Api-Key":"1234",
            "X-Voolks-App-Id":"demo"
	    },                                        
	    type: "GET",
	    success: function(r) {
            console.log(r);
        }
	});

To obtain all items for a class, send a GET request to:

/classes/<class name>
	
	$.ajax({
	    url: "https://api.voolks.com/classes/Client/",
	    headers: {
          "X-Voolks-Api-Key":"1234",
          "X-Voolks-App-Id":"demo"
	    },                                        
	    type: "GET",
	    success: function(r) {
           console.log(r);
        }
	});

### Update

Send an PUT request to:

/classes/\<class name>/\<id>

With the new object that will replace the older.
	
	$.ajax({
	    url: "https://api.voolks.com/classes/Client/53b566cafd625c5955d73b07/",
	    headers: {
            "X-Voolks-Api-Key":"1234",
            "X-Voolks-App-Id":"demo"
	        "Content-Type": "application/json"
	    },                                        
	    type: "PUT",
	    data: {
           "name": "Juan Perez",
           "city": "Córdoba"
	    },
	    success: function(r) {
             console.log(r);
        }
	});

### Delete

Send a DELETE request to:

/classes/\<class name>/\<id>

	$.ajax({
	    url: "https://api.voolks.com/classes/Client/53b566cafd625c5955d73b07/",
	    headers: {
           "X-Voolks-Api-Key":"1234",
           "X-Voolks-App-Id":"demo"
	    },                                        
	    type: "DELETE"
	});

### Filter

Send a GET request with a where parameter to:

/classes/<class name>/

	$.ajax({
	    url: 'https://api.voolks.com/classes/Client/?where={"name":"Juan Perez"}',
	    headers: {
            "X-Voolks-Api-Key":"1234",
            "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	});

### Operations

This query system is based on MongoDB:

http://docs.mongodb.org/manual/tutorial/query-documents/
Regular expresions

Regular expressions on the where parameter.

	$.ajax({
	    url: 'https://api.voolks.com/classes/app/?where={"name":{"$regex":"^R(.*)$"}}',
	    headers: {
           "X-Voolks-Api-Key":"1234",
           "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	});

### Projections

Send an array on the where parameter.

	$.ajax({
	    url: 'https://api.voolks.com/classes/Client/?where=[{},{"_id":1}]',
	    headers: {
           "X-Voolks-Api-Key":"1234",
           "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})

### Limit

Send a GET request with the limit parameter.

	$.ajax({
	    url: 'https://api.voolks.com/classes/Client/?limit=1',
	    headers: {
           "X-Voolks-Api-Key":"1234",
            "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})

### Skip

Send a GET request with the skip parameter.

	$.ajax({
	    url: 'https://api.voolks.com/classes/Client/?skip=1',
	    headers: {
           "X-Voolks-Api-Key":"1234",
            "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})

### Count

Send a GET request with the count=true parameter.
	
	$.ajax({
	    url: 'https://api.voolks.com/classes/Client/?count=true',
	    headers: {
           "X-Voolks-Api-Key":"1234",
           "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})
	
### Sort

Send a GET request with an object for sort parameter.
	
	$.ajax({
	    url: 'https://api.voolks.com/classes/Client/?sort={"name":1,"age":-1}',
	    headers: {
           "X-Voolks-Api-Key":"1234",
           "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})

## Users

https://api.voolks.com/auth/

### Sign up

Send a POST request with username and password data to /users/signup/


	$.ajax({
	    url: "https://api.voolks.com/users/signup/",
	    headers: {
            "X-Voolks-Api-Key":"1234",
            "X-Voolks-App-Id":"demo"
	        "Content-Type": "application/json"
	    },                                        
	    type: "POST",
	    data: {
           "username": "someone@somewhere.com",
           "password": "mySecretPass123"
	    },
	    success: function(r) {
             console.log(r);
        }
	});

### Login

Send a GET request with username and password parameters to /users/login/

	$.ajax({
	    url: 'https://api.voolks.com/users/login/?username=demo&password=abc321',
	    headers: {
	            "X-Voolks-Api-Key":"1234",
	            "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})


### Delete

Send a DELETE request with X-Voolks-Session header to /users/

	$.ajax({
	    url: 'https://api.voolks.com/users/',
	    headers: {
	            "X-Voolks-Api-Key":"1234",
	            "X-Voolks-App-Id":"demo"
	            "X-Voolks-Session-Id":"w4s8s4dcjedu9cl4tl1gupdt734a45j2"
	    },                                      
	    type: "DELETE",
	    success: function(r) {
	        console.log(r);
	    }
	})
	
	
### Permissions

1. Get user session id

Send a GET request to authenticate and get a session id:

	$.ajax({
	    url: 'https://api.voolks.com/users/login/?username=demo&password=abc321',
	    headers: {
            "X-Voolks-Api-Key":"1234",
            "X-Voolks-App-Id":"demo"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})

2. Create an object, as usual:

		$.ajax({
		    url: "https://api.voolks.com/classes/Client/",
		    headers: {
		        "X-Voolks-Api-Key":"1234",
		        "X-Voolks-App-Id":"demo",
		        "Content-Type": "application/json"
		    },                                        
		    type: "POST",
		    data: {
		       "name": "Juan Perez",
		       "city": "Buenos Aires"
		    },
		    success: function(r) {
		        console.log(r);
		    }
		});
	

3. Send a POST request to /auth/permissions using object's id, user's session id and a permissions object:

		$.ajax({
		    url: "https://api.voolks.com/auth/permissions/",
		    headers: {
		             "X-Voolks-Api-Key":"1234",
		             "X-Voolks-App-Id":"demo"
		             "Content-Type": "application/json"
		    },                                        
		    type: "POST",
		    data: {
		        "w4s8s4dcjedu9cl4tl1gupdt734a45j2": {
			    	"20": { "read": "true", "write": "true" },
			    	"*": { "read": "false", "write": "false" } 
			    }
		   	},
		    success: function(r) {
		            console.log(r);
		        }
		});
	

Explained:
	
	"<object id>": {
		"<user id>": { "read": "true", "write": "true" },
		"*": { "read": "false", "write": "false" } 
	}


4. Get objects using session id

Send a GET request with the session id obtained from the login response.
	
	$.ajax({
	    url: 'https://api.voolks.com/classes/Client/53b56b91fd625c5b465dd7d1/',
	    headers: {
	            "X-Voolks-Api-Key":"1234",
	            "X-Voolks-App-Id":"demo", 
	            "X-Voolks-Session-Id":"w4s8s4dcjedu9cl4tl1gupdt734a45j2"
	    },                                      
	    type: "GET",
	    success: function(r) {
	        console.log(r);
	    }
	})

## PDF

This service can generate PDF files from a HTML template.

https://api.voolks.com/pdf/

#### Generate PDF

**Method A:** Send a GET request with the url parameter to /pdf/

	https://api.voolks.com/pdf/?VoolksApiKey=1234&VoolksAppId=demo&url=http://yourdomain.com/mypdf.html

**Method B:** Send a POST request with HTML code to /pdf/

		$.ajax({
		    url: "https://api.voolks.com/pdf/",
		    headers: {
		             "X-Voolks-Api-Key":"1234",
		             "X-Voolks-App-Id":"demo"
		    },                                        
		    type: "POST",
		    data: "<h1>Hello, world</h1><p>This is a PDF!</p>",
		    success: function(r) {
		            console.log(r);
		        }
		});
	

The HTML template must be compatible with pisa XHTML/HTML/CSS to PDF converter:

	http://xhtml2pdf.appspot.com/static/pisa-en.html

The response will be an URL with an application/pdf document.

## File

https://api.voolks.com/file/

### Get

Send a GET request to /file/<filename>/

	https://api.voolks.com/file/2048.jpg/?VoolksAppId=demo&VoolksApiKey=1234

### Create

Send a POST request to: /file/create/

	<form action="https://api.voolks.com/file/create/?VoolksAppId=demo&VoolksApiKey=1234" enctype="multipart/form-data" method="post">
	
	    <input type="file" name="testing">
	    <input type="submit" value="Send">
	
	</form>

### Using Apache Cordova (FileTransfer plugin)

	var fileUrl = “cdvfile://localhost/persistent/test.txt”;
	
	var win = function (r) {
	    alert(“Ok!”);
	}
	
	var fail = function (error) {
	    alert("Error (" + error.code + “)”);
	}
	
	var options = new FileUploadOptions();
	options.fileKey = "file.txt";
	options.fileName = fileURL.substr(fileURL.lastIndexOf('/') + 1);
	options.mimeType = "text/plain";
	
	var ft = new FileTransfer();
	ft.upload(fileURL, encodeURI("https://api.voolks.com/file/create/?VoolksAppId=demo&VoolksApiKey=1234"), win, fail, options);
	
### Base 64 pictures
	
Send a POST request to /file/createBase64/ with the base64 data of a  image and file name.
	
	$.ajax({
	    url: 'https://api.voolks.com/file/createBase64/',
	    data: "sign0034=" + window.encodeURIComponent(“/9j//gAOTGF2YzUxLjI4LjAA/9sAQwAIDAwODA4QEBAQEBATEhMU...”),
	    headers: {
	            "X-Voolks-Api-Key":"1234",
	            "X-Voolks-App-Id":"demo", 
	    },                                      
	    type: "POST",
	    success: function(r) {
	        console.log(r);
	    }
	})

### Delete

Send a GET request to /file/\<filename>/delete/

	https://api.voolks.com/file/2048.jpg/delete/?VoolksAppId=demo&VoolksApiKey=1234

## Mail

This service can send e-mails from a HTML template.

https://api.voolks.com/mail/

#### Send an e-mail

Send a POST request to /mail/ with the e-mail from, to, subject and body:

	$.ajax({
	    url: 'https://api.voolks.com/mail/',
	    headers: {
	            "X-Voolks-Api-Key":"1234",
	            "X-Voolks-App-Id":"demo", 
	            "Content-type": "application/json"
	    },                                      
	    type: "POST",
	    data: {
	    	"from": "someone@voolks.com",
	    	"to": "other@someplace.com",
	    	"subject": "Hello, world",
	    	"body": "<h1>Hello, world<</h1><p>This is my message.</p"
	    }

	    success: function(r) {
	        console.log(r);
	    }
	})

The response will be the status of the message.


## API services permissions

As the API admin, you can set permissions for the API services (data, file, mail, pdf, auth) using the app-id.

1. Login to key.api admin and go to Key > App permissions

http://localhost:7999/key/admin/key/apppermission/

2. Add a new entry, write the app-id on the *Objid* field and the permissions can be:

* -delete *Block delete operations*
* -get *Block get operations*
* -put *Block update operations*
* -create *Block create operations*
* -classCreation *Block new data classes creation, useful when your app go to production*










