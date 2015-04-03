function initialize() {
    var markers = [];
    var mapCanvas = document.getElementById('map');
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
	
	//google.maps.event.addListener(map, 'click', function(event) {
	//	alert('Lat: ' + event.latLng.lat() + ' Lng: ' + event.latLng.lng());
	//});
	
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