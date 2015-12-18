(function()
{
	//Angular App Module and Controller
	angular.module('app')
		.controller('LocationController', ['$scope', '$http', '$timeout',
            'djangoUrl',
            function($scope, $http, $timeout, $djangoUrl)
			{
				var GET_LOC = $djangoUrl.reverse('artifact:map_location', [$scope.map_id]);
				var GET_MARKERS = $djangoUrl.reverse('artifact:markers', [$scope.map_id]);
				var GET_CSV = $djangoUrl.reverse('artifact:csv_points', [$scope.map_id]);
				var DOWNLOAD_CSV = $djangoUrl.reverse('artifact:download_csv', [$scope.map_id]);
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
					$scope.description = data.description;
					$scope.map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

					var infoWindow = new google.maps.InfoWindow();

					// change the selected marker on mouseover
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

				// adds a single point to the map
				$scope.formData = {};
				$scope.processForm = function()
				{
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
							$('#singlepointmodal')
								.modal('hide');
						});
				};

				// uploads a file with multiple csv points to the map
				$scope.uploadFile = function()
				{
					// configuration for csv parser
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
								// list of points to pass to api.py
								var submitlist = [];
								for (i = 0; i < results.data.length; i++)
								{
									// if the title is empty, we ignore the row
									if (results.data[i].title.length > 0)
									{
										submitlist.push(results.data[i]);
										createMarker(
										{
											'title': results.data[i].title,
											'latitude': results.data[i].latitude,
											'longitude': results.data[i].longitude,
											'description': results.data[i].description,
											'external_url': results.data[i].externalurl
										});
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
									});
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
					// get the file that is selected
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
					$('#addlist')
						.modal('hide');
				};

				// download a CSV with all the points from the map
				$scope.downloadcsv = function()
				{
					$http(
					{
						method: 'GET',
						url: DOWNLOAD_CSV,
						headers:
						{
							'Content-Type': 'text/csv'
						} // set the headers so angular passing info as form data (not request payload)
					}).success(function(data){
						var csvContent = "data:text/csv;charset=utf-8,";
						csvContent += data
						var encodedUri = encodeURI(csvContent);
						var link = document.createElement("a");
						link.setAttribute("href", encodedUri);
						link.setAttribute("download", "" + $scope.maptitle + "_points.csv");
						link.click();
						// window.open(encodedUri);
					})	
				};


			}]);
















	angular.module('app')
		.controller('ModalDemoCtrl', function($scope, $uibModal, $log)
		{

			$scope.items = ['item1', 'item2', 'item3'];

			$scope.animationsEnabled = true;

			$scope.open = function(size)
			{

				var modalInstance = $uibModal.open(
				{
					animation: $scope.animationsEnabled,
					template: '#myModalContent',
					controller: 'ModalInstanceCtrl',
					size: size,
					resolve:
					{
						items: function()
						{
							return $scope.items;
						}
					}
				});

				modalInstance.result.then(function(selectedItem)
				{
					$scope.selected = selectedItem;
				}, function()
				{
					$log.info('Modal dismissed at: ' + new Date());
				});
			};

			$scope.toggleAnimation = function()
			{
				$scope.animationsEnabled = !$scope.animationsEnabled;
			};

		});

	// Please note that $modalInstance represents a modal window (instance) dependency.
	// It is not the same as the $uibModal service used above.

	angular.module('app')
		.controller('ModalInstanceCtrl', function($scope, $uibModalInstance, items)
		{

			$scope.items = items;
			$scope.selected = {
				item: $scope.items[0]
			};

			$scope.ok = function()
			{
				$uibModalInstance.close($scope.selected.item);
			};

			$scope.cancel = function()
			{
				$uibModalInstance.dismiss('cancel');
			};
		});






























})();