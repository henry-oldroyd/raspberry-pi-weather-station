let initialData = [28,29,31];
var lights = []
var x = 4;
var chart;
var running = false;
var interval;
var jsondata;
var day = 2;

function createChart(intialData,ctx) {
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Light',
            data: lights,
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

function outputData(data) {
    console.log("Data addaed!")
    console.log(jsondata)
    jsondata = data;
    // adds the data value
    let i = 0;
    for (let i=0; i < data.length; i++) {
        lights.push(data[i]['light'])
        // adds the lable
        chart.data.labels.push("Day " + (i+1));
    }


    console.log(lights)
    chart.update();
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


function createTable() {

    var table = document.getElementById("table");
    jsondata.forEach(function(thisData) {
        // inserts row to the bottom
        var newRow = table.insertRow(-1);

        // day
        let newCell1 = newRow.insertCell(0);
        let newText1 = document.createTextNode(day);
        day ++;

        // temp
        let newCell2 = newRow.insertCell(1);
        let newText2 = document.createTextNode(thisData['light']);


        // rain
        let newCell3 = newRow.insertCell(2);
        let newText3 = document.createTextNode(thisData['rain']);

        newCell1.appendChild(newText1);
        newCell2.appendChild(newText2);
        newCell3.appendChild(newText3);



    });
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
    });

    var stopDataButton = document.getElementById('stop');
    stopDataButton.addEventListener("click", function(){
        clearInterval(interval);
        running = false;
    });

    var getDatabutton = document.getElementById("getDataButton");
    getDataButton.addEventListener("click", () => {
        // fetch("/data")
        fetch("http://127.0.0.1:5000/data")
            .then(response => response.json())
            .then(outputData)
            .catch((error) =>  console.log(error));
    });

    var createTableButton = document.getElementById("makeTable");
    createTableButton.addEventListener("click", function(){

        createTable();
    });

    }


)
