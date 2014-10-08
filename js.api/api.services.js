(function($) {
    
    "use strict";

    var _hash = function() {
        return 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }
    
    
    var API;

    // localhost (true) or remote API (false)
    var APIDEBUG = true;
    
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
                    "X-Voolks-Api-Key":"1234",
                }
            }
        }        
    } else {
        API = {
            Config: {
                base: "",
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
                    "X-Voolks-App-Id":"",
                    "X-Voolks-Api-Key":"",
                }
            }
        } 
    }

    
    angular.module('API.services', [])
        .factory('API', function($q, $window, $http, appConfig) {
            return {
        
                Config: API.Config,
        
                "File": {
                    createBase64: function(data, filename, remotefilename) {

                        var deferred = $q.defer();
                                                
                        if (data && data !== "") {
                            
                            if (remotefilename === undefined) {
                                remotefilename = _hash();
                            }
                            
                            $http({
                                url: API.Config.file() + '/createBase64/',
                                data: remotefilename + "=" + window.encodeURIComponent(data),
                                headers: $.extend(
                                    API.Config.headers,
                                    {"content-type": "application/x-www-form-urlencoded"}
                                ),                                      
                                method: "POST"}).success(function(r) {
                                    deferred.resolve({
                                        url: window.encodeURI(API.Config.file() + "/" +
                                         r + "/?VoolksAppId=" + API.Config.headers["X-Voolks-App-Id"] +
                                          "&amp;VoolksApiKey=" + API.Config.headers["X-Voolks-Api-Key"]),
                                        filename: filename
                                    });
                                })

                        } else {
                            window.setTimeout(function() {
                                deferred.resolve({url: "",filename:""});
                            }, 1);
                        }

                        return deferred.promise;
        
                    }
                },
        
                Data: {
                    
                    get: function(className, id) {
                        var deferred = $q.defer();
                        var url = API.Config.data() + "/" + className + '/';
                        
                        if (id) {
                           url += id + '/';    
                        }

                        $http({
                            url: url,
                            headers: $.extend(
                                API.Config.headers
                            )})                                    
                            .success(function(r) {
                                deferred.resolve(r);
                            });

                        return deferred.promise;
                    },
                    
                    create: function(className, data) {
                        var deferred = $q.defer();
                        
                        $http({
                            url: API.Config.data() + "/" + className + '/',
                            data: JSON.stringify(data),
                            headers: $.extend(
                                API.Config.headers
                            ),                                      
                            method: "POST"})
                            .success(function(r) {
                                deferred.resolve(r);
                            })

                        return deferred.promise;
                    },
                },
        
                Users: {
                    
                    login: function(user, pass) {
                        var deferred = $q.defer();

                        if (user && pass) { 
    
                            if (appConfig.debug === true && appConfig.debugOffline === true) {
                                 deferred.resolve({});
                            } else {
                                $http({
                                    url: API.Config.auth() + '/login/',
                                    method: 'GET',
                                    params: {
                                        username: user,
                                        password: pass
                                    },
                                    headers: API.Config.headers
                                })
                                    .success(function(data, status, headers, config) {
                                        if (data.code === 46 || data.code === 44) {
                                            deferred.reject(data.text);
                                        } else {
                                            deferred.resolve(data);
                                        }
                                    })
                                    .error(function(err) {
                                        deferred.reject(err);
                                    });
        
                            }
    
                        } else {
                            deferred.reject('Please enter user & password');
                        }

                        return deferred.promise;
                    }
                }
                
            }
        })

}(window.angular));
