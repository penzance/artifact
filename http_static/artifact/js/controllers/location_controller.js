(function(){

	//Angular App Module and Controller
	angular.module('app').controller('LocationController', ['$scope', '$http', '$timeout', 'djangoUrl', function ($scope, $http, $timeout, $djangoUrl) {

		//var GET_LOC = $djangoUrl.reverse('artifact:map_location', [window.globals.MAP_ID]);
		var GET_LOC = '/artifact/api/v1/location/4'; //+window.globals.MAP_ID
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

  }]);

})();
