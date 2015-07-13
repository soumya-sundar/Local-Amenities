var map = L.map('map').setView([51.505, -0.09], 13);
var userPostCode;
var marker;


var gpIcon = L.icon({
    iconUrl: '../img/gp.png',
    iconSize:     [38, 38], // size of the icon
    iconAnchor:   [22, 30], // point of the icon which will correspond to marker's location
    popupAnchor:  [-3, -30] // point from which the popup should open relative to the iconAnchor
});


L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
	maxZoom: 18,
	id: 'soumyasundar.f9f4c7f8',
	accessToken: 'pk.eyJ1Ijoic291bXlhc3VuZGFyIiwiYSI6ImFmMWMzNTMxOGVkZTVlMGNmYmE4ZGQ5ZWJkZWE3YTU2In0.zipdQb4X9PVTAMVvu4r-6g'
}).addTo(map);

$('#submitButton').on("click",function(event){
	userPostCode = $('#postcode').val();
	$.ajax({
		type: 'POST',
		url: '/processPostCode',
		dataType: 'json',
		ContentType: 'application/json',
		data: {'postcode': userPostCode},
		success: function(response){
			var resParsed;
			if(response.found === true) {
				marker = L.marker([response.latitude, response.longitude]).addTo(map);
				map.setView(new L.LatLng(response.latitude, response.longitude), 13);
				lookUp(response.postcode, response.latitude, response.longitude);
			}
			else {
				$('#postcode').popover('show');
			}
		},
		error: function(e) {
			console.log(e.message);
		}
	});
	event.preventDefault();
});

function lookUp(postcode, latitude, longitude){
	$.ajax({
		type: 'POST',
		url: '/lookUp',
		dataType: 'json',
		ContentType: 'application/json',
		data: {'postcode': postcode, 'latitude': latitude, 'longitude': longitude},
		success: function(response){
			if(response) {
				displayGP(response);
			}
			else {
				alert("not found");
			}
		},
		error: function(e) {
			console.log(e.message);
		}
	});
	event.preventDefault();
}

function displayGP(gpObject) {
	$.each(gpObject, function(index, gpObject) {
		L.marker([gpObject.latitude, gpObject.longitude], {icon: gpIcon}).addTo(map).bindPopup(gpObject.name + '<br/>' + gpObject.address + '<br/>' +
		gpObject.postcode + ' ' + '['+ gpObject.distance + ' mi]');
		/*$('#test').append('<p><strong>' + gpObject.name + '</strong><br /> address: ' +
			gpObject.address + '<br /> postcode: ' +
			gpObject.postcode + '<br />latitude: ' +
			gpObject.latitude + '<br />longitude: ' +
			gpObject.longitude + '</p>');*/
	});
}



