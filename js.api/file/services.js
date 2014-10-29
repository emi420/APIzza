(function($) {

    "use strict";

    angular.module('api.file', [])
        .factory('APIFile', function($q, $window, $http, appConfig) {
            return {

                    createBase64: function(data, filename) {

                        var deferred = $q.defer();

                        if (data && data !== "") {
                          
                            $http({
                                url: APIConfig.file() + '/createBase64/',
                                data: _hash() + "=" + window.encodeURIComponent(data),
                                headers: $.extend(
                                    APIConfig.headers,
                                    {"content-type": "application/x-www-form-urlencoded"}
                                ),                                      
                                method: "POST"}).success(function(r) {
                                    console.log(r);
                                    deferred.resolve({
                                        url: window.encodeURI(APIConfig.file() + "/" +
                                         r + "/?VoolksAppId=" + APIConfig.headers["X-Voolks-App-Id"] +
                                          "&amp;VoolksApiKey=" + APIConfig.headers["X-Voolks-Api-Key"]),
                                        filename: filename
                                    });
                                })
                                .error(function(err) {
                                    deferred.reject(err);
                                });
                        } else {
                            window.setTimeout(function() {
                                deferred.resolve({
                                    url: "",
                                    filename: ""
                                });
                            }, 1);
                        }

                        return deferred.promise;

                    }
            }
        });


}(window.angular));
