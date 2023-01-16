// 实例化 Minimap 插件
const minimap = new G6.Minimap({
  size: [100, 100],
  className: "minimap",
  type: 'delegate'
});

// 实例化 Grid 插件
const grid = new G6.Grid();

const graph = new G6.Graph({
  container: 'mountNode',
  width: 800,
  height: 600,
  defaultNode: {
    labelCfg: {
      style: {
        fill: '#fff'
      }
    }
  },
  defaultEdge: {
    labelCfg: {
      autoRotate: true
    }
  },
  nodeStateStyles: {
    hover: {
      fill: '#cfd8dc'
    },
    click: {
      stroke: '#000',
      lineWidth: 0
    }
  },
  edgeStateStyles: {
    click: {
      stroke: 'steelblue'
    }
  },
  layout: {
    type: 'force',
    linkDistance: 200,
    preventOverlap: true,
    nodeStrength: -30,
    edgeStrength: 0.1
  },
  modes: {
    default: ['drag-node', 'drag-canvas', 'zoom-canvas',
      // 点提示框交互工具的配置
      {
        type: 'tooltip',
        formatText(model) {
          const text = 'label: ' + model.label
            + '<br/> class: ' + model.class;
          return text;
        },
        shouldUpdate: e => {
          return true;
        }
      },
      // 边提示框交互工具的配置
      {
        type: 'edge-tooltip',
        formatText(model) {
          const text = 'source: ' + model.source
            + '<br/> target: ' + model.target
            + '<br/> weight: ' + model.weight;
          return text;
        },
        shouldUpdate: e => {
          return true;
        }
      }
    ]
  },
  plugins: [minimap, grid],    // 将 Minimap 和 Grid 插件的实例配置到图上
  fitCenter: true,
});
//$.getJSON('https://gw.alipayobjects.com/os/basement_prod/6cae02ab-4c29-44b2-b1fd-4005688febcb.json', data => {
const main = async () => {
  // const response = await fetch('https://gw.alipayobjects.com/os/basement_prod/6cae02ab-4c29-44b2-b1fd-4005688febcb.json');
  // const data = await response.json();
  // const data =
  // const response = fetch('./kg_sample.json')
  // const data = (await response).json
  data = document.getElementById('data').value;
  // console.log('TTTHHH');
  // var data = [[${processed_text_re}]];
  // var data = $('#data').val();
  // console.log(data);
  data = eval('(' + data + ')');
  // console.log(data);
  const nodes = data.nodes;
  const edges = data.edges;
  nodes.forEach(node => {
    if (!node.style) {
      node.style = {};
    }
    node.style.lineWidth = 0;
    node.style.stroke = '#666';
    node.style.fill = 'steelblue';
    switch (node.class) {
      case 'c0': {
        node.type = 'circle';
        node.size = 60;
        node.style.fill = '#d4e157';
        break;
      }
      case 'c1': {
        node.type = 'circle';
        node.size = 40;
        node.style.fill = '#8bc34a';
        break;
      }
      case 'c2': {
        node.type = 'circle';
        node.size = 30;
        break;
      }
    }
  });
  edges.forEach(edge => {
    if (!edge.style) {
      edge.style = {};
    }
    edge.style.lineWidth = 1;
    edge.style.opacity = 0.6;
    edge.style.stroke = 'grey';
  });


  graph.data(data);
  graph.render();

  graph.on('node:mouseenter', e => {
    const nodeItem = e.item;
    graph.setItemState(nodeItem, 'hover', true);
  });
  graph.on('node:mouseleave', e => {
    const nodeItem = e.item;
    graph.setItemState(nodeItem, 'hover', false);
  });
  graph.on('node:click', e => {
    const clickNodes = graph.findAllByState('node', 'click');
    clickNodes.forEach(cn => {
      graph.setItemState(cn, 'click', false);
    });
    const nodeItem = e.item;
    graph.setItemState(nodeItem, 'click', true);
  });
  graph.on('edge:click', e => {
    const clickEdges = graph.findAllByState('edge', 'click');
    clickEdges.forEach(ce => {
      graph.setItemState(ce, 'click', false);
    });
    const edgeItem = e.item;
    graph.setItemState(edgeItem, 'click', true);
  });
};
main();

