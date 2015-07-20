var map = L.map('map').setView([51.505, -0.09], 13);
var userPostCode;
var marker;


var gpIcon = L.icon({
    iconUrl: '../img/gp.png',
    iconSize:     [30, 30], // size of the icon
    iconAnchor:   [30, 30], // point of the icon which will correspond to marker's location
    popupAnchor:  [-15, -27] // point from which the popup should open relative to the iconAnchor
});

var trainStIcon = L.icon({
    iconUrl: '../img/trainSt.jpg',
    iconSize:     [30, 20], // size of the icon
    iconAnchor:   [30, 20], // point of the icon which will correspond to marker's location
    popupAnchor:  [-15, -18] // point from which the popup should open relative to the iconAnchor
});

var supermarketIcon = L.icon({
    iconUrl: '../img/supermarket.png',
    iconSize:     [30, 30], // size of the icon
    iconAnchor:   [30, 30], // point of the icon which will correspond to marker's location
    popupAnchor:  [-15, -30] // point from which the popup should open relative to the iconAnchor
});

var schoolIcon = L.icon({
    iconUrl: '../img/school.png',
    iconSize:     [30, 28], // size of the icon
    iconAnchor:   [30, 28], // point of the icon which will correspond to marker's location
    popupAnchor:  [-15, -28] // point from which the popup should open relative to the iconAnchor
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
				marker = L.marker([response.latitude, response.longitude]).addTo(map).bindPopup('<p>You are here ' + response.postcode + '</p>');
				map.setView(new L.LatLng(response.latitude, response.longitude), 14);
				lookUpGP(response.postcode, response.latitude, response.longitude);
				lookUpTrainStation(response.postcode, response.latitude, response.longitude);
				lookUpSupermarket(response.postcode, response.latitude, response.longitude);
				lookUpSchool(response.postcode, response.latitude, response.longitude);
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

function lookUpGP(postcode, latitude, longitude){
	$.ajax({
		type: 'POST',
		url: '/lookUpGP',
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

function lookUpTrainStation(postcode, latitude, longitude){
	$.ajax({
		type: 'POST',
		url: '/lookUpTrainStation',
		dataType: 'json',
		ContentType: 'application/json',
		data: {'postcode': postcode, 'latitude': latitude, 'longitude': longitude},
		success: function(response){
			if(response) {
				displayTrainStation(response);
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

function lookUpSupermarket(postcode, latitude, longitude){
	$.ajax({
		type: 'POST',
		url: '/lookUpSupermarket',
		dataType: 'json',
		ContentType: 'application/json',
		data: {'postcode': postcode, 'latitude': latitude, 'longitude': longitude},
		success: function(response){
			if(response) {
				displaySupermarket(response);
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

function lookUpSchool(postcode, latitude, longitude){
	$.ajax({
		type: 'POST',
		url: '/lookUpSchool',
		dataType: 'json',
		ContentType: 'application/json',
		data: {'postcode': postcode, 'latitude': latitude, 'longitude': longitude},
		success: function(response){
			if(response) {
				displaySchool(response);
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
	});
}

function displayTrainStation(tObject) {
	$.each(tObject, function(index, tObject) {
		L.marker([tObject.latitude, tObject.longitude], {icon: trainStIcon}).addTo(map).bindPopup(tObject.name + ' ' + '['+ tObject.distance + ' mi]');
	});
}

function displaySupermarket(spObject) {
	$.each(spObject, function(index, spObject) {
		L.marker([spObject.latitude, spObject.longitude], {icon: supermarketIcon}).addTo(map).bindPopup(spObject.name + '<br/>' + spObject.address + '<br/>' +
		spObject.postcode + ' ' + '['+ spObject.distance + ' mi]');
	});
}

function displaySchool(slObject) {
	$.each(slObject, function(index, slObject) {
		L.marker([slObject.latitude, slObject.longitude], {icon: schoolIcon}).addTo(map).bindPopup(slObject.name + '<br/>' + slObject.address + '<br/>' +
		slObject.postcode + ' ' + '['+ slObject.distance + ' mi]');
	});
}




