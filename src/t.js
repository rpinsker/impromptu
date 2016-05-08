
function generateTuneB() {
    $.ajax({
        type: "POST",
        url: "app.py",
        success: callbackFunc
    }).done(function (o) {
        //location.reload();
    });
}


function generateTune() {
    $.ajax({
        type: "POST",
        url: "/",
        success: callbackFunc
    }).done(function (o) {
        //location.reload();
    });
}

function callbackFunc(response) {
    // do something with the response
    console.log(response);
}
