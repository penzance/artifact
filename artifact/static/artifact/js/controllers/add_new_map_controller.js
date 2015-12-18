(function()
{
  /*
   Angular controller
   */
  angular.module('app')
    .controller('AddNewMapController', ['$scope', '$http', '$timeout', 'djangoUrl',
      function($scope, $http, $timeout, $djangoUrl)
      {
        var GET_MAPS = $djangoUrl.reverse('artifact:maps', [$scope.canvas_course_id]);


        var responsePromise = $http.get(GET_MAPS);

        var addnewmap = function(info)
        {
          var adddiv = $('<div class="map-block"><a href="location/' + info.id + '"><img alt="' +
            info.title + '" src="' + info.thumbnail + '"></a><p class="image-title">' + info.title +
            '</p></div>');
          $(adddiv)
            .insertBefore('#add-location-container');
        };


        responsePromise.success(function(data, status, headers, config)
        {
          $scope.maps = data;
        });

        $scope.formData = {};

        var param = function(data)
        {
          var returnString = '';
          for (var d in data)
          {
            if (data.hasOwnProperty(d))
            {
              returnString += d + '=' + data[d] + '&';
            }
          }
          // Remove last ampersand and return
          return returnString.slice(0, returnString.length - 1);
        };

        // process the form
        $scope.processForm = function()
        {
          $http(
            {
              method: 'POST',
              url: GET_MAPS, //'api/v1/maps/1',
              data: param($scope.formData), // pass in data as strings
              headers:
              {
                'Content-Type': 'application/x-www-form-urlencoded'
              } // set the headers so angular passing info as form data (not request payload)
            })
            .then(function(data)
            {
              addnewmap(
              {
                'id': data.data.id,
                'title': data.data.title,
                'thumbnail': data.data.thumbnail,
              });
            });
          $('#myModal')
            .modal('hide')
        };
  }]);
})();