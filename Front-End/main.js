let initialData = [28,29,31];
var x = 4;
var chart;
var running = false;
var interval;

function createChart(intialData,ctx) {
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Day 1', 'Day2', 'Day 3'],
        datasets: [{
            label: 'Temperature',
            data: initialData,
            backgroundColor: 'rgba(255,0,0,1)',
            color: 'rgba(255,0,0,1)',
            borderColor: 'rgba(255,0,0,0.2)'

        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
                }
            },
        responsive: false,
        interaction: {
            intersection: false,
        }
        }
    });
    return myChart;
}

function updateChart(data) {
    newData = Math.floor((Math.random() +2)* 10);

    chart.data.labels.push("Day " + x);
    x = ++x;
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(newData);
    });
    chart.update();

}


window.addEventListener('load', function(){
    var ctx = document.getElementById('myChart').getContext('2d');
    chart = createChart(initialData,ctx);

    var addDataButton = document.getElementById("oneData");
    addDataButton.addEventListener("click", function(){updateChart("data goes here")})

    var contDataButton = document.getElementById("contData");
    contDataButton.addEventListener('click', function(){
        if (running == false) {
            running = true;
            interval = setInterval(function(){
                updateChart("data goes here")
            },100)
        }

    var stopDataButton = document.getElementById('stop');
    stopDataButton.addEventListener("click", function(){
        clearInterval(interval);
        running = false;
    });

    })

})
