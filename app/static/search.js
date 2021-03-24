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
$('.alert-success').css('margin-bottom', '0').css('padding', '0.375rem');
// Student info form
$('#s_read').modal('show').on('shown.bs.modal', function () {
    // Disable del button if not selected
    let dell_button = $('#del_course');
    let used_courses = $("#select");
    let available_courses = $('#available_courses');
    let add_button = $('#add_course');
    if ($("#select option:selected").text() === ""){
        dell_button.attr('disabled', true);
    }
    used_courses.change(function (){
        dell_button.attr('disabled', false);
    });
    available_courses.change(function (){
        if ($("#available_courses option:selected").text() === "Choice course") {
            add_button.attr('disabled', true);
        } else {
            add_button.attr('disabled', false);
        }
   });

    // Make text fields as readonly
    $('.form-control-plaintext').attr('readonly', true);

    // Hide the  in the modal
    $('.alert').delay(2000).slideUp(function () {
        $(this).alert('close');
    });
    // Add selected course for the student
    add_button.click(function () {
        let to_add_course = $("#available_courses option:selected").text();
        $.post('/add_del_course/', {course: to_add_course, student_id: student_id, operation: 'add'})
            .done(function () {
                location.reload();
            });
    });
    // Delete selected course for the student
    dell_button.click(function () {
        let to_del_course = $("#select option:selected").text();
        $.post('/add_del_course/', {course: to_del_course, student_id: student_id, operation: 'del'})
            .done(function () {
                location.reload();
            });
    });
})