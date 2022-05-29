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
    let tempReadOutBox = new Dataset("Temperature", "°C", "readout-box-temp", tempData);
    let pressureReadOutBox = new Dataset("Pressure", "mb", "readout-box-pressure", pressureData);
    let humidityReadOutBox = new Dataset("Humidity", "%", "readout-box-humidity", humidityData);
    let rainReadOutBox = new Dataset("Rain", "mm", "readout-box-rain", rainData);
    let windSpeedReadOutBox = new Dataset("Wind Speed", "mph", "readout-box-wind", windSpeedData);

    // // smaller graphs on page 2
    // let tempGraph = new Graph('Temparure', 'graph-temp', tempData, "°C", boldRed, faintRed)
    // let pressureGraph = new Graph('Pressure', 'graph-pressure', pressureData, "Pa", boldOrange, faintOrange)
    // let humidityGraph = new Graph('Humidity', 'graph-humidity', humidityData, "%", boldPurple, faintPurple)
    // let rainGraph = new Graph('Precipitation', 'graph-precip', rainData, "mm", boldBlue, faintBlue)
    // let windSpeedGraph = new Graph('Wind Speed', 'graph-wind-speed', windSpeedData, "mph", boldGreen, faintGreen)

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

    updateBGimg(tempReadOutBox, rainReadOutBox);
    sandringhamLogo();
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
        this.div = document.getElementById(this.divName);
        this.child = this.div.getElementsByTagName("p");
        console.log('now')
        console.log(this.div)

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

    let img_file = "cold" // no .png  ${img_file}
    console.log('making getch')
    fetch(`http://127.0.0.1:5000/images/cold`)
        // .then(response => console.log(response))
        .then(img => {
            var r = document.getElementsByClassName('intro')[0];
            console.log(img['url'])
            console.log('background image set')
            r.style.setProperty('background-image', `url(${img['url']})`);
        })
}

function sandringhamLogo() {
    fetch("http://127.0.0.1:5000/images/logo")
        .then(img => {
            var logoImg = document.getElementById("sand-logo")
            console.log(img)
            console.log(logoImg)
            logoImg.src = img['url']
        })
}

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