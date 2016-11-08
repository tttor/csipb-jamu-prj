declare let d3 : any, nv: any;

export const ChartTypes = [
  'forceDirectedGraph'
];

const color = d3.scale.category20()

export const AllOptions = {
  forceDirectedGraph: {
    chart: {
      type: 'forceDirectedGraph',
      height: 500,
      width: (function(){ return nv.utils.windowSize().width })(),
      margin:{top: 20, right: 20, bottom: 20, left: 20},
      color: function(d){
        return color(d.Jenis)
      },
      nodeExtras: function(node) {
        node && node
          .append("text")
          .attr("dx", 8)
          .attr("dy", "1em")
          .text(function(d) { return d.name })
          .style('font-size', '10px');
      }
    }
  }
}

export const AllData = {
  forceDirectedGraph: {
    "nodes":[
      {"name":"Myriel","Jenis":"Tanaman"},
      {"name":"Napoleon","Jenis":"Tanaman"},
      {"name":"Mlle.Baptistine","Jenis":"Tanaman"},
      {"name":"Mme.Magloire","Jenis":"Tanaman"},
      {"name":"CountessdeLo","Jenis":"Tanaman"},
      {"name":"Geborand","Jenis":"Tanaman"},
      {"name":"Champtercier","Jenis":"Tanaman"},
      {"name":"Cravatte","Jenis":"Tanaman"},
      {"name":"Count","Jenis":"Tanaman"},
      {"name":"OldMan","Jenis":"Tanaman"},
      {"name":"Labarre","Jenis":"Compound"},
      {"name":"Valjean","Jenis":"Compound"},
      {"name":"Marguerite","Jenis":"Disease"},
    ],
    "links":[
      {"source":1,"target":0,"value":1},
      {"source":2,"target":0,"value":8},
      {"source":3,"target":0,"value":10},
      {"source":3,"target":2,"value":6},
      {"source":4,"target":0,"value":1}
    ]
  }
}
