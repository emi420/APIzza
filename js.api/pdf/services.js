(function($) {

    "use strict";

    angular.module('api.pdf', [])
        .factory('APIPDF', function($q, $window, $http, APIConfig) {
            return {

                    create: function(data) {

                        var deferred = $q.defer();

                        $http({
                                url: APIConfig.pdf(),
                                method: 'POST',
                                headers: {
                                    "X-Voolks-App-Id": APIConfig.headers["X-Voolks-App-Id"],
                                    "X-Voolks-Api-Key": APIConfig.headers["X-Voolks-Api-Key"],
                                    'accept': '*/*',//we need to add these things to the header to make POST work in angular
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                },
                                data: data
                            })
                            .success(function(data, status) {
                                console.log(data);
                                deferred.resolve(data);
                            })
                            .error(function(err) {
                                console.error('some error');
                                deferred.reject('An error occurred.');
                            })

                        return deferred.promise;    
                    }

            }
        });

}(window.angular));
