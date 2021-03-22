// Validate Group search form
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


// Student info form
$('#s_read').modal('show').on('shown.bs.modal', function () {
    // Set text in fields readonly
    $('.form-control-plaintext').attr('readonly', true);
    // Hide the  in the modal
    $('.alert').delay(2000).slideUp(function () {
        $(this).alert('close');
    });
    // Add selected course for the student
    $('#add_course').click(function () {
        let selected_course = $("#available_courses option:selected").text();
        $.post('/add_del_course/', {course: selected_course, student_id: student_id, operation: 'add'})
            .done(function () {
                location.reload();
            });
    });
    $('#del_course').click(function () {
        let selected_course = $("#select option:selected").text();
        $.post('/add_del_course/', {course: selected_course, student_id: student_id, operation: 'del'})
            .done(function () {
                location.reload();
            });
    });
})