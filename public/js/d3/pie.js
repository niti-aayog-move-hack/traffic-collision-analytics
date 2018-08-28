

var pie_margin = {top: 0, right: 20, bottom: 20, left: 20};
	pie_width = 400 - pie_margin.left - pie_margin.right;
	pie_height = pie_width - pie_margin.top - pie_margin.bottom;


function draw_pie( pos , remPrev, recolor, insights){
  data = insights;
  console.log(data);
  if(remPrev){
    d3.select("#" + pos).selectAll("*").remove();
  }


var colorspie = d3.scale.ordinal()
  .range(['#5ab4ac','#fdaf8b']);

  if(recolor){
   colorspie = d3.scale.ordinal()
    .range(['#31a354','transparent']);
  }

var chart = d3.select("#" + pos)
				.append('svg')
			    .attr("width", pie_width + pie_margin.left + pie_margin.right)
			    .attr("height", pie_height + pie_margin.top + pie_margin.bottom)
			   .append("g")
    			.attr("transform", "translate(" + ((pie_width/2)+pie_margin.left) + "," + ((pie_height/2)+pie_margin.top) + ")");


var radius = 125;


var arc = d3.svg.arc()
    .outerRadius(radius)
    .innerRadius(radius - 20);

var pie = d3.layout.pie()
    .sort(null)
    .startAngle(1.1*Math.PI)
    .endAngle(3.1*Math.PI)
    .value(function(d) { return d.value; });


var g = chart.selectAll(".arc")
  .data(pie(data))
.enter().append("g")
  .attr("class", "arc")
  .on("mousemove", function(data, i){
        chart.select(".text-tooltip")
         .attr("fill", colorspie(i))
         .text(data.data.value + "%");

    if(!recolor){
        chart.select(".text")
         .attr("fill", "#293742")
         .text(data.data.name.toString().toUpperCase());
        }
    });

g.append("path")
  .style("fill", function(d, i) { return colorspie(i); })
  .transition().delay(function(d, i) { return i * 500; }).duration(500)
  .attrTween('d', function(d) {
       var i = d3.interpolate(d.startAngle+0.1, d.endAngle);
       return function(t) {
           d.endAngle = i(t);
         return arc(d);
       }
  });
  
   chart.append("text")
          .datum(data)
          .attr("x", 5 )
          .attr("y", 8 + radius/10 )
          .attr("class", "text-tooltip")        
          .style("text-anchor", "middle")
          .attr("font-weight", "bold")
          .style("font-size", radius/2.5+"px"); 
   chart.append("text")
          .datum(data)
          .attr("x", 3 )
          .attr("y",  5- radius/4)
          .attr("class", "text")
          .style("text-anchor", "middle")
          .style("font-size", radius/5.5+"px");
}

draw_pie("sentiment-pie")