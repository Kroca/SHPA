$(document).ready(function () {
    $("#myButton").on('click', function () {
        var checkedValue = document.getElementById('myButton');
        var action = "";
        var actor = "LightControl";
        if (checkedValue.checked){
            action = "TURN_ON"
        }else {
            action = "TURN_OFF"
        }
        $.ajax({
            data: JSON.stringify({ actor_name : actor, action_name:action}),
            type: 'POST',
            url : "/performAction"
        }).done(function(data){
         
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