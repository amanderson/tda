// Based on http://bl.ocks.org/mbostock/4062045

// The following code is intended as a template for generating
// a force-directed graph in Jupyter notebooks. This script uses
// cola.js to equilibrate the graph.

require.config({
    paths: {
        "d3": "http://d3js.org/d3.v4.min.js",
        "cola": "http://marvl.infotech.monash.edu/webcola/cola.v3.min.js"
    },
    shim: {
        "cola": {
            "exports": "cola",
            "deps": ["d3"]
        }
    }
});

require(["d3","cola"], function(d3) {

    var width = 960,
        height = 800;

// use D3 force implementation
//var force = d3.layout.force()
//    .charge(-100)
//    .linkDistance(10)
//    .size([width, height]);

    // use Cola force implementation
    var force = cola.d3adaptor()
        .linkDistance(10)
        .size([width, height])
        .avoidOverlaps(true);

    d3.select("#maindiv${divnum}").selectAll("svg").remove();
    var svg = d3.select("#maindiv${divnum}").append("svg")
        .attr("width", width)
        .attr("height", height);

    var graph = ${data};

    force
        .nodes(graph['vertices'])
        .links(graph['edges'])
        .start(20,20,20);

    var nodeattr = d3.set();
    for(n in graph['vertices']) {
        nodeattr.add(graph['vertices'][n]['attribute']);
    }

    var color = d3.scale.linear()
        .range(['blue', 'red'])
        .domain([0, d3.max(nodeattr.values())]);

    var link = svg.selectAll(".link")
        .data(graph['edges'])
        .enter().append("line")
        .attr("class", "link");

    var node = svg.selectAll(".node")
        .data(graph.vertices)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", function(d) { return Math.min(10,(3+Math.sqrt(d.members.length))); })
        .style("fill", function(d) { return color(d.attribute); })
        .text(function(d) { return d.index; })
        .call(force.drag);

    node.append("title")
        .text(function(d) { return d.name; });

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    });
});
