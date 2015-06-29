
	var map = L.map('map').setView([51.505, -0.09], 13);

	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
	maxZoom: 18,
	id: 'soumyasundar.f9f4c7f8',
	accessToken: 'pk.eyJ1Ijoic291bXlhc3VuZGFyIiwiYSI6ImFmMWMzNTMxOGVkZTVlMGNmYmE4ZGQ5ZWJkZWE3YTU2In0.zipdQb4X9PVTAMVvu4r-6g'
	}).addTo(map);
