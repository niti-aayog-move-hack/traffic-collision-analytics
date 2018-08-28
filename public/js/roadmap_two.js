list = []
themcircles_two = []


/*Temprorary fix to reload the whole thing on sentiment, need to create a fucntion that changes teh color of circles on click, whitout calling the API again*/

function initialize_two(sentiment) {
        
        url = "/demo/road-loc";
    

    $.post(url, {data : {}},function(list, status){ 
        console.log(list);           
        

        var map_options = {
            center: new google.maps.LatLng("12.9798", "77.7309"),
            zoom: 13.5,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        google_map_two = new google.maps.Map(document.getElementById("map_canvas_two"), map_options);

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

                thecolor = "#ff0000";

            var circleOptions = {
                strokeColor: "#000000",
                strokeOpacity: 0.5,
                strokeWeight: 0.5,
                fillColor: thecolor,
                fillOpacity: 0.65,
                map: google_map_two,
                center: new google.maps.LatLng(parseFloat(list[i].lat), parseFloat(list[i].lng)),
                radius: list[i].speed * 4
            };

                themcircles_two.push(new google.maps.Circle(circleOptions));
                themcircles_two[i].setMap(google_map_two);
        }
        console.log(themcircles_two);

        heatmap_two = new google.maps.visualization.HeatmapLayer({
            data: htmp,
            maxIntensity:5,
            opacity:0.7,
            radius:20,
            gradient: ['#ffffb2','#fd8d3c','#fd8d3c','#f03b20','#bd0026']
        });

        var z =0;
   //$()
        var i = 0;
        markers_two = [];
        for ( item in t ) {
            var marker = new
                google.maps.Marker({
                map:       google_map_two,
                animation: google.maps.Animation.DROP,
                title:     t[i],
                position:  new google.maps.LatLng(x[i],y[i]),
                html:      h[i]
            });

            markers_two.push(marker); // Add the current marker to the array for later processing

            google.maps.event.addListener(marker, 'click', function() {
                info_window.setContent(this.html);
                info_window.open(google_map_two, this);
            });
            i++;
        }
    });
}

var trafficLayer_two = new google.maps.TrafficLayer();

function dispTraffic_two(){
  if(trafficLayer_two.getMap()){
      trafficLayer_two.setMap(null);
  }
  else{
    trafficLayer_two.setMap(google_map_two);
  }
}



function heat_two(){

  if(heatmap_two.getMap()){
      heatmap_two.setMap(null);
      console.log(themcircles_two);
      for(var iter = 0; iter<list.length; iter++){
        themcircles_two[iter].setOptions({fillOpacity:0.65, strokeOpacity:0.5});
      }
      document.getElementById("heatmap_map_two").innerHTML = "Show heatmap";
  }
  else{
    heatmap_two.setMap(google_map_two);
    for(var iter = 0; iter<list.length; iter++){
        themcircles_two[iter].setOptions({fillOpacity:0, strokeOpacity:0});
    }
    document.getElementById("heatmap_map_two").innerHTML = "Hide heatmap";

  }
}



isDis = false;

function distribution_two(){
    if(isDis){
    document.getElementById("distribution_map_two").innerHTML = "Show Distribution";
  }
  else{
    document.getElementById("distribution_map_two").innerHTML = "Unhide Marker";
  }
    for(x =0; x < markers_two.length; x++){
            markers_two[x].setVisible(isDis);
       }
    isDis = !isDis;
}

initialize_two();  //Initialize map function
heat_two();
