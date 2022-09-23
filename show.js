var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

myChart.showLoading();
$.getJSON('data.json', function (data) {
    // concole.log(graph.categories)
    myChart.hideLoading();
    option = {
        title: {
            text: 'ECharts 关系图'
        },
        // 提示框的配置
        tooltip: {
            formatter: function (x) {
                return x.data.des;
            }
        },
        // 工具箱
        toolbox: {
            // 显示工具箱
            show: true,
            feature: {
                mark: {
                    show: true
                },
                // 还原
                restore: {
                    show: true
                },
                // 保存为图片
                saveAsImage: {
                    show: true
                }
            }
        },
        legend: [{
            // selectedMode: 'single',
            data: data.categories && data.categories.map(function (a) {
                return a.name;
            })
        }],
        series: [{
            type: 'graph', // 类型:关系图
            layout: 'force', //图的布局，类型为力导图
            symbolSize: 20, // 调整节点的大小
            roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            draggable: false,
            edgeSymbol: ['circle', 'arrow'],
                edgeSymbolSize: [1, 2],
                edgeLabel: {
                    show: true,
                    position: "middle",
                    fontSize: 15,
                    formatter: (params) => {
                        return params.data.name;
                        },
                    color:'#000'
                },
            focusNodeAdjacency: true,
            legendHoverLink: true,
            lineStyle: {
             color: "source",
             opacity: 0.2,
            curveness: 0.3,
            },
            force: {
                repulsion: 1500,
                edgeLength: [10, 50],
                layoutAnimation: false
            },

            emphasis: {
              itemStyle: {
                shadowColor: "rgba(0, 0, 0, 0.4)",
                shadowBlur: 15,
              },
              lineStyle: {
                width: 3,
              },
              label: {
                textBorderColor: "rgba(255, 255, 255, 0.8)",
                textBorderWidth: 2,
              },
            },
            label: {
                normal: {
                    show: true,
                    textStyle: {}
                }
            },
            data: data.nodes,
            links: data.links,
            categories: data.categories,

            }
        ]
    };
    myChart.setOption(option);
    myChart.on('click', function(params) {
        console.log(params.data.weblink);
        window.open(params.data.weblink);
});
});

option && myChart.setOption(option);