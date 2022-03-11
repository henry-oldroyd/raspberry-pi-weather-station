var globalData; // global variable

window.addEventListener('load', function(){
    let lightGraph = new Graph('temp', 'graph--temp', [25,35,23,45, 32,86,92])
    let pressureGraph = new Graph('pressure', 'graph--pressure', [30,28,53,20,10,15,14])
    let humidityGraph = new Graph('humidity', 'graph--humidity', [1,22,3,4,7,8,0])
    let precipitationGraph = new Graph('precipitation', 'graph--precip', [5,2,1,0.1,10,2,3])
    let windSpeedGraph = new Graph('wind speed', 'graph--wind-speed', [1,2,1,2,4,8,10])

    let bigGraph = new Graph('Temp', 'graph--graph-big', [1,2,3,4,5,6,6,7,8])
})

class Graph {
    constructor(title, id, data){
        this.title = title
        this.backgroundColour = 'rgba(255,0,0,1)'
        this.colour = 'rgba(255,0,0,1)'
        this.borderColour = 'rgba(255,0,0,0.2)'
        this.ctx = document.getElementById(id).getContext('2d')
        this.data = data

        this.dataBeingUsed = this.data
        this.xlabels = this.createXlabels()
        this.initialiseGraph()

    }

    initialiseGraph(){
        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                labels: this.xlabels,
                datasets: [{
                    label: this.title,
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
