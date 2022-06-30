var globalData; // global variable
window.addEventListener('load', function(){


    var getDatabutton = document.getElementById("getDataButton");
    getDataButton.addEventListener("click", () => {getData()})

    var createGraph = document.getElementById("createGraph");
    createGraph.addEventListener("click", () => {let lightGraph = new Graph('light', filterData('light'))});

    var createTableButton = document.getElementById("makeTableButton");
    createTableButton.addEventListener("click", () => {createTable()});
})

class Graph {
    constructor(title, data){
        this.title = title
        this.backgroundColour = 'rgba(255,0,0,1)'
        this.colour = 'rgba(255,0,0,1)'
        this.borderColour = 'rgba(255,0,0,0.2)'
        this.ctx = document.getElementById('myChart').getContext('2d')
        this.data = data

        this.dataBeingUsed = this.data
        this.xlabels = this.createXlabels()



        this.slider = document.getElementById('slider1')
        this.slider.addEventListener("input", () => {this.editDisplayData()})

        this.addDataButton = document.getElementById("oneData")
        this.addDataButton.addEventListener("click", () => {this.addDataPoint(0)}) // 0 has no signficangce
        // currently adds a random data point

        this.initialiseGraph()

    }

    initialiseGraph(){
        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                labels: this.xlabels,
                datasets: [{
                    label: 'Light',
                    data: this.dataBeingUsed,
                    backgroundColor: this.backgroundColour,
                    color: this.colour,
                    borderColor: this.borderColour

                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                        }
                    },
                responsive: true,
                interaction: {
                    intersection: false,
                }
                }
            }

        );
    }

    createXlabels() {
        let xlabels = [] // local variable
        for (let dayCounter=1; dayCounter <= this.dataBeingUsed.length; dayCounter++){
            xlabels.push("Day " + dayCounter)
        }
        return xlabels
    }

    addDataPoint(dataPoint){
        let newDataPoint = Math.floor((Math.random() +2)* 10);
        this.dataBeingUsed.push(newDataPoint);
        this.len++
        this.xlabels.push("Day " + (this.len))
        this.chart.update()
    }

    removeDataPoint(){
        this.dataBeingUsed.pop()
        this.xlabels.pop()
        this.len--;
        this.chart.update()
    }

    editDisplayData(){
        let val = this.slider.value;
        console.log(val)

        this.dataBeingUsed = this.data.slice(0,val); // edits which part of data set is shwon
        this.xlabels = this.createXlabels()


        this.chart.data.datasets.forEach((dataset) => {
            dataset.data = this.dataBeingUsed;
        })
        this.chart.data.labels = this.xlabels;
        this.chart.update()
    }


}


function createTable() {
    var table = document.getElementById("table");
    let day = 1;
    globalData.forEach(function(thisData) {
        // inserts row to the bottom
        var newRow = table.insertRow(-1);

        // day
        let newCell1 = newRow.insertCell(0);
        let newText1 = document.createTextNode(day);
        day ++;

        // light
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

function getData() { // gets all data
    fetch("http://127.0.0.1:5000/data")
        .then(response => response.json())
        .then(jsondata => {
            globalData = jsondata

        })
        .catch((error) => console.log(error));

}

function filterData(filter) { // returns just light data
    filteredData = []
    for (let i=0; i < globalData.length; i++){
        filteredData.push(globalData[i][filter]) // eg filter = 'light'
    }
    return filteredData
}
