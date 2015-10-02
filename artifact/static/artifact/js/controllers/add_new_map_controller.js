(function(){
  /*
   Angular controller
   */
  angular.module('app').controller('AddNewMapController', ['$scope', '$http', '$timeout', 'djangoUrl', function ($scope, $http, $timeout, $djangoUrl) {
    var GET_MAPS = $djangoUrl.reverse('artifact:maps', [$scope.canvas_course_id]);


    var responsePromise = $http.get(GET_MAPS);

    responsePromise.success(function (data, status, headers, config) {
      $scope.maps = data;
    });

    $scope.formData = {};

    var param = function (data) {
      var returnString = '';
      for (d in data) {
        if (data.hasOwnProperty(d)) {
          returnString += d + '=' + data[d] + '&';
        }
      }
      // Remove last ampersand and return
      return returnString.slice(0, returnString.length - 1);
    };

    // process the form
    $scope.processForm = function () {
      console.log($scope.formData);
      $http({
        method: 'POST',
        url: GET_MAPS, //'api/v1/maps/1',
        data: param($scope.formData), // pass in data as strings
        headers: {'Content-Type': 'application/x-www-form-urlencoded'} // set the headers so angular passing info as form data (not request payload)
      }).then(function (data) {
        $scope.maps.push({
          'title': data.title,
          'latitude': data.latitude,
          'longitude': data.longitude,
          'zoom': parseInt(data.zoom),
          'maptype': data.maptype,
          'markers': []
        });
      });
    };
  }]);
})();