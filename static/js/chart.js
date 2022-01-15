var updateChartSeries;
var addPattern;
$(document).ready(function () {


        var charts = initChart({})
        var chart = charts[0]
        var chartBar = charts[1]
        var numberOfRows = $("#number-of-candles").val();
        var symbol = "";
        var timeFrame = "1m"

        addPattern = function () {
            let pattern = $("#chart-pattern").find(":selected").val()
            $.post("/add_pattern", {
                symbol: symbol,
                pattern: pattern
            }, function (data) {
                df = JSON.parse(data.symbol.json_df);
                pattern_json = getPattern(df, JSON.parse(data.symbol.json_df)[pattern]);
                console.log(pattern_json);
                chart.updateOptions(pattern_json);
            });
        }

        updateChartSeries = function (_symbol) {
            symbol = _symbol
            numberOfRows = $("#number-of-candles").val()
            timeFrame = $("#chart-time-frame").val()
            $.post("/get_symbol", {
                symbol: symbol,
                time_frame: timeFrame
            }, function (data) {
                df = JSON.parse(data)
                chart.updateSeries([{data: dfToSeries(df)}])
                chartBar.updateOptions(updateBarOptions(df))
            });
            return false;
        }

        $("#chart-auto-update").click(function () {
            setInterval(updateChartSeries, 5000);
        });

        function dfToSeries(df) {
            var value = Object.entries(df)
            var dfSeries = [];
            for (var i = 0; i <= numberOfRows; i++) {

                var last_index = Object.keys(value[0][1]).length - i
                dfSeries.push({
                    x: new Date(value[0][1][last_index]),
                    y: [value[1][1][last_index], value[2][1][last_index], value[3][1][last_index], value[4][1][last_index]]
                })
            }
            return dfSeries;
        }

        function getPattern(df, pattern_json) {
            var value = Object.entries(df)

            var patternData = [];
            for (var i = 0; i <= numberOfRows; i++) {

                var last_index = Object.keys(value[0][1]).length - i;
                if (pattern_json[last_index] !== 0){
                    patternData.push(

                    {
                        // in a datetime series, the x value should be a timestamp, just like it is generated below
                        x: new Date(value[0][1][last_index]).getTime(),
                        strokeDashArray: 0,
                        borderColor: "#775DD0",
                        label: {
                            borderColor: "#775DD0",
                            style: {
                                color: "#fff",
                                background: "#775DD0"
                            },
                            text: ">"
                        }
                    },
                    )}

            }
            let candleData = dfToSeries(df);
            return {
                annotations: {
                    xaxis: patternData
                },
                series: [
                    {
                        data: candleData
                    }
                ]
            }
        }

        function updateBarOptions(df) {
            var minY = 100000000000000
            var value = Object.entries(df)
            var dfSeries = [];
            for (var i = 0; i <= numberOfRows; i++) {

                var last_index = Object.keys(value[0][1]).length - i
                var yValue = value[1][1][last_index];
                dfSeries.push({
                    x: new Date(value[0][1][last_index]),
                    y: yValue
                })
                if (yValue < minY) minY = yValue;
            }
            var options = {
                series: [{
                    name: 'volume',
                    data: dfSeries
                }],
                chart: {
                    height: 160,
                    type: 'bar',
                    brush: {
                        enabled: true,
                        target: 'candles'
                    },
                    selection: {
                        enabled: false,
                    },
                },
                dataLabels: {
                    enabled: false
                },

                stroke: {
                    width: 1
                },
                xaxis: {
                    type: 'datetime',
                    axisBorder: {
                        offsetX: 13
                    }
                },
                yaxis: {
                    labels: {
                        show: true
                    },
                    min: minY

                }

            };
            return options;
        }

        function initChart(df) {
            var dfSeries = dfToSeries(df);
            var options = {
                series: [
                    {
                        name: 'candle',
                        type: 'candlestick',
                        data: dfSeries
                    }
                ],

                chart: {
                    type: 'candlestick',
                    height: 500,
                    id: 'candles',
                    toolbar: {
                        autoSelected: 'pan',
                        show: false
                    },
                    zoom: {
                        enabled: true
                    },
                },
                stroke: {
                    width: 1
                },
                xaxis: {
                    type: 'datetime'
                },
            };

            chart = new ApexCharts(document.querySelector("#chart"), options);

            chart.render();

            var optionsBar = updateBarOptions(df)
            chartBar = new ApexCharts(document.querySelector("#chart-bar"), optionsBar);
            chartBar.render();

            return [chart, chartBar];

        }

    }
)

