$('#searchModal').on('shown.bs.modal', (function () {
    $('#gr').on('input change', function () {
        if ($(this).val() !== '') {
            $('[id=st]').prop('disabled', true);
        } else {
            $('[id=st]').prop('disabled', false);
        }
    });
    $('[id=st]').on('input change', function () {
        if ($(this).val() !== '') {
            $('#gr').prop('disabled', true);
        } else {
            $('#gr').prop('disabled', false);
        }
    });
    bootstrapValidate('#gr', 'numeric:Please only enter numeric characters!', function (isValid) {
   if (isValid) {
        $("#gr").addClass('has-success').removeClass('has-error');
   } else {
        $("#gr").removeClass('has-error').addClass('has-success');
   }
});
}));
