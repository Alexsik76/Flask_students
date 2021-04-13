// Validate Group search form


//Scroll to top
$(window).scroll(function () {
    if ($(this).scrollTop()) {
        $('#toTop').fadeIn();
    } else {
        $('#toTop').fadeOut();
    }
});

$("#toTop").click(function () {
    $("html, body").animate({scrollTop: 0}, 1000);
});


$("#search_group_btn").click(function () {
    $('#ModalLabel span').text('Search groups');
    $('.modal-body').load('/groups/?needed_form=search_groups');
});
$("#search_student_btn").click(function () {
    $('#ModalLabel span').text('Search student');
    $('.modal-body').load('/students?needed_form=search_student');
});
$("#create_student_btn").click(function () {
    $('#ModalLabel span').text('Create student');
    $('.modal-body').load('/create_student/');
});

$('#main_table').ready(function () {
    $("#main_table tr").click(function () {
        let $clickedRowId = $(this).children("th").text();
        $('#ModalLabel span').text('Student info');
        $('.modal-body').load('/students/' + $clickedRowId)
    });
    if (typeof last_modified !== 'undefined') {
        let $tableRow = $('#main_table th:contains("' + last_modified + '")').closest("tr");
        $('html, body').animate({
            scrollTop: ($tableRow.offset().top - 180)
        }, 1000);
    }
});


$('.modal').on('shown.bs.modal', function () {
    $("#gr").on("focus", function () {
        bootstrapValidate('#gr', 'integer:Please only enter integer characters!', function (isValid) {
            if (isValid) {
                $('#submit').attr('disabled', false);
                $('#gr').removeClass('is-invalid').addClass('is-valid');
            } else {
                $('#submit').attr('disabled', true);
                $('#gr').removeClass('is-valid');
            }
        });
    });
    let $courses = $('#courses');
    let $dell_course_btn = $('#del_course');
    let $av_courses = $('#available_courses');
    let $add_course_btn = $('#add_course');
    let $alert = $('.alert');
    let $del_student_btn = $('#del_student');

    function add_focus() {
        $courses.focus().delay(1000).queue(function () {
            $(this).blur().dequeue();
        });
    }

    function switch_buttons() {
        if ($("#courses option:selected").text() === "") {
            $dell_course_btn.attr('disabled', true);
        }
        $courses.change(function () {
            $dell_course_btn.attr('disabled', false);
        });
        if ($("#available_courses option:selected").text() === "Choice course") {
            $add_course_btn.attr('disabled', true);
        } else {
            $add_course_btn.attr('disabled', false);
        }
        $av_courses.change(function () {
            $add_course_btn.attr('disabled', false);
        });
    }

    function update_courses(response) {
        $courses.empty();
        $courses.attr("size", response['courses'].length);
        $.each(response['courses'], function (key, value) {
            $courses.append($("<option></option>")
                .attr("value", key).text(value['name']));
        });
        $av_courses.empty();
        $.each(response['av_courses'], function (key, value) {
            $av_courses.append($("<option></option>")
                .attr("value", value['name']).text(value['name']));
        });
    }

    // Make text fields as readonly
    $('.form-control-plaintext').attr('readonly', true);

    switch_buttons();

    // Add selected course for the student
    $add_course_btn.click(function () {
        let to_add_course = $("#available_courses option:selected").text();
        $.post('/update_courses/', {course: to_add_course, student_id: student_id, action: "append"})
            .done(function (response) {
                update_courses(response);
                switch_buttons();
                add_focus();
                $alert.text("Course added").fadeIn(500).fadeOut(2000);
            });
    });

    // Delete selected course for the student
    $dell_course_btn.click(function () {
        let to_del_course = $("#courses option:selected").text();
        $.post('/update_courses/', {course: to_del_course, student_id: student_id, action: "remove"})
            .done(function (response) {
                update_courses(response);
                switch_buttons();
                add_focus();
                $alert.text("Course deleted").fadeIn(500).fadeOut(2000);
            });
    });

    // Delete curent student
    $del_student_btn.click(function () {
        $.post('/delete_student/', {student_id: student_id})
            .done(function (response) {
                if (response["success"]) {
                    window.location.replace($SCRIPT_ROOT + 'students');
                }
            });
    });
});



