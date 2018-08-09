const defaultOptions = {}
function forceGraphD3Wrapper(classElement, data, options = defaultOptions) {
  options = {
    ...options,
    svg : {
      width: '100%',
      height: '100%',
    }
  }
  const svgOptions = options.svg
  let svg = d3.select(`${classElement}`).append('svg')
  svg.attr('height', svgOptions.height)
  svg.attr('width', svgOptions.width)
  svg.attr('id', 'force-graph-d3-wrapper-svg')
  if(data && data.results){
    console.log(data)
    data = parseNeo4jD3toD3data(data, options)
  }
  console.log(data)
  drawGraph(data, options)
  return this
}

const drawGraph = (data, options) => {
  const color = d3.scaleOrdinal(d3.schemeCategory20)
  const svg = d3.select("#force-graph-d3-wrapper-svg")
  const svgParent = document.querySelector('#force-graph-d3-wrapper-svg').parentElement

  const width = svgParent.offsetWidth,
    height = svgParent.offsetHeight

  

  var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2))

    var link = svg.append("g")
      .attr("class", "relationships")
      .selectAll("line")
        .data(data.relationships)
        .enter().append("line")
          .attr("stroke-width", function(d) { return 1 })

    var node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("circle")
        .data(data.nodes)
        .enter().append("circle")
          .attr("r", (d) => d.r ? d.r : 25)
          .on('click', d => {
            if (typeof options.onNodeClick === 'function') {
              options.onNodeClick(d);
            }
          })
          .on('dblclick', function(d) {

            if (typeof options.onNodeDoubleClick === 'function') {
                options.onNodeDoubleClick(d);
            }
          })
          .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))

    node.append("title")
      .text(function(d) { return d.id })

    simulation
      .nodes(data.nodes)
      .on("tick", ticked)
      .force('collide', d3.forceCollide().radius(function(d) {
        return d.r * 2;
      }).iterations(2))

    simulation.force("link")
      .links(data.relationships)

    function ticked() {
      link
        .attr("x1", function(d) { return d.source.x })
        .attr("y1", function(d) { return d.source.y })
        .attr("x2", function(d) { return d.target.x })
        .attr("y2", function(d) { return d.target.y })

      node
        .attr("cx", function(d) { return d.x })
        .attr("cy", function(d) { return d.y })
    }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart()
    d.fx = d.x
    d.fy = d.y
  }

  function dragged(d) {
    d.fx = d3.event.x
    d.fy = d3.event.y
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0)
    d.fx = null
    d.fy = null
  }
}

const getRadius = (node, options) => {
  const specificNodeRadius = options.specificNodeRadius
  for (let property in specificNodeRadius) {
    if (specificNodeRadius.hasOwnProperty(property)) {
        if (node.labels.includes(property)){
          return specificNodeRadius[property]
        }
    }
  }
  return options.generalNodeRadius
}

const parseNeo4jD3toD3data = (data, options) => {
  let parsedData = {
    nodes: [],
    relationships: []
  };
  data.results.forEach( result => {
    result.data.forEach( data => {
        data.graph.nodes.forEach( node => {
            if (!contains(parsedData.nodes, node.id)) {
              node.r = getRadius(node, options)
              parsedData.nodes.push(node)
            }
        });

        data.graph.relationships.forEach( relationship => {
            relationship.source = relationship.startNode
            relationship.target = relationship.endNode
            parsedData.relationships.push(relationship)
        });

        data.graph.relationships.sort((a, b) => {
            if (a.source > b.source) {
                return 1
            } else if (a.source < b.source) {
                return -1
            } else {
                if (a.target > b.target) {
                    return 1
                }

                if (a.target < b.target) {
                    return -1
                } else {
                    return 0
                }
            }
        })

        for (let i = 0; i < data.graph.relationships.length; i++) {
            if (i !== 0 && data.graph.relationships[i].source === data.graph.relationships[i-1].source && data.graph.relationships[i].target === data.graph.relationships[i-1].target) {
                data.graph.relationships[i].linknum = data.graph.relationships[i - 1].linknum + 1
            } else {
                data.graph.relationships[i].linknum = 1;
            }
        }
    });
  });

  return parsedData
}

const contains = (array, id) => {
  var filter = array.filter(function(elem) {
      return elem.id === id;
  });

  return filter.length > 0;
}