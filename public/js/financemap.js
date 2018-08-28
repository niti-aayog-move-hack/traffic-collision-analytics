list = []
themcircles = []



function initialize() {
        
       total_amount = 0;

    

    $.get('/demo/expenditure',function(data, status){       
       list = data;

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


       /* 
       list = [
        {   constituency: "Delhi",
                lat: "28.7041",
                lng: "77.1025",
            
            expenditure: 4330000,
            name: "Dr Vishnuvardan"

        },

        {   constituency: "Mumbai",
                lat: "19.0760",
                lng: "72.8777",
            
            expenditure: 3300000,
            name: "Uday Thackeray"
        },

        {   constituency: "Bangalore South",
                lat: "31.1471",
                lng: "75.3412",
            
            expenditure: 20000000,
            name: "Ananth Kumar"
        }
       
        ]*/



        for(i =0; i<list.length; i++){
            htmp.push({location: new google.maps.LatLng(list[i].lat, list[i].lng), weight: list[i].expenditure/4000000});
            t.push(list[i].constituency);
            x.push(parseFloat(list[i].lat));
            y.push(parseFloat(list[i].lng));
            h.push('<p><strong><span style = "font-size:15px">'+ list[i].constituency + " : " + list[i].candidate +  "</span><br /> <strong>Expenditure:</strong>"+ list[i].expenditure);

            if(list[i].expenditure < 1500000){
                thecolor = "#31a354";
            }
            else if(list[i].expenditure < 3000000){
                thecolor = "#8fccc6";
            }
            else if(list[i].expenditure < 6000000){
                thecolor = "#24504d";
            }
            else{
                thecolor = "#8d31a3";
            }

        var circleOptions = {
            strokeColor: "#000000",
            strokeOpacity: 0.5,
            strokeWeight: 0.5,
            fillColor: thecolor,
            fillOpacity: 0.65,
            map: google_map,
            center: new google.maps.LatLng(parseFloat(list[i].lat), parseFloat(list[i].lng)),
            radius: 35000
        };

            themcircles.push(new google.maps.Circle(circleOptions));
            themcircles[i].setMap(google_map);
        }

        heatmap = new google.maps.visualization.HeatmapLayer({
            data: htmp,
            maxIntensity:5,
            opacity:0.7,
            radius:10,
            gradient: ['#8fccc6','#ffffb2','#fd8d3c','#f03b20','#bd0026']
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
for(iter =0; iter < list.length; iter++){
    total_amount += list[iter].expenditure;
    console.log(list[iter].expenditure)
}

console.log(total_amount);
}

isCirclefilter = false;


function heat(){
  isCirclefilter = false;

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


function circlemarkerfilter(low, high){
    document.getElementById("showall_map").style.display = "Block";
    for(var iter = 0; iter<list.length; iter++){
        if(list[iter].expenditure < (100000 * low) || list[iter].expenditure > ( 100000 * high)) {
            themcircles[iter].setOptions({fillOpacity:0, strokeOpacity:0});
            markers[iter].setVisible(false);
        }
        else{
            themcircles[iter].setOptions({fillOpacity:0.65, strokeOpacity:0.5});
            markers[iter].setVisible(false);
        }
    }
    if(high){
        isCirclefilter = true;
    }
    else{
        isCirclefilter = false;
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
  if(!isCirclefilter){
    for(x =0; x < markers.length; x++){
            markers[x].setVisible(isDis);
       }
    isDis = !isDis;
  }
}


