function create_chart(ctx) {
    const chart = new Chart(ctx, {
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

    return chart;
}

function addData(ch, label, data) {
    ch.data.labels.push(label);
    ch.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    ch.update();
}


window.onload = () => {
    const ctx = document.getElementById('myChart').getContext('2d');
    const chart = create_chart(ctx);

    $.ajax({
        url: '/temperatures/temperatures',
        success: function (data) {
            let temperatures = data.map(x => x["temperature"]);
            let labels = data.map(x => new Date(x["datetime"]));

            for (i = 0; i < temperatures.length; i++) {
                addData(chart, labels[i], temperatures[i]);
            }
        }
    });
};
