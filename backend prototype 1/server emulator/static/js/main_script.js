// async function get_weather_data() {
//     // data = await fetch("{{ url_for('data') }}")
//     data = await fetch("/data")
//     console.log(data)
// }
function output_weather_data(data) {
    console.log("data that would be added to website")
    console.log(data);
    // document.body.innerHTML += `<br/><p>${String(data)}</p>`;
    // document.body.innerHTML += "<p>" + String(data) + "</p>";
}

// $(document).ready(() => {
//     $("#get_data_btn").click(() => {
//         get_weather_data()
//         .then((value) => {
//             output_weather_data(value)
//         })
//         .catch((error) => {
//             alert("error")
//             console.log(error)
//         })
//     });
// });

document.querySelector("#get_data_btn").addEventListener("click", () => {
    fetch("/data")
        .then(response => response.json())
        .then(output_weather_data)
        .catch((error)=>   console.log(error));
})