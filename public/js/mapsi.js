list = []
themcircles = []


/*Temprorary fix to reload the whole thing on sentiment, need to create a fucntion that changes teh color of circles on click, whitout calling the API again*/

function initialize(sentiment) {
        
        url = "/demo/map";
        postdata = {name : pol_name};
    

    $.post(url, {data : JSON.stringify(postdata)},function(data, status){            
        list = data[0];

        var map_options = {
            center: new google.maps.LatLng("20.5937", "78.9629"),
            zoom: 4,
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
            htmp.push({location: new google.maps.LatLng(list[i].position.lat, list[i].position.lng), weight: list[i].frequency})
            t.push(list[i].name);
            x.push(parseFloat(list[i].position.lat));
            y.push(parseFloat(list[i].position.lng));
            h.push('<p><strong><span style = "font-size:15px">'+ list[i].name + '</strong></span><br/><strong>Top words </strong>' + list[i].words + "<br /> <strong>Sentiment:</strong>"+ list[i].compound);

            if(sentiment){
                thecolor = colorsentiments(list[i].compound * 10); //Colorsentiment defined in top30.js
            }
            else {
                thecolor = "#31a354";
            }

        var circleOptions = {
            strokeColor: "#000000",
            strokeOpacity: 0.5,
            strokeWeight: 0.5,
            fillColor: thecolor,
            fillOpacity: 0.65,
            map: google_map,
            center: new google.maps.LatLng(parseFloat(list[i].position.lat), parseFloat(list[i].position.lng)),
            radius: Math.min(Math.max(2500 * list[i].frequency, 50000), 500000)
        };

            themcircles.push(new google.maps.Circle(circleOptions));
            themcircles[i].setMap(google_map);
        }

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


function sentimap(isSenti){
    if(!isSenti){
        for(var iter = 0; iter<list.length; iter++){
            themcircles[iter].setOptions({fillColor: colorsentiments(list[iter].compound * 10)});
        }
    }
    else{
        for(var iter = 0; iter<list.length; iter++){
            themcircles[iter].setOptions({fillColor: "#31a354"});
        }
    }
    isSenti = !isSenti;
}


function heat(){

  if(heatmap.getMap()){
      heatmap.setMap(null);
      for(var iter = 0; iter<list.length; iter++){
        themcircles[iter].setOptions({fillOpacity:0.65, strokeOpacity:0.5});
      }
      document.getElementById("heatmap_map").innerHTML = "Show Heatmap";
  }
  else{
    heatmap.setMap(google_map);
    for(var iter = 0; iter<list.length; iter++){
        themcircles[iter].setOptions({fillOpacity:0, strokeOpacity:0});
    }
    document.getElementById("heatmap_map").innerHTML = "Hide Heatmap";

  }
}



initialize();  //Initialize map function
isDis = false;

function distribution(){
    if(isDis){
    document.getElementById("distribution_map").innerHTML = "Show Distribution";
  }
  else{
    document.getElementById("distribution_map").innerHTML = "Unhide Marker";
  }
    for(x =0; x < markers.length; x++){
            markers[x].setVisible(isDis);
       }
    isDis = !isDis;
}

