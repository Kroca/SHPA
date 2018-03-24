$(document).ready(function () {
    $("#myButton").on('click', function () {
        var checkedValue = document.getElementById('myButton');
        $.ajax({
            data: JSON.stringify({ state : checkedValue.checked}),
            type: 'POST',
            url : "/process"
        }).done(function(data){
            // code
        });   
    });
});

function updateSensorValues(){
    $.getJSON("/updateSensors",function(data){
        $("#Humidity").text(data.hum);
        $("#Light").text(data.light);
        $("#Temperature").text(data.temp);
    });
}
updateSensorValues();
setInterval(updateSensorValues,10*1000);