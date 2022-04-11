var globalData; // global variable

window.addEventListener('load', function(){
    // smaller graphs on page 2
    let lightGraph = new Graph('temp', 'graph-temp', [25,35,23,45, 32,86,92])
    let pressureGraph = new Graph('pressure', 'graph-pressure', [30,28,53,20,10,15,14])
    let humidityGraph = new Graph('humidity', 'graph-humidity', [1,22,3,4,7,8,0])
    let precipitationGraph = new Graph('precipitation', 'graph-precip', [5,2,1,0.1,10,2,3])
    let windSpeedGraph = new Graph('wind speed', 'graph-wind-speed', [1,2,1,2,4,8,10])

    // main graph on page 3
    let bigGraph = new Graph('Temp', 'graph-graph-big', [1,2,3,4,5,6,6,7,8])

    // buttons on page 3
    let tempButton = document.getElementById("temp-button-big-graph");
    let pressureButton = document.getElementById("pressure-button-big-graph");
    let lightButton = document.getElementById("light-button-big-graph");
    let windButton = document.getElementById("wind-button-big-graph");
    let humidButton = document.getElementById("humid-button-big-graph");

    let buttons = [tempButton, pressureButton, lightButton, windButton, humidButton]
    page3Buttons(buttons); // adds functionality to each button

    //button that spins compass
    let compassButton = document.getElementById("img-compass-arrow");
    //function for button to spin the compass
    compassSpin(compassButton);
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


// Update the background image to the current weather
var r = document.querySelector(':root');
r.style.setProperty('--bgImg', "url('images/cold.png')");
//To-do: Set image based off current weather with if statements
//DP: Will do above once GA has finished read-outs in section 1
//GA: I didn't realise this was my job... doesn't this require hooking up with the backend,
//    at least a pseduo version, that requires Henry?

function compassSpin(compassButton){
    let timesClicked = 0;
    compassButton.addEventListener("click", (timesClicked) => {
        timesClicked = timesClicked + 1;
        let rotation = (-45 + (timesClicked*45));
        rotation = 0;
        compassButton.style.transform = "translate(-49.5%, -50%) rotate(${rotation}deg"
        console.log('Hi');
    })
}

function page3Buttons(buttons){
    buttons.forEach((button) => {

        button.addEventListener("click", () => {
            console.log(button);

            // checks how many buttons are hidden
            let buttonsHidden = 0;
            buttons.forEach((button) => {
                if (button.classList.contains("hidden-button")) {
                    buttonsHidden++;
                    console.log(buttonsHidden)
                }
            })

            //if multiple buttons are hidden, show them all on click.
            if (buttonsHidden > 1) {
                console.log("showing all")
                buttons.forEach((button) => {
                    if (button.classList.contains("hidden-button")) {
                        button.classList.remove("hidden-button")
                    }
                    if (button.classList.contains("selected-button")){
                        button.classList.remove("selected-button");
                    }

                })

            } else {  // if no buttons are hidden
                // shows the right one
                console.log("showing one")
                buttons.forEach((button) => {
                    button.classList.add("hidden-button");
                });

                button.classList.add("selected-button");
                button.classList.remove("hidden-button");


            }
        });
    });
}

function buttonClicked(button) { // page 3 buttons
    // button.classList.toggle("hidden-button")
    console.log('hi')
}


// function getData() { // gets all data
//     fetch("http://127.0.0.1:5000/data")
//         .then(response => response.json())
//         .then(jsondata => {
//             globalData = jsondata
//         })
//         .catch((error) => console.log(error));
//
// }
//
// function filterData(filter) { // returns just light data
//     filteredData = []
//     for (let i=0; i < globalData.length; i++){
//         filteredData.push(globalData[i][filter]) // eg filter = 'light'
//     }
//     return filteredData
// }
