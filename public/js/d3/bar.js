ww = document.getElementById('main-content').clientWidth - 33;
hh = Math.max( 150, Math.min( 550, document.body.clientHeight));

if(ww<300){
    ww +=23;
}

var margin = {top: 40, right: 20, bottom: 30, left: 30},
    width = Math.min(1050, ww - margin.left - margin.right),
    height = hh - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .02)
    .domain(0,100);

var y = d3.scale.linear()
    .range([height, 0]);

xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10)
  .tickFormat(d3.format("s"));

function updateChartBar( upd ){

var label = upd;

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "Number of occurances: <strong><span style='color:#E34B48'>" + d.number + "</span></strong><br />" + label + ":<strong> <span style='color:#E34B48'>" + d.class+ "</span></strong>";
  })


var id_of = "#bar_" + upd;
var svg = d3.select(id_of).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom + 20)
    .attr("id", "chr")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);

var xa = svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")");

var ya = svg.append("g")
      .attr("class", "y axis");


// Hover line. 
var hoverLineGroup = svg.append("g")
          .attr("class", "hover-line");

var hoverLine = hoverLineGroup
  .append("line")
    .attr("x1", 10).attr("x2", 10)
    .attr("y1", 0).attr("y2", height);

// Hide hover line by default.
hoverLine.style("opacity", 1e-6);



d3.json("/data/June_"+ upd +"_count.json", function(data){
  
  console.log(data);
  max_y = 0;

  for(i=0; i < data.length; i++){
      var max_y = Math.max(max_y, data[i].number);
  }


  x.domain(data.map(function(d, i) { 
      return d.class 
  }));

  y.domain([0, max_y+5]);
  
  xa.call(xAxis)
          .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "5em")
            .attr("dy", "-.15em")
            .style("font-size", "0.66rem")
            .attr("transform", "rotate(65)");


  ya.call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("number");

  var bars = svg.selectAll(".bar")
    .data(data);

    bars.enter().append("rect")
    .attr("width", x)
    .attr("class", "bar")
    .attr("x",function(d, i) {
       return x(d.class); 
     })
    .attr("width", x.rangeBand())
    .attr("y", height - 2)
    .attr("height", 1);

    bars.attr("fill", "#E34B48");
      

    bars.transition()
      .duration(1000)
      .delay(function (d, i) {
        return i * 100;
      })
      .attr("y", function(d) { return y(d.number); })
      .attr("height", function(d) { return height- y(d.number); });

    bars.on('mouseover', tip.show)
      .on('mouseout', tip.hide);

    bars
    .exit().remove();

  });

  // Add mouseover events.
  d3.select("#bar").on("mouseover", function() { 

    })

  .on("mousemove", function() {
    var x = d3.mouse(this)[0];
    hoverLine.attr("x1", x).attr("x2", x).style("opacity", 2);
    })
  
  .on("mouseout", function() {
    hoverLine.style("opacity", 1e-6);
  });

}

function type(d) {
  d.number = +d.number;
  return d;
}

updateChartBar("wards");
updateChartBar("speed");
// updateChartBar();