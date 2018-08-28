list = []
themcircles_four = []


/*Temprorary fix to reload the whole thing on sentiment, need to create a fucntion that changes teh color of circles on click, whitout calling the API again*/

function initialize_four(sentiment) {
        
        url = "/demo/road-weather";
    

    $.post(url, {data : {}},function(list, status){ 
        console.log(list);           
        

        var map_options = {
            center: new google.maps.LatLng("12.9698", "77.7309"),
            zoom: 12.5,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        google_map_four = new google.maps.Map(document.getElementById("map_canvas_four"), map_options);

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

                thecolor = "#7BDFF2";

            var circleOptions = {
                strokeColor: "#000000",
                strokeOpacity: 0.5,
                strokeWeight: 0.5,
                fillColor: thecolor,
                fillOpacity: 0.65,
                map: google_map_four,
                center: new google.maps.LatLng(parseFloat(list[i].lat), parseFloat(list[i].lng)),
                radius: list[i].speed * 4
            };

                themcircles_four.push(new google.maps.Circle(circleOptions));
                themcircles_four[i].setMap(google_map_four);
        }
        console.log(themcircles_four);

        heatmap_four = new google.maps.visualization.HeatmapLayer({
            data: htmp,
            maxIntensity:5,
            opacity:0.7,
            radius:20,
            gradient: ['#ffffb2','#fd8d3c','#fd8d3c','#f03b20','#bd0026']
        });

        var z =0;
   //$()
        var i = 0;
        markers_four = [];
        for ( item in t ) {
            var marker = new
                google.maps.Marker({
                map:       google_map_four,
                animation: google.maps.Animation.DROP,
                title:     t[i],
                position:  new google.maps.LatLng(x[i],y[i]),
                html:      h[i]
            });

            markers_four.push(marker); // Add the current marker to the array for later processing

            google.maps.event.addListener(marker, 'click', function() {
                info_window.setContent(this.html);
                info_window.open(google_map_four, this);
            });
            i++;
        }
    });
}

var trafficLayer_four = new google.maps.TrafficLayer();

function dispTraffic_four(){
  if(trafficLayer_four.getMap()){
      trafficLayer_four.setMap(null);
  }
  else{
    trafficLayer_four.setMap(google_map_four);
  }
}



function heat_four(){

  if(heatmap_four.getMap()){
      heatmap_four.setMap(null);
      console.log(themcircles_four);
      for(var iter = 0; iter<list.length; iter++){
        themcircles_four[iter].setOptions({fillOpacity:0.65, strokeOpacity:0.5});
      }
      document.getElementById("heatmap_map_four").innerHTML = "Show heatmap";
  }
  else{
    heatmap_four.setMap(google_map_four);
    for(var iter = 0; iter<list.length; iter++){
        themcircles_four[iter].setOptions({fillOpacity:0, strokeOpacity:0});
    }
    document.getElementById("heatmap_map_four").innerHTML = "Hide heatmap";

  }
}



isDis = false;

function distribution_four(){
    if(isDis){
    document.getElementById("distribution_map_four").innerHTML = "Show Distribution";
  }
  else{
    document.getElementById("distribution_map_four").innerHTML = "Unhide Marker";
  }
    for(x =0; x < markers_four.length; x++){
            markers_four[x].setVisible(isDis);
       }
    isDis = !isDis;
}

initialize_four();  //Initialize map function
heat_four();
