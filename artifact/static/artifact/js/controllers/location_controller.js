(function() {
    //Angular App Module and Controller
    angular.module('app')
        .controller('LocationController', ['$scope', '$http', '$timeout',
            'djangoUrl',
            function($scope, $http, $timeout, $djangoUrl)
            {
                var GET_LOC = $djangoUrl.reverse('artifact:map_location', [$scope.map_id]);
                var GET_MARKERS = $djangoUrl.reverse('artifact:markers', [$scope.map_id]);
                var UPDATE_MARKER = $djangoUrl.reverse('artifact:updatePoint', [$scope.selectedMarker]);
                var GET_CSV = $djangoUrl.reverse('artifact:csv_points', [$scope.map_id]);
                var DOWNLOAD_CSV = $djangoUrl.reverse('artifact:download_csv', [$scope.map_id]);
                var responsePromise = $http.get(GET_LOC);

                // gather the information of the selected point on the right sidebar
                var showInfo = function(marker) {
                    $scope.point.title = marker.title;
                    $scope.point.description = marker.description;
                    $scope.point.external_url = marker.external_url;
                    $scope.point.latitude = marker.latitude;
                    $scope.point.longitude = marker.longitude;
                };

                $("#hideshow")
                    .click(function() {
                        $("#panorama-wrapper")
                            .toggle();
                    });

                // Generates small panorama image in right sidebar. It also makes sure the street view is
                // always facing in the direction of the marker that is selected
                function setPanorama(location) {
                    var panodiv = document.getElementById('panorama-canvas');
                    var panowarn = document.getElementById('panorama-warning');
                    if (pano) {
                        pano.setPosition(location);
                        service.getPanoramaByLocation(pano.getPosition(), 1000, function(panoData) {
                            if (panoData !== null) {
                                panodiv.style.visibility = 'visible';
                                panowarn.innerHTML = "Street View:";
                                var panoCenter = panoData.location.latLng;
                                var heading = google.maps.geometry.spherical.computeHeading(panoCenter, location);
                                var pov = pano.getPov();
                                pov.heading = heading;
                                pano.setPov(pov);
                            }
                            else {
                                panowarn.innerHTML = "No street view available.";
                                panodiv.style.visibility = 'hidden';
                            }
                        });
                    }
                    else {
                        var panoOptions = {
                            position: location,
                            panControl: false,
                            addressControl: false,
                            linksControl: false,
                            zoomControlOptions: false
                        };
                        var pano = new google.maps.StreetViewPanorama(document.getElementById('panorama-canvas'), panoOptions);
                        var service = new google.maps.StreetViewService();
                        service.getPanoramaByLocation(pano.getPosition(), 50, function(panoData) {
                            if (panoData !== null) {
                                panodiv.style.visibility = 'visible';
                                panowarn.innerHTML = "Street View:";
                                var panoCenter = panoData.location.latLng;
                                var heading = google.maps.geometry.spherical.computeHeading(panoCenter, location);
                                var pov = pano.getPov();
                                pov.heading = heading;
                                pano.setPov(pov);
                            }
                            else {
                                panodiv.style.visibility = 'hidden';
                                panowarn.innerHTML = "No street view available.";
                            }
                        });
                    }
                }

                // creates markers on page load and when submitting new point form
                var createMarker = function(info) {
                    var marker = new google.maps.Marker({
                        map: $scope.map,
                        position: new google.maps.LatLng(info.latitude, info.longitude),
                        title: info.title
                    });
                    marker.id = info.id || undefined;
                    marker.description = info.description;
                    marker.external_url = info.external_url;
                    marker.latitude = info.latitude;
                    marker.longitude = info.longitude;
                    $scope.markers.push(marker);
                    marker.setMap($scope.map);

                    // on map click, put temporary marker that can be used to create a new point
                    var newmarker;
                    $scope.formData = {};

                    function placeMarker(location) {
                        var pinColor = "008000";
                        var pinImage = new google.maps.MarkerImage(
                            "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
                            new google.maps.Size(21, 34),
                            new google.maps.Point(0, 0),
                            new google.maps.Point(10, 34));
                        if (newmarker) {
                            newmarker.setPosition(location);
                            $scope.newmarker_window.setContent("<a data-target='#singlepointmodal' data-toggle='modal' id='add-location' type='button'>Save this point</a>");
                            $scope.newmarker_window.open($scope.map, newmarker);
                        }
                        else {
                            newmarker = new google.maps.Marker({
                                position: location,
                                map: $scope.map,
                                icon: pinImage,
                            });
                            $scope.newmarker_window.setContent("<a data-target='#singlepointmodal' data-toggle='modal' id='add-location' type='button'>Save this point</a>");
                            $scope.newmarker_window.open($scope.map, newmarker);

                            google.maps.event.addListener(newmarker, 'mouseover', function(event) {
                                $scope.newmarker_window.open($scope.map, this);
                                // placeMarker(event.latLng);
                                $scope.infowindow.close($scope.map, marker);
                                $scope.point.title = 'New point';
                                $scope.point.description = '';
                                $scope.point.external_url = '';
                                $scope.point.latitude = event.latLng.lat();
                                $scope.point.longitude = event.latLng.lng();
                                setPanorama(event.latLng);
                                $scope.formData.latitude = $scope.point.latitude;
                                $scope.formData.longitude = $scope.point.longitude;
                                $scope.$apply();
                                ;
                            });
                        }
                    }


                    // on marker mouseover, change the information in the right sidebar
                    google.maps.event.addListener(marker, 'mouseover', function(event) {
                        $scope.newmarker_window.close($scope.map, newmarker);
                        $scope.infowindow.setContent("<p><b>" + marker.title + "</b></p><p>" + marker.description + "</p>");
                        $scope.infowindow.open($scope.map, marker);
                        setPanorama(event.latLng);
                        showInfo(marker);
                        $scope.$apply();
                    });


                    // Move the marker that the user has added by clicking
                    google.maps.event.addListener($scope.map, 'click', function(event) {
                        $scope.newmarker_window.open($scope.map, this);
                        placeMarker(event.latLng);
                        $scope.infowindow.close($scope.map, marker);
                        $scope.point.title = 'New point';
                        $scope.point.description = '';
                        $scope.point.external_url = '';
                        setPanorama(event.latLng);
                        $scope.$apply();
                    });
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
                    $scope.description = data.description;
                    $scope.map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
                    $scope.newmarker_window = new google.maps.InfoWindow();
                    $scope.infowindow = new google.maps.InfoWindow();

                    // change the selected marker on when clicking from list
                    $scope.selectMarker = function(e, marker) {
                        setPanorama(marker.position);
                        showInfo(marker);
                        $scope.infowindow.setContent("<p><b>" + marker.title + "</b></p><p>" + marker.description + "</p>");
                        $scope.infowindow.open($scope.map, marker);
                        $scope.newmarker_window.close($scope.map, this);
                    };
                    $scope.editMarker = function(e, marker) {
                        $scope.updateData = {};
                        $scope.updateData = $.extend(true, {}, marker);
                        $scope.selectedMarker = marker.id;

                    };

                    $scope.point = [];
                    $scope.markers = [];
                    for (i = 0; i < data.markers.length; i++) {
                        createMarker(data.markers[i]);
                    }
                });



                // adds a single point to the map
                $scope.processForm = function() {
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
                            $scope.formData = {};
                            $('#singlepointmodal')
                                .modal('hide');
                        });
                };
                $scope.clear = function(){
                    $scope.formData = {};
                }
                $scope.updateForm = function() {
                    $http({
                            method: 'POST',
                            url: UPDATE_MARKER,
                            data: $.param($scope.updateData),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            } // set the headers so angular passing info as form data (not request payload)
                        })
                        .then(function(data) {
                            // TODO update marker instead of creating new one
                            createMarker({
                                'id': $scope.updateData.id,
                                'title': $scope.updateData.title,
                                'latitude': $scope.updateData.latitude,
                                'longitude': $scope.updateData.longitude,
                                'description': $scope.updateData.description,
                                'external_url': $scope.updateData.externalurl,
                                'fileupload': $scope.updateData.fileupload,
                            });
                            $('#editpoint')
                                .modal('hide');
                        });
                };


                // uploads a file with multiple csv points to the map
                $scope.uploadFile = function() {
                    // configuration for csv parser
                    function buildConfig() {
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
                            complete: function(results, file) {
                                // list of points to pass to api.py
                                var submitlist = [];
                                for (i = 0; i < results.data.length; i++) {
                                    // if the title is empty, we ignore the row
                                    if (results.data[i].title.length > 0) {
                                        submitlist.push(results.data[i]);
                                        createMarker({
                                            'title': results.data[i].title,
                                            'latitude': results.data[i].latitude,
                                            'longitude': results.data[i].longitude,
                                            'description': results.data[i].description,
                                            'external_url': results.data[i].externalurl
                                        });
                                    }
                                    else {
                                        continue;
                                    }
                                }
                                $http({
                                    method: 'POST',
                                    url: GET_CSV,
                                    data: submitlist,
                                    headers: {
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
                    if (files.length > 0) {
                        $('#files')
                            .parse({
                                config: config,
                                before: function(file, inputElem) {},
                                complete: function() {}
                            });
                    }
                    else {
                        window.alert("You must upload a valid file. Please try again.");
                    }
                    $('#addlist')
                        .modal('hide');
                };


                // download a CSV with all the points from the map
                $scope.downloadcsv = function() {
                    $http({
                            method: 'GET',
                            url: DOWNLOAD_CSV,
                            headers: {
                                'Content-Type': 'text/csv'
                            }
                        })
                        .success(function(data) {
                            var csvContent = "data:text/csv;charset=utf-8,";
                            csvContent += data;
                            var encodedUri = encodeURI(csvContent);
                            var link = document.createElement("a");
                            link.setAttribute("href", encodedUri);
                            link.setAttribute("download", "" + $scope.maptitle + "_points.csv");
                            link.click();
                        });
                };
   }]);
})();