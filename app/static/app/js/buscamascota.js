
function initMap(mapDivId,isIndex) {
    /**
     Initialize leaflet Map in the DOM
     @param mapDivName: ID of the map's div in the DOM
     @param isIndex: boolean to know if the map is Index page
      **/
    var map;
    if (isIndex){
        map = L.map(mapDivId, {
            scrollWheelZoom: false,
            fullscreenControl: true,
            // OR
            fullscreenControl: {
                pseudoFullscreen: false // if true, fullscreen to page width and height
            },
            minZoom: 2
        }).setView([0, 0], 2);
    }
    else{
        map = L.map(mapDivId, {
            fullscreenControl: true,
            // OR
            fullscreenControl: {
                pseudoFullscreen: false // if true, fullscreen to page width and height
            },
            minZoom: 2
        }).setView([-23.3165935,-58.1693445], 6); //Paraguay's coordenates
    }

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    return map;
}

function completeUbicationWidgets(latitude, longitude){
    /**
    * Complete widgets (country, postal_code,city, address, ubication_resume) from the form related with ubication when click.
    * @param latitude: latitude of marker when click
    * @param longitude: longitude of marker when click
    **/
    let xhttp = new XMLHttpRequest();
    let url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" + latitude + "&lon="+ longitude;
    let pagina;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            pagina = xhttp.responseText;
            let parseado = JSON.parse(pagina);
            if(parseado.display_name){
                document.getElementById("id_ubication_resume").value = parseado.display_name;
                if(parseado['address'].country)
                    document.getElementById("id_country").value = parseado['address'].country;
                if(parseado['address'].postcode)
                    document.getElementById("id_postal_code").value = parseado['address'].postcode;
                if(parseado['address'].city)
                    document.getElementById("id_city").value = parseado['address'].city;
                if(parseado['address'].road)
                    document.getElementById("id_address").value = parseado['address'].road;
            }
            else{
                document.getElementById("id_ubication_resume").value = '';
                document.getElementById("id_country").value = '';
                document.getElementById("id_postal_code").value = '';
                document.getElementById("id_city").value = '';
                document.getElementById("id_address").value = '';
            }
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}