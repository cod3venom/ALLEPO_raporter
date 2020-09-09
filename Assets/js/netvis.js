
function colorGen() 
{
	var colors = ['#FE5685','#C979E6','#FAFF1A','#02C6FE','#FC8A07','#CFCFCF']
	return colors[Math.floor(Math.random()*colors.length)];
}
var margin = {
		top: 0,
		bottom: 0,
		right: 0,
		left: 40
	};
	var width = 960,  height = 500
	var stack = [];
	//Load Color Scale
	var c10 = d3.scale.category10();
	//Create an SVG element and append it to the DOM
	var svgElement = d3.select(".map")
						.append("svg")
						.append("g")
						.attr("transform","translate("+margin.left+","+margin.top+")");	
	//Load External Data
	d3.json("export.json", function(dataset){
		//Extract data from dataset
		var nodes = dataset.nodes,
			links = dataset.links;
			
		//Create Force Layout
		var force = d3.layout.force()
						.size([width, height])
						.nodes(nodes)
						.links(links)
						.gravity(0.1)
						.charge(-50)
						.linkDistance(120);
		
		//Add links to SVG
		var link = svgElement.selectAll(".link")
					.data(links)
					.enter()
					.append("line")
					.attr("stroke-width", function(d){ return .5; })
					.attr("class", "link")
					.attr('class', function(d){return 'link '+d.id;})
		
		
		//Add nodes to SVG
		var node = svgElement.selectAll(".node")
					.data(nodes)
					.enter()
					.append("g")
					.attr("class", "node")
	
					
					.call(force.drag);
		//Add labels to each node
		var label = node.append("text")
						.attr("dx", 20)
						.attr("dy", "1em")
						.attr('class',function(d){return d.id + " label";})
						.text(function(d){ return d.store; });
		//Add circles to each node
		var circle = node.append("circle")
						.attr("r", function(d){ return 2; })
						.attr("class",function(d){stack.push(d.id); return d.id})
						.attr("fill", function(d){ return c10(d.zone*10); });
		
		//This function will be executed for every tick of force layout 
		force.on("tick", function(){
			//Set X and Y of node
			node.attr("cx", function(d){ return d.x; })
				.attr("cy", function(d){ return d.y; });
			//Set X, Y of link
			link.attr("x1", function(d){ return d.source.x; })
			link.attr("y1", function(d){ return d.source.y; })
			link.attr("x2", function(d){ return d.target.x; })
			link.attr("y2", function(d){ return d.target.y; });
			//Shift node a little
		    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
		});
		//Start the force layout calculation
		force.start();
		for(var item of stack)
		{
			var elem = $("."+item);
			var color = colorGen();
			elem.css({
				'fill':'#C70D17',//'#00526A',//color,
				'stroke':color
			});
			$('.link').css({
				'stroke':'#00526A',
				'stroke-width':'1.5'
			});
		}
	});