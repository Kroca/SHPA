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
        for(var d in data){
            $("#"+d).text(data[d]);
        }
    });
}
updateSensorValues();
setInterval(updateSensorValues,10*1000);