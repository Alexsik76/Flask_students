//Main buttons events
$("#search_group_btn").click(function () {
    fill_modal('Search groups', '/groups/?needed_form=search_groups');
});
$("#search_student_btn").click(function () {
    fill_modal('Search student', '/students/?needed_form=search_student');
});
$("#create_student_btn").click(function () {
    fill_modal('Create student', '/_create_student/');
});
$(window).scroll(function () { // Disable button if on top.
    if ($(this).scrollTop()) {
        $('#toTop').fadeIn();
    } else {
        $('#toTop').fadeOut();
    }
});
$("#toTop").click(function () {
    $("html, body").animate({scrollTop: 0}, 1000);
});

// Fill modal by button or row click
function fill_modal(label, path) {
    $('#ModalLabel span').text(label);
    $('.modal-body').load(path);
}

$('#main_table').ready(function () {
    // Show student modal by click on row
    $("#main_table tr").click(function () {
        let $clickedRowId = $(this).children("th").text();
        fill_modal('Student info', '/students/' + $clickedRowId);
        student_id = $clickedRowId;
    });

    // Scroll to last modified row and animate it
    // console.log(last_modified);
    if (typeof last_modified !== 'undefined' && last_modified['updated'] !== undefined) {
        console.log(last_modified)
        let $tableRow = $('#main_table th').filter(function() {
            return $(this).text() == last_modified['updated'];
        }).closest('tr');
        $('html, body').animate({
            scrollTop: ($tableRow.offset().top - 180)
        }, 1000);
        $tableRow.delay(1200).queue(function () {
            $(this).addClass("table-success", 200, 'swing', function (){
                $(this).removeClass("table-success", 1200, 'swing');
                last_modified['updated'] = undefined;
            }).dequeue();
        });
    }
    else { //TODO: Problem with first student
        if (typeof last_modified !== 'undefined' && last_modified['deleted_after'] !== undefined) {
            let $tableRow = $('#main_table th').filter(function () {
                return $(this).text() == last_modified['deleted_after'];
            }).closest('tr');
            $($tableRow).after('<tr id="deleted_row"><th colspan="5">Deleted</th></tr>');
            $('html, body').animate({
            scrollTop: ($('#deleted_row').offset().top - 180)
        }, 1000);
            $('#deleted_row').delay(1200).queue(function () {
            $(this).addClass("table-danger", 200, 'swing', function (){
                $(this).removeClass("table-danger", 1200, 'swing', function (){
                    last_modified['updated'] = undefined;
                    $(this).remove();
                });

            }).dequeue();
        });
        }
    }
});

$('.modal').on('shown.bs.modal form_updated', function () {

    // Make text fields as readonly
    $('.form-control-plaintext').attr('readonly', true);

    // Validate field of the search group form (is integer)
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

    // Disable buttons if course not changed
    $('#del_course').attr('disabled', true);
    $('#courses').change(function () {
        $('#del_course').attr('disabled', false);
    });
    $('#add_course').attr('disabled', true);
    $('#available_courses').change(function () {
        $('#add_course').attr('disabled', false);
    });

    // Update form after add or dell course
    function update_courses(response) {
        $('#student_form').html(response['new_template']).trigger('form_updated');
        $('#courses').focus().delay(1000).queue(function () {
            $(this).blur().dequeue();
        });
    }

    // Add selected course for the student
    $('#add_course').click(function () {
        let to_add_course = $("#available_courses option:selected").text();
        $.post('/_update_courses/', {course: to_add_course, student_id: student_id, action: "append"})
            .done(function (response) {
                update_courses(response);
                $('.alert').text("Course added").fadeIn(500).fadeOut(2000);
            });
    });

    // Delete selected course for the student
    $('#del_course').click(function () {
        let to_del_course = $("#courses option:selected").text();
        $.post('/_update_courses/', {course: to_del_course, student_id: student_id, action: "remove"})
            .done(function (response) {
                update_courses(response);
                $('.alert').text("Course deleted").fadeIn(500).fadeOut(2000);
            });
    });

    // Delete current student
    $('#del_student').click(function () {
        $.post('/_delete_student/', {student_id: student_id})
            .done(function (response) {
                if (response["success"]) {
                    window.location.replace($SCRIPT_ROOT + 'students');
                }
            });
    });
});