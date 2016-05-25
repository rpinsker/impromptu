$( document ).ready(function() {

    var modal = document.getElementById('uploadModal');
    var btn = document.getElementById('upload');
    var span = document.getElementById("close-x-u");

    btn.onclick = function () {
        modal.style.display = "block";
    }
    span.onclick = function () {
        modal.style.display = "none";
    }

    var modal2 = document.getElementById('editModal');
    var btn2 = document.getElementById('edit');
    var span2 = document.getElementById("close-x-n");

    btn2.onclick = function () {
        var m = document.getElementById('measure-select').value;
        $.ajax({
            type: "POST",
            url: "/measure",
            data : m,
            success: function (result) {
                $('#measureImg').html("<img src="+result+"\>");
                console.log(m);
            }
        });

        var measureID = "ne-" + m;
        document.getElementById(measureID).style.display = "block";
        document.getElementById('edit-title').innerHTML = "Editing Measure " + m;
        modal2.style.display = "block";
        var infoboxID = "note-info-box-" + m;
        var addboxID = "note-add-box-" + m;
        var deleteboxID = "note-delete-box-" + m;
        document.getElementById(infoboxID).style.display = "none";
        document.getElementById(addboxID).style.display = "none";
        document.getElementById(deleteboxID).style.display = "none";
    }
    span2.onclick = function () {
        var m = document.getElementById('measure-select').value;
        var measureID = "ne-" + m;
        document.getElementById(measureID).style.display = "none";
        modal2.style.display = "none";
    }

    var modal3 = document.getElementById('jsonModal');
    var btn3 = document.getElementById('load');
    var span3 = document.getElementById("closeJSON");

    btn3.onclick = function () {
        modal3.style.display = "block";
    }
    span3.onclick = function () {
        modal3.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }

        if (event.target == modal2) {
            modal2.style.display = "none";
            var m = document.getElementById('measure-select').value;
            var measureID = "ne-" + m;
            document.getElementById(measureID).style.display = "none";
            var infoboxID = "note-info-box-" + m;
            var addboxID = "note-add-box-" + m;
            var deleteboxID = "note-delete-box-" + m;
            document.getElementById(infoboxID).style.display = "none";
            document.getElementById(addboxID).style.display = "none";
            document.getElementById(deleteboxID).style.display = "none";
        }

        if (event.target == modal3) {
            modal3.style.display = "none";
        }
    }

    var edit = document.getElementById('note-edit');
    var add = document.getElementById('note-add');
    var del = document.getElementById('note-delete');

    edit.onclick = function () {
        var infoboxID = "note-info-box-" + document.getElementById('measure-select').value;
        var addboxID = "note-add-box-" + document.getElementById('measure-select').value;
        var deleteboxID = "note-delete-box-" + document.getElementById('measure-select').value;
        document.getElementById(infoboxID).style.display = "block";
        document.getElementById(addboxID).style.display = "none";
        document.getElementById(deleteboxID).style.display = "none";
        var info_boxes = document.getElementsByClassName('note-info');
        for (var i = 0; i < info_boxes.length; i++) {
            info_boxes[i].style.display = 'none';
        }
        var m = document.getElementById('measure-select').value;
        measureID = "ns-" + m;
        var n = document.getElementById(measureID).value;
        var noteID = "m-" + m + "ni-" + n;
        console.log(noteID);
        document.getElementById(noteID).style.display = "block";
    }

    add.onclick = function () {
        var infoboxID = "note-info-box-" + document.getElementById('measure-select').value;
        var addboxID = "note-add-box-" + document.getElementById('measure-select').value;
        var deleteboxID = "note-delete-box-" + document.getElementById('measure-select').value;
        document.getElementById(infoboxID).style.display = "none";
        document.getElementById(addboxID).style.display = "block";
        document.getElementById(deleteboxID).style.display = "none";
        var info_boxes = document.getElementsByClassName('note-add');
        for (var i = 0; i < info_boxes.length; i++) {
            info_boxes[i].style.display = 'none';
        }
        var m = document.getElementById('measure-select').value;
        measureID = "ns-" + m;
        var n = document.getElementById(measureID).value;
        var noteID = "m-" + m + "na-" + n;
        console.log(noteID);
        document.getElementById(noteID).style.display = "block";
    }

    del.onclick = function () {
        var infoboxID = "note-info-box-" + document.getElementById('measure-select').value;
        var addboxID = "note-add-box-" + document.getElementById('measure-select').value;
        var deleteboxID = "note-delete-box-" + document.getElementById('measure-select').value;
        document.getElementById(infoboxID).style.display = "none";
        document.getElementById(addboxID).style.display = "none";
        document.getElementById(deleteboxID).style.display = "block";
        var info_boxes = document.getElementsByClassName('note-delete');
        for (var i = 0; i < info_boxes.length; i++) {
            info_boxes[i].style.display = 'none';
        }
        var m = document.getElementById('measure-select').value;
        measureID = "ns-" + m;
        var n = document.getElementById(measureID).value;
        var noteID = "m-" + m + "nd-" + n;
        console.log(noteID);
        document.getElementById(noteID).style.display = "block";
    }

    var cancel = document.getElementById('note-cancel');
    var apply = document.getElementById('note-apply');

    apply.onclick = function() {
        var m = document.getElementById('measure-select').value;
        measureID = "ns-" + m;
        var n = document.getElementById(measureID).value;
        if ($('#note-info-box-'+ m).is(":visible")) {
            infoID = "#m-" + m + "ni-" + n;
            $('input[name=submit-type]').val('edit');
            var d = $(infoID).find(".edit-select-duration").val();
            var l = $(infoID).find(".edit-select-pitch").val();
            var a = $(infoID).find(".edit-select-acc").val();
            var o = $(infoID).find(".edit-select-octave").val();
        } else if ($('#note-add-box-'+ m).is(":visible")) {
            infoID = "#m-" + m + "na-" + n;
            $('input[name=submit-type]').val('add');
            var d = $(infoID).find(".add-select-duration").val();
            var l = $(infoID).find(".add-select-pitch").val();
            var a = $(infoID).find(".add-select-acc").val();
            var o = $(infoID).find(".add-select-octave").val();
        } else if ($('#note-delete-box-'+ m).is(":visible")) {
            infoID = "#m-" + m + "nd-" + n;
            $('input[name=submit-type]').val('delete');
            var d = $(infoID).find(".add-select-duration").val();
            var l = $(infoID).find(".add-select-pitch").val();
            var a = $(infoID).find(".add-select-acc").val();
            var o = $(infoID).find(".add-select-octave").val();
        } else {
            $('input[name=submit-type]').val('edit');
            var d = $(infoID).find(".add-select-duration").val();
            var l = $(infoID).find(".add-select-pitch").val();
            var a = $(infoID).find(".add-select-acc").val();
            var o = $(infoID).find(".add-select-octave").val();
        }
        $('input[name=measure_number]').val(m);
        $('input[name=note_number]').val(n);
        $('input[name=duration0]').val('1');
        $('input[name=duration1]').val(d);
        $('input[name=pitch]').val(l);
        $('input[name=acc]').val(a);
        $('input[name=octave]').val(o);
        console.log(l);
        console.log(o);
    }

    cancel.onclick = function () {
        modal2.style.display = "none";
        var m = document.getElementById('measure-select').value;
        var measureID = "ne-" + m;
        document.getElementById(measureID).style.display = "none";
        var infoboxID = "note-info-box-" + m;
        var addboxID = "note-add-box-" + m;
        var deleteboxID = "note-delete-box-" + m;
        document.getElementById(infoboxID).style.display = "none";
        document.getElementById(addboxID).style.display = "none";
        document.getElementById(deleteboxID).style.display = "none";
    }

});
