function concept_edit() {
    var item = $(this).parent();
    var title = item.find(".edit").attr("title");
    item.load("/staff/new/?ajax&name="+escape(title),null,function () { $("#save-form").submit(concept_save); });
    return false;
}

$(document).ready(function () {
    $(".edit").click(concept_edit);
})

function concept_save() {
    var item = $(this).parent();
    var data = {
        name: item.find("#id_name").val(),
        due: item.find("#id_due").val(),
        notes: item.find("#id_notes").val()        
    };
    $.post("/staff/new/?ajax",data,function(result) {
        if (result != "failure") {
            item.remove();
            $(".edit").click(concept_edit);
        }
        else {
            alert("Failed to validate the concept before saving.");
        }
    });
    return false;
}