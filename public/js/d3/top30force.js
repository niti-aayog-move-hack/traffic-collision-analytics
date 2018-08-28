	var color = d3.scale.linear()
		.range(['#ffeda0','#fc9101'])
		.domain(d3.range(m));
		
	var colorsentiments = d3.scale.linear()
		.range(['#fdaf8b','#5ab4ac'])
		.domain(d3.range(3));

   var sideinfo = d3.select("#sideInfoTop30")
        .attr("class", "dashboard-word-options")               
        .style("opacity", 0.5);

	svg = d3.select("#top30").append("svg")
		.attr("width", width)
		.attr("height", height);

	var tooltip = d3.tip()
	  .attr('class', 'd3-tip')
	  .offset([-10, 0])
	  .html(function(d) {
		return "Word:<span style= 'font-weight:400;font-size:1.2em;color:#fc9101'>"+d.cluster+"</span><br />Rel Freq: <span style= 'font-weight:400;font-size:1.2em;color:#fc9101'>"+d.value.toString().substring(0, 5)+"</span>";
	  })

    svg.call(tooltip);

isData = false;
normal_data= [];

function drawTop30(filename, resize, sentiment){


	function putData(data){
		normal_data = data;
	}

	postdata = {}

	if(resize){
			var url = "/demo/top30/word";
			var postdata = {name : pol_name, word: filename};
			$.post(url, {data : JSON.stringify(postdata)},function(data, status){
		    	actual_top30_draw(resize, sentiment, data[0].graph);
			 });
			}
	
	else{
		if(!isData){
			

			var url = "/demo/top30";
			var postdata = {name : pol_name};
 			
 			$.post(url, {data : JSON.stringify(postdata)},function(data, status){
    			normal_data = data[0];
    			isData = !isData;
    			putData(normal_data);

	 			actual_top30_draw(resize, sentiment, normal_data);

	 		});
			
		}

		else{

			actual_top30_draw(resize, sentiment, normal_data);

		}
  }
}

function actual_top30_draw(resize, sentiment, data){
		svg.selectAll("*").remove();
	 	maximum = d3.max(data, function(d) { return +d.frequency; });
	 	minimum = d3.min(data, function(d) { return +d.frequency; });
		maxRadius = mR;

		if(maximum < 571){
			resize = true;
		}
		
		arr = [];
		i=0;


		data.forEach(function(d) {
			arr[i] = d.word;
			i++;
		  });

		populate_words(arr);


		if(resize){
			maxRadius = mR * 571/maximum;
		}


		var nodes = data.map(function (item) {
				var i = item['word'],
					r = +item['frequency'], // note the + to convert to number here.
					c = +item['compound'],
					p = +item['pos'],
					n = +item['neg'],
					nu = +item['neu'],
					d = {
					  cluster: i,
					  compound:c,
					  positive:p,
					  negative:n,
					  neutral:nu,
					  frequency: r,
					  value : r * mR/100,
					  radius: r * maxRadius/100,
					  x: Math.cos(i / m * 2 * Math.PI) * 200 + width / 2 + Math.random(),
					  y: Math.sin(i / m * 2 * Math.PI) * 200 + height / 2 + Math.random()
					};
				if (!clusters[i] || (r > clusters[i].radius)) {
					clusters[i] = d;
				}
				return d;
			});
		
			var force = d3.layout.force()
			.nodes(nodes)
			.size([width, height])
			.gravity(0.1)
			.charge(1)
			.on("tick", tick)
			.start();

		force.start();
		
		var node = svg.selectAll("circle")
			.data(nodes);
			
		  node.enter().append("circle")
		  	.style("fill", function(d) { return color(d.radius/m) })
			.attr("class", "circles");
		if(sentiment){
				node.style("fill", function(d) { return colorsentiments(d.compound * 10);})
		}
		
		  node.call(force.drag);
		

		node.transition()
			.duration(750)
			.delay(function(d, i) { return i * 5; })
			.attrTween("r", function(d) {
			  var i = d3.interpolate(0, d.radius);
			  return function(t) { return d.radius = i(t); };
			});

		if(sentiment){
			node.on('click', function(d,i) {
				sideinfo.transition().duration(200).style("opacity", .9);
				sideinfo.html("<h3>More Infomation:</h3><h4>" + d.cluster+ "</h4>Positive<span style = 'color: #5ab4ac'> : "
				+ d.positive +"</span><br />Negative<span style = 'color: #fc7b40'> : "+d.negative
				+"</span><br />Neutral<span style = 'color: #000'> : "+d.neutral);
			});
		}	
			
		else{
		node.on('click', function(d,i) {
				sideinfo.transition().duration(300).style("opacity", .9);
				sideinfo.html("<h3>More Infomation:</h3><h4>" + d.cluster+ "</h4>Mentions: <span style = 'color: #fc9101'>" + 
				d.frequency + "</span>");
			});
		}

		
		node.on('mouseover',tooltip.show)
			  .on('mouseout', tooltip.hide);
		
		var label = svg.selectAll(".mytext")
							.data(nodes);
					
		label.enter()
				.append("text")
				.text(function (d) { return d.cluster.substring(0, d.radius / 3); })
				.style("text-anchor", "middle")
				.style("fill", "#333")
				.style("font-family", "Arial")
				.style("font-size", "0.75em");


		 node
	    .exit().remove();


	function tick(e) {
	  node
	      .each(cluster(10 * e.alpha * e.alpha))
	      .each(collide(.5))
	      .attr("cx", function(d) { return d.x; })
	      .attr("cy", function(d) { return d.y; });
	  label.attr("x", function(d) { return d.x; })
			  .attr("y", function(d) { return d.y; });
	}

	// Move d to be adjacent to the cluster node.
	function cluster(alpha) {
	  return function(d) {
	    var cluster = clusters[d.cluster];
	    if (cluster === d) return;
	    var x = d.x - cluster.x,
	        y = d.y - cluster.y,
	        l = Math.sqrt(x * x + y * y),
	        r = d.radius + cluster.radius;
	    if (l != r) {
	      l = (l - r) / l * alpha;
	      d.x -= x *= l;
	      d.y -= y *= l;
	      cluster.x += x;
	      cluster.y += y;
	    }
	  };
	}

	// Resolves collisions between d and all other circles.
	function collide(alpha) {
	  var quadtree = d3.geom.quadtree(nodes);
	  return function(d) {
	    var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
	        nx1 = d.x - r,
	        nx2 = d.x + r,
	        ny1 = d.y - r,
	        ny2 = d.y + r;
	    quadtree.visit(function(quad, x1, y1, x2, y2) {
	      if (quad.point && (quad.point !== d)) {
	        var x = d.x - quad.point.x,
	            y = d.y - quad.point.y,
	            l = Math.sqrt(x * x + y * y),
	            r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
	        if (l < r) {
	          l = (l - r) / l * alpha;
	          d.x -= x *= l;
	          d.y -= y *= l;
	          quad.point.x += x;
	          quad.point.y += y;
	        }
	      }
	      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
	    });
	  };
	}
}	

function getAvg(){
	return minimum;
}


drawTop30("top30");
