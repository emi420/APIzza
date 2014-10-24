(function($) {

    "use strict";

    angular.module('api.auth', ['api.config'])
        .factory('APIAuth', function($q, $window, $http, APIConfig) {
            return {

                    login: function(user, pass) {
                        var deferred = $q.defer();

                        if (user && pass) {

                            $http({
                                    url: APIConfig.auth() + '/login/',
                                    method: 'GET',
                                    params: {
                                        username: user,
                                        password: pass
                                    },
                                    headers: APIConfig.headers
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

                        } else {
                            deferred.reject('Please enter user & password');
                        }

                        return deferred.promise;
                    }
            }
        });

}(window.angular));
