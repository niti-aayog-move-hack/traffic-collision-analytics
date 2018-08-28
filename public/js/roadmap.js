list = []
themcircles = []

var alarm_color_mapper = {
    "UFCW": "#1446A0", 
    "PCW": "#C7FFED",
    "Overspeed": "#3B3355",
    "HMW": "#7BDFF2",
    "FCW": "#4062BB" ,
    "LDWL": "#B2F7EF", 
    "LDWR": "#1B998B"
}

/*Temprorary fix to reload the whole thing on sentiment, need to create a fucntion that changes teh color of circles on click, whitout calling the API again*/

function initialize_one(sentiment) {
        
        url = "/demo/road-overall";
    

    $.post(url, {data : {}},function(list, status){ 
        console.log(list);           
        

        var map_options = {
            center: new google.maps.LatLng("12.9558", "77.7609"),
            zoom: 12.8,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        google_map = new google.maps.Map(document.getElementById("map_canvas"), map_options);

        var info_window = new google.maps.InfoWindow({
            content: 'loading'
        });
  


        var t = [];
        var x = [];
        var y = [];
        var h = [];
        var htmp = [];



        for(i =0; i<list.length; i++){
                htmp.push({location: new google.maps.LatLng(list[i].lat, list[i].lng), weight: list[i].speed})
                t.push(list[i].ward);
                x.push(parseFloat(list[i].lat));
                y.push(parseFloat(list[i].lng));
                h.push('<p><strong><span style = "font-size:15px">'+ list[i].ward + '</strong></span><br/><strong>Alarm </strong>' + list[i].alarm + "<br /> <strong>Speed:</strong>"+ list[i].speed);

                thecolor = alarm_color_mapper[list[i].alarm];

            var circleOptions = {
                strokeColor: "#000000",
                strokeOpacity: 0.5,
                strokeWeight: 0.5,
                fillColor: thecolor,
                fillOpacity: 0.65,
                map: google_map,
                center: new google.maps.LatLng(parseFloat(list[i].lat), parseFloat(list[i].lng)),
                radius: list[i].speed * 4
            };

                themcircles.push(new google.maps.Circle(circleOptions));
                themcircles[i].setMap(google_map);
        }
        console.log(themcircles);

        heatmap = new google.maps.visualization.HeatmapLayer({
            data: htmp,
            maxIntensity:5,
            opacity:0.7,
            radius:20,
            gradient: ['#ffffb2','#fd8d3c','#fd8d3c','#f03b20','#bd0026']
        });

        var z =0;
   //$()
        var i = 0;
        markers = [];
        for ( item in t ) {
            var marker = new
                google.maps.Marker({
                map:       google_map,
                animation: google.maps.Animation.DROP,
                title:     t[i],
                position:  new google.maps.LatLng(x[i],y[i]),
                html:      h[i]
            });

            markers.push(marker); // Add the current marker to the array for later processing

            google.maps.event.addListener(marker, 'click', function() {
                info_window.setContent(this.html);
                info_window.open(google_map, this);
            });
            i++;
        }
    });
}

var trafficLayer = new google.maps.TrafficLayer();

function dispTraffic_one(){
  if(trafficLayer.getMap()){
      trafficLayer.setMap(null);
  }
  else{
    trafficLayer.setMap(google_map);
  }
}



function heat_one(){

  if(heatmap.getMap()){
      heatmap.setMap(null);
      console.log(themcircles);
      for(var iter = 0; iter<list.length; iter++){
        themcircles[iter].setOptions({fillOpacity:0.65, strokeOpacity:0.5});
      }
      document.getElementById("heatmap_map_one").innerHTML = "Show Heatmap";
  }
  else{
    heatmap.setMap(google_map);
    for(var iter = 0; iter<list.length; iter++){
        themcircles[iter].setOptions({fillOpacity:0, strokeOpacity:0});
    }
    document.getElementById("heatmap_map_one").innerHTML = "Hide Heatmap";

  }
}



isDis = false;

function distribution_one(){
    if(isDis){
    document.getElementById("distribution_map_one").innerHTML = "Show Distribution";
  }
  else{
    document.getElementById("distribution_map_one").innerHTML = "Unhide Marker";
  }
    for(x =0; x < markers.length; x++){
            markers[x].setVisible(isDis);
       }
    isDis = !isDis;
}

initialize_one();  //Initialize map function
heat_one();
