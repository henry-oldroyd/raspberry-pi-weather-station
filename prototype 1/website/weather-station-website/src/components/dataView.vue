// https://vue-chartjs.org/guide/#example
<template>


<div id="topBanner">
    <h1 id="title">{{ title }}</h1>
</div>

    <div id="buttonMenu">
        <span>
        <button type="button" id="oneData" class="button">Add one data point</button>
        <button type="button" id="contData" class="button">Lots of data</button>
        <button type="button" id="stop" class="button">Stop adding points</button>
        <button type="button" id="getDataButton" class="button">Get Data</button>
        <button type="button" id="makeTable" class="button">Create Table</button>
        </span>
    </div>


    <div id="chartDiv">
        <line-chart :chart-data="datacollection"></line-chart>
    </div>

    <table id="table">
        <tr>
            <th id='day'>Day</th>
            <th class='maindata'>Light</th>
            <th class='maindata'>Rain</th>

        </tr>
    </table>


    <div class="slidercontainer">
        <input type="range" min="1" max="7" value="1" class="slider" id="slider1">

    </div>


    <div id="footer">
        <p1 id="footerText">This is a footer. <br> This is a new line of the footer to show the spacing is center</p1>
        <p1> </p1>
    </div>




</template>

<script>
    import * as dataView from '../assets/dataView.js';
    import LineChart from '../assets/lineChart.js';
    // import LineChart from '..assets/lineChart.js'


    export default {
        name: 'dataView',
        components: {
            LineChart
        },
        data() { return {
            title: 'weather station project'
        } }
    }



</script>

<style>

</style>
