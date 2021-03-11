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

$('#s_read').modal('show').on('shown.bs.modal', (function () {
    $('.form-control-plaintext').attr('readonly', true);
}));
// $('#g_search').on('shown.bs.modal', (function () {
//     $('#gr').on('input', function () {
//         let text1 = Number.parseInt($(this).val(), 10);
//         if (text1 > 0) {
//             $('#gr').removeClass('is-invalid').addClass('is-valid');
//             $('#submit').attr('disabled', false);
//         } else {
//             let feedback = $('.form-group').find('.invalid-feedback').length;
//             console.log((feedback))
//             $('#gr').removeClass('is-valid').addClass('is-invalid');
//             if (!feedback) {
//                 $('.form-group').append(
//                     '<div class="invalid-feedback">Please only enter numeric characters!</div>'
//                 );
//             }
//             $('#submit').attr('disabled', true);
//         }
//     });
// }));