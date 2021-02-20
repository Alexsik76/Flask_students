$(document).ready(function () {
    $('#gr').on('input', function () {
        if ($(this).val().length)
            $(this).next('#st').prop('disabled', true).val('').removeAttr("alt"); // disable and clear other fields
        else $(this).next('#st').prop('disabled', false);
    }).trigger("input");
});