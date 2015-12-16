(function() {
	//Angular App Module and Controller
	angular.module('app')
		.controller('LocationController', ['$scope', '$http', '$timeout',
            'djangoUrl',
            function($scope, $http, $timeout, $djangoUrl) {
				var mc = this;
				var GET_LOC = $djangoUrl.reverse('artifact:map_location', [$scope.map_id]);
				var GET_MARKERS = $djangoUrl.reverse('artifact:markers', [$scope.map_id]);
				var GET_CSV = $djangoUrl.reverse('artifact:csv_points', [$scope.map_id]);
				var responsePromise = $http.get(GET_LOC);

				var showInfo = function(marker) {
					$scope.point.title = marker.title;
					$scope.point.description = marker.description;
					$scope.point.external_url = marker.external_url;
					$scope.point.latitude = marker.latitude;
					$scope.point.longitude = marker.longitude;
				};

				var createMarker = function(info) {
					var marker = new google.maps.Marker({
						map: $scope.map,
						position: new google.maps.LatLng(info.latitude, info.longitude),
						title: info.title
					});
					marker.description = info.description;
					marker.external_url = info.external_url;
					google.maps.event.addListener(marker, 'mouseover', function() {
						showInfo(marker);
						$scope.$apply();
					});
					$scope.markers.push(marker);
					marker.setMap($scope.map);
				};
				
				responsePromise.success(function(data, status, headers, config) {
					var mapOptions = {
						zoom: data.zoom,
						center: new google.maps.LatLng(data.latitude, data.longitude)
					};
					switch (data.maptype) {
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
					$scope.map = new google.maps.Map(document.getElementById('map-canvas'),
						mapOptions);

					var infoWindow = new google.maps.InfoWindow();
					

					$scope.selectMarker = function(e, marker) {
						showInfo(marker);
					};



					$scope.point = [];
					$scope.markers = [];
					for (i = 0; i < data.markers.length; i++) {
						createMarker(data.markers[i]);
					}
				});

				$scope.formData = {};
				$scope.processForm = function() {
					console.log($scope.formData);
					$http({
							method: 'POST',
							url: GET_MARKERS,
							data: $.param($scope.formData),
							headers: {
								'Content-Type': 'application/x-www-form-urlencoded'
							} // set the headers so angular passing info as form data (not request payload)
						})
						.then(function(data) {
							createMarker({
								'title': $scope.formData.title,
								'latitude': data['data']['latitude'],
								'longitude': data['data']['longitude'],
								'description': $scope.formData.description,
								'external_url': $scope.formData.externalurl,
								'fileupload': $scope.formData.fileupload,
							});
							$('#myModal')
								.modal('hide');
						});
				};
  }]);
})();