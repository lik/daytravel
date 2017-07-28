function address () {
console.log("address")
}

var autocomplete = new google.maps.places.Autocomplete($("#pac-input")[0]);


 autocomplete.addListener('place_changed', address);
