(function(){

	//Angular App Module and Controller
	angular.module('app').controller('LocationController', ['$scope', '$http', '$timeout', 'djangoUrl', function ($scope, $http, $timeout, $djangoUrl) {

		var GET_LOC = $djangoUrl.reverse('artifact:map_location', [$scope.map_id]);

		var responsePromise = $http.get(GET_LOC);
		responsePromise.success(function(data, status, headers, config) {
			var mapOptions = {
				zoom: data.zoom,
	      		center: new google.maps.LatLng(data.latitude, data.longitude)
				};
			switch(data.maptype){
				case 1:
					mapOptions["mapTypeId"] = google.maps.MapTypeId.SATELLITE;
					break;
				case 2:
					mapOptions["mapTypeId"] = google.maps.MapTypeId.ROADMAP;
					break;
				case 3:
					mapOptions["mapTypeId"] = google.maps.MapTypeId.HYBRID;
					break;
				case 4:
					mapOptions["mapTypeId"] = google.maps.MapTypeId.TERRAIN;
					break;
				}
			$scope.maptitle = data.title;
	      	$scope.map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	      	$scope.markers = [];

	      	var infoWindow = new google.maps.InfoWindow();
	      	var showInfo = function(marker) {
	        	$scope.title = marker.title;
	        	$scope.description = marker.description;
	        	$scope.external_url = marker.external_url;
	      		}
			var createMarker = function (info){
				var marker = new google.maps.Marker({
					map: $scope.map,
					position: new google.maps.LatLng(info.latitude, info.longitude),
					title: info.title
					});
				marker.description = info.description;
				marker.external_url = info.external_url;
				google.maps.event.addListener(marker, 'mouseover', function(){
					showInfo(marker);
					$scope.$apply();
					});
				$scope.markers.push(marker);
				}

			for (i = 0; i < data.markers.length; i++){
				createMarker(data.markers[i]);
				}

			$scope.selectMarker = function(e, marker){
				e.preventDefault();
				google.maps.event.trigger(marker, 'mouseover');
				}

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

    $scope.processForm = function () {
      console.log($scope.formData);
      console.log($scope.formData.title);
      console.log("TESTTESTTEST");
      console.log(formData.title);
      $http({
        method: 'POST',
        url: 'api/v1/location/' + $scope.map_id,
        data: param($scope.formData), // pass in data as strings
        headers: {'Content-Type': 'application/x-www-form-urlencoded'} // set the headers so angular passing info as form data (not request payload)
      }).then(function (data) {
        $scope.markers.push({
          'title': formData.title,
          'latitude': formData.latitude,
          'longitude': formData.longitude,
          'description': formData.description,
          'external_url': formData.external_url,
          // 'fileupload': formData.fileupload,
        });
      });
    	console.log($scope.markers)
    };
    $scope.add = function(){
      var f = document.getElementById('id_fileupload').files[0],
      r = new FileReader();
      r.onloadend = function(e){
        var data = e.target.result;
        // console.log(data)
        //send you binary data via $http or $resource or do anything else with it
      }
      r.readAsBinaryString(f);
    };
  }]);

})();
