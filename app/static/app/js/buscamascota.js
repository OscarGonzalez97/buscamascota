

function initMap(mapDivId,isIndex) {
    /**
     mapDivName: ID of the map's div in the html code
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
        }).setView([-23.3165935,-58.1693445], 6); //coordenadas de Paraguay
    }


    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    return map;
}