(function()
{
	//Angular App Module and Controller
	angular.module('app')
		.controller('LocationController', ['$scope', '$http', '$timeout',
            'djangoUrl',
            function($scope, $http, $timeout, $djangoUrl)
			{
				// var mc = this;
				var GET_LOC = $djangoUrl.reverse('artifact:map_location', [$scope.map_id]);
				var GET_MARKERS = $djangoUrl.reverse('artifact:markers', [$scope.map_id]);
				var GET_CSV = $djangoUrl.reverse('artifact:csv_points', [$scope.map_id]);
				var responsePromise = $http.get(GET_LOC);

				// displays the selected point on the right sidebar
				var showInfo = function(marker)
				{
					$scope.point.title = marker.title;
					$scope.point.description = marker.description;
					$scope.point.external_url = marker.external_url;
					$scope.point.latitude = marker.latitude;
					$scope.point.longitude = marker.longitude;
				};

				// creates markers on page load and when submitting new point form
				var createMarker = function(info)
				{
					var marker = new google.maps.Marker(
					{
						map: $scope.map,
						position: new google.maps.LatLng(info.latitude, info.longitude),
						title: info.title
					});

					marker.description = info.description;
					marker.external_url = info.external_url;

					google.maps.event.addListener(marker, 'mouseover', function()
					{
						showInfo(marker);
						$scope.$apply();
					});

					$scope.markers.push(marker);
					marker.setMap($scope.map);
				};


				responsePromise.success(function(data, status, headers, config)
				{
					var mapOptions = {
						zoom: data.zoom,
						center: new google.maps.LatLng(data.latitude, data.longitude)
					};
					switch (data.maptype)
					{
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

					var infoWindow = new google.maps.InfoWindow();
					$scope.selectMarker = function(e, marker)
					{
						showInfo(marker);
					};

					$scope.point = [];
					$scope.markers = [];

					for (i = 0; i < data.markers.length; i++)
					{
						createMarker(data.markers[i]);
					}
				});

				// processform adds a single point to the map
				$scope.formData = {};
				$scope.processForm = function()
				{
					console.log($scope.formData);
					$http(
						{
							method: 'POST',
							url: GET_MARKERS,
							data: $.param($scope.formData),
							headers:
							{
								'Content-Type': 'application/x-www-form-urlencoded'
							} // set the headers so angular passing info as form data (not request payload)
						})
						.then(function(data)
						{
							createMarker(
							{
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

				// uploads a file with multiple csv points to the map
				$scope.uploadFile = function()
				{

					function buildConfig()
					{
						return {
							delimiter: "",
							newline: "",
							header: true,
							dynamicTyping: false,
							preview: 0,
							step: undefined,
							encoding: "",
							worker: false,
							comments: false,
							complete: function(results, file)
							{
								var submitlist = []
								for (i = 0; i < results.data.length; i++)
								{
									if (results.data[i].title.length > 0)
									{
										submitlist.push(results.data[i])
										createMarker(
										{
											'title': results.data[i].title,
											'latitude': results.data[i].latitude,
											'longitude': results.data[i].longitude,
											'description': results.data[i].description,
											'external_url': results.data[i].externalurl
										});
										console.log(results.data[i]);
									}
									else
									{
										continue;
									}
								}
								$http
								(
									{
										method: 'POST',
										url: GET_CSV,
										data: submitlist,
										headers:
										{
											'Content-Type': 'application/x-www-form-urlencoded'
										} // set the headers so angular passing info as form data (not request payload)
									}
								)
								// console.log(results.data);
							},
							error: undefined,
							download: false,
							fastMode: undefined,
							skipEmptyLines: true,
							chunk: undefined,
							beforeFirstChunk: undefined,
						};
					}
					var config = buildConfig();
					var files = $('#files')[0].files;
					if (files.length > 0)
					{
						$('#files')
							.parse(
							{
								config: config,
								before: function(file, inputElem) {},
								complete: function() {}
							});
					}
					else
					{
						window.alert("You must upload a valid file. Please try again.");
					}
					// $http(
					// 	{
					// 		method: 'POST',
					// 		url: GET_CSV,
					// 		data: results.data,
					// 		headers:
					// 		{
					// 			'Content-Type': 'application/x-www-form-urlencoded'
					// 		} // set the headers so angular passing info as form data (not request payload)
					// 	})
					// 	.then(function() {});
					$('#addlist')
						.modal('hide');
				};


				// $('#parse_csv')
				// 	.click(function()
				// {


				// 	function buildConfig()
				// 	{
				// 		return {
				// 			delimiter: "",
				// 			newline: "",
				// 			header: true,
				// 			dynamicTyping: false,
				// 			preview: 0,
				// 			step: undefined,
				// 			encoding: "",
				// 			worker: false,
				// 			comments: false,
				// 			complete: function(results, file)
				// 			{
				// 				for (i = 0; i < results.data.length; i++)
				// 				{
				// 					if (results.data[i].title.length > 0)
				// 					{
				// 						createMarker(
				// 						{
				// 							'title': results.data[i].title,
				// 							'latitude': results.data[i].latitude,
				// 							'longitude': results.data[i].longitude,
				// 							'description': results.data[i].description,
				// 							'external_url': results.data[i].externalurl
				// 						});
				// 						console.log(results.data[i]);
				// 					}
				// 					else
				// 					{
				// 						continue;
				// 					}
				// 				}
				// 				// console.log(results.data);
				// 			},
				// 			error: undefined,
				// 			download: false,
				// 			fastMode: undefined,
				// 			skipEmptyLines: true,
				// 			chunk: undefined,
				// 			beforeFirstChunk: undefined,
				// 		};
				// 	}
				// 	var config = buildConfig();
				// 	var files = $('#files')[0].files;
				// 	if (files.length > 0)
				// 	{
				// 		$('#files')
				// 			.parse(
				// 			{
				// 				config: config,
				// 				before: function(file, inputElem) {},
				// 				complete: function() {}
				// 			});
				// 	}
				// 	else
				// 	{
				// 		window.alert("You must upload a valid file. Please try again.");
				// 	}


				// });
			}]);
})();