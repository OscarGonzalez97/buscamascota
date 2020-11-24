
function initMap(mapDivId) {
    /**
     Initialize leaflet Map in the DOM
     @param mapDivName: ID of the map's div in the DOM
     @param isIndex: boolean to know if the map is Index page
      **/
    let map;
    map = L.map(mapDivId, {
        scrollWheelZoom: true,
        fullscreenControl: true,
        // OR
        fullscreenControl: {
            pseudoFullscreen: false
        },
        minZoom: 2
    }).setView([-23.3165935,-58.1693445], 6); //Paraguay's coordenates
    

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    return map;
}

function addMarkers(reports, map, markers) {

    /***
    map: variable containing the map
    markers: variable containing the group of markers
    ***/
    
    // Create markers
    let inst_lat, inst_lng; 
    let arr_pos = [];
    let new_lat, new_lng;

    for (i=0; i < reports.length; i++) {
        lat = reports[i].latitude;
        lon = reports[i].longitude;

        let leafletMarker = L.marker([lat,lon]);
        
        leafletMarker.bindPopup(generateInfoWindowContent(reports[i]), {
            minWidth : 200
        } ).openPopup();
        
        markers.addLayer(leafletMarker);
    }

    //leaflet cluster added to map
    map.addLayer(markers);
}

function generateInfoWindowContent(report_info) {
    let content = "";
    content = "<p class='text-center text-uppercase h4' style='color: red;'>" + report_info.report_type + "</p>" 
    content += "<img src='"+report_info.picture+"' alt='mascota' style='width: 100%; height: 100%;'>";
    if (report_info.phone != null) 
        content += "<p class='text-center h6'> Contacto: " + report_info.phone + "</p>";
    content += "<p class='text-center text-dark'> <a class=\"btn btn-warning mt-1 amarillo\" href=\"http://buscamascota.org/reporte/"+ report_info.id +"\"> Ver reporte completo </a>  </p>"
    return content
}

function completeUbicationWidgets(latitude, longitude){
    /**
    * Complete widgets (country, postal_code,city, address, ubication_resume) from the form related with ubication when clicked.
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

function enableSubmit(){
    /**
    * Enable submit button of the form when accept terms of use or disable when not, depends on checkbox.
    **/
    if(document.getElementById("id_accept_terms").checked){
        document.getElementById("submitButton").disabled = false;
    }
    else{
        document.getElementById("submitButton").disabled = true;
    }
}

function changeView(){
    if(document.getElementById("viewMap").checked){
        document.getElementById("divMapView").style.display = 'block';
        document.getElementById("divListView").style.display = 'none';
    }
    else if (document.getElementById("viewList").checked){
        document.getElementById("divMapView").style.display = 'none';
        document.getElementById("divListView").style.display = 'block';
    }
    else{

    }
}