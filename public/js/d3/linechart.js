 line_chart_new_average_flag = false;

 function InitChart() {
      margin = {
                top: 20,
                right: 20,
                bottom: 20,
                left: 50
            };

        width = Math.max(250, Math.min(700, ww - margin.left - margin.right)),
                    heightLine = 500;
        usableWidth = width - margin.right;
        vis = d3.select("#chr")
                            
        max_x = 0, max_y = 0, min = 100;

        updateLineChart();
    }

  function updateLineChart(newaverage){
  $.ajax({url: "/distribution-marks", success: function(result){

        //vis.selectAll("path").remove();
        //vis.selectAll("g").remove();
 
        data = result[0];

    for(i=0; i < data.length; i++){
            max_y = Math.max(max_y, data[i].number);
            max_x = Math.max(max_x, data[i].class);
            min = Math.min(min, data[i].class);
        }
        xScale = d3.scale.linear().range([margin.left, width - margin.right]).domain([max_x, 0]);

        yScale = d3.scale.linear().range([heightLine - margin.top, margin.bottom]).domain([0, max_y]);


        xAxisLine = d3.svg.axis()
        .scale(xScale),

        yAxisLine = d3.svg.axis()
        .scale(yScale)
        .orient("left");

          var lineGen = d3.svg.area()
              .x(function(d) {
                  return xScale(d.class);
              })
              .y(function(d) {
                  return yScale(d.number);
              })
              .interpolate("basis");

          var pth = vis.append('path')
	            .attr('d', lineGen(data))
              .attr('stroke', '#000')
              .attr('stroke-width', 1.5)
              .attr('class', 'area');
                              
          var totalLength = pth.node().getTotalLength();

          pth
            .attr("stroke-dasharray", totalLength + " " + totalLength)
            .attr("stroke-dashoffset", totalLength)
            .transition()
              .duration(1500)
              .ease("linear")
              .attr("stroke-dashoffset", 0);

          //Line chart mouse over 
          var hoverLineGroup = vis.append("g")
                              .attr("class", "hover-line");

          var hoverLine = hoverLineGroup
              .append("line")
                  .attr("stroke", "#000")
                  .attr("x1", 10).attr("x2", 10) 
                  .attr("y1", 0).attr("y2", heightLine); 

          var hoverTT = hoverLineGroup.append('text')
             .attr("class", "hover-tex capo")
             .attr('dy', "0.35em");

          var cle = hoverLineGroup.append("circle")
              .attr("r",3.5)
              .attr("fill", "#E34B48");
          
          var cleX = hoverLineGroup.append("circle")
              .attr("r", 5);
          
          var hoverTT2 = hoverLineGroup.append('text')

             .attr("class", "hover-text capo")
             .attr('dy', "0.35em");

          hoverLineGroup.style("opacity", 1e-6);

          var rectHover = vis.append("rect")
            .data(data)
            .attr("class", "overlay")
            .attr("width", width)
            .attr("opacity", 0)
            .attr("color", "#accccc")
            .attr("height", heightLine);

           
          vis  
          .on("mouseout", hoverMouseOff)
          .on("mousemove", hoverMouseOn);

          var bisectDate = d3.bisector(function(d) { return d.class; }).left;

          function hoverMouseOn() {

              var mouse_x = d3.mouse(this)[0];
              var mouse_y = d3.mouse(this)[1];
              var graph_y = yScale.invert(mouse_y);
              var graph_x = xScale.invert(mouse_x);
              
              var mouseDate = xScale.invert(mouse_x);
              var i = bisectDate(data, mouseDate); // returns the index to the current data item

              var d0 = data[i - 1]
              var d1 = data[i];
              // work out which date value is closest to the mouse
              if(d1 && d0){

                var d = mouseDate - d0[0] > d1[0] - mouseDate ? d1 : d0;
                  hoverTT.text("Marks: " + Math.round(graph_x * 100)/100); 
                  hoverTT.attr('x', mouse_x+20);
                  hoverTT.attr('y', yScale(d.number));


                  hoverTT2.text("Dist. Frequency: " + Math.round(d.number * 100)/100)
                     .attr('x', mouse_x +20)
                     .attr('y', yScale(d.number) + 15);

                  cle
                    .attr("transform", "translate(" + (margin.left) + " ," + yScale(d.number) + ")");
                  cleX
                    .attr("transform", "translate(" + mouse_x + " ," + (heightLine -margin.bottom) + ")");

                  hoverLine.attr("x1", mouse_x).attr("x2", mouse_x)
                  hoverLineGroup.style("opacity", 1);
              }


          }
          
          function hoverMouseOff() {
                  hoverLineGroup.style("opacity", 1e-6);
          };

		}});
}

InitChart();
