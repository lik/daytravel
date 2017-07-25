var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://api.yelp.com/v3/businesses/search?location=Mountain%20View",
  "method": "GET",
  "headers": {
    "authorization": "Bearer BIO6_LpbIcFkeKDB9SsSAONt3lE2IwrdiTxUeq-Ag1MKOzSc4m-8QyPjdV6WmI27ySuLEKv7czHoJmJjFHrCyjfgxucTvKPpJG9JCsg_08KCz4J-WrEfeaiACoJ2WXYx",
    "cache-control": "no-cache",
    "postman-token": "91ce3f24-a298-cae4-7e6f-f010bb6b094a"
  }
}

$.ajax(settings).done(function (response) {
  console.log(response[0]);
});
