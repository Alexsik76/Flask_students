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

});
$('#add_course').click(function () {
        let selected_course = $("#available_courses option:selected").text();
        $.post('/add_course/', {course: selected_course, student_id: student_id}).done(function() {
            document.location.reload();
        });
    });