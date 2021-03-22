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
    // if ($("#select option:selected").text() == "") {
    //     $('#del_course').attr('disabled', true);
    // } else {
    //     $('#del_course').attr('disabled', false);
    // }
    // Set text in fields readonly
    $('.form-control-plaintext').attr('readonly', true);

    // Hide the  in the modal
    $('.alert').delay(2000).slideUp(function () {
        $(this).alert('close');
    });
        // Add selected course for the student
    $('#add_course').click(function () {
        let to_add_course = $("#available_courses option:selected").text();
        $.post('/add_del_course/', {course: to_add_course, student_id: student_id, operation: 'add'})
            .done(function () {
                location.reload();
            });
    });
    // Delete selected course for the student
    $('#del_course').click(function () {
        let to_del_course = $("#select option:selected").text();
        $.post('/add_del_course/', {course: to_del_course, student_id: student_id, operation: 'del'})
            .done(function () {
                location.reload();
            });
    });
})