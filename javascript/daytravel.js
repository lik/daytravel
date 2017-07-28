function address () {
console.log("address")
}
var options = {
  types: ['(cities)'],
  componentRestrictions: {country: "us"}
 };

 var input = document.getElementById('pac-input');
 var autocomplete = new google.maps.places.Autocomplete(input, options);



 autocomplete.addListener('place_changed', address);

function next2Click() {
  var city = $('#pac-input').val();
  window.location = '/plan?city=' + city

}
