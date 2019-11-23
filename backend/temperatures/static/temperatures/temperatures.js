function create_chart(ctx) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperatures',
                borderColor: 'rgb(255,11,0)',
                data: [],
                fill: false,
            }]
        },

        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 40
                    }
                }],
                xAxes: [{
                    type: "time",
                    distribution: "series",
                    bounds: "data",
                }]
            },
            responsive: true,
        }

    });
}

function addData(ch, item) {
    ch.data.datasets.forEach((dataset) => {
        dataset.data.push(item);
    });
    ch.update();
}


window.onload = () => {
    const ctx = document.getElementById('myChart').getContext('2d');
    const chart = create_chart(ctx);

    $.ajax({
        url: '/temperatures/temperatures',
        success: function (data) {
            let temperatures = data.map(x => {
                return {
                    x: new Date(x["datetime"]),
                    y: x["temperature"]
                }
            });

            for (i = 0; i < temperatures.length; i++) {
                addData(chart, temperatures[i]);
            }
        }
    });
};
