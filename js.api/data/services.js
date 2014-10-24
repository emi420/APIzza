(function($) {

    "use strict";


    angular.module('api.data', [])
        .factory('APIData', function($q, $window, $http, APIConfig) {
            return {

                    get: function(className, id) {
                        var deferred = $q.defer();
                        var url = APIConfig.data() + "/" + className + '/';

                        if (id) {
                            url += id + '/';
                        }

                        $http({
                                url: url,
                                headers: $.extend(
                                    APIConfig.headers
                                )
                            })
                            .success(function(r) {
                                deferred.resolve(r);
                            })
                            .error(function(err) {
                                deferred.reject(err);
                            });

                        return deferred.promise;
                    },

                    create: function(className, data) {
                        var deferred = $q.defer();

                        $http({
                                url: APIConfig.data() + "/" + className + '/',
                                data: JSON.stringify(data),
                                headers: $.extend(
                                    APIConfig.headers
                                ),
                                method: "POST"
                            })
                            .success(function(r) {
                                deferred.resolve(r);
                            })
                            .error(function(err) {
                                deferred.reject(err);
                            });

                        return deferred.promise;
                    },

            }
        });

}(window.angular));
