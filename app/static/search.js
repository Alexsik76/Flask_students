// $('#g_search').on('shown.bs.modal', (function () {
//     bootstrapValidate('#gr', 'numeric:Please only enter numeric characters!', function (isValid) {
//    if (isValid) {
//        $('#submit').attr('disabled', false);
//    } else {
//        $('#submit').attr('disabled', true);
//    }
// });
// }));
$('#s_read').modal('show');

$('#g_search').on('shown.bs.modal', (function () {
    $('#gr').on('input', function () {
        let text1 = Number.parseInt($(this).val(), 10);
        if (text1 > 0) {
            $('#gr').removeClass('is-invalid').addClass('is-valid');
            $('#submit').attr('disabled', false);
        } else {
            let feedback = $('.form-group').has('.invalid-feedback');
            $('#gr').removeClass('is-valid').addClass('is-invalid');
                if (!feedback) {
                    $('.form-group').append(
                        '<div class="invalid-feedback">Please only enter numeric characters!</div>'
                    );
                }
            $('#submit').attr('disabled', true);
        }
    });
}));