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
$('#modal-alert').css({
    'margin-bottom': '0',
    'padding': '0.375rem',
    'display': 'none'
});
$('#s_create').modal('show');
// Student info form
$('#s_read').modal('show').on('shown.bs.modal', function () {
    // Disable del button if not selected
    let $courses = $("#courses");
    let $dell_button = $('#del_course');
    let $av_courses = $('#available_courses');
    let $add_button = $('#add_course');
    let $alert = $('.alert');

    function switch_buttons() {
        if ($("#courses option:selected").text() === "") {
            $dell_button.attr('disabled', true);
        }
        $courses.change(function () {
            $dell_button.attr('disabled', false);
        });
        if ($("#available_courses option:selected").text() === "Choice course") {
            $add_button.attr('disabled', true);
        } else {
            $add_button.attr('disabled', false);
        }
        $av_courses.change(function () {
            $add_button.attr('disabled', false);
        });
    }

    function update_courses(response) {
        $courses.empty();
        $courses.attr("size", response['courses'].length);
        $.each(response['courses'], function (key, value) {
            $courses.append($("<option></option>")
                .attr("value", key).text(value));
        });
        $av_courses.empty();
        $.each(response['av_courses'], function (key, value) {
            $av_courses.append($("<option></option>")
                .attr("value", key).text(value));
        });
    }

    // Make text fields as readonly
    $('.form-control-plaintext').attr('readonly', true);

    switch_buttons();

    // Add selected course for the student
    $add_button.click(function () {
        let to_add_course = $("#available_courses option:selected").text();
        $.post('/process_course/', {course: to_add_course, student_id: student_id, process: "add"})
            .done(function (response) {
                update_courses(response);
                switch_buttons();
                $alert.text("Course added").fadeIn(500).fadeOut(2000);
            });
    });


    // Delete selected course for the student
    $dell_button.click(function () {
        let to_del_course = $("#courses option:selected").text();
        $.post('/process_course/', {course: to_del_course, student_id: student_id, process: "remove"})
            .done(function (response) {
                update_courses(response);
                switch_buttons();
                $alert.text("Course deleted").fadeIn(500).fadeOut(2000);

            });
    });
})