var modal = document.getElementById('uploadModal');
var btn = document.getElementById('upload');
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}
span.onclick = function() {
    modal.style.display = "none";
}

var modal2 = document.getElementById('editModal');
var btn2 = document.getElementById('edit');
var span2 = document.getElementsByClassName("close")[0];

btn2.onclick = function() {
    var m = document.getElementById('measure-select').value;
    document.getElementById('edit-title').innerHTML = "Editing Measure " + m;
    modal2.style.display = "block";
}
span2.onclick = function() {
    modal2.style.display = "none";
}


var modal3 = document.getElementById('jsonModal');
var btn3 = document.getElementById('load');
var span3 = document.getElementsByClassName("closeJSON")[0];

btn3.onclick = function() {
    modal3.style.display = "block";
}
span3.onclick = function() {
    modal3.style.display = "none";
}


window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
    if (event.target == modal) {
        modal.style.display = "none";
    }

    if (event.target == modal3) {
        modal3.style.display = "none";
    }
}