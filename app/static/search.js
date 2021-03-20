$('#g_search').on('shown.bs.modal', (function () {
    bootstrapValidate('#gr', 'integer:Please only enter integer characters!', function (isValid) {
    if (isValid) {
        $('#submit').attr('disabled', false);
        $('#gr').removeClass('is-invalid').addClass('is-valid');
    } else {
        $('#submit').attr('disabled', true);
        $('#gr').removeClass('is-valid');
    }
 });
 }));
$('#s_read').modal('show').on('shown.bs.modal', function () {
    $('.form-control-plaintext').attr('readonly', true);
     let str_value = $('.custom-select');
     let size_value = parseInt(str_value.attr('size'));
    $('#add_course').click(function () {
        let selected_course = $("#available_courses option:selected").text();
        $.post('/add_course/', {course: selected_course, student_id: student_id})
            .done(function() {
                size_value += 1;
                $('<option value = "' + size_value + '">' + selected_course + '</option>').insertAfter('.custom-select option:last');
                str_value.attr('size', size_value.toString());
            });
    });
});
