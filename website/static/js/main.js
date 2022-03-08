

class Graph {
    constructor(title){
        this.title = title


        this.backgroundColour = 'rgba(255,0,0,1)'
        this.color = 'rgba(255,0,0,1)'
        this.borderColour = 'rgba(255,0,0,0.2)'
        this.ctx = document.getElementById('myChart').getContext('2d')
        this.data = [25,23, 20,19]
        this.dataBeingUsed = this.data
        this.xlabels = this.createXlabels()

        console.log(this.xlabels)


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
                    backgroundColour: this.backgroundColour,
                    colour: this.colour,
                    borderColour: this.borderColour

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
    jsondata.forEach(function(thisData) {
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


window.addEventListener('load', function(){

    let lightGraph = new Graph("Light");


    var getDatabutton = document.getElementById("getDataButton");
    getDataButton.addEventListener("click", () => {
        // fetch("/data")
        fetch("http://127.0.0.1:5000/data")
            .then(response => response.json())
            .then(storeData)
            .catch((error) =>  console.log(error));
    });

    // var createTableButton = document.getElementById("makeTable");
    // createTableButton.addEventListener("click", function(){
    //
    //     createTable();
    // });




}


)
