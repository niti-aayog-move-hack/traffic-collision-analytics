list = []
themcircles_three = []


/*Temprorary fix to reload the whole thing on sentiment, need to create a fucntion that changes teh color of circles on click, whitout calling the API again*/

function initialize_three(sentiment) {
        
        url = "/demo/road-speed";
    

    $.post(url, {data : {}},function(list, status){ 
        console.log(list);           
        

        var map_options = {
            center: new google.maps.LatLng("12.9408", "77.7609"),
            zoom: 12.5,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        google_map_three = new google.maps.Map(document.getElementById("map_canvas_three"), map_options);

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

                thecolor = "#144149";

            var circleOptions = {
                strokeColor: "#000000",
                strokeOpacity: 0.5,
                strokeWeight: 0.5,
                fillColor: thecolor,
                fillOpacity: 0.65,
                map: google_map_three,
                center: new google.maps.LatLng(parseFloat(list[i].lat), parseFloat(list[i].lng)),
                radius: list[i].speed * 4
            };

                themcircles_three.push(new google.maps.Circle(circleOptions));
                themcircles_three[i].setMap(google_map_three);
        }
        console.log(themcircles_three);

        heatmap_three = new google.maps.visualization.HeatmapLayer({
            data: htmp,
            maxIntensity:5,
            opacity:0.7,
            radius:20,
            gradient: ['#ffffb2','#fd8d3c','#fd8d3c','#f03b20','#bd0026']
        });

        var z =0;
   //$()
        var i = 0;
        markers_three = [];
        for ( item in t ) {
            var marker = new
                google.maps.Marker({
                map:       google_map_three,
                animation: google.maps.Animation.DROP,
                title:     t[i],
                position:  new google.maps.LatLng(x[i],y[i]),
                html:      h[i]
            });

            markers_three.push(marker); // Add the current marker to the array for later processing

            google.maps.event.addListener(marker, 'click', function() {
                info_window.setContent(this.html);
                info_window.open(google_map_three, this);
            });
            i++;
        }
    });
}

var trafficLayer_three = new google.maps.TrafficLayer();

function dispTraffic_three(){
  if(trafficLayer_three.getMap()){
      trafficLayer_three.setMap(null);
  }
  else{
    trafficLayer_three.setMap(google_map_three);
  }
}



function heat_three(){

  if(heatmap_three.getMap()){
      heatmap_three.setMap(null);
      console.log(themcircles_three);
      for(var iter = 0; iter<list.length; iter++){
        themcircles_three[iter].setOptions({fillOpacity:0.65, strokeOpacity:0.5});
      }
      document.getElementById("heatmap_map_three").innerHTML = "Show heatmap";
  }
  else{
    heatmap_three.setMap(google_map_three);
    for(var iter = 0; iter<list.length; iter++){
        themcircles_three[iter].setOptions({fillOpacity:0, strokeOpacity:0});
    }
    document.getElementById("heatmap_map_three").innerHTML = "Hide heatmap";

  }
}



isDis = false;

function distribution_three(){
    if(isDis){
    document.getElementById("distribution_map_three").innerHTML = "Show Distribution";
  }
  else{
    document.getElementById("distribution_map_three").innerHTML = "Unhide Marker";
  }
    for(x =0; x < markers_three.length; x++){
            markers_three[x].setVisible(isDis);
       }
    isDis = !isDis;
}

initialize_three();  //Initialize map function
heat_three();
