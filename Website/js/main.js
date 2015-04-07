function initialize() {
    var markers = [];
    var mapCanvas = document.getElementById('map');
	document.getElementById('doSearch').onclick = performRadarSearch;
    var mapOptions = {
        center: new google.maps.LatLng(44.5403, -78.5463),
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
    var input = document.getElementById('searchTextField');
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    var searchBox = new google.maps.places.SearchBox(input);
	var infowindow = new google.maps.InfoWindow();
	var service = new google.maps.places.PlacesService(map);
	var sock;
	$(document).ready(function() {
		
		sock = new WebSocket("ws://compute.cse.tamu.edu:12345/yelp");
		sock.onopen = function(){console.log("Connected ws"); };
		sock.onmessage = function(event) { document.getElementById('line1').innerHTML = event.data;};
	
	
	});
	
	
	
	google.maps.event.addListener(map, 'click', function(event) {
		//sock.send('Lat: ' + event.latLng.lat() + ' Lng: ' + event.latLng.lng());
		
		//alert('Lat: ' + event.latLng.lat() + ' Lng: ' + event.latLng.lng());
	});
	
	function performRadarSearch() {
		var request = {
			bounds: map.getBounds(),
			keyword: 'interesting' //work with this		
		};
		service.radarSearch(request, callback);		
	}
	
	function callback(results, status) {
		
		if(status != google.maps.places.PlacesServiceStatus.OK) {
			alert(status);
			return;			
		}
		for(var i = 0, result; result = results[i]; i++) {
			createMarker(result);
		}			
	}
	
	function createMarker(place) {
		var marker = new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            });
			console.log(place.name);
			google.maps.event.addListener(marker, 'click', function() {
				service.getDetails(place, function(result, status) {
					if(status != google.maps.places.PlacesServiceStatus.OK) {
						alert(status);
						return;
					}
					infowindow.setContent(result.name);
					infowindow.open(map, marker);
					sock.send(result.name);
					
				});
				
				
				

			});			
			
	}
	
    // Listen for the event fired when the user selects an item from the
    // pick list. Retrieve the matching places for that item.
    google.maps.event.addListener(searchBox, 'places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
          return;
        }
        for (var i = 0, marker; marker = markers[i]; i++) {
          marker.setMap(null);
        }

        // For each place, get the icon, place name, and location.
        markers = [];
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places[i]; i++) {
			var image = {
				url: place.icon,
				size: new google.maps.Size(71, 71),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(17, 34),
				scaledSize: new google.maps.Size(25, 25)
			};

            // Create a marker for each place.
            var marker = new google.maps.Marker({
                map: map,
                //icon: image,
                title: place.name,
                position: place.geometry.location
            });

			google.maps.event.addListener(marker, 'click', function() {
				infowindow.setContent(this.title);
				infowindow.open(map, this);

			});
            markers.push(marker);

            bounds.extend(place.geometry.location);
        }

        map.fitBounds(bounds);
  });

  
  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(map, 'bounds_changed', function() {
        var bounds = map.getBounds();
        searchBox.setBounds(bounds);
  });
}

google.maps.event.addDomListener(window, 'load', initialize);