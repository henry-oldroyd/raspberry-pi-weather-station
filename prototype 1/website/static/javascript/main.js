function output_weather_data(data) {
    console.log("data that would be added to website");
    console.log(data);
}
document.querySelector("#get_data_btn").addEventListener("click", () => {
    fetch("http://127.0.0.1:5000/data")
        .then(response => response.json())
        .then(output_weather_data)
        .catch((error) => console.log(error));
});
