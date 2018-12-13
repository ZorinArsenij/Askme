function avatatPreview(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $("#avatar-preview").attr("src", e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_avatar").change(function () {
    avatatPreview(this);
});