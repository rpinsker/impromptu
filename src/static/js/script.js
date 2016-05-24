var modal = document.getElementById('uploadModal');
var btn = document.getElementById('upload');
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
};
span.onclick = function() {
    modal.style.display = "none";
};
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

var modal2 = document.getElementById('editModal');
var btn2 = document.getElementById('edit');
var span2 = document.getElementsByClassName("close")[0];

btn2.onclick = function() {
    console.log("CLICKED");
    var m = document.getElementById('measure-select').value;
    var measureID = "ne-" + m;
    document.getElementById(measureID).style.display = "block";
    document.getElementById('edit-title').innerHTML = "Editing Measure " + m;
    modal2.style.display = "block";
};
span2.onclick = function() {
    modal2.style.display = "none";
    var m = document.getElementById('measure-select').value;
    var measureID = "ne-" + m;
    document.getElementById(measureID).style.display = "none";
};
window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
        var m = document.getElementById('measure-select').value;
        var measureID = "ne-" + m;
        document.getElementById(measureID).style.display = "none";
    }
};