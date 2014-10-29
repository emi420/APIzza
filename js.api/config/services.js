(function() {

    "use strict";

    var API;

    // localhost (true) or remote API (false)
    var APIDEBUG = false;

    if (APIDEBUG === true) {
        // Localhost API config
        API = {
            Config: {
                base: "http://192.168.0.13",
                auth: function() {
                    return this.base + ":8000";
                },
                data: function() {
                    return this.base + ":8001/classes";
                },
                file: function() {
                    return this.base + ":7998";
                },
                pdf: function() {
                    return this.base + ":7997";
                },
                headers: {
                    "X-Voolks-App-Id": "1",
                    "X-Voolks-Api-Key": "1234",
                }
            }
        }
    } else {
        API = {
            Config: {
                base: "https://api.voolks.com",
                auth: function() {
                    return this.base + "/users/";
                },
                data: function() {
                    return this.base + "/classes/";
                },
                file: function() {
                    return this.base + "/file/";
                },
                pdf: function() {
                    return this.base + "/pdf/";
                },
                headers: {
                    "X-Voolks-App-Id": "",
                    "X-Voolks-Api-Key": "",
                }
            }
        }
    }


    angular.module('api.config', [])
        .factory('APIConfig', function($q, $window, $http) {
            return API.Config
        });
        
}());
    
                
