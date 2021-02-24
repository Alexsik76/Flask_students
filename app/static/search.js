$('#searchModal').on('shown.bs.modal', (function () {

    bootstrapValidate('#gr', 'numeric:Please only enter numeric characters!', function (isValid) {
   if (isValid) {
       $("#gr").removeClass('has-warning').addClass('has-success');
       $('#submit').attr('disabled', false);
   } else {
       $("#gr").addClass('has-success').removeClass('has-warning');
       $('#submit').attr('disabled', true);
   }
});
}));

// $('#gr').on('input change', function () {
//         if ($(this).val() !== '') {
//             $('[id=st]').prop('disabled', true);
//         } else {
//             $('[id=st]').prop('disabled', false);
//         }
//     });
//     $('[id=st]').on('input change', function () {
//         if ($(this).val() !== '') {
//             $('#gr').prop('disabled', true);
//         } else {
//             $('#gr').prop('disabled', false);
//         }
//     });