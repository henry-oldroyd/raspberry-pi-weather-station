

window.addEventListener('load', function(){
    // create readout boxes
    let tempReadOutBox = new Dataset("Temperature", "°C", "temperature-readout-box");
    let pressureReadOutBox = new Dataset("Pressure", "Pa", "pressure-readout-box");
    let humidityReadOutBox = new Dataset("Humidity", "%", "humidity-readout-box");
    let rainReadOutBox = new Dataset("Rain", "mm", "rain-readout-box");
    let windSpeedReadOutBox = new Dataset("Wind Speed", "mph", "wind-speed-readout-box");

    // smaller graphs on page 2
    let tempGraph = new Graph('temp', 'graph-temp', [25,35,23,45, 32,86,92])
    let pressureGraph = new Graph('pressure', 'graph-pressure', [30,28,53,20,10,15,14])
    let humidityGraph = new Graph('humidity', 'graph-humidity', [1,22,3,4,7,8,0])
    let rainGraph = new Graph('precipitation', 'graph-precip', [5,2,1,0.1,10,2,3])
    let windSpeedGraph = new Graph('wind speed', 'graph-wind-speed', [1,2,1,2,4,8,10])

    // main graph on page 3
    let bigGraph = new Graph('Temp', 'graph-graph-big', [1,2,3,4,5,6,6,7,8], true)

    let dropdown = document.getElementById("dropdown");
    dropdown.addEventListener("input", (dropdown) => {dropdownFunctionality(dropdown);})


    // buttons on page 3
    // let tempButton = document.getElementById("temp-button-big-graph");
    // let pressureButton = document.getElementById("pressure-button-big-graph");
    // let rainButton = document.getElementById("rain-button-big-graph");
    // let windButton = document.getElementById("wind-button-big-graph");
    // let humidButton = document.getElementById("humid-button-big-graph");
    //
    // let buttons = [tempButton, pressureButton, rainButton, windButton, humidButton]
    // page3Buttons(buttons); // adds functionality to each button

    //button that spins compass
    let compassButton = document.getElementById("img-compass-arrow");
    //function for button to spin the compass
    compassSpin(compassButton);
})

class Dataset {
    constructor(title, unit, divName){
        this.title = title;
        this.unit = unit;
        this.divName = divName;
        this.getSpecificData();
        this.editReadOut();
    }

    getSpecificData(param){
        this.data = getFilterData(param); // global function, see at bottom

    }

    editReadOut(){
        this.currentData = this.data[0];
        this.div = document.getElementsByClassName(this.divName);
        this.child = this.div[0].getElementsByTagName("p");
        this.child[0].innerText = this.currentData + this.unit;
    }


}

class Graph {
    constructor(title, id, data, slider=false){
        this.title = title
        this.backgroundColour = 'rgba(255,0,0,1)'
        this.colour = 'rgba(255,0,0,1)'
        this.borderColour = 'rgba(255,0,0,0.2)'
        this.ctx = document.getElementById(id).getContext('2d')
        this.data = data

        this.dataBeingUsed = this.data
        this.xlabels = this.createXlabels()
        this.initialiseGraph()
        if (slider == true) {
            this.sliders = document.getElementsByClassName("slider-big-graph"); // only lets you take as a list
            this.slider = this.sliders[0] // one element array
            this.slider.max = 9;
            this.slider.addEventListener("input", () => {this.editDisplayData()});
        }

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
        console.log(this.slider.value);
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
    // let negative = -5; // so that the arrow can spin back and forth
    let rotation = -45 // upwards
    compassButton.addEventListener("click", () => {
        rotation = rotation + 45;
        compassButton.style.transform = `translate(-49.5%, -50%) rotate(${rotation}deg`
    })

    // let id = setInterval(function() {
    //     compassShake(rotation, compassButton, negative);
    //     negative = 20*(Math.random())
    //     negative = negative * -1
    // },Math.random()*5000);
}

function compassShake(rotation, compassButton, negative){

    if (1==2){
        console.log('test for spinning')
    } else{
        rotation = rotation + negative
        compassButton.style.transform = `translate(-49.5%, -50%) rotate(${rotation}deg`
    }
}

// function page3Buttons(buttons){
//     buttons.forEach((button) => {
//
//         button.addEventListener("click", () => {
//             console.log(button);
//
//             // checks how many buttons are hidden
//             let buttonsHidden = 0;
//             buttons.forEach((button) => {
//                 if (button.classList.contains("hidden-button")) {
//                     buttonsHidden++;
//                     console.log(buttonsHidden)
//                 }
//             })
//
//             //if multiple buttons are hidden, show them all on click.
//             if (buttonsHidden > 1) {
//                 console.log("showing all")
//                 buttons.forEach((button) => {
//                     if (button.classList.contains("hidden-button")) {
//                         button.classList.remove("hidden-button")
//                     }
//                     if (button.classList.contains("selected-button")){
//                         button.classList.remove("selected-button");
//                     }
//
//                 })
//
//             } else {  // if no buttons are hidden
//                 // shows the right one
//                 console.log("showing one")
//                 buttons.forEach((button) => {
//                     button.classList.add("hidden-button");
//                 });
//
//                 button.classList.add("selected-button");
//                 button.classList.remove("hidden-button");
//
//
//             }
//         });
//     });
// }



function getFilterData(param) { // gets all data
    // fetch("http://127.0.0.1:5000/data")
    //     .then(response => response.json())
    //     .then(jsondata => {
    //         globalData = jsondata
    //     })
    //     .catch((error) => console.log(error));
    let data = [];
    for (let i =0; i<10; i++){
        let num = Math.round(Math.random() * 30);
        data.push(num);
    }
    return data
}
//
// function filterData(filter) { // returns just light data
//     filteredData = []
//     for (let i=0; i < globalData.length; i++){
//         filteredData.push(globalData[i][filter]) // eg filter = 'light'
//     }
//     return filteredData
// }


function dropdownFunctionality(dropdown){
    let value = dropdown.target.value; // oh thank god!!!
    console.log(value);

    



}
