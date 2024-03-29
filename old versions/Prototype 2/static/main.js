let boldRed = "rgba(255,0,0,1)";
let faintRed = "rgba(255,0,0,0.2)";
let boldOrange = "rgba(255,196,0,1)";
let faintOrange = "rgba(255,196,0,0.4)";
let boldPurple = "rgba(156,0,130,1)";
let faintPurple = "rgba(156,0,130,0.2)";
let boldBlue = "rgba(0,0,255,1)";
let faintBlue = "rgba(0,0,255,0.2)";
let boldGreen = "rgba(0,255,0,1)";
let faintGreen = "rgba(0,255,0,0.2)";
let boldBlack = "rgba(0,0,0,1)";
let faintBlack = "rgba(0,0,0,0.2)";


async function get_all_json_data() {
    let response = await fetch("http://127.0.0.1:5000/data");
    let data = response.json()
    return data;
}
window.addEventListener('load', function() {
    get_all_json_data()
        .then(data => load_page(data))
});


function load_page(jsondata) {

    let tempData = []
    let rainData = []
    let pressureData = []
    let windSpeedData = []
    let humidityData = []

    jsondata.forEach(dataset => {
        tempData.push(dataset['temp'])
        rainData.push(dataset['rain'])
        pressureData.push(dataset['pressure'])
        windSpeedData.push(dataset['windspeed'])
        humidityData.push(dataset['humidity'])
    });

    windDirectionData = "west";

    // create readout boxes
    let tempReadOutBox = new Dataset("Temperature", "°C", "temperature-readout-box", tempData);
    let pressureReadOutBox = new Dataset("Pressure", "mb", "pressure-readout-box", pressureData);
    let humidityReadOutBox = new Dataset("Humidity", "%", "humidity-readout-box", humidityData);
    let rainReadOutBox = new Dataset("Rain", "mm", "rain-readout-box", rainData);
    let windSpeedReadOutBox = new Dataset("Wind Speed", "mph", "wind-speed-readout-box", windSpeedData);

    // smaller graphs on page 2
    let tempGraph = new Graph('Temparure', 'graph-temp', tempData, "°C", boldRed, faintRed)
    let pressureGraph = new Graph('Pressure', 'graph-pressure', pressureData, "Pa", boldOrange, faintOrange)
    let humidityGraph = new Graph('Humidity', 'graph-humidity', humidityData, "%", boldPurple, faintPurple)
    let rainGraph = new Graph('Precipitation', 'graph-precip', rainData, "mm", boldBlue, faintBlue)
    let windSpeedGraph = new Graph('Wind Speed', 'graph-wind-speed', windSpeedData, "mph", boldGreen, faintGreen)

    // main graph on page 3
    let bigGraph = new Graph('Temp', 'graph-graph-big', tempData, "°C", boldBlack, faintBlack, true)

    // dropdown box on page 3
    // let dropdown = document.getElementById("dropdown");
    // dropdown.addEventListener("input", (dropdown) => {dropdownFunctionality(dropdown, bigGraph);})




    // buttons on page 3
    let tempButton = document.getElementById("temp-button-big-graph");
    let pressureButton = document.getElementById("pressure-button-big-graph");
    let rainButton = document.getElementById("rain-button-big-graph");
    let windButton = document.getElementById("wind-button-big-graph");
    let humidButton = document.getElementById("humid-button-big-graph");

    let buttons = [tempButton, pressureButton, rainButton, windButton, humidButton]
    page3Buttons(buttons, bigGraph, jsondata); // adds functionality to each button, and the big graph 

    //button that spins compass
    let compassButton = document.getElementById("img-compass-arrow");
    //function for button to spin the compass
    compassSpin(compassButton, windDirectionData);

    updateBGimg(tempReadOutBox, rainReadOutBox);
}

class Dataset {
    constructor(title, unit, divName, data) {
        this.title = title;
        this.unit = unit;
        this.divName = divName;
        this.data = data;
        this.editReadOut();
    }


    editReadOut() {
        this.currentData = this.data[0]; // shows the first element in readout box 
        this.div = document.getElementsByClassName(this.divName);
        this.child = this.div[0].getElementsByTagName("p");

        // Add spacing between unit and value for some data series
        if (this.unit == "°C" || this.unit == "%") {
            this.child[0].innerText = this.currentData + this.unit;
        } else {
            this.child[0].innerText = this.currentData + " " + this.unit;
        }

    }


}

class Graph {
    constructor(title, id, data, unit, rgbaFront, rgbaBack, slider = false) {
        this.title = title
        this.backgroundColour = rgbaFront
        this.colour = rgbaFront
        this.borderColour = rgbaBack
        this.ctx = document.getElementById(id).getContext('2d')
        this.data = data;
        this.dataBeingUsed = this.data
        this.unit = unit;
        this.xlabels = this.createXlabels()
        this.initialiseGraph(unit)
        if (slider == true) {
            this.initialiseSlider();
        }

    }

    initialiseSlider() {
        this.sliders = document.getElementsByClassName("slider-big-graph"); // only lets you take as a list
        this.slider = this.sliders[0] // one element array
        this.slider.max = this.data.length;
        this.slider.value = this.slider.max;
        this.slider.addEventListener("input", () => { this.editDisplayData() });
        this.editDisplayData();
    }

    initialiseGraph(unit) {
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
                            beginAtZero: false,
                            ticks: {
                                callback: function(value, index, ticks) {
                                    value = value + " " + unit;
                                    return value;
                                }
                            }
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
        for (let dayCounter = 1; dayCounter <= this.dataBeingUsed.length; dayCounter++) {
            xlabels.push("Day " + dayCounter)
        }
        return xlabels
    }

    addDataPoint(dataPoint) {
        let newDataPoint = Math.floor((Math.random() + 2) * 10);
        this.dataBeingUsed.push(newDataPoint);
        this.len++
            this.xlabels.push("Day " + (this.len))
        this.chart.update()
    }

    removeDataPoint() {
        this.dataBeingUsed.pop()
        this.xlabels.pop()
        this.len--;
        this.chart.update()
    }

    editDisplayData() {
        let val = this.slider.value;


        this.dataBeingUsed = this.data.slice(0, val); // edits which part of data set is shwon
        this.xlabels = this.createXlabels()


        this.chart.data.datasets.forEach((dataset) => {
            dataset.data = this.dataBeingUsed;
        })
        this.chart.data.labels = this.xlabels;
        this.chart.update()
    }
}


// Update the background image to the current weather

function updateBGimg(tempReadOutBox, rainReadOutBox) {
    var r = document.querySelector(':root');
    var time = new Date().getHours(); // Used for condition of night time below

    //console.log(tempReadOutBox.currentData);

    // if (time <= 6 && time >= 18) {

    //     r.style.setProperty('--bgImg', "url('../images/night.png')");
    // } else {
    //     if (rainReadOutBox.currentData > 0) {
    //         r.style.setProperty('--bgImg', "url('../images/rain.png')");
    //     } else {
    //         if (tempReadOutBox.currentData > 20) {
    //             r.style.setProperty('--bgImg', "url('../images/sunny.png')");
    //         } else if (tempReadOutBox.currentData > 14) {
    //             r.style.setProperty('--bgImg', "url('../images/mild.png')");
    //         } else {
    //             r.style.setProperty('--bgImg', "url('../images/cold.png')");
    //         }
    //     }
    // }

    let img_file = "cold" // no .png 
    fetch(`http://127.0.0.1:5000/images/${img_file}`)
        // .then(response => console.log(response))
        .then(img => {
            var r = document.querySelector(':root');
            console.log(img['url'])
            r.style.setProperty('--bgImg', `url(${img['url']})`);
        })
}

function compassSpin(compassButton, orientation) {
    // let negative = -5; // so that the arrow can spin back and forth
    var rotation = -28 // upwards
    switch (orientation) {
        case "north":
            rotation = -28; // sets it to north 
            break;

        case "south":
            rotation = -28 + 180
            break;

        case "east":
            rotation = -28 + 90
            break;

        case "west":
            rotation = -28 + 270
            break;
        default:
            break;
    }

    compassButton.style.transform = `translate(-48.3%, -50%) rotate(${rotation}deg`



    // let id = setInterval(function() {
    //     compassShake(rotation, compassButton, negative);
    //     negative = 20*(Math.random())
    //     negative = negative * -1
    // },Math.random()*5000);
}

// function compassShake(rotation, compassButton, negative) {

//     if (1 == 2) {
//         console.log('test for spinning')
//     } else {
//         rotation = rotation + negative
//         compassButton.style.transform = `translate(-49.5%, -50%) rotate(${rotation}deg`
//     }
// }


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


// HENRYYYYYYYYY - this is where you come in
// I'm thinking that you have one function that makes a json requests and
// stores the data to a variable in the JS file, then this function simply uses this
// variable and filters the correct data.

function getFilterData(param = null) { // gets all data
    let data = [];
    for (let i = 0; i < 10; i++) {
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


function dropdownFunctionality(value, bigGraph, jsondata) {
    if (value == "Temperature") {
        unit = "°C"
        filter = "temp"
    } else if (value == "Pressure") {
        unit = "Pa"
        filter = "pressure"
    } else if (value == "Rain") {
        unit = "mm"
        filter = "rain"
    } else if (value == "Wind Speed") {
        unit = "mph";
        filter = "windspeed"
    } else if (value == "Humidity") {
        unit = "%";
        filter = "humidity"
    }
    let newdata = [];
    jsondata.forEach(dataset => {
        newdata.push(dataset[filter])
    });

    // bigGraph.data = [4,3,2,1,2,4,5,6,6,4];

    bigGraph.chart.data.datasets.forEach((dataset) => {
        dataset.data = newdata; // changes the data
        dataset.label = value; // changes the title
    })

    bigGraph.data = newdata;
    // bigGraph.chart.data.datasets.label = dropdown.target.value;

    bigGraph.xlabels = bigGraph.createXlabels()
    bigGraph.chart.data.labels = this.xlabels;
    bigGraph.initialiseSlider();
    bigGraph.chart.options.scales.y.ticks.callback = function(value, index, ticks) {
        value = value + " " + unit;
        return value
    }
    bigGraph.chart.update()
}

function page3Buttons(buttons, bigGraph, jsondata) {
    // console.log(buttons)
    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            //removes selected from all
            buttons.forEach((button) => {
                button.classList.remove("selected-button")
            });
            button.classList.toggle("active")

            // changes the graph
            dropdownFunctionality(button.innerText, bigGraph, jsondata)

            // makes the button selected
            button.classList.add("selected-button");
        })

    });

}