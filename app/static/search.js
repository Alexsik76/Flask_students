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
    $('.modal-body').load('/students/?needed_form=search_student');
});
$("#create_student_btn").click(function () {
    $('#ModalLabel span').text('Create student');
    $('.modal-body').load('/create_student/');
});

$('#main_table').ready(function () {
    $("#main_table tr").click(function () {
        let $clickedRowId = $(this).children("th").text();
        $('#ModalLabel span').text('Student info');
        $('.modal-body').load('/students/' + $clickedRowId);
        student_id = $clickedRowId;

    });
    if (typeof last_modified !== 'undefined') {
        let $tableRow = $('#main_table th:contains("' + last_modified + '")').closest("tr");
        $('html, body').animate({
            scrollTop: ($tableRow.offset().top - 180)
        }, 1000);
    }
});

$('.modal').on('shown.bs.modal form_updated', function () {
    console.log('selected');
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

    function add_focus() {
        $('#courses').focus().delay(1000).queue(function () {
            $(this).blur().dequeue();
        });
    }
    function switch_buttons() {
        if ($("#courses option:selected").text() === "") {
            $('#del_course').attr('disabled', true);
        }
        $('#courses').change(function () {
            $('#del_course').attr('disabled', false);
        });
        if ($("#available_courses option:selected").text() === "Choice course") {
            $('#add_course').attr('disabled', true);
        } else {
            $('#add_course').attr('disabled', false);
        }
        $('#available_courses').change(function () {
            $('#add_course').attr('disabled', false);
        });
    }

    switch_buttons();

    function update_courses2(response) {
        let $div_form = $('#student_form');
        let new_form = response['new_template'];
        $div_form.html(new_form).trigger('form_updated');
            add_focus();
            switch_buttons();
    }

    // Make text fields as readonly
    $('.form-control-plaintext').attr('readonly', true);


    // Add selected course for the student
    $('#add_course').click(function () {
        let to_add_course = $("#available_courses option:selected").text();
        $.post('/update_courses/', {course: to_add_course, student_id: student_id, action: "append"})
            .done(function (response) {
                update_courses2(response);
                $('.alert').text("Course added").fadeIn(500).fadeOut(2000);
            });
    });

    // Delete selected course for the student
    $('#del_course').click(function () {
        let to_del_course = $("#courses option:selected").text();
        $.post('/update_courses/', {course: to_del_course, student_id: student_id, action: "remove"})
            .done(function (response) {
                update_courses2(response);
                $('.alert').text("Course deleted").fadeIn(500).fadeOut(2000);
            });
    });

    // Delete curent student
    $('#del_student').click(function () {
        $.post('/delete_student/', {student_id: student_id})
            .done(function (response) {
                if (response["success"]) {
                    window.location.replace($SCRIPT_ROOT + 'students');
                }
            });
    });
});


