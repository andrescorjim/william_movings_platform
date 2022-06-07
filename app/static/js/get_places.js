$(function () {
  // add input listeners
  google.maps.event.addDomListener(window, "load", function () {
    var from_places = new google.maps.places.Autocomplete(document.getElementById("from_places"));
    var to_places = new google.maps.places.Autocomplete(document.getElementById("to_places"));

    google.maps.event.addListener(from_places, "place_changed", function () {
      var from_place = from_places.getPlace();
      var from_address = from_place.formatted_address;
      $("#origin").val(from_address);
    });

    google.maps.event.addListener(to_places, "place_changed", function () {
      var to_place = to_places.getPlace();
      var to_address = to_place.formatted_address;
      $("#destination").val(to_address);
    });
  });
});
