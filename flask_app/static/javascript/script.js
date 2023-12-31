const center = { lat: 50.064192, lng: -130.605469 };
const defaultBounds = {
    north: center.lat + 0.1,
    south: center.lat - 0.1,
    east: center.lng + 0.1,
    west: center.lng - 0.1,
};
const input = document.getElementById("ship-address");
const options = {
    bounds: defaultBounds,
    componentRestrictions: { country: "us" },
    fields: ["address_components", "geometry", "icon", "name"],
    strictBounds: false,
    types: ["establishment"],
};
const autocomplete = new google.maps.places.Autocomplete(input, options);
