(function(){

	//Angular App Module and Controller
	angular.module('app').controller('LocationController', ['$scope', '$http', '$timeout', 'djangoUrl', function ($scope, $http, $timeout, $djangoUrl) {
		var mc = this;
		var GET_LOC = $djangoUrl.reverse('artifact:map_location', [$scope.map_id]);
		var GET_MARKERS= $djangoUrl.reverse('artifact:markers', [$scope.map_id]);
		var GET_CSV= $djangoUrl.reverse('artifact:csv_points', [$scope.map_id]);
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
    // 	var param = function (data) {
    //   		var returnString = '';
    //   		for (d in data) {
    //     		if (data.hasOwnProperty(d)) {
    //       			returnString += d + '=' + data[d] + '&';
    //     			}
    //   			}
    //   // Remove last ampersand and return
    //   return returnString.slice(0, returnString.length - 1);
    // };

    $scope.processForm = function () {
      console.log($scope.formData);
      $http({
        method: 'POST',
        url: GET_MARKERS,
        data: $.param($scope.formData),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'} // set the headers so angular passing info as form data (not request payload)
      }).then($scope.markers.push({
          'title': $scope.formData.title,
          'latitude': $scope.formData.latitude,
          'longitude': $scope.formData.longitude,
          'description': $scope.formData.description,
          'external_url': $scope.formData.externalurl,
          'fileupload': $scope.formData.fileupload,
        }));
    	console.log($scope.markers);
    	$('#myModal').modal('hide');
    };
    $scope.uploadFile = function(){
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        var uploadUrl = GET_CSV;
        var fd = new FormData();
        fd.append('file', file);
        $http({
        	method: 'POST',
        	url: GET_CSV,
        	data: fd,
        	headers: {'Content-Type': 'application/x-www-form-urlencoded'} // set the headers so angular passing info as form data (not request payload)
      }).then($('#addlist').modal('hide'))
    };

    // $scope.processAddPoints = function () {
    //   console.log($scope.formData);
    //   $http({
    //     method: 'POST',
    //     url: GET_CSV,
    //     data: $scope.formData,
    //     headers: {'Content-Type': 'application/x-www-form-urlencoded'} // set the headers so angular passing info as form data (not request payload)
    //   }).then($('#addlist').modal('hide'))
    // };
  }])
// .service('fileUpload', ['$http', function ($http) {
//     this.uploadFileToUrl = function(file, uploadUrl){
//         var fd = new FormData();
//         fd.append('file', file);
//         $http.post(uploadUrl, fd, {
//             transformRequest: angular.identity,
//             headers: {'Content-Type': undefined}
//         })
//         .success(function(){
//         })
//         .error(function(){
//         });
//     }
// }]);
})();
